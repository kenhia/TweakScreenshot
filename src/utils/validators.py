"""Input validation utilities for image operations."""

from pathlib import Path


def validate_image_dimensions(width: int, height: int) -> None:
    """Validate image dimensions are positive integers.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Raises:
        ValueError: If dimensions are not positive
    """
    if width <= 0 or height <= 0:
        raise ValueError(f"Dimensions must be positive, got: {width}x{height}")


def validate_crop_region(
    x: int, y: int, width: int, height: int, image_width: int, image_height: int
) -> None:
    """Validate crop region is within image bounds.

    Args:
        x: Left coordinate (0-based)
        y: Top coordinate (0-based)
        width: Selection width
        height: Selection height
        image_width: Parent image width
        image_height: Parent image height

    Raises:
        ValueError: If crop region is invalid or out of bounds
    """
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError(f"Invalid crop region: x={x}, y={y}, width={width}, height={height}")

    if x + width > image_width or y + height > image_height:
        raise ValueError(
            f"Crop region ({x}, {y}, {width}, {height}) exceeds image bounds "
            f"({image_width}x{image_height})"
        )


def validate_file_path(path: Path) -> None:
    """Validate file path exists and is readable.

    Args:
        path: Path to validate

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If path is not a file
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")


def validate_image_format(format_str: str) -> None:
    """Validate image format is supported.

    Args:
        format_str: Format string (e.g., 'PNG', 'JPEG', 'BMP')

    Raises:
        ValueError: If format is not supported
    """
    supported = ("PNG", "JPEG", "JPG", "BMP")
    if format_str.upper() not in supported:
        raise ValueError(f"Unsupported format: {format_str}. Supported: {', '.join(supported)}")


def validate_resize_parameters(
    width: int | None, height: int | None, percentage: float | None
) -> None:
    """Validate resize parameters.

    Args:
        width: Target width in pixels (optional)
        height: Target height in pixels (optional)
        percentage: Scale percentage (optional)

    Raises:
        ValueError: If parameters are invalid
    """
    # Must specify either dimensions or percentage, not both
    has_dimensions = width is not None or height is not None
    has_percentage = percentage is not None

    if not has_dimensions and not has_percentage:
        raise ValueError("Must specify either dimensions or percentage")

    if has_dimensions and has_percentage:
        raise ValueError("Cannot specify both dimensions and percentage")

    # Validate dimensions if provided
    if width is not None and width <= 0:
        raise ValueError(f"Width must be positive, got: {width}")

    if height is not None and height <= 0:
        raise ValueError(f"Height must be positive, got: {height}")

    # Validate percentage if provided
    if percentage is not None and percentage <= 0:
        raise ValueError(f"Percentage must be positive, got: {percentage}")


def check_extreme_dimensions(width: int, height: int) -> str | None:
    """Check if dimensions are unusually large or small.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        Warning message if dimensions are extreme, None otherwise
    """
    if width < 50 or height < 50:
        return f"Image is very small ({width}x{height}px). Quality may be poor."

    if width > 10000 or height > 10000:
        return (
            f"Image is very large ({width}x{height}px). "
            f"This may use significant memory or processing time."
        )

    return None


def validate_resize_dimensions(width: int, height: int) -> None:
    """Validate resize dimensions are positive integers.

    Args:
        width: Target width in pixels
        height: Target height in pixels

    Raises:
        ValueError: If dimensions are not positive
    """
    if width <= 0 or height <= 0:
        raise ValueError(f"Resize dimensions must be positive, got: {width}x{height}")


def is_extreme_dimension(width: int, height: int) -> bool:
    """Check if dimensions are extreme (too small or too large).

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        True if dimensions are extreme, False otherwise
    """
    return width < 50 or height < 50 or width > 10000 or height > 10000
