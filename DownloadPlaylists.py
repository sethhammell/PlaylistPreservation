from yt_dlp import YoutubeDL
import os

format = "bestvideo[height<=?1080]+bestaudio/best"
base_dir = "D:\\Playlists"


def downloadPlaylists(playlists_current):
    youtube_prefix = "https://www.youtube.com/watch?v="

    for playlist in playlists_current:
        playlist_path = f"{base_dir}\\{playlist.name}"

        download_folder = os.path.join(os.getcwd(), playlist_path)

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for video in playlist.videos:
            already_downloaded = any(video[1] in s for s in os.listdir(download_folder))

            if not already_downloaded:
                with YoutubeDL(
                    {
                        "outtmpl": os.path.join(
                            download_folder, f"{video[0]} - {video[1]}" + ".%(ext)s"
                        ),
                        "format": format,
                    }
                ) as ydl:
                    try:
                        ydl.download(youtube_prefix + video[1])
                    except Exception as e:
                        print(f"Error downloading video {video[0]} - {video[1]}: {e}")

        for videoname in os.listdir(download_folder):
            if videoname.endswith(".mkv"):
                os.remove(os.path.join(playlist_path, videoname))
