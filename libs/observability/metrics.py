import os
import socket
import threading
from typing import Any, Callable, Dict, Optional

from loguru import logger
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    Info,
    generate_latest,
    start_http_server,
)

_service_registries: Dict[str, "MetricsRegistry"] = {}
_metrics_servers: Dict[str, Any] = {}
_metrics_lock = threading.Lock()

DURATION_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float('inf'))
SIZE_BUCKETS = (64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 16777216, float('inf'))
COUNT_BUCKETS = (1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, float('inf'))


class MetricsRegistry:
    def __init__(
        self,
        service_name: str,
        port: Optional[int] = None,
        port_mapping: Optional[Dict[str, int]] = None,
        label_extractor: Optional[Callable[[str], Dict[str, str]]] = None,
    ):
        self.service_name = service_name
        self.registry = CollectorRegistry()
        self.port = port
        self.server = None
        self._port_mapping = port_mapping or {}
        self._label_extractor = label_extractor or self._default_label_extractor
        self._common_labels = self._label_extractor(service_name)
        self._init_common_metrics()

    def _default_label_extractor(self, service_name: str) -> Dict[str, str]:
        return {"service": service_name}

    def _init_common_metrics(self):
        self.service_info = Info(
            'service_info',
            'Service information',
            registry=self.registry
        )
        self.service_info.info({
            'service_name': self.service_name,
            'version': '1.0.0',
            **self._common_labels
        })

        self.service_start_time = Gauge(
            'service_start_time_seconds',
            'Service start time in Unix timestamp',
            registry=self.registry
        )
        self.service_start_time.set_to_current_time()

        self.errors_total = Counter(
            'service_errors_total',
            'Total number of errors by type',
            ['error_type', 'component'],
            registry=self.registry
        )

        self.health_status = Gauge(
            'service_health_status',
            'Service health status (1=healthy, 0=unhealthy)',
            registry=self.registry
        )
        self.health_status.set(1)

    def create_counter(self, name: str, description: str, labelnames: Optional[list] = None) -> Counter:
        return Counter(
            name,
            description,
            labelnames or [],
            registry=self.registry
        )

    def create_histogram(
        self,
        name: str,
        description: str,
        labelnames: Optional[list] = None,
        buckets: Optional[tuple] = None,
    ) -> Histogram:
        kwargs = {
            'name': name,
            'documentation': description,
            'labelnames': labelnames or [],
            'registry': self.registry
        }
        if buckets:
            kwargs['buckets'] = buckets
        return Histogram(**kwargs)

    def create_gauge(self, name: str, description: str, labelnames: Optional[list] = None) -> Gauge:
        return Gauge(
            name,
            description,
            labelnames or [],
            registry=self.registry
        )

    def start_metrics_server(self, port: Optional[int] = None) -> bool:
        if self.server is not None:
            logger.warning(f"Metrics server already running for {self.service_name}")
            return True

        target_port = port or self.port or self._get_default_port()

        if not self._is_port_available(target_port):
            logger.warning(f"Port {target_port} not available, trying next available port")
            target_port = self._find_available_port(target_port)

        self.server = start_http_server(target_port, registry=self.registry)
        self.port = target_port
        logger.info(f"Metrics server started for {self.service_name} on port {target_port}")
        logger.info(f"Metrics available at: http://localhost:{target_port}/metrics")
        return True

    def _get_default_port(self) -> int:
        env_port = os.getenv('METRICS_PORT')
        if env_port:
            return int(env_port)

        for key, port in self._port_mapping.items():
            if key in self.service_name:
                return port

        return 9090

    def _is_port_available(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except OSError:
                return False

    def _find_available_port(self, start_port: int) -> int:
        for port in range(start_port, start_port + 100):
            if self._is_port_available(port):
                return port
        raise RuntimeError(f"No available ports found starting from {start_port}")

    def get_metrics_text(self) -> str:
        return generate_latest(self.registry).decode('utf-8')

    def record_error(self, error_type: str, component: str = "unknown"):
        self.errors_total.labels(error_type=error_type, component=component).inc()

    def set_health_status(self, healthy: bool):
        self.health_status.set(1 if healthy else 0)


def setup_metrics(
    service_name: str,
    port: Optional[int] = None,
    port_mapping: Optional[Dict[str, int]] = None,
    start_server: bool = True,
) -> MetricsRegistry:
    with _metrics_lock:
        if service_name in _service_registries:
            logger.debug(f"Metrics already setup for {service_name}")
            return _service_registries[service_name]

        metrics_registry = MetricsRegistry(service_name, port, port_mapping)
        _service_registries[service_name] = metrics_registry

        if start_server:
            success = metrics_registry.start_metrics_server()
            if success:
                _metrics_servers[service_name] = metrics_registry.server

        logger.info(f"Metrics setup completed for service: {service_name}")
        return metrics_registry


def get_metrics_registry(service_name: str) -> Optional[MetricsRegistry]:
    return _service_registries.get(service_name)


def shutdown_metrics_servers():
    with _metrics_lock:
        for service_name, server in _metrics_servers.items():
            if hasattr(server, 'shutdown'):
                server.shutdown()
            logger.info(f"Shutdown metrics server for {service_name}")

        _metrics_servers.clear()
