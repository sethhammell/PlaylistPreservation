from datetime import datetime, timedelta, date
import firebase_admin
import firebase_admin.credentials as credentials
import firebase_admin.db as db
import json
import logging
from Playlist import Playlist
from EmailResults import emailError

specific_date = False
format_change_date = date(2021, 9, 2)
date_since_last_removed = date(2023, 6, 1)

if not firebase_admin._apps:
    firebase_json = open("data.json")
    firebase_data = json.load(firebase_json)

    cred = credentials.Certificate(firebase_data["credentials"])

    try:
        default_app = firebase_admin.initialize_app(
            cred, {"databaseURL": firebase_data["databaseURL"]}
        )
    except Exception as ex:
        error_msg = "Failed to connect to database"
        logging.exception(error_msg)
        emailError(error_msg, ex)


def postPlaylistsToFirebase(playlists_current):
    ref = db.reference("playlists", app=default_app)
    id = datetime.now().date()
    playlists_ref_current = ref.child(str(id))

    try:
        for playlist in playlists_current:
            playlists_ref_current.update({playlist.name: json.dumps(playlist.videos)})
    except Exception as ex:
        error_msg = "Failed to post data"
        logging.exception(error_msg)
        emailError(error_msg, ex)


def readPastPlaylistsFromFirebase():
    ref = db.reference("playlists", app=default_app)
    id = datetime.now().date() + timedelta(days=-1)

    try:
        playlists_past = []
        playlists_ref_past = ref.child(str(id))
        playlists_past_json = playlists_ref_past.get(etag=True)

        if specific_date:
            all_songs = {}
            while id > format_change_date:
                print(id)
                id += timedelta(days=-1)
                playlists_ref_past = ref.child(str(id))
                playlists_past_json = playlists_ref_past.get(etag=True)

                if playlists_past_json[0] != None:
                    if not len(all_songs):
                        for playlist in playlists_past_json[0]:
                            all_songs[playlist] = {}
                    for playlist in playlists_past_json[0]:
                        new_songs = json.loads(playlists_past_json[0][playlist])

                        for song in new_songs:
                            if song[1] not in all_songs[playlist]:
                                all_songs[playlist][song[1]] = song[0]

            for playlist in all_songs:
                new_playlist = [(name, id) for id, name in all_songs[playlist].items()]
                playlists_past.append(Playlist(playlist, "None", new_playlist))

        else:
            i = 0
            while (playlists_past_json[0] == None) and i < 365:
                id += timedelta(days=-1)
                playlists_ref_past = ref.child(str(id))
                playlists_past_json = playlists_ref_past.get(etag=True)
                i += 1

            for playlist in playlists_past_json[0]:
                playlists_past.append(
                    Playlist(
                        playlist, "None", json.loads(playlists_past_json[0][playlist])
                    )
                )
    except Exception as ex:
        error_msg = "Failed to read data"
        logging.exception(error_msg)
        emailError(error_msg, ex)

    return playlists_past
