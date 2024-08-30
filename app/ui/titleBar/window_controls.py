# app/ui/titleBar/window_controls.py

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

def create_minimize_button(parent):
    minimize_button = QPushButton('-', parent)
    minimize_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
        }
        QPushButton:hover {
            background-color: transparent;
            color: #89CFF0;
            border: 2px solid #89CFF0;
            border-radius: 5px;
        }
    """)
    minimize_button.setFixedSize(30, 30)
    minimize_button.clicked.connect(parent.showMinimized)
    return minimize_button

def create_close_button(parent):
    close_button = QPushButton('X', parent)
    close_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 15px; /* Match the window's border radius */
        }
        QPushButton:hover {
            background-color: transparent;
            color: red;
            border: 2px solid red;
            border-radius: 15px; /* Match the window's border radius */
        }
    """)
    close_button.setFixedSize(30, 30)
    close_button.clicked.connect(parent.close)
    return close_button
