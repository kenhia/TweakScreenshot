"""Core image editor with load, edit, and save operations."""

from pathlib import Path

from PIL import Image as PILImage

from core.clipboard import load_image_from_clipboard
from core.file_ops import load_image_from_file
from models.edit_history import EditHistory
from models.image_model import Image


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
