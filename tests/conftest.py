"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

import pytest

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for Qt tests."""
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # Don't quit - pytest-qt handles cleanup


@pytest.fixture
def qtbot(qapp, request):
    """Provide qtbot fixture (pytest-qt integration)."""
    from pytestqt.qtbot import QtBot

    bot = QtBot(request)
    return bot
