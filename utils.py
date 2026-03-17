
from typing import Final
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

LINK_LIBARY_PATH: Final = os.getenv('LINK_LIBRARY_PATH', './links')



def addLinktToFile(url, path, file):
    LinkFilePath = LINK_LIBARY_PATH + "/" + file
    if not os.path.exists(LinkFilePath):
        print(LinkFilePath + " does not exist. Please create it first.")
        return

    df = pd.read_csv(LinkFilePath)

    # Append the new data to the DataFrame
    new_data = {"Url": url, "Path": path}
    df = pd.concat([df, pd.DataFrame(
        new_data, index=[0])], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(LinkFilePath, index=False)
    print("New data added to " + LinkFilePath)




def updateLinkStatus(url, path, file, StatusID):
    LinkFilePath = LINK_LIBARY_PATH + "/" + file
    if not os.path.exists(LinkFilePath):
        print(LinkFilePath + " does not exist. Please create it first.")
        return

    df = pd.read_csv(LinkFilePath)

    # Locate the row that matches the "Url" and "Path"
    mask = (df["Url"] == url) & (df["Path"] == path)
    matching_row = df.loc[mask]

    # Check if a matching row is found
    if not matching_row.empty:
        # Update the value in the matching row
        df.loc[mask, "StatusID"] = StatusID
        df.to_csv(LinkFilePath, index=False)
        print("Value updated successfully.")
    else:
        print("No matching row found for the given 'Url' and 'Path'.")


def checkIfLinkisAlreadyProcessed(url, path, file):
    LinkFilePath = LINK_LIBARY_PATH + "/" + file
    if not os.path.exists(LinkFilePath):
        print(LinkFilePath + " does not exist. Please create it first.")
        return False

    df = pd.read_csv(LinkFilePath)

    # Locate the row that matches the "Url" and "Path"
    mask = (df["Url"] == url) & (df["Path"] == path)
    matching_rows = df.loc[mask]

    # Check if any matching rows are found
    if not matching_rows.empty:
        print("Link is already downloaded.")
        return True
    else:
        print("Link is not fully downloaded yet.")
        return False

def getFolders(path):
    """
    Returns a list of all folders in a directory
    """
    folders = []
    for folder in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder)):
            folders.append(folder)
    return folders