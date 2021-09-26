import cv2
import spotipy
import sys
import pytesseract
import json


SPOTIFY_CLIENT_ID = ''
SPOTIFY_SECRET_KEY = ''

scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative'
username = input("Enter username found on Account overview on Spotify website: ")

token = spotipy.util.prompt_for_user_token(username=username, scope=scope,
                                           client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET_KEY,
                                           redirect_uri='http://localhost:8888/callback')

spotify = spotipy.Spotify(auth=token)


user_playlist_name = input("Enter name for playlist: ")
# user_playlist_name = "playlistNew"


# Crates a playlist in users account
def CreatePlaylist(playlistName):
    spotify.user_playlist_create(user=username, name=playlistName, public=True, collaborative=False, description="Playlist created through python")


CreatePlaylist(user_playlist_name)
user_playlist_id = input("After playlist has been created please enter the playlist id (example: "
                         "2wSXPMF2pq1sa06cwJ8YM7): ")
user_song_screenshot = input("Enter name of image file (include the extension): ")
# user_song_screenshot = "tester4_cropped.jpg"


# Adds song to users newly created playlist
def AddSong(playlistID, fileName):

    counter = 0
    counter1 = 0
    counter2 = 0


# Adds identifier to the left of each line, song has an odd number and artist has an even number
    with open(fileName, 'r') as src:
        with open('outputNew.txt', 'w') as dest:
            for line in src:
                counter += 1
                countStr = str(counter)
                strCount = countStr
                dest.write("{}: {}".format(strCount, line))
    src.close()

    # counter to finish execution of code,
    # it finishes after it counts half the amount of lines in outputNew as the total number of
    # lines is song name and artist name, so half would execute all songs
    range1 = counter/2

    for i in range(int(range1)):
        with open('outputNew.txt', 'r') as src2:
            # uri
            for line in src2:
                counter1 += 1
                # checks if first element (identifier) is an odd int
                if int(line[0]) % 2 != 0:
                    if counter1 == int(range1) + 1:
                        exit()
                    try:
                        # check if second element can be converted to int, meaning the number is double
                        # digit
                        if isinstance(int(line[1]), int):
                            if int(line[1]) % 2 != 0:
                                songName = line
                                # takes the song name, removes index, removes white spaces on right, 4 for double
                                # digit, 3 for single digit
                                # takes away new line char
                                songNameNoNewLine = songName[4:len(songName)-1].rstrip()
                    except ValueError:
                        songName = line
                        songNameNoNewLine = songName[3:len(songName) - 1].rstrip()

                    for line2 in src2:  # artist name
                        if counter2 == int(range1) + 1:
                            break
                        if isinstance(int(line2[0]), int):  # check if first char is int
                            try:
                                # check if second element can be converted to int
                                if isinstance(int(line2[1]), int):
                                    if int(line2[1]) % 2 == 0:
                                        artistName = line2
                                        artistNameNoNewLine = artistName[4:len(artistName)-1].rstrip()
                                        uri = GetURI(songNameNoNewLine, artistNameNoNewLine)

                                        try:
                                            if spotify.playlist_add_items(playlist_id=playlistID, items=[uri]) == 200:
                                                print("Song added")
                                        except LookupError:
                                            print("Song could not be found")

                            except ValueError:
                                if int(line2[0]) % 2 == 0:
                                    artistName = line2
                                    artistNameNoNewLine = artistName[3:len(artistName) - 1].rstrip()
                                    uri = GetURI(songNameNoNewLine, artistNameNoNewLine)

                                    try:
                                        if spotify.playlist_add_items(playlist_id=playlistID, items=[uri]) == 200:
                                            print("Song added")
                                    except LookupError:
                                        print("Song could not be found")
                        break
        src2.close()



# gets the uri of the song
def GetURI(songName, artistName):

    songNameWhitespaceReplaced = songName.replace(" ", "+")

    # search for song name
    if len(sys.argv) > 1:
        search_str = sys.argv[1]
    else:
        search_str = "{}".format(songNameWhitespaceReplaced)

    result = spotify.search(search_str)

    if result != None:
        # this saves all the json data in json format
        with open('outputJSON2.txt', 'w') as outfile:
            json.dump(result, outfile, ensure_ascii=False, indent=4)
        outfile.close()

        with open('outputJSON2.txt') as json_file:
            my_dict = json.loads(json_file.read())

            # looks for an instance of the song name
            for value in my_dict['tracks']['items']:
                if value['name'] == songName:
                    # looks for the songs artist in a nested dictionary
                    for value3 in value['artists']:
                        if value3['name'] == artistName:
                            return value['uri']
    else:
        return


# converts image to text through pytesseract
def ImageToText(fileName):
    print("Converting image to text......")
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    img = cv2.imread(fileName)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2.imshow('Result', img)
    cv2.waitKey(0)

    f = open('output.txt', 'w+')
    f.write(pytesseract.image_to_string(img))
    f.close()

    fh = open('output.txt', 'r')
    lines = fh.readlines()
    fh.close()

    lines = filter(lambda x: not x.isspace(), lines)

    fh = open('output.txt', 'w+')
    fh.write("".join(lines))
    fh.close()

    o = open('output.txt', 'r')
    count = 0

    while True:
        count += 1

        # get next line from file
        line = o.readline()
        bracket = line.find('(')  # if result is -1 then no bracket, bracket + 1 is bracket
        if bracket != -1:
            line1 = line[0:bracket] + '\n'  # this removes things after bracket
            fin = open('output.txt', 'rt')
            data = fin.read()
            data = data.replace(line, line1)
            fin.close()
            fin = open('output.txt', 'wt')
            fin.write(data)
            fin.close()

        # if line is empty end of line is reached
        if not line:
            break
    o.close()
    print("Image converted......")


ImageToText(user_song_screenshot)
AddSong(user_playlist_id, 'output.txt')
