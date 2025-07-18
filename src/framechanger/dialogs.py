from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
    QLineEdit,
    QApplication,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QTimer

class AutoChangerDialog(QDialog):
    """A dialog to configure the automatic wallpaper changer settings."""
    def __init__(self, auto_changer_enabled, auto_changer_interval):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("<h2 style='color: #35495E; font-family: Segoe UI;'>AutoChanger Settings</h2>")
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        self.auto_changer_checkbox = QCheckBox("Enable Automatic Changes")
        self.auto_changer_checkbox.setStyleSheet("font-family: Segoe UI; font-size: 20px;")
        self.auto_changer_checkbox.setToolTip("Check this box to let FrameChanger switch wallpapers automatically.")
        self.auto_changer_checkbox.setChecked(auto_changer_enabled)
        layout.addWidget(self.auto_changer_checkbox)

        self.auto_changer_combobox = QComboBox()
        self.auto_changer_combobox.setStyleSheet("font-family: Segoe UI; font-size: 16px;")
        self.auto_changer_combobox.setToolTip("Pick how often you'd like FrameChanger to change your wallpaper.")
        self.auto_changer_combobox.addItems(["1 Minute", "5 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"])
        self.auto_changer_combobox.setCurrentIndex(auto_changer_interval)
        layout.addWidget(self.auto_changer_combobox)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.setStyleSheet("font-family: Segoe UI; font-size: 16px;")
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

class EditDialog(QDialog):
    """A dialog to edit the details of a title in the list."""
    def __init__(self, title, media_type):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("<h2 style='color: #35495E; font-family: Segoe UI;'>Edit Title</h2>")
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        self.title_input = QLineEdit()
        self.title_input.setText(title)
        self.title_input.setStyleSheet("font-family: Segoe UI; font-size: 16px;")
        self.title_input.setPlaceholderText("Enter the movie or TV show title")
        layout.addWidget(self.title_input)

        self.media_type_input = QComboBox()
        self.media_type_input.setStyleSheet("font-family: Segoe UI; font-size: 16px;")
        self.media_type_input.addItems(["movie", "tv"])
        self.media_type_input.setCurrentIndex(0 if media_type.lower() == "movie" else 1)
        layout.addWidget(self.media_type_input)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButton.Cancel)
        buttonBox.setStyleSheet("font-family: Segoe UI; font-size: 16px;")
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

class CustomNotification(QDialog):
    """A custom notification dialog."""
    def __init__(self, title, message, duration=500, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(500, 150)

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        # Set the timer to close the dialog
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(duration)

        # Move the dialog to the bottom right corner of the screen
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.move(screen_geometry.width() - self.width() - 25, screen_geometry.height() - self.height() - 25)

def show_welcome_message(load_settings, save_settings):
    """Display a welcome message to the user when the app starts for the first time."""
    settings = load_settings()
    if not settings.get('welcome_shown', False):
        welcome_dialog = QMessageBox()
        welcome_dialog.setIcon(QMessageBox.Information)
        welcome_dialog.setWindowTitle("Welcome to FrameChanger")

        welcome_text = (
            "<h2 style='color: #35495E; font-family: Segoe UI;'>Welcome to FrameChanger</h2>"
            "<p style='font-size: 16px; font-family: Segoe UI;'>"
            "FrameChanger helps you add wallpapers from your favorite movies and TV shows to your desktop. Here's how to use it:</p>"
            "<ul style='font-size: 16px; list-style-type: disc; padding-left: 20px; font-family: Segoe UI;'>"
            "<li><b>Add your favorite movies and TV shows</b> to your Favorites list.</li>"
            "<li><b>Double-click</b> a title in your Favorites list to change your wallpaper to an image from that movie or TV show.</li>"

            "<li><b>Change Wallpaper:</b> Randomly select a wallpaper from your Favorites list.</li>"
            "<li><b>Auto Wallpaper Changer:</b> Switch wallpapers automatically at regular intervals.</li>"
            "<li><b>To close the app</b>, right-click the FrameChanger icon in the taskbar and select 'Exit'.</li>"
            "</ul>"
            "<p style='font-size: 16px; font-family: Segoe UI;'>To get started, add some titles to your Favorites list and enjoy a new look for your desktop!</p>"
            "<p style='font-size: 16px; font-family: Segoe UI;'>"
            "Thank you for using FrameChanger! If you have any questions or feedback, please let us know.</p>"
        )

        welcome_dialog.setTextFormat(Qt.RichText)
        welcome_dialog.setText(welcome_text)
        welcome_dialog.setStandardButtons(QMessageBox.Ok)
        welcome_dialog.setMinimumSize(400, 300)
        welcome_dialog.exec_()

        settings['welcome_shown'] = True
        save_settings(settings)
