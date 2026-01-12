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


class TestSaveWorkflows:
    """Test end-to-end workflows for saving images."""

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
        img_path = tmp_path / "save_test.png"
        img = PILImage.new("RGB", (400, 300), color="cyan")
        img.save(img_path, "PNG")
        return img_path

    # T040: Integration test for "Save workflow with PNG format"
    @pytest.mark.integration
    def test_save_png_workflow(self, main_window, test_image, tmp_path, qtbot, monkeypatch):
        """Test complete workflow: Load image, File > Save As PNG."""
        # Load image first
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Setup save dialog mock
        output_path = tmp_path / "saved.png"
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName",
            lambda *args, **kwargs: (str(output_path), "PNG Files (*.png)"),
        )

        # Trigger File > Save As
        main_window.action_save_as.trigger()

        # Verify file was created
        assert output_path.exists()
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "PNG"
        assert saved_img.size == (400, 300)

    # T041: Integration test for "Save workflow with JPG format"
    @pytest.mark.integration
    def test_save_jpg_workflow(self, main_window, test_image, tmp_path, qtbot, monkeypatch):
        """Test complete workflow: Load image, File > Save As JPG with quality."""
        # Load image first
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Mock quality dialog to return 85
        monkeypatch.setattr(
            "PySide6.QtWidgets.QInputDialog.getInt",
            lambda *args, **kwargs: (85, True),
        )

        # Setup save dialog mock
        output_path = tmp_path / "saved.jpg"
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName",
            lambda *args, **kwargs: (str(output_path), "JPEG Files (*.jpg)"),
        )

        # Trigger File > Save As
        main_window.action_save_as.trigger()

        # Verify file was created
        assert output_path.exists()
        saved_img = PILImage.open(output_path)
        assert saved_img.format == "JPEG"

    @pytest.mark.integration
    def test_save_overwrite_confirmation(
        self, main_window, test_image, tmp_path, qtbot, monkeypatch
    ):
        """Saving over existing file shows confirmation dialog."""
        from PySide6.QtWidgets import QMessageBox

        # Load image first
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Create existing file at save location
        output_path = tmp_path / "existing.png"
        PILImage.new("RGB", (10, 10), color="black").save(output_path, "PNG")

        # Setup save dialog mock
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getSaveFileName",
            lambda *args, **kwargs: (str(output_path), "PNG Files (*.png)"),
        )

        # Mock confirmation dialog to return "No"
        monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.StandardButton.No)

        # Trigger File > Save As
        main_window.action_save_as.trigger()

        # File should NOT be overwritten (original size remains)
        saved_img = PILImage.open(output_path)
        assert saved_img.size == (10, 10)  # Original size, not new (400, 300)


class TestCropWorkflows:
    """Test end-to-end workflows for cropping images."""

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
        img_path = tmp_path / "crop_test.png"
        img = PILImage.new("RGB", (200, 200), color="yellow")
        img.save(img_path, "PNG")
        return img_path

    # T057: Integration test for "Crop workflow"
    @pytest.mark.integration
    def test_crop_workflow(self, main_window, test_image, qtbot, monkeypatch):
        """Test complete workflow: Load image, select region, crop."""
        # Load image first
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Verify image loaded (200x200)
        status_text = main_window.statusBar().currentMessage()
        assert "200x200" in status_text

        # Simulate crop operation (mock CropSelector for now)
        # In full implementation, this would simulate mouse drag to select region

        editor = main_window._editor
        editor.crop(x=50, y=50, width=100, height=100)

        # Verify image is now cropped (100x100)
        cropped_img = editor.get_current_image()
        assert cropped_img.size == (100, 100)

        # Verify has unsaved changes
        assert editor.has_unsaved_changes() is True

        # Status bar should update
        # (In full implementation, MainWindow would call _display_current_image)

    @pytest.mark.integration
    def test_crop_enables_revert(self, main_window, test_image, qtbot, monkeypatch):
        """Cropping an image enables the Revert action."""
        # Load image
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Initially revert should be disabled
        assert main_window.action_revert.isEnabled() is False

        # Perform crop
        editor = main_window._editor
        editor.crop(x=25, y=25, width=150, height=150)

        # After crop, revert should be enabled (when UI updates)
        # (In full implementation, MainWindow would enable this in _update_ui_state)
        assert editor.has_unsaved_changes() is True

    # T057a: Integration test for "Keyboard crop workflow"
    @pytest.mark.integration
    def test_keyboard_crop_workflow(self, main_window, test_image, qtbot, monkeypatch):
        """Test complete workflow: Load image, use Edit > Crop with keyboard controls."""

        # Load image first
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Verify image loaded (200x200)
        status_text = main_window.statusBar().currentMessage()
        assert "200x200" in status_text

        # Trigger Edit > Crop action (would activate CropSelector)
        # Note: This test will be updated once CropSelector widget is implemented
        # For now, we simulate the keyboard actions on a mock crop selector

        # Simulate keyboard crop workflow:
        # 1. Arrow keys should move crop region
        # 2. Shift+Arrow keys should resize crop region
        # 3. Enter should apply crop
        # 4. Escape should cancel crop

        # This is a placeholder test that will be expanded once CropSelector is implemented
        # The full test will:
        # - main_window.action_crop.trigger()  # activates crop mode
        # - QTest.keyClick(crop_selector, Qt.Key_Right)  # move right
        # - QTest.keyClick(crop_selector, Qt.Key_Down)  # move down
        # - QTest.keyClick(crop_selector, Qt.Key_Right, Qt.ShiftModifier)  # increase width
        # - QTest.keyClick(crop_selector, Qt.Key_Down, Qt.ShiftModifier)  # increase height
        # - QTest.keyClick(crop_selector, Qt.Key_Return)  # apply crop

        # For now, just verify that the action exists and is enabled when image loaded
        assert hasattr(main_window, "action_crop")
        assert main_window.action_crop.isEnabled() is True


