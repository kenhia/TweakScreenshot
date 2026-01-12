"""Core image editor with load, edit, and save operations."""

from datetime import UTC, datetime
from pathlib import Path

from PIL import Image as PILImage

from core.clipboard import load_image_from_clipboard
from core.file_ops import load_image_from_file, save_image_to_file
from models.edit_history import EditHistory, EditOperation
from models.image_model import Image
from models.selection import Selection


class ImageEditor:
    """Orchestrates image loading, editing operations, and state management."""

    def __init__(self) -> None:
        """Initialize image editor with empty state."""
        self._image: Image | None = None
        self._edit_history: EditHistory | None = None

    def load_from_file(self, file_path: Path) -> None:
        """Load image from file system.

        Args:
            file_path: Path to image file (PNG, JPG, BMP)

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file is not a valid image or format not supported
            PIL.UnidentifiedImageError: If file is corrupted

        Postconditions:
            - has_image() returns True
            - get_current_image() returns PIL Image object
            - has_unsaved_changes() returns False
            - get_edit_history() returns empty list
        """
        pil_img = load_image_from_file(file_path)

        # Determine format from file extension
        format_str = file_path.suffix.upper().lstrip(".")
        if format_str == "JPG":
            format_str = "JPEG"

        # Create Image model (original and current are same initially)
        self._image = Image(
            original_data=pil_img.copy(),
            current_data=pil_img.copy(),
            format=format_str,
            file_path=file_path,
        )

        # Initialize edit history
        self._edit_history = EditHistory(original_image=pil_img.copy())

    def load_from_clipboard(self) -> None:
        """Load image from system clipboard.

        Raises:
            ValueError: If clipboard does not contain image data

        Postconditions:
            - has_image() returns True
            - get_current_image() returns PIL Image object
            - get_file_path() returns None (clipboard has no file path)
            - has_unsaved_changes() returns False
        """
        pil_img = load_image_from_clipboard()

        # Create Image model (no file path or format for clipboard)
        self._image = Image(
            original_data=pil_img.copy(),
            current_data=pil_img.copy(),
            format=None,
            file_path=None,
        )

        # Initialize edit history
        self._edit_history = EditHistory(original_image=pil_img.copy())

    def save_to_file(self, file_path: Path, format_str: str, quality: int = 90) -> None:
        """Save current image to file system.

        Args:
            file_path: Destination file path
            format_str: Image format (PNG, JPEG, BMP)
            quality: JPG quality (1-100), default 90. Ignored for PNG/BMP.

        Raises:
            ValueError: If no image loaded or format not supported
            IOError: If save fails

        Postconditions:
            - has_unsaved_changes() returns False
            - get_file_path() returns file_path
        """
        if self._image is None:
            raise ValueError("No image loaded. Load an image before saving.")

        # Save current image data
        save_image_to_file(self._image.current_data, file_path, format_str, quality)

        # Update image model with new file path and format
        self._image.file_path = file_path
        self._image.format = format_str
        self._image.has_unsaved_changes = False

    def has_image(self) -> bool:
        """Check if an image is currently loaded.

        Returns:
            True if image is loaded, False otherwise
        """
        return self._image is not None

    def get_current_image(self) -> PILImage.Image | None:
        """Get the current edited image.

        Returns:
            PIL Image object or None if no image loaded
        """
        if self._image is None:
            return None
        return self._image.current_data

    def get_original_image(self) -> PILImage.Image | None:
        """Get the original unedited image.

        Returns:
            PIL Image object or None if no image loaded
        """
        if self._image is None:
            return None
        return self._image.original_data

    def get_file_path(self) -> Path | None:
        """Get the file path of loaded image.

        Returns:
            Path object or None if image from clipboard
        """
        if self._image is None:
            return None
        return self._image.file_path

    def has_unsaved_changes(self) -> bool:
        """Check if image has unsaved changes.

        Returns:
            True if there are unsaved changes, False otherwise
        """
        if self._image is None:
            return False
        return self._image.has_unsaved_changes

    def get_edit_history(self) -> list:
        """Get list of edit operations.

        Returns:
            List of EditOperation objects, or empty list if no image
        """
        if self._edit_history is None:
            return []
        return self._edit_history.operations.copy()

    def crop(self, x: int, y: int, width: int, height: int) -> None:
        """Crop image to specified rectangular region.

        Args:
            x: Left coordinate (pixels from left edge)
            y: Top coordinate (pixels from top edge)
            width: Width of crop region in pixels
            height: Height of crop region in pixels

        Raises:
            ValueError: If no image loaded, invalid dimensions, or region outside bounds

        Postconditions:
            - get_current_image() returns cropped image
            - has_unsaved_changes() returns True
            - get_edit_history() includes crop operation
        """
        if self._image is None:
            raise ValueError("No image loaded. Load an image before cropping.")

        # Validate dimensions
        if width <= 0 or height <= 0:
            raise ValueError("Crop dimensions must be positive")

        # Create selection and validate bounds
        selection = Selection(x=x, y=y, width=width, height=height)
        current_img = self._image.current_data

        if not selection.is_within_bounds(current_img.width, current_img.height):
            raise ValueError(
                f"Crop region ({x}, {y}, {width}, {height}) "
                f"outside image bounds ({current_img.width}, {current_img.height})"
            )

        # Perform crop
        crop_box = selection.to_tuple()
        cropped_img = current_img.crop(crop_box)

        # Update image model
        self._image.current_data = cropped_img
        self._image.has_unsaved_changes = True

        # Record operation in history
        if self._edit_history:
            operation = EditOperation(
                type="crop",
                timestamp=datetime.now(UTC),
                parameters={"x": x, "y": y, "width": width, "height": height},
            )
            self._edit_history.add_operation(operation)

    def revert(self) -> None:
        """Revert image to original unedited state.

        Raises:
            ValueError: If no image loaded

        Postconditions:
            - get_current_image() returns copy of original image
            - has_unsaved_changes() returns False
            - get_edit_history() returns empty list
        """
        if self._image is None:
            raise ValueError("No image loaded. Load an image before reverting.")

        # Restore original image data
        self._image.current_data = self._image.original_data.copy()
        self._image.has_unsaved_changes = False

        # Clear edit history
        if self._edit_history:
            self._edit_history.clear()

    def resize(self, width: int | None, height: int | None) -> None:
        """Resize image to new dimensions.

        Args:
            width: Target width in pixels (None to auto-calculate from height)
            height: Target height in pixels (None to auto-calculate from width)

        Raises:
            ValueError: If no image loaded, or both/neither dimensions provided,
                       or dimensions are not positive

        Postconditions:
            - Image resized to new dimensions using LANCZOS resampling
            - has_unsaved_changes() returns True
            - Edit operation recorded in history
        """
        if self._image is None:
            raise ValueError("No image loaded. Load an image before resizing.")

        current_img = self._image.current_data

        # Calculate missing dimension if only one provided (maintain aspect ratio)
        if width is not None and height is None:
            # Calculate height from width
            aspect_ratio = current_img.height / current_img.width
            height = int(width * aspect_ratio)
        elif height is not None and width is None:
            # Calculate width from height
            aspect_ratio = current_img.width / current_img.height
            width = int(height * aspect_ratio)
        elif width is None and height is None:
            raise ValueError("Must provide at least one dimension (width or height)")

        # Validate dimensions (width and height are guaranteed to be int here)
        from utils.validators import validate_resize_dimensions

        assert width is not None and height is not None
        validate_resize_dimensions(width, height)

        # Resize using LANCZOS filter for high quality
        resized_img = current_img.resize((width, height), PILImage.Resampling.LANCZOS)

        # Update image model
        self._image.current_data = resized_img
        self._image.has_unsaved_changes = True

        # Record operation in history
        if self._edit_history:
            operation = EditOperation(
                type="resize",
                timestamp=datetime.now(UTC),
                parameters={"width": width, "height": height},
            )
            self._edit_history.add_operation(operation)
