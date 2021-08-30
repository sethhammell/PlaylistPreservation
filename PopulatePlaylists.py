from Playlist import Playlist
import json

def populatePlaylists():
    playlists = []

    # Playlists must be in alphabetical order in json
    playlists_json = open("data.json")
    playlists_data = json.load(playlists_json)

    for playlist in playlists_data["playlists"]:
        playlists.append(Playlist(playlist["name"], playlist["url"]))

    return playlists
    