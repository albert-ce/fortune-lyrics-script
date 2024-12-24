import tokens
import lyricsgenius
from http.server import HTTPServer, BaseHTTPRequestHandler
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import random
import json


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
                self.wfile.write(b"Authentication successful. You can close this window.")

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

    auth_url = sp_oauth.get_authorize_url()

    webbrowser.open(auth_url)
    print("Waiting for authentication in the browser...")

    server = HTTPServer(('localhost', 5002), SimpleHTTPRequestHandler)
    server.timeout = 5
    server.handle_request()

    if not access_token:
        print("Timeout: Authentication was not completed in time.")

    server.server_close()
    print("Server stopped.")

    return access_token

if __name__ == "__main__":
    access_token = spotify_auth()

    sp = spotipy.Spotify(auth=access_token)

    print("Retrieving saved songs...")
    saved_songs = sp.current_user_saved_tracks()

    random_track = random.choice(saved_songs['items'])['track']
    artist = random_track['artists'][0]['name']
    name = random_track['name']

    # for item in saved_songs['items']:
    #     track = item['track']
    #     artist = track['artists'][0]['name']
    #     name = track['name']
    #     print(name + " by " + artist)

    # with open("saved_songs.json", "w") as json_file:
    #     json.dump(results, json_file, indent=4) 

    genius = lyricsgenius.Genius(tokens.GENIUS_ACCESS_TOKEN, verbose=False)
    song = genius.search_song(name, artist)
    print(song.lyrics)