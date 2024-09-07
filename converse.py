import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build

# Define your Spotify and YouTube credentials

# Scopes for accessing user's playlists
SCOPE = 'playlist-read-private playlist-read-collaborative'

def get_spotify_playlists(sp):
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return playlists

def get_spotify_playlist_tracks(sp_playlist_id, sp):
    results = sp.playlist_tracks(sp_playlist_id)
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            tracks.append(f"{track['name']} {track['artists'][0]['name']}")
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return tracks

def search_youtube(query, youtube):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=1
    ).execute()
    if search_response['items']:
        return search_response['items'][0]['id']['videoId']
    return None

def create_youtube_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
    )
    response = request.execute()
    return response['id']

def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
    ).execute()

def main(sp_playlist_name, yt_playlist_name):
    # Spotify Setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    ))

    # YouTube Setup
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    # Get User's Spotify Playlists
    playlists = get_spotify_playlists(sp)
    sp_playlist_id = None
    for playlist in playlists:
        if playlist['name'] == sp_playlist_name:
            sp_playlist_id = playlist['id']
            break

    if not sp_playlist_id:
        print("Spotify playlist not found.")
        return

    # Get Tracks from Spotify Playlist
    tracks = get_spotify_playlist_tracks(sp_playlist_id, sp)

    # Create YouTube Playlist
    yt_playlist_id = create_youtube_playlist(youtube, yt_playlist_name, 'Created from Spotify playlist')

    # Add Tracks to YouTube Playlist
    for track in tracks:
        video_id = search_youtube(track, youtube)
        if video_id:
            add_video_to_playlist(youtube, yt_playlist_id, video_id)
            print(f"Added {track} to YouTube playlist.")
        else:
            print(f"Could not find {track} on YouTube.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <Spotify Playlist Name> <YouTube Playlist Name>")
    else:
        sp_playlist_name = sys.argv[1]
        yt_playlist_name = sys.argv[2]
        main(sp_playlist_name, yt_playlist_name)
