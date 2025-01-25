from Playlist import Playlist
import json
import os
import shutil

logging = True

# Playlists must be in alphabetical order in json
playlists_json = open("data.json")
playlists_data = json.load(playlists_json)


def ResetLogDirectory():
    directory = "TodaysLogs"
    parent_dir = playlists_data["logPath"]
    path = os.path.join(parent_dir, directory)
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)


def populatePlaylists():
    playlists = []

    if logging:
        ResetLogDirectory()

        # playlists.append(
        #     Playlist(playlists_data["playlists"][1]["name"], playlists_data["playlists"][1]["url"]))

    for playlist in playlists_data["playlists"]:
        playlists.append(Playlist(playlist["name"], playlist["url"]))

    return playlists
