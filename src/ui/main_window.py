"""Main window for TweakScreenshot application."""

import time
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeyEvent, QPixmap
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMenuBar, QStatusBar

from core.clipboard import pil_to_qimage
from core.image_editor import ImageEditor
from ui.widgets.image_viewer import ImageViewer
from utils.error_handlers import show_confirmation_dialog, show_error_dialog
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
        self.action_save_as.triggered.connect(self._handle_save_as)
        self.action_revert.triggered.connect(self._handle_revert)
        self.action_resize.triggered.connect(self._handle_resize)
        self.action_revert.triggered.connect(self._handle_revert)

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
        has_unsaved = self._editor.has_unsaved_changes()

        # Enable actions when image is loaded
        self.action_save_as.setEnabled(has_image)
        self.action_resize.setEnabled(has_image)

        # Enable revert only when there are unsaved changes
        self.action_revert.setEnabled(has_image and has_unsaved)

    def _handle_save_as(self) -> None:
        """Handle File > Save As action."""
        if not self._editor.has_image():
            return

        # Open save dialog with format filters
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp);;All Files (*.*)",
        )

        if not file_path:
            return  # User cancelled

        path_obj = Path(file_path)

        # T047: Check if file exists and confirm overwrite
        if path_obj.exists():
            from PySide6.QtWidgets import QMessageBox

            reply = show_confirmation_dialog(
                self,
                "Overwrite File?",
                f"File '{path_obj.name}' already exists.",
                "Do you want to overwrite it?",
            )
            if reply != QMessageBox.StandardButton.Yes:
                return  # User cancelled overwrite

        # Determine format from filter or extension
        format_str = self._get_format_from_filter(selected_filter, path_obj)

        # T049: Get JPG quality if saving as JPEG
        quality = 90  # Default
        if format_str == "JPEG":
            from PySide6.QtWidgets import QInputDialog

            quality, ok = QInputDialog.getInt(
                self,
                "JPEG Quality",
                "Select JPEG quality (1-100):",
                90,  # Default value
                1,  # Minimum
                100,  # Maximum
                1,  # Step
            )
            if not ok:
                return  # User cancelled

        # T048: Check disk space
        from core.file_ops import check_disk_space, estimate_file_size

        pil_img = self._editor.get_current_image()
        if pil_img:
            estimated_size = estimate_file_size(pil_img.width, pil_img.height, format_str)
            if not check_disk_space(path_obj, estimated_size):
                details = (
                    f"Required: {estimated_size / 1024:.1f} KB\n"
                    "Please free up disk space and try again."
                )
                show_error_dialog(
                    self,
                    "Insufficient Disk Space",
                    "Cannot save image due to insufficient disk space.",
                    details,
                )
                return

        # T050: Save with logging
        try:
            start_time = time.time()
            self._editor.save_to_file(path_obj, format_str, quality)
            duration_ms = (time.time() - start_time) * 1000

            self._logger.info(
                f"Saved image to {file_path} (format={format_str}, quality={quality})"
            )
            log_operation(self._logger, "save_to_file", duration_ms)

            self.update_status(f"Saved to {path_obj.name}")

        except Exception as e:
            self._logger.error(f"Failed to save image: {e}")
            show_error_dialog(
                self,
                "Cannot Save Image",
                "Failed to save image to file.",
                f"Error: {e}",
            )

    def _get_format_from_filter(self, selected_filter: str, path_obj: Path) -> str:
        """Determine image format from filter string or file extension.

        Args:
            selected_filter: Filter string from QFileDialog
            path_obj: File path object

        Returns:
            Format string (PNG, JPEG, BMP)
        """
        # Try to extract format from selected filter
        if "PNG" in selected_filter.upper():
            return "PNG"
        elif "JPEG" in selected_filter.upper() or "JPG" in selected_filter.upper():
            return "JPEG"
        elif "BMP" in selected_filter.upper():
            return "BMP"

        # Fall back to file extension
        ext = path_obj.suffix.upper().lstrip(".")
        if ext == "JPG":
            return "JPEG"
        elif ext in ("PNG", "BMP"):
            return ext
        else:
            # Default to PNG
            return "PNG"

    def _handle_revert(self) -> None:
        """Handle Edit > Revert action to restore original image."""
        if not self._editor.has_image():
            return

        try:
            start_time = time.time()
            self._editor.revert()
            duration_ms = (time.time() - start_time) * 1000

            self._logger.info("Reverted to original image")
            log_operation(self._logger, "revert", duration_ms)

            self._display_current_image()
            self._update_ui_state()
            self.update_status("Image reverted to original")

        except Exception as e:
            self._logger.error(f"Failed to revert image: {e}")
            show_error_dialog(
                self, "Cannot Revert Image", "Failed to revert to original image.", f"Error: {e}"
            )

    def _handle_resize(self) -> None:
        """Handle Edit > Resize action to resize image."""
        if not self._editor.has_image():
            return

        from PySide6.QtWidgets import QInputDialog, QMessageBox

        from utils.validators import is_extreme_dimension

        current_img = self._editor.get_current_image()
        current_width = current_img.width
        current_height = current_img.height

        # Prompt for new width
        new_width, ok = QInputDialog.getInt(
            self,
            "Resize Image",
            f"Enter new width (current: {current_width}px):",
            current_width,
            1,
            20000,
            1,
        )

        if not ok:
            return  # User cancelled

        # Calculate proportional height
        aspect_ratio = current_height / current_width
        new_height = int(new_width * aspect_ratio)

        # T089: Check for extreme dimensions
        if is_extreme_dimension(new_width, new_height):
            warning_msg = (
                f"The new dimensions ({new_width}x{new_height}px) are extreme.\n\n"
                f"Small images (<50px) may appear pixelated.\n"
                f"Large images (>10000px) may use significant memory.\n\n"
                f"Do you want to proceed anyway?"
            )
            reply = QMessageBox.warning(
                self,
                "Extreme Dimensions Warning",
                warning_msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply != QMessageBox.StandardButton.Yes:
                return  # User cancelled

        # Perform resize
        try:
            start_time = time.time()
            self._editor.resize(width=new_width, height=None)  # Height auto-calculated
            duration_ms = (time.time() - start_time) * 1000

            self._logger.info(f"Resized image to {new_width}x{new_height}px")
            log_operation(self._logger, "resize", duration_ms)

            self._display_current_image()
            self._update_ui_state()
            self.update_status(f"Image resized to {new_width}x{new_height}px")

        except Exception as e:
            self._logger.error(f"Failed to resize image: {e}")
            show_error_dialog(self, "Cannot Resize Image", "Failed to resize image.", f"Error: {e}")
