from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re
import os
import pandas as pd
from threading import Thread
import time
from downloadLogic import downloadSpotify, downloadSoundCloud, downloadYoutube
from utils import getFolders
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final = os.getenv('TELEGRAM_BOT_USERNAME')
LINK_LIBARY_PATH: Final = os.getenv('LINK_LIBRARY_PATH', './links')
TREADNUMBER: Final = int(os.getenv('THREAD_NUMBER', '5'))


SpotifyRegex: Final = r'https:\/\/open.spotify.com(\/\S+)*\/(?:track|playlist|album)\/[a-zA-Z0-9]+(\?[a-zA-Z0-9=&]+)?'
SpotifyRegexFallBack: Final = r'https:\/\/spotify.link(\/\S+)*[a-zA-Z0-9]+(\?[a-zA-Z0-9=&]+)?'
SoundCloudRegex: Final = r'https:\/\/soundcloud.com\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+'
YoutubeRegex: Final = r'https:\/\/www.youtube.com\/(?:watch|playlist)\?(v=[-a-zA-Z0-9]|list=[a-zA-Z0-9])+'
YoutTubeFalBackIDK: Final = r'https:\/\/youtu.be\/[a-zA-Z0-9]*'
YoutubeRegexForPlaylist: Final = r'[?&]list=([^#?&]*)'


SwitchFolderRegex: Final = r'[sS]witch[fF]older: (.*)'

global currentPath
currentPath = './songs'
global botEnabled
botEnabled = False

global downloadYTVideo
downloadYTVideo = False


global threads
threads = []


# TODO:
# Logging
# run as service
# ensure just the link in download
# mp3 gain
# sequential redownload of SatusID 1 and -1
# count download attempts







# fucntion to delete stoped threads
def deleteStoppedThreads():
    global threads
    for thread in threads:
        if not thread.is_alive():
            threads.remove(thread)


def delete_stopped_threads_repeatedly():
    while True:
        deleteStoppedThreads()
        time.sleep(5)  # Adjust the delay as needed

# Create and start the thread
thread = Thread(target=delete_stopped_threads_repeatedly)
thread.daemon = True  # Optional: makes the thread exit when the main program exits
thread.start()


def initLinkLibary():
    linkFiles = ["spotify.csv", "soundcloud.csv", "youtube.csv"]
    for file in linkFiles:
        path = LINK_LIBARY_PATH + "/" + file
        # Check if the CSV file already exists
        if not os.path.exists(path):
            df = pd.DataFrame(columns=["Url", "Path", "StatusID"])
            df.to_csv(path, index=False)
            print("DataFrame saved to " + path)
        else:
            print(path+" already exists. Skipping save.")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global botEnabled
    botEnabled = True
    print("Start is running")
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global botEnabled
    botEnabled = False
    print("Stop is running")
    await update.message.reply_text('going to sleep now.')


# /help command for adisstional info
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond! \n ' +
                                    'Send Youtube Spotify or SoundCloud Links to download them. withs switchfolder: \\'+
                                    'anyPath you can go where you want in the directory\n with the command showDir or showDirs you can see the current or all directorys')


def create_folder_recursive(path):
    try:
        os.makedirs(path)
        print(f"Folder '{path}' created successfully.")
    except FileExistsError:
        print(f"Folder '{path}' already exists.")


def redownloadAllLinks():

    linkFiles = ["spotify.csv", "soundcloud.csv", "youtube.csv"]

    for file in linkFiles:
        LinkFilePath = LINK_LIBARY_PATH + "/" + file
        if not os.path.exists(LinkFilePath):
            print(LinkFilePath + " does not exist. Please create it first.")
            return

        df = pd.read_csv(LinkFilePath)
        mask = (df["StatusID"] != 0)
        matching_rows = df.loc[mask]
        # Check if any matching rows are found
        if not matching_rows.empty:
            for index, row in matching_rows.iterrows():
                if row["StatusID"] == -1:
                    print("Redownload Spotify: " + row["Url"])
                    if file == "spotify.csv":
                        downloadSpotify(row["Url"], row["Path"])
                    elif file == "soundcloud.csv":
                        downloadSoundCloud(row["Url"], row["Path"])
                    elif file == "youtube.csv":
                        downloadYoutube(row["Url"], row["Path"])

        else:
            print("No " + file + " Links to redownload")


