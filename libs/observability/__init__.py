"""
Observability module with logging, metrics, and shutdown handling.
"""
from libs.observability.logging import (
    generate_correlation_id,
    get_correlation_id,
    set_correlation_id,
    setup_logger,
)
from libs.observability.shutdown import (
    async_wait_for_termination,
    install_shutdown_handlers,
    shutdown_handler,
    terminate_event,
)
from libs.observability.metrics import (
    COUNT_BUCKETS,
    DURATION_BUCKETS,
    SIZE_BUCKETS,
    MetricsRegistry,
    get_metrics_registry,
    setup_metrics,
    shutdown_metrics_servers,
)
from libs.observability.decorators import log_errors, manage_metrics

__all__ = [
    # Logging
    "generate_correlation_id",
    "get_correlation_id",
    "set_correlation_id",
    "setup_logger",
    # Shutdown handling
    "async_wait_for_termination",
    "install_shutdown_handlers",
    "shutdown_handler",
    "terminate_event",
    # Metrics
    "COUNT_BUCKETS",
    "DURATION_BUCKETS",
    "SIZE_BUCKETS",
    "MetricsRegistry",
    "get_metrics_registry",
    "setup_metrics",
    "shutdown_metrics_servers",
    # Decorators
    "log_errors",
    "manage_metrics",
]
