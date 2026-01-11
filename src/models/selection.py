"""Selection model for crop operations."""

from dataclasses import dataclass


@dataclass
class Selection:
    """Rectangular selection region for cropping.

    Attributes:
        x: Left coordinate (pixels from left edge)
        y: Top coordinate (pixels from top edge)
        width: Width of selection in pixels
        height: Height of selection in pixels
    """

    x: int
    y: int
    width: int
    height: int

    def __post_init__(self) -> None:
        """Validate selection parameters.

        Raises:
            ValueError: If coordinates are negative or dimensions are not positive
        """
        if self.x < 0 or self.y < 0:
            raise ValueError("Selection coordinates cannot be negative")

        if self.width <= 0 or self.height <= 0:
            raise ValueError("Selection dimensions must be positive")

    def is_within_bounds(self, image_width: int, image_height: int) -> bool:
        """Check if selection is within image bounds.

        Args:
            image_width: Width of image in pixels
            image_height: Height of image in pixels

        Returns:
            True if selection is fully within image, False otherwise
        """
        return (self.x + self.width) <= image_width and (self.y + self.height) <= image_height

    def to_tuple(self) -> tuple[int, int, int, int]:
        """Convert selection to PIL crop tuple.

        Returns:
            Tuple of (left, upper, right, lower) coordinates for PIL.Image.crop()
        """
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def area(self) -> int:
        """Calculate selection area in pixels.

        Returns:
            Area in square pixels
        """
        return self.width * self.height
