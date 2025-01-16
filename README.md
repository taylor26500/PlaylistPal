# YouTube Music Playlist Creator

## Overview

This project allows you to create playlists on YouTube Music by searching for songs based on a list you provide. It utilizes the `ytmusicapi` library to interact with YouTube Music and requires authentication headers and cookies to function properly.

## Getting Started

```
youtube_music_playlist/
│
├── src/
│   ├── __init__.py
│   ├── auth_manager.py
│   ├── header_handler.py
│   ├── playlist_manager.py
│   ├── song_handler.py
│   └── utils.py
│
├── config/
│   └── headers_auth.json
│
├── requirements.txt
└── main.py
```

### Prerequisites

- Python 3.x
- `ytmusicapi` library (install via pip)

### Installation

1. Clone the repository or download the code files.
2. Install the required library:
   ```bash
   pip install ytmusicapi
   ```

### Getting Authentication Headers and Cookies

To use the script, you need to obtain your authentication headers and cookies from YouTube Music. Follow these steps:

1. Open your web browser and navigate to [YouTube Music](https://music.youtube.com/).
2. Right-click anywhere on the page and select **Inspect** to open the Developer Tools.
3. Click on the **Network** tab.
4. Refresh the page by pressing `F5`.
5. In the filter box, type `browse` to find the relevant network request.
6. Click on the request that appears in the list.
7. In the right panel, look for the **Request Headers** section. You will need to copy the headers listed here.

### Example of Required Headers

You will typically need the following headers:

- `accept`
- `accept-language`
- `authorization`
- `cookie`
- `user-agent`
- `x-goog-authuser`
- `x-origin`

### Saving Headers and Cookies

1. After copying the headers, run the script.
2. When prompted, paste your raw headers and then your cookie. Type `END` on a new line when finished.
3. The script will save these headers to a file named `headers_auth.json`.

### Resetting Headers

If you need to reset your headers, the script includes a function to do so. This will clear all header values and set them to default.

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. Follow the prompts to enter the name of your input file containing the list of songs.
3. The script will search for the songs and create a playlist on YouTube Music.

## Notes

- Ensure that your input file is formatted correctly, with one song title per line.
- If you encounter authentication issues, you may need to refresh your headers and cookies.

## License

This project is open-source and available for modification and distribution under the MIT License.