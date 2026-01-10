"""Main window for TweakScreenshot application."""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar, QWidget


class MainWindow(QMainWindow):
    """Main application window with menu bar, toolbar, and status bar."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        self.setWindowTitle("TweakScreenshot")
        self.setMinimumSize(800, 600)

        # Initialize UI components
        self._setup_menus()
        self._setup_status_bar()
        self._setup_central_widget()

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
        """Create central widget (placeholder for image viewer)."""
        # Placeholder - will be replaced with ImageViewer widget in US1
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

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
