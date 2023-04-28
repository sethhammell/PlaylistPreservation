import requests
import json

playlistIncrement = 90
logging = True


def removeAscii(text):
    return text.encode("ascii", "ignore").decode()


def printTextToFile(text, name):
    return
    directory = "TodaysLogs/"
    f = open(directory + name + ".txt", "a")
    f.write(text.encode("ascii", "ignore").decode())
    f.close()


def printBlockedVideos(blockedCountryVideos, blockedCountryUrls, name):
    youtubePrefix = 'www.youtube.com/watch?v='

    print("Blocked videos from " + name +
          " (" + str(len(blockedCountryVideos)) + "):")
    for i in range(0, len(blockedCountryVideos)):
        print(youtubePrefix +
              blockedCountryUrls[i] + " : " + blockedCountryVideos[i])
    print('')


def scrapePrivatedOrRemovedSongs(privatedOrRemovedUrls, name):
    urlPrefix = 'https://web.archive.org/web/20180203081816/https://www.youtube.com/watch?v='
    youtubePrefix = 'www.youtube.com/watch?v='
    searchText = '<meta itemprop="name" content="'
    foundSongs = []
    notFoundUrls = []

    for privatedOrRemovedUrl in privatedOrRemovedUrls:
        url = urlPrefix + privatedOrRemovedUrl

        html = requests.get(url)
        text = html.text

        if (searchText in text):
            index = text.find(searchText) + len(searchText)
            title = ''
            for i in range(index, len(text)):
                if (text[i] == '"' and text[i + 1] == '>'):
                    break
                else:
                    title += text[i]
            foundSongs.append([youtubePrefix + privatedOrRemovedUrl, title])
        else:
            notFoundUrls.append(youtubePrefix + privatedOrRemovedUrl)

    print("Results of Scraping " + str(len(privatedOrRemovedUrls)) +
          " Privated or Removed Songs from " + name + ':')
    print("Found (" + str(len(foundSongs)) + "):")
    for song in foundSongs:
        print(song[0] + " : " + song[1])
    print("Not Found (" + str(len(notFoundUrls)) + "):")
    for url in notFoundUrls:
        print(url, end=', ')
    print('\n')


