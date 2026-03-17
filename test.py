import os

# Das Verzeichnis des aktuellen Skripts extrahieren
current_script_directory = os.path.dirname(os.path.realpath(__file__)) + "\songs"

print("Verzeichnis des aktuellen Skripts:", current_script_directory)

















"""import os
import subprocess
import re
from pytube import YouTube
from pytube import Playlist

text = "https://www.youtube.com/watch?v=cLGcGnGJvL0&ab_channel=LinusTechTips"
yt = YouTube(text)

audio = yt.streams.get_audio_only()
downloaded_file = audio.download("songs")
base, ext = os.path.splitext(downloaded_file)

ffmpeg = 'ffmpeg -i \"'+ downloaded_file + '\" -vn -acodec libmp3lame -q:a 2 \"' + base + '.mp3\"'
#ffmpeg -i '"Starting at" is the Biggest Lie in Tech.mp4' -vn -acodec libmp3lame -q:a 2 output_audio.mp3

print(ffmpeg)
subprocess.check_call(ffmpeg, shell=True)

try:
    # Attempt to remove the file
    os.remove(downloaded_file)
    print(f"File '{downloaded_file}' removed successfully.")
except FileNotFoundError:
    print(f"File '{downloaded_file}' not found.")
except PermissionError:
    print(f"Permission error: Unable to remove '{downloaded_file}'.")
except OSError as e:
    print(f"Error occurred while removing '{downloaded_file}': {e}")"""
