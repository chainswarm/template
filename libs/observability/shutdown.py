import asyncio
import signal
import threading
import time

from loguru import logger

terminate_event = threading.Event()


def shutdown_handler(signum, frame):
    """Handle shutdown signals (SIGINT, SIGTERM)"""
    logger.info(f"Shutdown signal received (signal={signum}). Waiting for current processing to complete...")
    terminate_event.set()
    time.sleep(2)


def install_shutdown_handlers():
    """Install signal handlers for graceful shutdown"""
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)


async def async_wait_for_termination(timeout: float, check_interval: float = 1.0) -> bool:
    """
    Async-compatible wait that checks termination event periodically.
    
   Use this instead of terminate_event.wait() inside async functions.
    The threading.Event.wait() blocks the asyncio event loop, preventing
    signal handlers from being processed. This function uses asyncio.sleep()
    which yields control back to the event loop.
    
    Args:
        timeout: Total wait time in seconds
        check_interval: How often to check terminate_event (default 1s)
    
    Returns:
        True if termination was requested, False if timeout occurred.
    
    Example:
        # In async code, instead of:
        terminate_event.wait(timeout=60)
        
        # Use:
        await async_wait_for_termination(60)
    """
    elapsed = 0.0
    
    while elapsed < timeout:
        if terminate_event.is_set():
            return True
        await asyncio.sleep(min(check_interval, timeout - elapsed))
        elapsed += check_interval
    
    return terminate_event.is_set()
