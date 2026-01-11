"""File I/O operations for loading and saving images."""

import shutil
from pathlib import Path

from PIL import Image as PILImage

from utils.validators import validate_file_path, validate_image_format


def load_image_from_file(file_path: Path) -> PILImage.Image:
    """Load image from file system.

    Args:
        file_path: Path to image file (PNG, JPG, BMP)

    Returns:
        PIL Image object

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file is not a valid image or format not supported
        PIL.UnidentifiedImageError: If file is corrupted
    """
    validate_file_path(file_path)

    try:
        img = PILImage.open(file_path)

        # Convert to RGB or RGBA if needed
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Verify it's a supported format
        if img.format:
            validate_image_format(img.format)

        return img

    except PILImage.UnidentifiedImageError as e:
        raise ValueError("Cannot load image: Invalid or corrupted file") from e
    except Exception as e:
        raise ValueError(f"Cannot load image: {e}") from e


def save_image_to_file(
    image: PILImage.Image, file_path: Path, format_str: str, quality: int = 90
) -> None:
    """Save image to file system.

    Args:
        image: PIL Image object to save
        file_path: Destination file path
        format_str: Image format (PNG, JPEG, BMP)
        quality: JPG quality (1-100), default 90. Ignored for PNG/BMP.

    Raises:
        ValueError: If format not supported
        IOError: If save fails
    """
    # Validate format
    supported_formats = {"PNG", "JPEG", "BMP"}
    if format_str not in supported_formats:
        raise ValueError(
            f"Unsupported format: {format_str}. Supported formats: {supported_formats}"
        )

    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save based on format
    try:
        if format_str == "JPEG":
            # Convert RGBA to RGB for JPG (no transparency support)
            if image.mode == "RGBA":
                rgb_img = PILImage.new("RGB", image.size, (255, 255, 255))
                rgb_img.paste(image, mask=image.split()[3])  # Alpha channel as mask
                rgb_img.save(file_path, format_str, quality=quality)
            else:
                image.save(file_path, format_str, quality=quality)
        else:
            # PNG and BMP
            image.save(file_path, format_str)
    except Exception as e:
        raise OSError(f"Cannot save image: {e}") from e


def estimate_file_size(width: int, height: int, format_str: str) -> int:
    """Estimate file size for image.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        format_str: Image format (PNG, JPEG, BMP)

    Returns:
        Estimated file size in bytes
    """
    pixels = width * height
    megapixels = pixels / 1_000_000  # For scaling

    # Rough estimates based on typical compression ratios for screenshots
    if format_str == "PNG":
        # PNG: ~20-30 KB per megapixel for screenshots (flat colors compress well)
        # Use 25 KB/MP estimate
        return int(megapixels * 25_000)
    elif format_str == "JPEG":
        # JPEG quality 90: ~10 KB per megapixel
        return int(megapixels * 10_000)
    elif format_str == "BMP":
        # BMP: Uncompressed RGB = 3 bytes per pixel
        return pixels * 3
    else:
        # Default conservative estimate
        return int(megapixels * 25_000)


def check_disk_space(file_path: Path, required_bytes: int) -> bool:
    """Check if sufficient disk space available.

    Args:
        file_path: Path where file will be saved
        required_bytes: Required space in bytes

    Returns:
        True if sufficient space available, False otherwise

    Raises:
        ValueError: If path does not exist
    """
    # Get parent directory (file may not exist yet)
    directory = file_path.parent if file_path.is_file() or not file_path.exists() else file_path

    if not directory.exists():
        raise ValueError(f"Path does not exist: {directory}")

    # Check available space
    disk_stat = shutil.disk_usage(directory)
    return disk_stat.free > required_bytes
