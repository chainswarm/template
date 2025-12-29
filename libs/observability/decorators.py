import traceback
from functools import wraps
from typing import Optional

from loguru import logger

from libs.observability.logging import (
    generate_correlation_id,
    get_correlation_id,
    set_correlation_id,
)
from libs.observability.metrics import get_metrics_registry


def log_errors(func):
    """
    Decorator to log exceptions with detailed context.
    
    Example:
        @log_errors
        def process_data(data):
            # Process data
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error in {func.__qualname__}",
                error=str(e),
                traceback=traceback.format_exc(),
                exc_info=True,
                extra={
                    "function": func.__qualname__,
                    "args_count": len(args),
                    "kwargs_keys": list(kwargs.keys()) if kwargs else [],
                }
            )
            raise
    return wrapper


def manage_metrics(
    success_metric_name: str = "execution_success",
    failure_metric_name: str = "execution_failure",
):
    """
    Decorator to automatically track success/failure metrics.
    
    Example:
        @manage_metrics("processing_success", "processing_failure")
        def process_batch(service_name, data):
            # Process data
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            metrics_registry = None
            correlation_id = get_correlation_id() or generate_correlation_id()
            set_correlation_id(correlation_id)

            try:
                if len(args) > 0 and isinstance(args[0], str):
                    metrics_registry = get_metrics_registry(args[0])
                elif 'service_name' in kwargs:
                    metrics_registry = get_metrics_registry(kwargs['service_name'])

                if metrics_registry is None:
                    local_vars = {}

                    def capture_locals(*a, **kw):
                        local_vars['metrics_registry'] = locals().get('metrics_registry')
                        return func(*a, **kw)

                    result = capture_locals(*args, **kwargs)
                    metrics_registry = local_vars.get('metrics_registry')
                else:
                    result = func(*args, **kwargs)

                if metrics_registry is not None:
                    if not hasattr(metrics_registry, success_metric_name):
                        setattr(
                            metrics_registry,
                            success_metric_name,
                            metrics_registry.create_counter(
                                name=success_metric_name,
                                description=f"Total number of successful {func.__name__} executions",
                                labelnames=["component"]
                            )
                        )
                    getattr(metrics_registry, success_metric_name).labels(component="main").inc()
                    metrics_registry.set_health_status(True)
                    logger.info(
                        f"Successfully recorded {success_metric_name} for {func.__name__}",
                        extra={"correlation_id": correlation_id}
                    )

                return result

            except Exception as e:
                if metrics_registry is not None:
                    metrics_registry.record_error(failure_metric_name, component="main")
                    metrics_registry.set_health_status(False)
                    logger.error(
                        f"Failed to execute {func.__name__}: {str(e)}",
                        extra={"correlation_id": correlation_id, "traceback": traceback.format_exc()}
                    )
                raise

            finally:
                set_correlation_id(None)

        return wrapper

    return decorator
