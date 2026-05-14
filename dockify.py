import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class DockifyUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.setup_ui()

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(18, 18, 18, 255);
                border: 2px solid rgba(255, 255, 255, 255);
                border-radius: 40px;
            }

            QPushButton {
                background-color: rgba(42, 42, 42, 255);
                border: none;
                border-radius: 10px;
                padding: 6px;
            }

            QPushButton:hover {
                color: #1DB954;
            }
        """)

    def setup_window(self):
        self.setWindowTitle("Dockify")
        self.setFixedSize(300, 80)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setup_ui(self):
        self.container = QWidget(self)

        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.album_cover = QLabel()
        pixmap = QPixmap("assets/default_album_cover.png")
        self.album_cover.setPixmap(pixmap)
        self.album_cover.setFixedSize(40, 40)
        self.album_cover.setScaledContents(True)

        self.previous_button = QPushButton()
        self.play_button = QPushButton()
        self.next_button = QPushButton()

        self.previous_button.setIcon(QIcon("assets/previous_button_icon.png"))
        self.play_button.setIcon(QIcon("assets/play_button_icon.png"))
        self.next_button.setIcon(QIcon("assets/next_button_icon.png"))

        self.previous_button.setFixedSize(30, 30)
        self.play_button.setFixedSize(35, 35)
        self.next_button.setFixedSize(30, 30)

        layout.addWidget(self.album_cover)
        layout.addStretch()
        layout.addWidget(self.previous_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.next_button)
        layout.addStretch()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)