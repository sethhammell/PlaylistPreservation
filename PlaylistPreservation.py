from PopulatePlaylists import populatePlaylists
from FindRemovedSongs import findRemovedSongs
from FirebaseContext import postPlaylistsToFirebase, readPastPlaylistsFromFirebase
from EmailResults import emailResults, sendEmail

playlists_current = populatePlaylists()

postPlaylistsToFirebase(playlists_current)
playlists_past = readPastPlaylistsFromFirebase()

removed_songs = findRemovedSongs(playlists_past, playlists_current)
print(removed_songs)

if (sendEmail(removed_songs)):
    emailResults(removed_songs)
