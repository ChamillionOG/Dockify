from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve


class HoverIconButton(QPushButton):
    def __init__(self, normal_path, hover_path, width, height):
        super().__init__()
        self.normal_icon = QIcon(normal_path)
        self.hover_icon = QIcon(hover_path)

        self.setIcon(self.normal_icon)
        self.setIconSize(QSize(width, height))
        self.setFixedSize(width + 10, height + 10)
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
        self.expanded = False
        self.offset = None

        font_id = QFontDatabase.addApplicationFont("assets/default_font.ttf")
        self.font_family = (
            QFontDatabase.applicationFontFamilies(font_id)[0]
            if font_id != -1 else "Arial"
        )

        self.setup_window()
        self.setup_ui()

        self.setCursor(Qt.OpenHandCursor)

        self.setStyleSheet(f"""
            QWidget#container {{
                background-color: rgba(18, 18, 18, 255);
                border: 0.5px solid rgba(255, 255, 255, 255);
                border-radius: 25px;
            }}

            QWidget#title_bar {{
                background-color: rgba(30, 30, 30, 255);
                border-top-left-radius: 25px;
                border-top-right-radius: 25px;
            }}

            QPushButton {{
                background-color: rgba(42, 42, 42, 255);
                border: none;
                border-radius: 10px;
                padding: 6px;
            }}

            QLabel {{
                font-family: "{self.font_family}";
                background: transparent;
                font-weight: bold;
                font-size: 15px;
                color: white;
            }}

            QLabel#app_name {{
                font-size: 15px;
            }}
        """)

    def setup_window(self):
        self.setWindowTitle("Dockify")
        self.resize(350, 90)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setup_ui(self):
        self.container = QWidget(self)
        self.container.setObjectName("container")

        self.window_anim = QPropertyAnimation(self, b"geometry")
        self.window_anim.setDuration(500)
        self.window_anim.setEasingCurve(QEasingCurve.OutBack)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(2, 2, 2, 2)
        self.container_layout.setSpacing(0)

        self.container.setLayout(self.container_layout)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(75, 10, 75, 10)
        self.content_layout.setSpacing(5)

        button_layout = QHBoxLayout()

        self.shuffle_button = HoverIconButton(
            "assets/shuffle_button_icon.png",
            "assets/shuffle_button_icon_hover.png",
            20, 20
        )
        self.previous_button = HoverIconButton(
            "assets/previous_button_icon.png",
            "assets/previous_button_icon_hover.png",
            20, 20
        )
        self.play_button = HoverIconButton(
            "assets/play_button_icon.png",
            "assets/play_button_icon_hover.png",
            25, 25
        )
        self.next_button = HoverIconButton(
            "assets/next_button_icon.png",
            "assets/next_button_icon_hover.png",
            20, 20
        )
        self.repeat_button = HoverIconButton(
            "assets/repeat_button_icon.png",
            "assets/repeat_button_icon_hover.png",
            20, 20
        )

        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.repeat_button)

        self.previous_button.clicked.connect(self.expand_ui)
        self.next_button.clicked.connect(self.collapse_ui)

        self.song_label = QLabel("Song Name Here")
        self.song_label.setAlignment(Qt.AlignCenter)

        self.content_layout.addWidget(self.song_label)
        self.content_layout.addLayout(button_layout)

        self.container_layout.addWidget(self.content_widget)

        self.create_title_bar()

    def create_title_bar(self):
        self.title_bar = QWidget()
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setFixedHeight(35)
        self.title_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)

        self.app_icon = QLabel()
        self.app_icon.setPixmap(QPixmap("assets/temp_icon.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.app_icon.setFixedSize(20, 20)

        self.app_name = QLabel("Dockify")
        self.app_name.setObjectName("app_name")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        title_layout.addWidget(self.app_icon)
        title_layout.addWidget(self.app_name)
        title_layout.addWidget(spacer)

    def animate_window(self, target_width, target_height):
        start_rect = self.geometry()

        center_x = start_rect.x() + start_rect.width() // 2
        bottom_y = start_rect.y() + start_rect.height()

        end_x = int(center_x - target_width // 2)
        end_y = bottom_y - target_height

        end_rect = QRect(end_x, end_y, target_width, target_height)

        self.window_anim.stop()
        self.window_anim.setStartValue(start_rect)
        self.window_anim.setEndValue(end_rect)
        self.window_anim.start()

    def expand_ui(self):
        if not self.expanded:
            self.container_layout.insertWidget(0, self.title_bar)

        self.title_bar.show()

        self.animate_window(325, 400)
        self.expanded = True

    def collapse_ui(self):
        self.title_bar.hide()

        self.animate_window(350, 90)
        self.expanded = False

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