"""Main GUI application for FrameChanger.

This module defines the Qt based interface used to manage favourite
movies and TV shows and to trigger wallpaper changes.  Core classes
include :class:`AutoChangerDialog`, :class:`EditDialog`,
:class:`CustomNotification` and :class:`MainWindow`.  The ``run``
function serves as the console entry point.
"""

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QRadioButton,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QLabel,
    QListView,
    QComboBox,
    QSystemTrayIcon,
    QMenu,
    QAction,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QSizePolicy,
    qApp,
    QFileDialog,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem, QPixmap
from framechanger.stylesheets import stylesheets
import logging
import sys
import sqlite3
import os
from framechanger.wallpaper_changer import (
    change_wallpaper,
    set_specific_wallpaper,
    load_settings,
    save_settings,
    initialize_database,
    download_random_image,
    download_wallpaper,
    set_wallpaper,
    get_api_key,
)

# Constants for database and settings file
DATABASE_NAME = 'titles.db'
SETTINGS_FILE = 'auto_changer_settings.json'

# Set up logging
LOG_FILE = os.path.join(os.path.expanduser("~"), "framechanger.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

class AutoChangerDialog(QDialog):
    """Dialog to configure the automatic wallpaper changer settings."""
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
    """Dialog to edit the details of a title in the list."""
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
    
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.setStyleSheet("font-family: Segoe UI; font-size: 16px;")
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

def show_welcome_message():
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

class CustomNotification(QDialog):
    """Class for displaying custom notifications."""
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

class MainWindow(QMainWindow):
    """The main window of the FrameChanger application."""
    def __init__(self):
        super().__init__()

        # Initialize stylesheets
        self.stylesheets = stylesheets

        initialize_database()  # Initialize the database

        # Set up window properties
        self.setWindowTitle("FrameChanger")
        self.setFixedWidth(400)

        # Main widget and layout setup
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Setup UI components
        self.setup_components(layout)

        # Load settings and apply if auto changer is enabled
        self.load_and_apply_settings()

    def setup_components(self, layout):
        """Set up the UI components."""
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Add a Movie or TV show to your favorites")
        self.title_input.setToolTip("Enter the name of your favorite movie or TV show to add it to your list.")
        self.title_input.setCursor(Qt.IBeamCursor)
        self.title_input.returnPressed.connect(self.add_title)
        layout.addWidget(self.title_input)

        # Media type selection using radio buttons
        media_type_layout = QHBoxLayout()
        self.movie_button = QRadioButton("Movie")
        self.movie_button.setCursor(Qt.PointingHandCursor)
        self.movie_button.setToolTip("Select this if you're adding a Movie")
        self.tvshow_button = QRadioButton("TV Show")
        self.tvshow_button.setCursor(Qt.PointingHandCursor)
        self.tvshow_button.setToolTip("Select this if you're adding a TV show")
        self.movie_button.setChecked(True)
        media_type_layout.addWidget(self.movie_button)
        media_type_layout.addWidget(self.tvshow_button)
        layout.addLayout(media_type_layout)

        self.add_button = QPushButton("Add to Favorites")
        self.add_button.setToolTip("Add the selected movie or TV show to your list of favorites.")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.setAccessibleName("addButton")
        self.add_button.clicked.connect(self.add_title)
        layout.addWidget(self.add_button)

        edit_delete_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit")
        self.edit_button.setToolTip("Edit the details of the selected title in the list.")
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.edit_button.setAccessibleName("editButton")
        self.edit_button.clicked.connect(self.edit_title)
        edit_delete_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setToolTip("Delete the selected title from the list. Hold the button to delete all titles at once.")
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setAccessibleName("deleteButton")
        self.delete_button.pressed.connect(self.start_delete_timer)
        self.delete_button.released.connect(self.stop_delete_timer)
        edit_delete_layout.addWidget(self.delete_button)
        layout.addLayout(edit_delete_layout)

        self.delete_timer = QTimer()
        self.delete_timer.setInterval(3500)
        self.delete_timer.timeout.connect(self.delete_all_titles)

        self.filter_input = QComboBox()
        self.filter_input.setToolTip("Filter titles by showing all, movies only, or TV shows only.")
        self.filter_input.setCursor(Qt.PointingHandCursor)
        self.filter_input.addItems(["All", "movie", "tv"])
        self.filter_input.currentTextChanged.connect(self.show_titles)
        layout.addWidget(self.filter_input)

        self.sort_input = QComboBox()
        self.sort_input.setToolTip("Sort titles in ascending or descending order based on their names.")
        self.sort_input.setCursor(Qt.PointingHandCursor)
        self.sort_input.addItems(["Unsorted", "Ascending", "Descending"])
        self.sort_input.currentTextChanged.connect(self.show_titles)
        layout.addWidget(self.sort_input)

        favorites_label = QLabel("<b>Favorites List:</b>")
        layout.addWidget(favorites_label)

        self.listView = QListView()
        self.listView.setCursor(Qt.PointingHandCursor)
        self.listView.setToolTip("Double-click on a title in the list to change your wallpaper to an image from that movie or TV show.")
        self.listView.doubleClicked.connect(self.set_specific_wallpaper)
        self.listView.setEditTriggers(QListView.NoEditTriggers)
        layout.addWidget(self.listView)

        self.count_label = QLabel()
        self.count_label.setObjectName("count_label")
        layout.addWidget(self.count_label)

        self.search_input = QLineEdit()
        self.search_input.setToolTip("Search for specific movies or TV shows in your list by typing their names here.")
        self.search_input.setPlaceholderText("Search Favorites")
        self.search_input.textChanged.connect(self.show_titles)
        layout.addWidget(self.search_input)

        self.theme_label = QLabel("Select Theme:")
        layout.addWidget(self.theme_label)

        self.theme_input = QComboBox()
        self.theme_input.setToolTip("Select a theme to change the app's appearance. Choose from Default, Dark, IMDB, TMDB, or GreyRed themes.")
        self.theme_input.setCursor(Qt.PointingHandCursor)
        self.theme_input.addItems(self.stylesheets.keys())
        self.theme_input.currentTextChanged.connect(self.change_theme)
        layout.addWidget(self.theme_input)

        # Set the current theme from settings
        settings = load_settings()
        current_theme = settings.get('theme', 'Default')
        self.theme_input.setCurrentText(current_theme)
        self.change_theme(current_theme)

        self.change_wallpaper_button = QPushButton("Change Wallpaper")
        self.change_wallpaper_button.setToolTip("Change your desktop wallpaper to a random image from your favorite movies and TV shows by clicking here.")
        self.change_wallpaper_button.setCursor(Qt.PointingHandCursor)
        self.change_wallpaper_button.setAccessibleName("changeWallpaperButton")
        self.change_wallpaper_button.clicked.connect(self.change_wallpaper)
        layout.addWidget(self.change_wallpaper_button)

        self.preview_button = QPushButton("Preview Wallpaper")
        self.preview_button.setCursor(Qt.PointingHandCursor)
        self.preview_button.setAccessibleName("previewButton")
        self.preview_button.clicked.connect(self.preview_random_wallpaper)
        layout.addWidget(self.preview_button)

        self.local_button = QPushButton("Set Local Image")
        self.local_button.setCursor(Qt.PointingHandCursor)
        self.local_button.setAccessibleName("localImageButton")
        self.local_button.clicked.connect(self.set_local_image)
        layout.addWidget(self.local_button)

        auto_credits_layout = QHBoxLayout()
        self.auto_changer_button = QPushButton("Auto Wallpaper")
        self.auto_changer_button.setToolTip("Enable automatic wallpaper changes at specified intervals by clicking here. You can adjust settings using the checkbox")
        self.auto_changer_button.setCursor(Qt.PointingHandCursor)
        self.auto_changer_button.clicked.connect(self.show_auto_changer_dialog)
        auto_credits_layout.addWidget(self.auto_changer_button)

        credits_button = QPushButton("App Info")
        credits_button.setToolTip("Get information about FrameChanger, its developer, and the data source (The Movie Database).")
        credits_button.setCursor(Qt.WhatsThisCursor)
        credits_button.clicked.connect(self.show_credits)
        auto_credits_layout.addWidget(credits_button)
        layout.addLayout(auto_credits_layout)

        self.setMinimumHeight(800)
        screen_height = QApplication.primaryScreen().availableGeometry().height()
        self.setMaximumHeight(screen_height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        padding = 60
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = int(screen_geometry.width() - self.frameGeometry().width() - padding)
        y = int((screen_geometry.height() - self.frameGeometry().height()) / 4)
        self.move(x, y)

        self.setFont(QFont("Segoe UI"))

        # Load and set the saved theme
        self.change_theme()

        self.show_titles()

        show_welcome_message()

        # System tray setup
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(dir_path, 'icon.ico')

        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        tray_menu = QMenu(self)
        randomize_wallpaper_action = QAction("Randomize", self)
        randomize_wallpaper_action.triggered.connect(self.change_wallpaper)
        tray_menu.addAction(randomize_wallpaper_action)

        auto_wallpaper_changer_action = QAction("AutoWallpaper Changer Settings", self)
        auto_wallpaper_changer_action.triggered.connect(self.show_auto_changer_dialog)
        tray_menu.addAction(auto_wallpaper_changer_action)

        show_action = QAction("Show App", self)
        show_action.triggered.connect(self.restore_window)
        tray_menu.addAction(show_action)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def restore_window(self):
        """Restore the main window from the system tray."""
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        """Handle the close event to minimize to the system tray instead of exiting."""
        event.ignore()
        self.hide()
        self.show_custom_notification(
            "Running in the background",
            "The app is still running in the system tray.\nTo exit the app, right-click the tray icon\nand select Exit.",
            5000
        )

    def show_credits(self):
        """Show the credits and app information."""
        credits_text = (
            "<h2 align='left'>FrameChanger v1.2</h2>"
            "<p align='left'><b>Developed by:</b> Akash Seam</p>"
            "<p align='left'>I created FrameChanger because I often get bored with my desktop wallpaper and didn't want to keep changing it manually. "
            "I also enjoy movies and TV shows and thought it would be cool to have wallpapers from my favorite titles. This app randomly selects wallpapers "
            "from a list of my favorite movies and TV shows. I hope it helps others who feel the same way.</p>"
            "<p align='left'>The app uses The Movie Database (TMDB) API to fetch wallpapers. All images are copyrighted by their respective owners.</p>"
            "<p align='left'>Built with Python, PyQt, and SQLite.</p>"
            "<p align='left'><b>Questions or Feedback:</b> For any questions or feedback, please email me at akash.seam@gmail.com.</p>"
            "<p align='left'><b>Disclaimer:</b> This software is provided 'as is'. The developer is not responsible for any data loss or damage.</p>"
            "<p align='left'><b>License:</b> This software is distributed under the MIT License. </p>"
            "<p align='left'>Thanks for using FrameChanger!</p>"
        )

        QMessageBox.information(self, "Credits", credits_text)

    def display(self, message, icon_type=QMessageBox.Information):
        """Display a message box with the specified message and icon."""
        title = "Error"
        msgBox = QMessageBox(self)
        msgBox.setIcon(icon_type)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()

    def add_title(self):
        """Add the title to the favorites list."""
        title = self.title_input.text().strip()
        media_type = "movie" if self.movie_button.isChecked() else "tv"

        if not title:
            self.display('Error: Title cannot be empty.')
            return
        if len(title) > 100:
            self.display('Error: Title is too long.')
            return

        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in title for char in invalid_chars):
            self.display('Error: Title contains invalid characters.')
            return

        try:
            with sqlite3.connect(DATABASE_NAME) as conn:
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO titles VALUES (?, ?)", (title, media_type.lower()))

                if c.rowcount > 0:
                    self.title_input.clear()

                conn.commit()

        except sqlite3.Error as e:
            self.display(f'Database Error: {e}')

        self.show_titles()

    def edit_title(self):
        """Edit the details of the selected title."""
        selected_indexes = self.listView.selectedIndexes()
        if not selected_indexes:
            return

        selected_index = selected_indexes[0]
        selected_item = selected_index.data()
        title, media_type = selected_item.split(' | ')

        dialog = EditDialog(title, media_type)
        if dialog.exec_() == QDialog.Accepted:
            new_title = dialog.title_input.text().strip()
            new_media_type = dialog.media_type_input.currentText().lower()

            if not new_title:
                self.display('Error: Title cannot be empty.')
                return

            if title != new_title or media_type.lower() != new_media_type:
                try:
                    with sqlite3.connect(DATABASE_NAME) as conn:
                        c = conn.cursor()

                        # Check for duplicate entry
                        c.execute("SELECT COUNT(*) FROM titles WHERE name=? AND media_type=?", (new_title, new_media_type))
                        if c.fetchone()[0] > 0:
                            self.display('Error: A title with this name and media type already exists.')
                            return

                        # Perform the update
                        c.execute("UPDATE titles SET name=?, media_type=? WHERE name=? AND media_type=?", 
                                (new_title, new_media_type, title, media_type.lower()))
                        conn.commit()

                except sqlite3.Error as e:
                    self.display(f'Database Error: {e}')

                self.show_titles()

    def delete_title(self):
        """Delete the selected title from the list."""
        selected_indexes = self.listView.selectedIndexes()
        if not selected_indexes:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Deletion',
            'Are you sure you want to delete the selected title(s)? This action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for selected_index in selected_indexes:
                selected_item = selected_index.data()
                title, media_type = selected_item.split(' | ')

                try:
                    with sqlite3.connect(DATABASE_NAME) as conn:
                        c = conn.cursor()
                        c.execute("DELETE FROM titles WHERE name=? AND media_type=?", (title, media_type.lower()))
                        conn.commit()

                except sqlite3.Error as e:
                    self.display(f'Database Error: {e}')

            self.show_titles()

    def delete_all_titles(self):
        """Delete all titles from the database."""
        reply = QMessageBox.question(self, 'Delete All Titles', 'Are you sure you want to delete all titles? This action cannot be undone.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DATABASE_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM titles")
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                self.display(f'Database Error: {e}')

            self.show_titles()

    def show_titles(self):
        """Show the titles in the list view."""
        model = QStandardItemModel(self.listView)
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            c = conn.cursor()

            filter_text = self.filter_input.currentText()
            search_text = self.search_input.text()

            query = "SELECT name, media_type FROM titles"
            params = []

            if filter_text != "All":
                query += " WHERE media_type=?"
                params.append(filter_text.lower())

            if search_text:
                query += " WHERE" if "WHERE" not in query else " AND"
                query += " name LIKE ?"
                params.append(f"%{search_text}%")

            c.execute(query, params)
            rows = c.fetchall()

            sort_text = self.sort_input.currentText()
            if sort_text == "Ascending":
                rows.sort(key=lambda x: x[0])
            elif sort_text == "Descending":
                rows.sort(key=lambda x: x[0], reverse=True)

            for row in rows:
                item = QStandardItem(' | '.join(row))
                model.appendRow(item)

            self.listView.setModel(model)

            self.count_label.setText(f"Number of titles: {len(rows)}")
            conn.close()
        except sqlite3.Error as e:
            self.display(f'Database Error: {e}')

    def load_and_apply_settings(self):
        """Load settings and apply auto changer settings if enabled."""
        self.auto_changer_timer = QTimer()
        self.auto_changer_timer.timeout.connect(self.change_wallpaper)

        self.auto_changer_enabled = False
        self.auto_changer_interval = 5

        self.load_auto_changer_settings()
        self.apply_auto_changer_settings()
    
    def apply_auto_changer_settings(self):
        """Apply auto changer settings."""
        if self.auto_changer_enabled:
            interval_mapping = {
                0: 60000,
                1: 300000,
                2: 900000,
                3: 1800000,
                4: 3600000,
                5: 10800000,
                6: 21600000,
                7: 43200000,
                8: 86400000
            }
            interval = interval_mapping[self.auto_changer_interval]
            self.auto_changer_timer.start(interval)
        else:
            self.auto_changer_timer.stop()

        self.save_auto_changer_settings()


    def save_auto_changer_settings(self):
        """Save auto changer settings to the configuration."""
        settings = load_settings()
        settings['auto_changer_enabled'] = self.auto_changer_enabled
        settings['auto_changer_interval'] = self.auto_changer_interval
        save_settings(settings)

    def load_auto_changer_settings(self):
        """Load auto changer settings from the configuration."""
        DEFAULT_ENABLED = False
        DEFAULT_INTERVAL = 5
        settings = load_settings()
        self.auto_changer_enabled = settings.get('auto_changer_enabled', DEFAULT_ENABLED)
        self.auto_changer_interval = settings.get('auto_changer_interval', DEFAULT_INTERVAL)

        if self.auto_changer_enabled:
            interval_mapping = {
                0: 60000,
                1: 300000,
                2: 900000,
                3: 1800000,
                4: 3600000,
                5: 10800000,
                6: 21600000,
                7: 43200000,
                8: 86400000
            }
            interval = interval_mapping[self.auto_changer_interval]
            self.auto_changer_timer.start(interval)
        else:
            self.auto_changer_timer.stop()


    def show_auto_changer_dialog(self):
        """Show the dialog to configure the automatic wallpaper changer settings."""
        dialog = AutoChangerDialog(self.auto_changer_enabled, self.auto_changer_interval)
        if dialog.exec_() == QDialog.Accepted:
            self.auto_changer_enabled = dialog.auto_changer_checkbox.isChecked()
            self.auto_changer_interval = dialog.auto_changer_combobox.currentIndex()

            if self.auto_changer_enabled:
                interval_mapping = {
                    0: 60000,
                    1: 300000,
                    2: 900000,
                    3: 1800000,
                    4: 3600000,
                    5: 10800000,
                    6: 21600000,
                    7: 43200000,
                    8: 86400000
                }
                interval = interval_mapping[self.auto_changer_interval]
                self.auto_changer_timer.start(interval)
            else:
                self.auto_changer_timer.stop()

            self.save_auto_changer_settings()

    def change_theme(self, theme=None):
        """Change the application theme."""
        if theme is None:
            settings = load_settings()
            theme = settings.get('theme', 'Default')
        logging.debug(f"Applying theme: {theme}")
        self.setStyleSheet(self.stylesheets[theme])
        settings = load_settings()
        settings['theme'] = theme
        save_settings(settings)

    def change_wallpaper(self):
        """Change the wallpaper to a random image from the favorites list."""
        result, title = change_wallpaper(self.tray_icon)
        if result == 0:
            self.show_custom_notification("Wallpaper Changed", f"Wallpaper changed to {title}", 3000)
        else:
            self.show_custom_notification("Error", "Failed to change wallpaper.", 3000)

    def set_specific_wallpaper(self, index):
        """Set a specific wallpaper based on the selected index."""
        selected_item = index.data()
        title, media_type = selected_item.split(' | ')
        result, title_name = set_specific_wallpaper(title, media_type, self.tray_icon)
        if result == 0:
            self.show_custom_notification("Wallpaper Changed", f"Wallpaper changed to {title_name}", 3000)
        else:
            self.show_custom_notification("Error", "Failed to change wallpaper.", 3000)

    def show_preview_dialog(self, image_path):
        dialog = QDialog(self)
        dialog.setWindowTitle("Preview Wallpaper")
        layout = QVBoxLayout()
        label = QLabel()
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap.scaled(800, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(label)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        return dialog.exec_() == QDialog.Accepted

    def preview_random_wallpaper(self):
        api_key = get_api_key()
        if not api_key:
            self.show_custom_notification("Error", "API key required", 3000)
            return
        image_path, title = download_random_image(api_key)
        if not image_path:
            self.show_custom_notification("Error", "Could not fetch wallpaper", 3000)
            return
        if self.show_preview_dialog(image_path):
            if set_wallpaper(image_path):
                self.show_custom_notification("Wallpaper Changed", f"Wallpaper changed to {title}", 3000)
            else:
                self.show_custom_notification("Error", "Failed to change wallpaper.", 3000)

    def set_local_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path and self.show_preview_dialog(path):
            if set_wallpaper(path):
                self.show_custom_notification("Wallpaper Changed", "Wallpaper changed", 3000)
            else:
                self.show_custom_notification("Error", "Failed to change wallpaper.", 3000)

    def show_custom_notification(self, title, message, duration):
        """Show a custom notification."""
        notification = CustomNotification(title, message, duration, self)
        notification.show()

    def start_delete_timer(self):
        """Start the delete timer."""
        self.delete_timer.start()

    def stop_delete_timer(self):
        """Stop the delete timer."""
        if self.delete_timer.isActive():
            self.delete_timer.stop()
            self.delete_title()

def run():
    """Run the application."""
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.setQuitOnLastWindowClosed(False)
    app.exec_()

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logging.error(e, exc_info=True)
        QMessageBox.warning(None, "Error", str(e))
