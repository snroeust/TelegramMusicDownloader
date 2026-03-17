# TelegramMusicDownloader

Ein Telegram-Bot, der Musik von **Spotify**, **SoundCloud** und **YouTube** herunterlädt. Einfach einen Link an den Bot senden und der Download startet automatisch.

## Features

- Spotify-Links (Tracks, Playlists, Alben) herunterladen
- SoundCloud-Links herunterladen
- YouTube-Videos/Playlists als MP3 herunterladen
- Mehrere gleichzeitige Downloads (konfigurierbare Thread-Anzahl)
- Download-Ordner per Telegram-Nachricht wechseln
- Fehlgeschlagene Downloads erneut starten
- Serato-Library-Sync via `/serato`
- Download-Verlauf in CSV-Dateien

## Voraussetzungen

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) installiert und im PATH
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installiert
- [scdl](https://github.com/flyingrub/scdl) installiert
- Ein Telegram-Bot-Token (über [@BotFather](https://t.me/BotFather) erstellen)

## Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/snroeust/TelegramMusicDownloader.git
   cd TelegramMusicDownloader
   ```

2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirments.txt
   ```

3. `.env`-Datei erstellen (siehe [Konfiguration](#konfiguration))

4. Bot starten:
   ```bash
   python main.py
   ```

## Konfiguration

Alle sensiblen Daten und Einstellungen werden über eine `.env`-Datei verwaltet. Diese Datei wird **nicht** ins Repository committed (ist in `.gitignore` aufgeführt).

### `.env`-Datei erstellen

Kopiere die Beispieldatei und trage deine Werte ein:

```bash
cp .env.example .env
```

### Umgebungsvariablen

| Variable | Beschreibung | Pflicht | Standard |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API Token (von @BotFather) | Ja | – |
| `TELEGRAM_BOT_USERNAME` | Benutzername des Bots (z.B. `@MeinBot`) | Ja | – |
| `THREAD_NUMBER` | Max. gleichzeitige Downloads | Nein | `5` |
| `DOWNLOAD_PATH` | Standard-Download-Verzeichnis | Nein | `./songs` |
| `LINK_LIBRARY_PATH` | Verzeichnis für die Link-CSV-Dateien | Nein | `./links` |

### Beispiel `.env`

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
TELEGRAM_BOT_USERNAME=@your_bot_username
THREAD_NUMBER=5
DOWNLOAD_PATH=./songs
LINK_LIBRARY_PATH=./links
```

## Bot-Befehle

| Befehl | Beschreibung |
|---|---|
| `/start` | Bot aktivieren |
| `/stop` | Bot deaktivieren |
| `/help` | Hilfe anzeigen |
| `/showDir` | Aktuellen Download-Ordner anzeigen |
| `/showDirs` | Alle verfügbaren Ordner anzeigen |
| `/redownload` | Fehlgeschlagene Downloads erneut starten |
| `/serato` | Serato-Library synchronisieren |
| `/video` | YouTube-Video-Download an/aus |

## Nutzung

1. Bot mit `/start` aktivieren
2. Einen Link von Spotify, SoundCloud oder YouTube senden
3. Der Bot lädt den Song automatisch herunter
4. Mit `switchFolder: ordnername` den Download-Ordner wechseln

## Projektstruktur

```
TelegramMusicDownloader/
├── main.py              # Bot-Logik und Telegram-Handler
├── downloadLogic.py     # Download-Funktionen für Spotify, SoundCloud, YouTube
├── utils.py             # Hilfsfunktionen (CSV-Verwaltung, Ordner-Listing)
├── requirments.txt      # Python-Abhängigkeiten
├── .env                 # Konfiguration (nicht im Repo)
├── .env.example         # Beispiel-Konfiguration
├── links/               # CSV-Dateien mit Download-Verlauf
│   ├── spotify.csv
│   ├── soundcloud.csv
│   └── youtube.csv
└── songs/               # Heruntergeladene Songs
    ├── newSongs/
    └── songs/
```