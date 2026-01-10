"""Edit history tracking for image operations."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from PIL import Image as PILImage


@dataclass
class EditOperation:
    """Represents a single edit operation.

    Attributes:
        type: Operation type ('crop', 'resize')
        timestamp: When the operation was performed
        parameters: Operation-specific parameters (e.g., crop coordinates)
    """

    type: str
    timestamp: datetime
    parameters: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate operation type."""
        if self.type not in ("crop", "resize"):
            raise ValueError(f"Invalid operation type: {self.type}")


@dataclass
class EditHistory:
    """Tracks editing operations for revert functionality.

    Attributes:
        operations: Stack of operations applied to the image
        original_image: Reference to the unmodified original
    """

    original_image: PILImage.Image
    operations: list[EditOperation] = field(default_factory=list)

    def add_operation(self, op: EditOperation) -> None:
        """Add operation to history.

        Args:
            op: The operation to record

        Raises:
            ValueError: If operations list exceeds maximum size
        """
        if len(self.operations) >= 100:
            raise ValueError("Operation history limit reached (100 operations)")

        self.operations.append(op)

    def clear(self) -> None:
        """Clear all operations (called after revert or new image load)."""
        self.operations.clear()

    def get_operation_summary(self) -> str:
        """Get human-readable summary of operations.

        Returns:
            Summary string like "2 operations: crop, resize"
        """
        if not self.operations:
            return "No operations"

        count = len(self.operations)
        types = ", ".join(op.type for op in self.operations)
        return f"{count} operation{'s' if count > 1 else ''}: {types}"