class Playlist(object):
    name = str()
    url = str()
    videos = list(str())

    def __init__(self, name, url="None", videos=None):
        self.name = name
        self.url = url
        self.videos = videos if videos is not None else []
        if url != "None":
            self.getAllPlaylistVideos()

    def filterRemovedVideos(self, items):
        badChars = '$#[]/"\\()\''
        youtubePrefix = 'http://www.youtube.com/watch?v='

        for i in items:
            newTitle = "".join(
                [char for char in i['snippet']['title'] if char not in badChars])
            newTitle = newTitle.replace('&', "u0026")

            if i['status']['privacyStatus'] == "public":
                self.videos.append(
                    (newTitle, i['snippet']['resourceId']['videoId']))
            elif i['status']['privacyStatus'] == "unlisted":
                html = requests.get(
                    youtubePrefix + i['snippet']['resourceId']['videoId'])
                text = html.text
                if (text.find('Video unavailable') == -1):
                    self.videos.append(
                        (newTitle, i['snippet']['resourceId']['videoId']))

    def getAllPlaylistVideos(self):
        playlist_json = open("data.json")
        playlist_data = json.load(playlist_json)

        print(self.name, self.url[-34:])

        params = {
            'part': 'snippet,status',
            'maxResults': 50,
            'playlistId': self.url[-34:],
            'key': playlist_data["apiKey"]
        }

        response = requests.get(
            'https://www.googleapis.com/youtube/v3/playlistItems', params=params)
        json_data = response.json()

        items = json_data['items']

        self.filterRemovedVideos(items)

        next_page_token = json_data.get('nextPageToken')

        while next_page_token:
            params['pageToken'] = next_page_token

            response = requests.get(
                'https://www.googleapis.com/youtube/v3/playlistItems', params=params)
            json_data = response.json()
            items = json_data['items']

            self.filterRemovedVideos(items)

            next_page_token = json_data.get('nextPageToken')

        print(len(self.videos))

    def getAllPlaylistVideosOld(self):
        badChars = '$#[]/"\\()\''
        html = requests.get(self.url)
        text = html.text
        titleSearchText = '"},"longBylineText":{"runs":[{"text":"'
        urlSearchText = '"commandMetadata":{"webCommandMetadata":{"url":"/watch?v='
        unplayableSearchText = 'unplayableText":{"simpleText":"'

        urlPrefix = 'https://www.youtube.com'

        currentVideo = 1
        newUrl = "index=" + str(currentVideo) + '"'
        videoTitles = []
        unplayableUrls = []
        blockedCountryUrls = []
        blockedCountryVideos = []
        printTextToFile(text, self.name + '- original')

        while (text.find(newUrl) != -1):
            mainTitle = ''
            # startAdding = False
            prevText = text

            while (mainTitle == ''):
                i = text.find(newUrl) - 1

                while (text[i] != '"'):
                    newUrl = text[i] + newUrl
                    i -= 1

                newUrl = urlPrefix + newUrl
                newUrl = newUrl.replace("\\u0026", '&')

                html = requests.get(newUrl)
                text = html.text

                for i in range(text.find('<title>') + len('<title>'), text.find(' - YouTube</title>')):
                    if (not text[i] in badChars):
                        mainTitle += text[i]

                mainTitle = mainTitle.replace('&quot;', '')
                mainTitle = mainTitle.replace('&39;', '')
                mainTitle = mainTitle.replace('amp;', '')
                # remove '&amp' ?

                if (mainTitle == ''):
                    text = prevText
                    if (currentVideo < 20):
                        currentVideo += 1
                    else:
                        currentVideo -= 1
                    newUrl = "index=" + str(currentVideo)
                elif logging:
                    printTextToFile(text, self.name + '-' + str(currentVideo))

            unplayableIndices = [i + len(unplayableSearchText) for i in range(
                len(text)) if text.startswith(unplayableSearchText, i)]
            for i in unplayableIndices:
                videoId = ''
                quoteCount = 0
                for j in range(i, len(text)):
                    if (quoteCount == 5):
                        unplayableUrls.append(videoId)
                        break
                    else:
                        if (text[j] == '"'):
                            quoteCount += 1
                        elif (quoteCount == 4):
                            videoId += text[j]

            unplayableUrls = list(dict.fromkeys(unplayableUrls))

            videoIndices = [
                i - 1 for i in range(len(text)) if text.startswith(titleSearchText, i)]
            urlIndices = [i + len(urlSearchText)
                          for i in range(len(text)) if text.startswith(urlSearchText, i)]

            for i in videoIndices:
                title = ''
                for j in range(i, -1, -1):
                    if (text[j] == '"' and text[j - 1] == ':' and text[j - 2] == '"'):
                        newUrl = ''
                        for k in urlIndices:
                            if (k > i):
                                for l in range(k, len(text)):
                                    if (text[l] == '"'):
                                        break
                                    else:
                                        newUrl += text[l]
                                break
                        if ("index" in newUrl):
                            newUrl = newUrl[0: newUrl.find('\\')]
                            if (not newUrl in unplayableUrls and '"' not in newUrl):
                                videoTitles.append((title, newUrl))
                            elif ('"' not in newUrl):
                                blockedCountryVideos.append(title)
                                blockedCountryUrls.append(newUrl)
                        break
                    if (not text[j] in badChars):
                        title = text[j] + title

            currentVideo += playlistIncrement
            newUrl = "index=" + str(currentVideo)

        blockedCountryVideos = list(dict.fromkeys(blockedCountryVideos))
        blockedCountryUrls = list(dict.fromkeys(blockedCountryUrls))

        # If uncommented, printBlockedVideos and scrapePrivatedOrRemovedSongs will only be printed on screen, not emailed
        # printBlockedVideos(blockedCountryVideos, blockedCountryUrls, self.name)

        # Takes at least 10 minutes
        # privatedOrRemovedUrls = [x for x in unplayableUrls if x not in blockedCountryUrls]
        # scrapePrivatedOrRemovedSongs(privatedOrRemovedUrls, self.name)

        self.videos = list(dict.fromkeys(videoTitles))
