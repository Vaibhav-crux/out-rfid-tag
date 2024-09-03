from PyQt5.QtWidgets import QFrame, QHBoxLayout, QDialog
from app.ui.titleBar.window_controls import create_minimize_button, create_close_button, create_image_button
from app.ui.mainWindow.fileScan import FileScanDialog

def create_title_bar(parent):
    title_bar_frame = QFrame(parent)
    title_bar_frame.setFixedHeight(40)
    title_bar_frame.setStyleSheet(parent.load_stylesheet('app/stylesheet/mainWindow/titleBar.qss'))
    title_bar_layout = QHBoxLayout(title_bar_frame)
    title_bar_layout.setContentsMargins(0, 0, 0, 0)

    # Add the image button to the title bar
    image_button = create_image_button(parent)
    title_bar_layout.addWidget(image_button)

    # Spacer to push the buttons to the right
    title_bar_layout.addStretch()

    # Add minimize and close buttons to the title bar
    minimize_button = create_minimize_button(parent)
    close_button = create_close_button(parent)
    title_bar_layout.addWidget(minimize_button)
    title_bar_layout.addWidget(close_button)

    return title_bar_frame

# Ensure that the show_file_scan_dialog is a method of the parent class (e.g., FullScreenWindow)
def show_file_scan_dialog(self):
    dialog = FileScanDialog(self)
    result = dialog.exec_()
    if result == QDialog.Accepted:
        # Handle what happens when the dialog is accepted (Save button clicked)
        print("Dialog accepted")
    else:
        # Handle what happens when the dialog is rejected (Cancel button clicked)
        print("Dialog canceled")
