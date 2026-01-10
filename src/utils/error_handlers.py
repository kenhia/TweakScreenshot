"""Error handling utilities for user-friendly dialogs."""


from PySide6.QtWidgets import QMessageBox, QWidget


def show_error_dialog(
    parent: QWidget | None,
    title: str,
    message: str,
    details: str | None = None,
) -> None:
    """Show error dialog with clear explanation and suggested action.

    Args:
        parent: Parent widget (can be None)
        title: Dialog title
        message: Main error message (clear, user-friendly)
        details: Optional technical details or suggested remediation
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if details:
        msg_box.setInformativeText(details)

    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def show_warning_dialog(
    parent: QWidget | None,
    title: str,
    message: str,
    details: str | None = None,
) -> bool:
    """Show warning dialog with Continue/Cancel options.

    Args:
        parent: Parent widget (can be None)
        title: Dialog title
        message: Warning message
        details: Optional additional information

    Returns:
        True if user clicked Continue, False if Cancel
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if details:
        msg_box.setInformativeText(details)

    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel)

    result = msg_box.exec()
    return result == QMessageBox.StandardButton.Ok


def show_confirmation_dialog(
    parent: QWidget | None,
    title: str,
    message: str,
    details: str | None = None,
) -> bool:
    """Show confirmation dialog with Yes/No options.

    Args:
        parent: Parent widget (can be None)
        title: Dialog title
        message: Question to confirm
        details: Optional additional context

    Returns:
        True if user clicked Yes, False if No
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if details:
        msg_box.setInformativeText(details)

    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.No)

    result = msg_box.exec()
    return result == QMessageBox.StandardButton.Yes


def show_info_dialog(
    parent: QWidget | None,
    title: str,
    message: str,
    details: str | None = None,
) -> None:
    """Show informational dialog.

    Args:
        parent: Parent widget (can be None)
        title: Dialog title
        message: Information message
        details: Optional additional details
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if details:
        msg_box.setInformativeText(details)

    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()
