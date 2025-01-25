# send_test_email.py

from EmailResults import emailResults

# Example test data for removed_songs:
# A list of dictionaries, each dictionary has the playlist name as the key,
# and a list of (title, YouTubeID) tuples as the value.
test_removed_songs = [
    {
        "Rock Classics": [
            ("Highway to Hell", "aBcDeFg123"),
            ("Back in Black", "hIjKlMn456")
        ]
    },
    {
        "Pop Hits": [
            ("Bad Romance", "GhIjKlMn789"),
            ("Poker Face", "OpQrStUv012")
        ]
    }
]

if __name__ == "__main__":
    try:
        emailResults(test_removed_songs)
        print("Test email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the test email.")
        print(e)
