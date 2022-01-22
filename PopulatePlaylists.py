from Playlist import Playlist
import json
import os
import shutil

logging = True

def ResetLogDirectory():
  directory = "TodaysLogs"
  parent_dir = "C:/Users/sethj/OneDrive/Desktop/Programming/PlaylistPreservation/"
  path = os.path.join(parent_dir, directory)
  shutil.rmtree(path)
  os.mkdir(path)

def populatePlaylists():
    playlists = []

    # Playlists must be in alphabetical order in json
    playlists_json = open("data.json")
    playlists_data = json.load(playlists_json)

    if logging:
        ResetLogDirectory()

    for playlist in playlists_data["playlists"]:
        playlists.append(Playlist(playlist["name"], playlist["url"]))

    return playlists
    