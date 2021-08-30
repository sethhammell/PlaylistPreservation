import requests

class Playlist(object):
    name = str()
    url = str()
    videos = list(str())

    def __init__(self, name, url = "None", videos = []):
        self.name = name
        self.url = url
        self.videos = videos
        if url != "None":
            self.getFirst100PlaylistVideos()

    def getFirst100PlaylistVideos(self):
        badChars = '$#[]/"\\()\''
        html = requests.get(self.url)
        text = html.text
        searchText = '}]},"title":{"runs":[{"text":"'

        indices = [i + len(searchText) for i in range(len(text)) if text.startswith(searchText, i)]

        videoTitles = []
        
        for i in indices:
            title = ''
            for j in range(i, len(text)):
                if (text[j] == '}'):
                    videoTitles.append(title)
                    break
                if (not text[j] in badChars):
                    title += text[j]

        videoTitles.pop()

        self.videos = videoTitles
