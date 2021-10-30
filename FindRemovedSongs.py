import logging
from EmailResults import emailError

def findRemovedSongs(playlists_past, playlists_current):
    removed_songs_all = []

    try:
        for playlist in range(len(playlists_past)):
            if (playlist >= len(playlists_current)):
                break
            removed_songs_playlist = []

            for video in playlists_past[playlist].videos:
                if (not (video[0], video[1]) in playlists_current[playlist].videos):
                    removed = True
                    for current_video in playlists_current[playlist].videos:
                        if video[1] == current_video[1]:
                            removed = False
                    if removed:
                        removed_songs_playlist.append(video)

            if (removed_songs_playlist != []):
                removed_songs_all.append({ playlists_current[playlist].name : removed_songs_playlist })
    except Exception as ex:
        error_msg = "Failed to find removed songs"
        logging.exception(error_msg)
        emailError(error_msg, ex)
    
    return removed_songs_all
