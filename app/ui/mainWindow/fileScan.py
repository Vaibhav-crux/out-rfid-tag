import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QFont

class FileScanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Scan")
        self.setFixedSize(300, 200)
        self.setup_ui()
        self.selected_file_content = ""  # This will store the content of the selected file

    def setup_ui(self):
        # Create the main layout
        layout = QVBoxLayout()

        # Add a label
        label = QLabel("Select an option:")
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        # Add a combo box and populate it with file names
        self.combo_box = QComboBox()
        self.populate_combo_box()
        layout.addWidget(self.combo_box)

        # Add the buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.clicked.connect(self.on_save_clicked)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont("Arial", 12))
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Set the main layout for the dialog
        self.setLayout(layout)

    def populate_combo_box(self):
        """Populates the combo box with file names from the specified directory."""
        directory = 'app/utils/rfidFile'
        try:
            file_names = os.listdir(directory)
            file_names = [f for f in file_names if os.path.isfile(os.path.join(directory, f))]
            self.combo_box.addItems(file_names)
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
            self.combo_box.addItem("No files found")

    def on_save_clicked(self):
        """Handles the Save button click event."""
        selected_file = self.combo_box.currentText()
        directory = 'app/utils/rfidFile'
        file_path = os.path.join(directory, selected_file)

        try:
            with open(file_path, 'r') as file:
                self.selected_file_content = file.read()
                print(f"Content of {selected_file}:")
                print(self.selected_file_content)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

        self.accept()  # Closes the dialog with a positive result

    def on_cancel_clicked(self):
        self.reject()  # Closes the dialog with a negative result

    def get_selected_file_content(self):
        """Returns the content of the selected file."""
        return self.selected_file_content
