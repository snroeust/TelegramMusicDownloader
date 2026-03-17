from typing import Final
import subprocess
import sys  # for sys.executable (The file path of the currently using python)
from spotdl import __main__ as spotdl  # To get the location of spotdl
import re
import os
from pytube import YouTube, Playlist


from utils import addLinktToFile, updateLinkStatus, checkIfLinkisAlreadyProcessed


def downloadSoundCloud(soundCloudUrl: str, path: str = './songs'):

    if not checkIfLinkisAlreadyProcessed(soundCloudUrl, path, "soundcloud.csv"):
        addLinktToFile(soundCloudUrl, path, "soundcloud.csv")

    updateLinkStatus(soundCloudUrl, path, "soundcloud.csv", 1)

    try:
        # scdl -l https://soundcloud.com/mantamanta/rumbleready?si=1ccb948d6daa472d9489be4514b300ef&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing --path "./songs" --no-playlist-folder

        command = 'scdl -l "' + soundCloudUrl + \
            '" --path "' + path + '" --no-playlist-folder'
        print(command)
        # Execute the command
        subprocess.check_call(command, shell=True)
        updateLinkStatus(soundCloudUrl, path, "soundcloud.csv", 0)
    except subprocess.CalledProcessError as e:
        print(
            f"Command execution failed in downloadSoundCloud with return code {e.returncode}.")
        updateLinkStatus(soundCloudUrl, path, "soundcloud.csv", -1)




def downloadYoutube(youtubeUrl: str, path: str = './songs', downloadVideo: bool = False):

    if not checkIfLinkisAlreadyProcessed(youtubeUrl, path, "youtube.csv"):
        addLinktToFile(youtubeUrl, path, "youtube.csv")

    updateLinkStatus(youtubeUrl, path, "youtube.csv", 1)


    try:
        
        command = 'yt-dlp -x --audio-format mp3 --audio-quality 0 --path ' + path + " " + youtubeUrl 
        print(command)
        # Execute the command
        subprocess.check_call(command, shell=True)
        updateLinkStatus(youtubeUrl, path, "youtube.csv", 0)
    except subprocess.CalledProcessError as e:
        print(
            f"Command execution failed in downloadSoundCloud with return code {e.returncode}.")
        updateLinkStatus(youtubeUrl, path, "youtube.csv", -1)





def downloadSpotify(spotifyUrl: str, path: str = './songs'):

    if not checkIfLinkisAlreadyProcessed(spotifyUrl, path, "spotify.csv"):
        addLinktToFile(spotifyUrl, path, "spotify.csv")
    updateLinkStatus(spotifyUrl, path, "spotify.csv", 1)

    try:
        subprocess.check_call(
            [sys.executable, spotdl.__file__, spotifyUrl, '--output', path])
        print("Downloaded")
        updateLinkStatus(spotifyUrl, path, "spotify.csv", 0)
    except subprocess.CalledProcessError as e:
        updateLinkStatus(spotifyUrl, path, "spotify.csv", -1)
        print(
            f"Command execution failed in downloadSpotify with return code {e.returncode}.")
