from logging import error
import logging
from EmailResults import emailError

def findRemovedSongs(playlists_past, playlists_current):

    removed_songs_all = []

    try:
        for playlist in range(len(playlists_past)):
            removed_songs_playlist = []
            i = 0

            # Find offset between playslists and inital removed videos
            while(not playlists_past[playlist].videos[i] in playlists_current[playlist].videos):
                removed_songs_playlist.append(playlists_past[playlist].videos[i])
                i += 1

            offset = playlists_current[playlist].videos.index(playlists_past[playlist].videos[i]) - i

            # Find rest of removed videos, stopping when at the end of either playlist
            i = 0
            while(i + offset < len(playlists_past[playlist].videos) and i < len(playlists_past[playlist].videos)):
                if (not playlists_past[playlist].videos[i] in playlists_current[playlist].videos):
                    removed_songs_playlist.append(playlists_past[playlist].videos[i])
                    offset -= 1
                i += 1

            if (removed_songs_playlist != []):
                removed_songs_all.append({ playlists_current[playlist].name : removed_songs_playlist })
    except Exception as ex:
        error_msg = "Failed to find removed songs"
        logging.exception(error_msg)
        emailError(error_msg, ex)
    
    return removed_songs_all
