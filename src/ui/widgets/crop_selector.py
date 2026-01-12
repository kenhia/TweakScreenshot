"""Crop selector widget for interactive region selection with mouse and keyboard."""

from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent, QMouseEvent, QPainter, QPen
from PySide6.QtWidgets import QWidget


class CropSelector(QWidget):
    """Interactive crop region selector with mouse drag and keyboard controls.

    Allows users to select a rectangular region using:
    - Mouse: Click and drag to create/move selection
    - Keyboard: Arrow keys to move, Shift+Arrow to resize
    - Enter to apply, Escape to cancel
    """

    # Signals
    crop_applied = Signal(int, int, int, int)  # x, y, width, height
    crop_cancelled = Signal()

    # Movement step size in pixels
    MOVE_STEP = 5
    RESIZE_STEP = 5

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize crop selector.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Selection rectangle (in widget coordinates)
        self._selection = QRect()
        self._is_active = False

        # Mouse drag state
        self._dragging = False
        self._drag_start = QPoint()

        # Widget configuration
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

        # Overlay styling
        self._selection_color = QColor(0, 120, 215)  # Blue
        self._selection_border_width = 2

    def activate_selection(self, image_rect: QRect) -> None:
        """Activate crop mode with initial selection covering entire image.

        Args:
            image_rect: Rectangle representing the image bounds
        """
        # Initialize selection to entire image with small margin
        margin = 20
        self._selection = image_rect.adjusted(margin, margin, -margin, -margin)
        self._is_active = True
        self.setFocus()
        self.update()

    def deactivate_selection(self) -> None:
        """Deactivate crop mode and clear selection."""
        self._is_active = False
        self._selection = QRect()
        self.update()

    def is_active(self) -> bool:
        """Check if crop mode is active.

        Returns:
            True if crop selection is active
        """
        return self._is_active

    def get_selection(self) -> tuple[int, int, int, int] | None:
        """Get current selection coordinates.

        Returns:
            Tuple of (x, y, width, height) or None if no selection
        """
        if not self._is_active or self._selection.isEmpty():
            return None
        return (
            self._selection.x(),
            self._selection.y(),
            self._selection.width(),
            self._selection.height(),
        )

    # Mouse event handlers

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Handle mouse press to start drag.

        Args:
            event: Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton and self._is_active:
            # Check if clicking inside selection to move, or outside to create new
            if self._selection.contains(event.pos()):
                self._dragging = True
                self._drag_start = event.pos()
            else:
                # Start new selection
                self._selection = QRect(event.pos(), event.pos())
                self._dragging = True
                self._drag_start = event.pos()
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Handle mouse move to drag selection.

        Args:
            event: Mouse event
        """
        if self._dragging and self._is_active:
            current_pos = event.pos()

            if self._selection.width() > 0 and self._selection.height() > 0:
                # Moving existing selection
                delta = current_pos - self._drag_start
                self._selection.translate(delta)
                self._drag_start = current_pos
            else:
                # Creating new selection
                self._selection = QRect(self._drag_start, current_pos).normalized()

            # Constrain to widget bounds
            self._constrain_to_bounds()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Handle mouse release to end drag.

        Args:
            event: Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False

    # Keyboard event handlers

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Handle keyboard input for crop control.

        Arrow keys: Move selection
        Shift+Arrow keys: Resize selection
        Enter: Apply crop
        Escape: Cancel crop

        Args:
            event: Keyboard event
        """
        if not self._is_active:
            super().keyPressEvent(event)
            return

        key = event.key()
        modifiers = event.modifiers()

        # Enter: Apply crop
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self._apply_crop()
            event.accept()
            return

        # Escape: Cancel crop
        if key == Qt.Key.Key_Escape:
            self.crop_cancelled.emit()
            self.deactivate_selection()
            event.accept()
            return

        # Arrow keys: Move or resize
        if key in (Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right):
            if modifiers & Qt.KeyboardModifier.ShiftModifier:
                self._resize_selection(key)
            else:
                self._move_selection(key)
            event.accept()
            return

        super().keyPressEvent(event)

    def _move_selection(self, key: Qt.Key) -> None:
        """Move selection in direction of arrow key.

        Args:
            key: Arrow key pressed
        """
        dx, dy = 0, 0

        if key == Qt.Key.Key_Left:
            dx = -self.MOVE_STEP
        elif key == Qt.Key.Key_Right:
            dx = self.MOVE_STEP
        elif key == Qt.Key.Key_Up:
            dy = -self.MOVE_STEP
        elif key == Qt.Key.Key_Down:
            dy = self.MOVE_STEP

        self._selection.translate(dx, dy)
        self._constrain_to_bounds()
        self.update()

    def _resize_selection(self, key: Qt.Key) -> None:
        """Resize selection with Shift+Arrow keys.

        Shift+Up/Down: Adjust height
        Shift+Left/Right: Adjust width

        Args:
            key: Arrow key pressed with Shift modifier
        """
        if key == Qt.Key.Key_Left:
            # Decrease width
            new_width = max(20, self._selection.width() - self.RESIZE_STEP)
            self._selection.setWidth(new_width)
        elif key == Qt.Key.Key_Right:
            # Increase width
            self._selection.setWidth(self._selection.width() + self.RESIZE_STEP)
        elif key == Qt.Key.Key_Up:
            # Decrease height
            new_height = max(20, self._selection.height() - self.RESIZE_STEP)
            self._selection.setHeight(new_height)
        elif key == Qt.Key.Key_Down:
            # Increase height
            self._selection.setHeight(self._selection.height() + self.RESIZE_STEP)

        self._constrain_to_bounds()
        self.update()

    def _constrain_to_bounds(self) -> None:
        """Constrain selection to widget bounds (image edges)."""
        widget_rect = self.rect()

        # Ensure selection stays within widget bounds
        x = max(0, min(self._selection.x(), widget_rect.width() - self._selection.width()))
        y = max(0, min(self._selection.y(), widget_rect.height() - self._selection.height()))

        # Ensure minimum size
        width = min(self._selection.width(), widget_rect.width())
        height = min(self._selection.height(), widget_rect.height())

        self._selection = QRect(x, y, width, height)

    def _apply_crop(self) -> None:
        """Apply the current crop selection."""
        if self._is_active and not self._selection.isEmpty():
            self.crop_applied.emit(
                self._selection.x(),
                self._selection.y(),
                self._selection.width(),
                self._selection.height(),
            )
            self.deactivate_selection()

    # Painting

    def paintEvent(self, event) -> None:  # noqa: N802
        """Paint crop selection overlay.

        Args:
            event: Paint event
        """
        super().paintEvent(event)

        if not self._is_active or self._selection.isEmpty():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw semi-transparent overlay outside selection
        overlay_color = QColor(0, 0, 0, 100)  # Semi-transparent black
        painter.fillRect(self.rect(), overlay_color)

        # Clear selection area (show image underneath)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.fillRect(self._selection, Qt.GlobalColor.transparent)

        # Draw selection border
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        pen = QPen(self._selection_color, self._selection_border_width)
        pen.setStyle(Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self._selection)

        painter.end()
