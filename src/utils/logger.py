"""Logging configuration for TweakScreenshot application."""

import logging
from pathlib import Path


def setup_logger(name: str = "tweakscreenshot", log_file: Path | None = None) -> logging.Logger:
    """Configure application logger.

    Args:
        name: Logger name
        log_file: Path to log file (default: tweakscreenshot.log in current directory)

    Returns:
        Configured logger instance
    """
    if log_file is None:
        log_file = Path("tweakscreenshot.log")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # File handler for persistent logs
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Formatter with timestamp and level
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_operation(logger: logging.Logger, operation: str, duration_ms: float) -> None:
    """Log an operation with duration tracking.

    Logs at INFO level for all operations, adds WARNING for slow operations (>500ms).

    Args:
        logger: Logger instance
        operation: Operation name (e.g., 'crop', 'resize', 'load')
        duration_ms: Operation duration in milliseconds
    """
    logger.info(f"Operation '{operation}' completed in {duration_ms:.2f}ms")

    # Constitution V: Performance monitoring for operations >500ms
    if duration_ms > 500:
        logger.warning(
            f"Slow operation detected: '{operation}' took {duration_ms:.2f}ms (>500ms threshold)"
        )
