"""Image entity representing the screenshot being edited."""

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image as PILImage


@dataclass
class Image:
    """Represents a screenshot with original and current state.

    Attributes:
        original_data: The unmodified image (immutable after load)
        current_data: The current edited version
        format: Original file format ('PNG', 'JPEG', 'BMP', None if from clipboard)
        file_path: Original file path if loaded from file, None if pasted
        has_unsaved_changes: Flag indicating if current differs from last save
    """

    original_data: PILImage.Image
    current_data: PILImage.Image
    format: str | None = None
    file_path: Path | None = None
    has_unsaved_changes: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        """Validate image data after initialization."""
        if self.original_data.width <= 0 or self.original_data.height <= 0:
            raise ValueError("Image dimensions must be positive")

        if self.format and self.format not in ("PNG", "JPEG", "BMP"):
            raise ValueError(f"Unsupported format: {self.format}")

        # Ensure images are in RGB or RGBA mode
        if self.original_data.mode not in ("RGB", "RGBA"):
            raise ValueError(f"Image must be RGB or RGBA, got: {self.original_data.mode}")

    @property
    def width(self) -> int:
        """Current image width in pixels."""
        return self.current_data.width

    @property
    def height(self) -> int:
        """Current image height in pixels."""
        return self.current_data.height

    def mark_modified(self) -> None:
        """Mark image as having unsaved changes."""
        self.has_unsaved_changes = True

    def clear_modified_flag(self) -> None:
        """Clear the unsaved changes flag (called after save)."""
        self.has_unsaved_changes = False
