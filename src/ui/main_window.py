"""Main window for TweakScreenshot application."""

import time
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeyEvent, QPixmap
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMenuBar, QStatusBar

from core.clipboard import pil_to_qimage
from core.image_editor import ImageEditor
from ui.widgets.image_viewer import ImageViewer
from utils.error_handlers import show_error_dialog
from utils.logger import log_operation, setup_logger


class MainWindow(QMainWindow):
    """Main application window with menu bar, toolbar, and status bar."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        self.setWindowTitle("TweakScreenshot")
        self.setMinimumSize(800, 600)

        # Initialize image editor
        self._editor = ImageEditor()
        self._logger = setup_logger()

        # Initialize UI components
        self._setup_menus()
        self._setup_status_bar()
        self._setup_central_widget()
        self._connect_signals()

    def _setup_menus(self) -> None:
        """Create menu bar with File, Edit, and Help menus."""
        menu_bar = self.menuBar()
        if menu_bar is None:
            menu_bar = QMenuBar(self)
            self.setMenuBar(menu_bar)

        # File menu
        file_menu = menu_bar.addMenu("&File")

        self.action_open = QAction("&Open...", self)
        self.action_open.setShortcut("Ctrl+O")
        self.action_open.setStatusTip("Open image file")
        file_menu.addAction(self.action_open)

        file_menu.addSeparator()

        self.action_save_as = QAction("Save &As...", self)
        self.action_save_as.setShortcut("Ctrl+Shift+S")
        self.action_save_as.setStatusTip("Save image to file")
        self.action_save_as.setEnabled(False)  # Disabled until image loaded
        file_menu.addAction(self.action_save_as)

        file_menu.addSeparator()

        self.action_exit = QAction("E&xit", self)
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_exit.setStatusTip("Exit application")
        self.action_exit.triggered.connect(self.close)
        file_menu.addAction(self.action_exit)

        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")

        self.action_crop = QAction("&Crop", self)
        self.action_crop.setStatusTip("Crop image to selection")
        self.action_crop.setEnabled(False)  # Disabled until selection made
        edit_menu.addAction(self.action_crop)

        self.action_resize = QAction("&Resize...", self)
        self.action_resize.setStatusTip("Resize image")
        self.action_resize.setEnabled(False)  # Disabled until image loaded
        edit_menu.addAction(self.action_resize)

        edit_menu.addSeparator()

        self.action_revert = QAction("Re&vert", self)
        self.action_revert.setShortcut("Ctrl+R")
        self.action_revert.setStatusTip("Revert to original image")
        self.action_revert.setEnabled(False)  # Disabled until edits made
        edit_menu.addAction(self.action_revert)

        # Help menu
        help_menu = menu_bar.addMenu("&Help")

        self.action_about = QAction("&About", self)
        self.action_about.setStatusTip("About TweakScreenshot")
        help_menu.addAction(self.action_about)

    def _setup_status_bar(self) -> None:
        """Create status bar for displaying image dimensions and messages."""
        status_bar = self.statusBar()
        if status_bar is None:
            status_bar = QStatusBar(self)
            self.setStatusBar(status_bar)

        status_bar.showMessage("Ready")

    def _setup_central_widget(self) -> None:
        """Create central widget with image viewer."""
        self._image_viewer = ImageViewer()
        self.setCentralWidget(self._image_viewer)

    def _connect_signals(self) -> None:
        """Connect menu actions to handlers."""
        self.action_open.triggered.connect(self._handle_open_file)

    def update_status(self, message: str) -> None:
        """Update status bar message.

        Args:
            message: Status message to display
        """
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage(message)

    def update_dimensions_status(self, width: int, height: int) -> None:
        """Update status bar with image dimensions.

        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.update_status(f"Image: {width}x{height}px")

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Handle keyboard shortcuts.

        Args:
            event: Key event
        """
        # Ctrl-V: Paste from clipboard
        if event.key() == Qt.Key.Key_V and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._handle_paste_clipboard()
        else:
            super().keyPressEvent(event)

    def _handle_open_file(self) -> None:
        """Handle File > Open action."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)"
        )

        if not file_path:
            return  # User cancelled

        try:
            start_time = time.time()
            self._editor.load_from_file(Path(file_path))
            duration_ms = (time.time() - start_time) * 1000

            self._logger.info(f"Loaded image from {file_path}")
            log_operation(self._logger, "load_from_file", duration_ms)

            self._display_current_image()
            self._update_ui_state()

        except Exception as e:
            self._logger.error(f"Failed to load image: {e}")
            show_error_dialog(
                self,
                "Cannot Load Image",
                "Failed to load image from file.",
                f"Error: {e}\n\nSupported formats: PNG, JPG, BMP",
            )

    def _handle_paste_clipboard(self) -> None:
        """Handle Ctrl-V paste from clipboard."""
        try:
            start_time = time.time()
            self._editor.load_from_clipboard()
            duration_ms = (time.time() - start_time) * 1000

            self._logger.info("Loaded image from clipboard")
            log_operation(self._logger, "load_from_clipboard", duration_ms)

            self._display_current_image()
            self._update_ui_state()

        except ValueError as e:
            # Expected error when clipboard is empty
            self._logger.warning(f"Clipboard paste failed: {e}")
            show_error_dialog(
                self,
                "No Image in Clipboard",
                "Clipboard does not contain image data.",
                "Please copy an image to the clipboard and try again.",
            )
        except Exception as e:
            self._logger.error(f"Unexpected error pasting from clipboard: {e}")
            show_error_dialog(
                self, "Cannot Paste Image", "Failed to paste image from clipboard.", f"Error: {e}"
            )

    def _display_current_image(self) -> None:
        """Display current image in viewer."""
        pil_img = self._editor.get_current_image()
        if pil_img is None:
            return

        # Convert PIL Image to QPixmap
        qimage = pil_to_qimage(pil_img)
        pixmap = QPixmap.fromImage(qimage)

        # Display in viewer
        self._image_viewer.set_image(pixmap)

        # Update status bar with dimensions
        self.update_dimensions_status(pil_img.width, pil_img.height)

    def _update_ui_state(self) -> None:
        """Update menu item enabled states based on current state."""
        has_image = self._editor.has_image()

        # Enable actions when image is loaded
        self.action_save_as.setEnabled(has_image)
        self.action_resize.setEnabled(has_image)
