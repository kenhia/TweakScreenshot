"""Integration tests for UI workflows."""


import pytest
from PIL import Image as PILImage


class TestLoadWorkflows:
    """Test end-to-end workflows for loading images."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Create main window for testing."""
        from ui.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    @pytest.fixture
    def test_image(self, tmp_path):
        """Create test image file."""
        img_path = tmp_path / "workflow_test.png"
        img = PILImage.new("RGB", (300, 200), color="purple")
        img.save(img_path, "PNG")
        return img_path

    # T021: Integration test for "Load from file workflow"
    @pytest.mark.integration
    def test_load_from_file_workflow(self, main_window, test_image, qtbot, monkeypatch):
        """Test complete workflow: File > Open loads and displays image."""
        # Simulate user selecting file from dialog
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )

        # Initially no image should be displayed
        assert main_window.action_save_as.isEnabled() is False
        assert main_window.action_resize.isEnabled() is False

        # Trigger File > Open action
        main_window.action_open.trigger()

        # After loading, save and edit actions should be enabled
        assert main_window.action_save_as.isEnabled() is True
        assert main_window.action_resize.isEnabled() is True

        # Status bar should show dimensions
        status_text = main_window.statusBar().currentMessage()
        assert "300x200" in status_text

    # T022: Integration test for "Paste from clipboard workflow"
    @pytest.mark.integration
    def test_paste_from_clipboard_workflow(self, main_window, qtbot):
        """Test complete workflow: Ctrl-V pastes and displays image."""
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QImage
        from PySide6.QtWidgets import QApplication

        # Put image in clipboard
        qimage = QImage(150, 150, QImage.Format.Format_RGB888)
        qimage.fill(0xFFFF00)  # Yellow

        clipboard = QApplication.clipboard()
        clipboard.setImage(qimage)

        # Initially no image displayed
        assert main_window.action_save_as.isEnabled() is False

        # Simulate Ctrl-V keypress
        qtbot.keyClick(main_window, Qt.Key.Key_V, Qt.KeyboardModifier.ControlModifier)

        # After paste, actions should be enabled
        assert main_window.action_save_as.isEnabled() is True
        assert main_window.action_resize.isEnabled() is True

        # Status bar should show dimensions
        status_text = main_window.statusBar().currentMessage()
        assert "150x150" in status_text

    @pytest.mark.integration
    def test_load_enables_edit_menu_items(self, main_window, test_image, qtbot, monkeypatch):
        """Loading image enables appropriate menu items."""
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )

        # Before load: edit actions disabled
        assert main_window.action_crop.isEnabled() is False
        assert main_window.action_resize.isEnabled() is False
        assert main_window.action_revert.isEnabled() is False

        # Load image
        main_window.action_open.trigger()

        # After load: some actions enabled
        assert main_window.action_resize.isEnabled() is True
        # Crop remains disabled until selection made
        # Revert remains disabled until edits made

    @pytest.mark.integration
    def test_paste_over_unsaved_warns_user(self, main_window, qtbot, monkeypatch):
        """Pasting over existing unsaved image shows warning dialog."""
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QImage
        from PySide6.QtWidgets import QApplication, QMessageBox

        # Put first image in clipboard and paste
        qimage1 = QImage(100, 100, QImage.Format.Format_RGB888)
        qimage1.fill(0xFF0000)
        QApplication.clipboard().setImage(qimage1)
        qtbot.keyClick(main_window, Qt.Key.Key_V, Qt.KeyboardModifier.ControlModifier)

        # Simulate making edit (marks as unsaved)
        # TODO: This will be implemented when edit operations exist

        # Put second image in clipboard
        qimage2 = QImage(100, 100, QImage.Format.Format_RGB888)
        qimage2.fill(0x00FF00)
        QApplication.clipboard().setImage(qimage2)

        # Mock the warning dialog to return "Cancel"
        monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.StandardButton.Cancel)

        # Attempt to paste again - should show warning
        # TODO: Verify warning appears when unsaved changes tracking is implemented
