import os
import sys
import time
import uuid
import threading
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

_correlation_context = threading.local()


def generate_correlation_id() -> str:
    """Generate a unique correlation ID for request tracking."""
    return f"req_{uuid.uuid4().hex[:12]}"


def get_correlation_id() -> Optional[str]:
    """Get the current thread's correlation ID."""
    return getattr(_correlation_context, 'correlation_id', None)


def set_correlation_id(correlation_id: str):
    """Set the correlation ID for the current thread."""
    _correlation_context.correlation_id = correlation_id


def _find_project_root() -> str:
    """Find the project root directory by looking for markers."""
    markers = ['pyproject.toml', 'requirements.txt', '.git', 'libs']
    
    start_dir = os.getcwd()
    current = start_dir
    
    for _ in range(10):
        for marker in markers:
            if os.path.exists(os.path.join(current, marker)):
                return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    
    return start_dir


def setup_logger(service_name: str, logs_dir: Optional[str] = None, log_level: Optional[str] = None) -> str:
    """
    Setup logger with file and console output.
    
    Args:
        service_name: Name of the service for log tagging
        logs_dir: Directory for log files (defaults to LOGS_DIR env var or ./logs)
        log_level: Log level (defaults to LOG_LEVEL env var or INFO)
    
    Returns:
        Service name
    """
    def patch_record(record):
        record["extra"]["service"] = service_name
        correlation_id = get_correlation_id()
        if correlation_id:
            record["extra"]["correlation_id"] = correlation_id
        record["extra"]["timestamp"] = time.time()
        return True

    if logs_dir is None:
        logs_dir = os.environ.get('LOGS_DIR')
    
    if logs_dir is None:
        project_root = _find_project_root()
        logs_dir = os.path.join(project_root, "logs")

    os.makedirs(logs_dir, exist_ok=True)

    if log_level is None:
        log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    else:
        log_level = log_level.upper()

    logger.remove()

    # File logging - JSON format for parsing
    logger.add(
        os.path.join(logs_dir, f"{service_name}.log"),
        rotation="500 MB",
        level=log_level,
        filter=patch_record,
        serialize=True,
        format="{time} | {level} | {extra[service]} | {message} | {extra}"
    )

    # Console logging - human-readable format
    console_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{extra[service]}</cyan> | {message} | <white>{extra}</white>"
    if get_correlation_id():
        console_format += " | <yellow>{extra[correlation_id]}</yellow>"

    logger.add(
        sys.stdout,
        format=console_format,
        level=log_level,
        filter=patch_record,
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

    logger.info(f"Logger configured", service=service_name, level=log_level, logs_dir=logs_dir)

    return service_name
