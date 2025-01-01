![Fortune Lyrics Banner](img/fortune_lyrics.png)

# Fortune Lyrics (*Script*): Turn your favorite songs into fortune cookies

**Fortune Lyrics (*Script*)** is a Python script that fetches random lyrics from your saved songs on Spotify and presents them as a "fortune cookie" message. It combines Spotify’s saved tracks feature with Genius’s lyrics API to deliver snippets of your favorite music.

> [!NOTE]  
> This repository contains the original version of Fortune Lyrics, created as a project for personal use. A new web-based version with a graphical interface is currently under development, keeping the same functionality.


## Features
- Retrieves saved tracks from your Spotify library.
- Fetches song lyrics from Genius.com.
- Displays a random n-line snippet from a song, styled like a fortune cookie.
- Lightweight and simple to use.

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/albert-ce/fortune-lyrics.git
cd fortune-lyrics
```

### 2. Install Requirements
Ensure you have Python 3.7+ installed. Then, install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Get API Tokens
> [!WARNING] 
> The script requires Spotify and Genius API tokens to work. Follow the instructions below to generate and configure them.
#### Spotify
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create an application. Make sure to mark the Web API checkbox in the application settings.
2. Note your **Client ID** and **Client Secret**.
3. Set the redirect URI to `http://localhost:5002/spotify-auth` in the application settings.
4. Save the `CLIENT_ID` and `CLIENT_SECRET` in a file named `tokens.py`:
    ```python
    CLIENT_ID = "your_spotify_client_id"
    CLIENT_SECRET = "your_spotify_client_secret"
    ```

#### Genius
1. Create an account at [Genius](https://genius.com/) if you don’t already have one.
2. Generate an access token at [Genius API](https://genius.com/api-clients) and save it in `tokens.py`:
    ```python
    GENIUS_ACCESS_TOKEN = "your_genius_access_token"
    ```
---

## Running the Script

1. Start the script:
    ```bash
    python lyrics.py [n_verses]
    ```
   Where `[n_verses]` is an optional argument specifying the number of verses (lines) to display. If not provided, the default value is `2`.

2. The script will open a browser for Spotify authentication.

3. After authentication, the script will fetch your saved songs and display a random snippet of lyrics styled like a fortune cookie.

---

## Example Output
```
┌───────────────────────────────────────────────────────┐
│ "And while you still had time, you had a chance       │
│ But you decided to take all your sorrys to the grave" │
│               - Posthumous Forgiveness by Tame Impala │
└───────────────────────────────────────────────────────┘
```

---

## Troubleshooting
- **Authentication Timeout**: Ensure you complete Spotify authentication in the browser within 60 seconds.
- **Lyrics Not Found**: Some songs might not have lyrics available on Genius.
- **Errors in Tokens**: Make sure that your `tokens.py` file contains correct API credentials.