from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtCore import Qt

class DockifyUI(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont("assets/default_font.ttf")

        if font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.font_family = "Arial"

        print(self.font_family)

        self.setup_window()
        self.setup_ui()

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(18, 18, 18, 255);
                border: 0.5px solid rgba(255, 255, 255, 255);
                border-radius: 25px;
            }

            QPushButton {
                background-color: rgba(42, 42, 42, 255);
                border: none;
                border-radius: 10px;
                padding: 6px;
            }
                           
            QLabel {
                font-family: "{self.font_family}";
                background-color: transparent;
                font-weight: bold;
                font-size: 15px;
                border: none;
                color: white;
            }

            QPushButton:hover {
                color: #1DB954;
            }
        """)
    
    def setup_window(self):
        self.setWindowTitle("Dockify")
        self.setFixedSize(350, 90)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setup_ui(self):
        self.container = QWidget(self)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.container)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(75, 10, 75, 10)
        container_layout.setSpacing(5)

        # Buttons
        button_layout = QHBoxLayout()

        self.shuffle_button = QPushButton()
        self.previous_button = QPushButton()
        self.play_button = QPushButton()
        self.next_button = QPushButton()
        self.repeat_button = QPushButton()

        self.shuffle_button.setIcon(QIcon("assets/shuffle_button_icon.png"))
        self.previous_button.setIcon(QIcon("assets/previous_button_icon.png"))
        self.play_button.setIcon(QIcon("assets/play_button_icon.png"))
        self.next_button.setIcon(QIcon("assets/next_button_icon.png"))
        self.repeat_button.setIcon(QIcon("assets/repeat_button_icon.png"))

        self.shuffle_button.setFixedSize(30, 30)
        self.previous_button.setFixedSize(30, 30)
        self.play_button.setFixedSize(35, 35)
        self.next_button.setFixedSize(30, 30)
        self.repeat_button.setFixedSize(30, 30)

        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.repeat_button)

        # Text
        text_layout = QVBoxLayout()

        self.song_label = QLabel("Song Name Here")
        self.song_label.setAlignment(Qt.AlignCenter)

        self.artist_label = QLabel("Artist Name")
        self.artist_label.setAlignment(Qt.AlignCenter)

        text_layout.addWidget(self.song_label)
        #text_layout.addWidget(self.artist_label)

        # Set Up
        container_layout.addLayout(text_layout)
        container_layout.addLayout(button_layout)

        self.container.setLayout(container_layout)