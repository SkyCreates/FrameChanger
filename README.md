# FrameChanger

FrameChanger changes your desktop wallpaper to images from your favorite movies and TV shows using The Movie Database (TMDB) API.

## Features

- Add favorite movies and TV shows
- Change wallpaper randomly or to a specific favorite
- Automatic wallpaper changer
- Customizable themes
- Search and filter favorites
- Edit and delete favorites
- System tray integration
- Notifications

## Installation

### From PyPI

Install with pip:

pip install framechanger

### From Source

1. Clone the repository:
git clone https://github.com/SkyCreates/FrameChanger.git
cd FrameChanger

2. Install dependencies:
pip install -r requirements.txt

3. Run the app:
python app.py

### Download as Release

Get the latest release from the [Releases](https://github.com/SkyCreates/FrameChanger/releases) page on GitHub.

## Usage

### Adding Favorites

- Enter a movie or TV show name and click "Add to Favorites" or press Enter.
- Select "Movie" or "TV Show" using the radio buttons.

### Changing Wallpaper

- Click "Change Wallpaper" to set a random wallpaper from your favorites.
- Double-click a title in the favorites list to set a specific wallpaper.

### Auto Wallpaper Changer

- Enable automatic wallpaper changes by clicking "Auto Wallpaper".
- Set the interval for automatic changes.

### Theming

- Choose a theme from the dropdown menu.
- Themes: Default, Dark, IMDB, TMDB, GreyRed.

### Search and Filter

- Use the search input to find movies or TV shows.
- Filter by all, movies only, or TV shows only.

### Edit and Delete Favorites

- Select a title and click "Edit" to modify it.
- Select a title and click "Delete" to remove it.
- To delete all titles, press and hold "Delete".

### System Tray Integration

- Minimize to the system tray by clicking close.
- Access features from the system tray icon:
- Randomize: Change wallpaper randomly.
- AutoWallpaper Changer Settings: Open auto changer settings.
- Show App: Restore the main window.
- Exit: Quit the app.

### Notifications

- Get notifications for wallpaper changes and other events.

## Configuration

- **Database:** Uses SQLite to store favorites.
- **Settings:** Configuration settings in `settings.json`.

## Credits

- **Developer:** Akash Seam
- **API:** The Movie Database (TMDB)

## License

MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, email me at akash.seam@gmail.com.
