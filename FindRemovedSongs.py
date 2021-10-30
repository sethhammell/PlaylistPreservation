import logging
from EmailResults import emailError

def findRemovedSongs(playlists_past, playlists_current):

    removed_songs_all = []

    try:
        for playlist in range(len(playlists_past)):
            if (playlist >= len(playlists_current)):
                break
            removed_songs_playlist = []

            for i, video in enumerate(playlists_past[playlist].videos):
                if (not (video[0], video[1]) in playlists_current[playlist].videos):
                    if (i != 0 and i != len(playlists_past[playlist].videos) - 1):
                        prev_video = playlists_current[playlist].videos[i - 1]
                        next_video = playlists_current[playlist].videos[i + 1]
                        if prev_video in playlists_current[playlist].videos and next_video in playlists_current[playlist].videos:
                            prev_video_index = playlists_current[playlist].videos.index(prev_video)
                            next_video_index = playlists_current[playlist].videos.index(next_video)
                            if next_video_index - prev_video_index != 2:
                                removed_songs_playlist.append(video)
                    else:
                      removed_songs_playlist.append(video)

            if (removed_songs_playlist != []):
                removed_songs_all.append({ playlists_current[playlist].name : removed_songs_playlist })
    except Exception as ex:
        error_msg = "Failed to find removed songs"
        logging.exception(error_msg)
        emailError(error_msg, ex)
    
    return removed_songs_all