class TestRevertWorkflows:
    """Test end-to-end workflows for reverting edits."""

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
        img_path = tmp_path / "revert_test.png"
        img = PILImage.new("RGB", (300, 300), color="blue")
        img.save(img_path, "PNG")
        return img_path

    # T072: Integration test for "Revert after crop"
    @pytest.mark.integration
    def test_revert_after_crop_workflow(self, main_window, test_image, qtbot, monkeypatch):
        """Test complete workflow: Load image, crop, revert to original."""
        # Load image first
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        # Verify original dimensions (300x300)
        editor = main_window._editor
        assert editor.get_current_image().size == (300, 300)

        # Crop to 100x100
        editor.crop(x=50, y=50, width=100, height=100)
        assert editor.get_current_image().size == (100, 100)
        assert editor.has_unsaved_changes() is True

        # Revert
        editor.revert()

        # Should be back to 300x300
        assert editor.get_current_image().size == (300, 300)
        assert editor.has_unsaved_changes() is False

    @pytest.mark.integration
    def test_revert_disables_after_use(self, main_window, test_image, qtbot, monkeypatch):
        """Revert action disables after reverting (no unsaved changes)."""
        # Load and crop
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        editor = main_window._editor
        editor.crop(x=50, y=50, width=150, height=150)

        # Revert should be enabled (when UI updated)
        assert editor.has_unsaved_changes() is True

        # After revert, should disable
        editor.revert()
        assert editor.has_unsaved_changes() is False


# T083-T084: Integration tests for resize workflows
@pytest.mark.integration
class TestResizeWorkflows:
    """Test end-to-end workflows for resizing images."""

    @pytest.fixture
    def main_window(self, qtbot):
        """Create main window for testing."""
        from ui.main_window import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        return window

    @pytest.fixture
    def test_image(self, tmp_path):
        """Create a test image for resize workflows (400x300)."""
        img = PILImage.new("RGB", (400, 300), color="blue")
        img_path = tmp_path / "resize_test.png"
        img.save(img_path, "PNG")
        return img_path

    # T083: Integration test for "Resize with proportional width"
    @pytest.mark.integration
    def test_resize_proportional_width(self, main_window, test_image, qtbot, monkeypatch):
        """Test resize workflow: Load image, resize to new width, maintain aspect ratio."""
        # Load image (400x300)
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        editor = main_window._editor
        assert editor.get_current_image().size == (400, 300)

        # Resize to width=200, height should auto-calculate to 150 (maintains 4:3 ratio)
        editor.resize(width=200, height=None)

        # Verify image is now 200x150
        resized_img = editor.get_current_image()
        assert resized_img.size == (200, 150)

        # Verify unsaved changes flag set
        assert editor.has_unsaved_changes() is True

    # T084: Integration test for "Resize with percentage"
    @pytest.mark.integration
    def test_resize_with_percentage(self, main_window, test_image, qtbot, monkeypatch):
        """Test resize workflow: Load image, resize to 50% scale."""
        # Load image (400x300)
        monkeypatch.setattr(
            "PySide6.QtWidgets.QFileDialog.getOpenFileName",
            lambda *args, **kwargs: (str(test_image), "PNG Files (*.png)"),
        )
        main_window.action_open.trigger()

        editor = main_window._editor
        original_img = editor.get_current_image()
        assert original_img.size == (400, 300)

        # Resize to 50% (200x150)
        new_width = int(400 * 0.5)
        new_height = int(300 * 0.5)
        editor.resize(width=new_width, height=new_height)

        # Verify image is now 200x150
        resized_img = editor.get_current_image()
        assert resized_img.size == (200, 150)
