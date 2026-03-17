# TelegramMusicDownloader

A Telegram bot that downloads music from **Spotify**, **SoundCloud**, and **YouTube**. Just send a link to the bot and the download starts automatically.

## Features

- Download Spotify links (tracks, playlists, albums)
- Download SoundCloud links
- Download YouTube videos/playlists as MP3
- Multiple simultaneous downloads (configurable thread count)
- Change the download folder via Telegram message
- Retry failed downloads
- Serato library sync via `/serato`
- Download history stored in CSV files

## Requirements

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available in PATH
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed
- [scdl](https://github.com/flyingrub/scdl) installed
- A Telegram bot token (create one via [@BotFather](https://t.me/BotFather))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/snroeust/TelegramMusicDownloader.git
   cd TelegramMusicDownloader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirments.txt
   ```

3. Create a `.env` file (see [Configuration](#configuration))

4. Start the bot:
   ```bash
   python main.py
   ```

## Configuration

All sensitive data and settings are managed through a `.env` file. This file is **not** committed to the repository because it is listed in `.gitignore`.

### Create the `.env` file

Copy the example file and enter your values:

```bash
cp .env.example .env
```

### Environment Variables

| Variable | Description | Required | Default |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token (from @BotFather) | Yes | – |
| `TELEGRAM_BOT_USERNAME` | Bot username (for example `@MyBot`) | Yes | – |
| `THREAD_NUMBER` | Maximum number of simultaneous downloads | No | `5` |
| `DOWNLOAD_PATH` | Default download directory | No | `./songs` |
| `LINK_LIBRARY_PATH` | Directory for the link CSV files | No | `./links` |

### Example `.env`

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
TELEGRAM_BOT_USERNAME=@your_bot_username
THREAD_NUMBER=5
DOWNLOAD_PATH=./songs
LINK_LIBRARY_PATH=./links
```

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Activate the bot |
| `/stop` | Deactivate the bot |
| `/help` | Show help |
| `/showDir` | Show the current download folder |
| `/showDirs` | Show all available folders |
| `/redownload` | Retry failed downloads |
| `/serato` | Sync the Serato library |
| `/video` | Toggle YouTube video download on/off |

## Usage

1. Activate the bot with `/start`
2. Send a Spotify, SoundCloud, or YouTube link
3. The bot downloads the song automatically
4. Change the download folder with `switchFolder: foldername`

## Project Structure

```
TelegramMusicDownloader/
├── main.py              # Bot logic and Telegram handlers
├── downloadLogic.py     # Download functions for Spotify, SoundCloud, YouTube
├── utils.py             # Helper functions (CSV management, folder listing)
├── requirments.txt      # Python dependencies
├── .env                 # Configuration (not committed)
├── .env.example         # Example configuration
├── links/               # CSV files with download history
│   ├── spotify.csv
│   ├── soundcloud.csv
│   └── youtube.csv
└── songs/               # Downloaded songs
    ├── newSongs/
    └── songs/
```