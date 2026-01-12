"""Image viewer widget with scroll area for displaying screenshots."""

from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

from ui.widgets.crop_selector import CropSelector


class ImageViewer(QScrollArea):
    """Scrollable image viewer widget with crop selection support."""

    # Signals
    crop_requested = Signal(int, int, int, int)  # x, y, width, height
    crop_cancelled = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize image viewer.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Create container widget for image and crop overlay
        self._container = QWidget()
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Create label to hold image
        self._image_label = QLabel()
        self._image_label.setScaledContents(False)
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._image_label)

        # Create crop selector overlay (initially hidden)
        self._crop_selector = CropSelector(self._image_label)
        self._crop_selector.crop_applied.connect(self._on_crop_applied)
        self._crop_selector.crop_cancelled.connect(self._on_crop_cancelled)
        self._crop_selector.hide()

        # Configure scroll area
        self.setWidget(self._container)
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

        # Update crop selector size to match image
        self._crop_selector.setGeometry(0, 0, pixmap.width(), pixmap.height())

    def clear_image(self) -> None:
        """Clear the currently displayed image."""
        self._image_label.clear()
        self._has_image = False
        self._crop_selector.deactivate_selection()
        self._crop_selector.hide()

    def has_image(self) -> bool:
        """Check if viewer has an image.

        Returns:
            True if image is displayed, False otherwise
        """
        return self._has_image

    def start_crop_mode(self) -> None:
        """Activate crop mode with selection overlay."""
        if not self._has_image:
            return

        # Show crop selector and activate
        pixmap = self._image_label.pixmap()
        if pixmap:
            image_rect = QRect(0, 0, pixmap.width(), pixmap.height())
            self._crop_selector.show()
            self._crop_selector.raise_()
            self._crop_selector.activate_selection(image_rect)

    def cancel_crop_mode(self) -> None:
        """Cancel crop mode and hide selection overlay."""
        self._crop_selector.deactivate_selection()
        self._crop_selector.hide()

    def is_crop_mode_active(self) -> bool:
        """Check if crop mode is currently active.

        Returns:
            True if crop mode is active
        """
        return self._crop_selector.is_active()

    def _on_crop_applied(self, x: int, y: int, width: int, height: int) -> None:
        """Handle crop application from selector.

        Args:
            x: X coordinate of crop region
            y: Y coordinate of crop region
            width: Width of crop region
            height: Height of crop region
        """
        self._crop_selector.hide()
        self.crop_requested.emit(x, y, width, height)

    def _on_crop_cancelled(self) -> None:
        """Handle crop cancellation from selector."""
        self._crop_selector.hide()
        self.crop_cancelled.emit()
