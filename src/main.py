"""TweakScreenshot application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    """Run the application.

    Returns:
        Exit code
    """
    app = QApplication(sys.argv)
    app.setApplicationName("TweakScreenshot")
    app.setOrganizationName("Ken")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
