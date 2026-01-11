"""File I/O operations for loading and saving images."""

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
