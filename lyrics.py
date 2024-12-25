import tokens
import lyricsgenius
from http.server import HTTPServer, BaseHTTPRequestHandler
from yaspin import yaspin
from yaspin.spinners import Spinners
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import random
import json
import re


sp_oauth = SpotifyOAuth(client_id=tokens.CLIENT_ID,
                         client_secret=tokens.CLIENT_SECRET,
                         redirect_uri="http://localhost:5002/spotify-auth",
                         scope="user-library-read")

access_token = None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global access_token

        if "/spotify-auth" in self.path:
            query = self.path.split('?')[-1]
            params = dict(qc.split('=') for qc in query.split('&'))
            code = params.get("code")

            if code:
                access_token = sp_oauth.get_access_token(code, as_dict=False)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"""
                <html>
                    <head>
                        <title>Authentication Successful</title>
                        <script>
                            window.close();
                        </script>
                    </head>
                    <body>
                        <p style="font-family: monospace;">
                            Authentication successful. You can close this window.
                        </p>
                    </body>
                </html>
                """)
                print("Authentication successful ✓")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: Authentication was not completed. Please try again.")

                print("Authentication failed: No code received.")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Route not found.")

    def log_message(self, format, *args):
        # Overriding this method to prevent printing the GET request logs
        return

def spotify_auth():
    global access_token

    token_info = sp_oauth.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
        print("Using cached token ✓")
        return access_token

    auth_url = sp_oauth.get_authorize_url()

    webbrowser.open(auth_url)
    print("Waiting for authentication in the browser...")

    server = HTTPServer(('localhost', 5002), SimpleHTTPRequestHandler)
    server.timeout = 60
    server.handle_request()

    if not access_token:
        print("Timeout: Authentication was not completed in time.")

    server.server_close()
    return access_token

def get_saved_songs(sp):
    saved_songs = []
    offset = 0
    limit = 50
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        saved_songs.extend(results['items'])
        if len(results['items']) < limit:
            break
        offset += limit
    return saved_songs

def get_random_lyrics(songs):
    global artist
    global name
    song = None
    while not song:
        random_track = random.choice(songs)['track']
        artist = random_track['artists'][0]['name']
        name = random_track['name']

        genius = lyricsgenius.Genius(tokens.GENIUS_ACCESS_TOKEN, verbose=False)
        song = genius.search_song(name, artist)

    return song.lyrics

def get_fortune_verses(lyrics, n_verses=2):
    strophes = lyrics.split('\n\n')
    strophes_cleaned = [re.sub('\[.*\]\n*|\n*\(.*\)','',strophe) for strophe in strophes[1:]]
    strophes_verses = [strophe.split('\n') for strophe in strophes_cleaned]

    verses_pairs = []
    for verses in strophes_verses:
        for i in range(0, len(verses) - 1, n_verses):
            verses_pair = '\n'.join(verses[i:i+n_verses])
            verses_pairs.append(verses_pair)

    return verses_pairs

def print_boxed(string):
    lines = string.split('\n')
    lines = [line.expandtabs(4) for line in lines]
    max_length = max(len(line) for line in lines)
    print('┌' + '─' * (max_length + 2) + '┐')
    for line in lines:
        print(f'│ {line.ljust(max_length)} │')
    print('└' + '─' * (max_length + 2) + '┘')

def print_verses(verses, name, artist):
    verses = "\""+verses+"\""
    reference = "- "+name+" by "+artist

    max_length = max(len(line) for line in verses.split('\n'))
    spaces = max(0, max_length-len(reference))
    reference = " "*spaces+reference

    print_boxed(verses+"\n"+reference)

if __name__ == "__main__":
    access_token = spotify_auth()
    sp = spotipy.Spotify(auth=access_token)

    spinner = yaspin(Spinners.arc, text="🥠")
    spinner.start()

    saved_songs = get_saved_songs(sp)

    fortune_verses = []
    while not fortune_verses:
        lyrics = get_random_lyrics(saved_songs)
        fortune_verses = get_fortune_verses(lyrics, 2)
        verses = random.choice(fortune_verses)

    spinner.stop()

    print("🥠 Finished ✓")
    print_verses(verses, name, artist)