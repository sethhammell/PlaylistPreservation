from PopulatePlaylists import populatePlaylists
from FindRemovedSongs import findRemovedSongs
from FirebaseContext import postPlaylistsToFirebase, readPastPlaylistsFromFirebase
from EmailResults import emailResults, sendEmail
from DownloadPlaylists import downloadPlaylists

# e.g. of video Youtube API can't recognize as unavailable:
# https://www.youtube.com/watch?v=s9NZI48GVQ8

# this video isn't being caught by any checks
# https://www.youtube.com/watch?v=Yh-LXWz3sUY&ab_channel=glitchz

playlists_current = populatePlaylists()

downloadPlaylists(playlists_current)

postPlaylistsToFirebase(playlists_current)
playlists_past = readPastPlaylistsFromFirebase()

removed_songs = findRemovedSongs(playlists_past, playlists_current)
print(removed_songs)

if sendEmail(removed_songs):
    emailResults(removed_songs)