async def redownload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Redownload is running")
    redownloadAllLinks()
    await update.message.reply_text('redownloading all Links now.')


def handle_response(text: str) -> str:

   
    # Create your own response logic
    # processed: str = text.lower()

    global botEnabled
    global currentPath
    global threads
    print("Bot Enabled: " + str(botEnabled))
    if not botEnabled:
        return "not enabled"

    if 'hello' in text:
        return 'Hey there!'

    if re.match(SpotifyRegex, text) or re.match(SpotifyRegexFallBack, text) and len(threads) <= TREADNUMBER:

        spotUrl = text
        if re.match(SpotifyRegexFallBack, text):
            r = requests.get(text) 
            spotUrl = r.url


        thread = Thread(target=downloadSpotify, args=(spotUrl, currentPath))
        thread.start()
        threads.append(thread)
       
        # downloadSpotify(text, currentPath)
        print("Get Spotify Link -----------")
        return 'Downloaded Spotify is running ...'

    if re.match(SoundCloudRegex, text) and len(threads) <= TREADNUMBER:
        print("Get SoundCloud Link -----------")
        thread = Thread(target=downloadSoundCloud, args=(text, currentPath))
        thread.start()
        threads.append(thread)
        # downloadSoundCloud(text, currentPath)
        return 'Downloaded SoundCloud is runnng ...'

    if re.match(YoutubeRegex, text) or re.match(YoutTubeFalBackIDK, text) and len(threads) <= TREADNUMBER:
        print("Get Youtube Link -----------")
        thread = Thread(target=downloadYoutube, args=(text, currentPath, downloadYTVideo))
        thread.start()
        threads.append(thread)
        # downloadYoutube(text, currentPath)
        return 'Downloaded Youtube is running ...'

    if re.match(SpotifyRegex, text) or re.match(SoundCloudRegex, text) or re.match(YoutubeRegex, text) or re.match(YoutTubeFalBackIDK, text) and len(threads) >= TREADNUMBER:
        return 'Please wait until the other downloads are finished.'

    if re.match(SwitchFolderRegex, text):

        print("Get switch Folder  -----------")
        currentPath = "./songs/" + text[15:]

        if not os.path.exists(currentPath):
            print("Path does not existed")
            create_folder_recursive(currentPath)
            return "Created Folder " + currentPath
        else:
            print("Path existed")

        return "You are now in " + currentPath

    return 'don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):


    print("Message")
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type != 'group':
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    if response != "not enabled":
        await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


async def showDir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global currentPath
    await update.message.reply_text('you are in: ' + currentPath)

async def showDirs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("show dirs is running")
    await update.message.reply_text(str(getFolders("./songs")) + ' are in the directory')


async def video_Enable_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global downloadYTVideo
    downloadYTVideo = not downloadYTVideo
    await update.message.reply_text('Download Video is now: ' + str(downloadYTVideo))
   
async def createCreates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        command = "cratedigger sync --library-dir=" + os.path.dirname(os.path.realpath(__file__)) + "\songs"
        print(command)
        # Execute the command
        subprocess.check_call(command, shell=True)
        print("Creates created")
        await update.message.reply_text('syncing Serato now')
      
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed in create creates with return code {e.returncode}.")
        await update.message.reply_text('syncing Serato failed')
    




# Run the program
if __name__ == '__main__':


    initLinkLibary()

        
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('stop', stop_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('showDir', showDir_command))
    app.add_handler(CommandHandler('showDirs', showDirs_command))
    app.add_handler(CommandHandler('redownload', redownload_command))
    app.add_handler(CommandHandler('serato', createCreates))
    app.add_handler(CommandHandler('video', video_Enable_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
