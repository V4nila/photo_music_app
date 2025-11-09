import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Mood → genres mapping
mood_to_genres = {
    "Chill": ["acoustic", "classical"],
    "Energetic": ["dance", "pop", "electronic"],
    "Happy": ["pop", "dance"],
    "Sad": ["acoustic"],
    "Romantic": ["r-n-b", "soul"],
    "Excited": ["dance", "electronic", "pop"],
    "Dark": ["rock", "metal"],
    "Nostalgic": ["indie", "classic-rock"],
    "Calm": ["classical", "acoustic"]
}

def recommend_songs(detected_mood, limit_per_genre=3):
    genres = mood_to_genres.get(detected_mood, ["pop"])
    tracks_list = []

    for genre in genres:
        # Search Spotify for tracks of this genre
        results = sp.search(q=f"genre:{genre}", type="track", limit=limit_per_genre)
        for track in results["tracks"]["items"]:
            tracks_list.append((track["name"], track["artists"][0]["name"]))

    return tracks_list
