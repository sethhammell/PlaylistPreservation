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
            self.getAllPlaylistVideos()

    def getAllPlaylistVideos(self):
        badChars = '$#[]/"\\()\''
        html = requests.get(self.url)
        text = html.text
        searchText = '"},"longBylineText":{"runs":[{"text":"'
        urlPrefix = 'https://www.youtube.com'

        currentVideo = 1
        newUrl = "index=" + str(currentVideo)
        videoTitles = []

        while(text.find(newUrl) != -1):
            mainTitle = ''
            startAdding = False
            prevText = text

            while(mainTitle == ''):
                i = text.find(newUrl) - 1

                while(text[i] != '"'):
                    newUrl = text[i] + newUrl
                    i -= 1

                newUrl = urlPrefix + newUrl
                newUrl = newUrl.replace("\\u0026", '&')

                html = requests.get(newUrl)
                text = html.text

                for i in range(text.find('<title>') + len('<title>'), text.find(' - YouTube</title>')):
                    if (not text[i] in badChars):
                        mainTitle += text[i]

                if (mainTitle == ''):
                    text = prevText
                    if (currentVideo < 20):
                        currentVideo += 1
                    else:
                        currentVideo -= 1
                    newUrl = "index=" + str(currentVideo)

            indices = [i - 1 for i in range(len(text)) if text.startswith(searchText, i)]

            
            for i in indices:
                title = ''
                for j in range(i, -1, -1):
                    if (text[j] == '"' and text[j - 1] == ':' and text[j - 2] == '"'):
                        if (startAdding):
                            videoTitles.append(title)
                        elif (title == mainTitle):
                            startAdding = True
                            videoTitles.append(title)
                        break
                    if (not text[j] in badChars):
                        title = text[j] + title

            currentVideo += 100
            newUrl = "index=" + str(currentVideo)

        self.videos = list(dict.fromkeys(videoTitles))
