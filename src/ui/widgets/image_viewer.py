"""Image viewer widget with scroll area for displaying screenshots."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QScrollArea, QWidget


class ImageViewer(QScrollArea):
    """Scrollable image viewer widget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize image viewer.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Create label to hold image
        self._image_label = QLabel()
        self._image_label.setScaledContents(False)
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Configure scroll area
        self.setWidget(self._image_label)
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # No image initially
        self._has_image = False

    def set_image(self, pixmap: QPixmap) -> None:
        """Set image to display.

        Args:
            pixmap: QPixmap to display
        """
        self._image_label.setPixmap(pixmap)
        self._image_label.resize(pixmap.size())
        self._has_image = True

    def clear_image(self) -> None:
        """Clear the currently displayed image."""
        self._image_label.clear()
        self._has_image = False

    def has_image(self) -> bool:
        """Check if viewer has an image.

        Returns:
            True if image is displayed, False otherwise
        """
        return self._has_image
