from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QSize


class HoverIconButton(QPushButton):
    def __init__(self, normal_path, hover_path, size, parent=None):
        super().__init__(parent)
        self.normal_icon = QIcon(normal_path)
        self.hover_icon = QIcon(hover_path)

        self.setIcon(self.normal_icon)
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size + 10, size + 10)
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        super().leaveEvent(event)


class DockifyUI(QWidget):
    def __init__(self):
        super().__init__()

        self.dragging = False
        self.offset = None

        font_id = QFontDatabase.addApplicationFont("assets/default_font.ttf")
        if font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.font_family = "Arial"

        self.setup_window()
        self.setup_ui()

        self.setCursor(Qt.OpenHandCursor)

        self.setStyleSheet(f"""
            QWidget#container {{
                background-color: rgba(18, 18, 18, 255);
                border: 0.5px solid rgba(255, 255, 255, 255);
                border-radius: 25px;
            }}

            QPushButton {{
                background-color: rgba(42, 42, 42, 255);
                border: none;
                border-radius: 10px;
                padding: 6px;
            }}

            QLabel {{
                font-family: "{self.font_family}";
                background-color: transparent;
                font-weight: bold;
                font-size: 15px;
                color: white;
            }}
        """)

    def setup_window(self):
        self.setWindowTitle("Dockify")
        self.setFixedSize(350, 90)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setup_ui(self):
        self.container = QWidget(self)
        self.container.setObjectName("container")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(75, 10, 75, 10)
        container_layout.setSpacing(5)

        button_layout = QHBoxLayout()

        self.shuffle_button = HoverIconButton(
            "assets/shuffle_button_icon.png",
            "assets/shuffle_button_icon_hover.png",
            20
        )
        self.previous_button = HoverIconButton(
            "assets/previous_button_icon.png",
            "assets/previous_button_icon_hover.png",
            20
        )
        self.play_button = HoverIconButton(
            "assets/play_button_icon.png",
            "assets/play_button_icon_hover.png",
            20
        )
        self.next_button = HoverIconButton(
            "assets/next_button_icon.png",
            "assets/next_button_icon_hover.png",
            20
        )
        self.repeat_button = HoverIconButton(
            "assets/repeat_button_icon.png",
            "assets/repeat_button_icon_hover.png",
            20
        )

        self.play_button.setFixedSize(35, 35)

        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.repeat_button)

        text_layout = QVBoxLayout()

        self.song_label = QLabel("Song Name Here")
        self.song_label.setAlignment(Qt.AlignCenter)
        text_layout.addWidget(self.song_label)

        container_layout.addLayout(text_layout)
        container_layout.addLayout(button_layout)
        self.container.setLayout(container_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.setCursor(Qt.OpenHandCursor)
        event.accept()