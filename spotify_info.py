import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import csv

# Your credentials
client_id = 'Client ID'
client_secret = 'Client Secret'
redirect_uri = 'Here place your local host address'

# Needed permissions
scope = 'user-library-read'

print("Starting authentication...")
# Authentication with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
print("Authentication done!...") 

# Here it goes the link or name of the track make sure to put between "" and add a , at the end
tracks = [
"Name or Link Here",
]
#if a link is put above the track name will be the link
 
# function to search the tracks
def get_track_info(track_name):
    results = sp.search(q=track_name, limit=1, type='track')
    tracks = results['tracks']['items']
    if tracks:
        track = tracks[0]
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'album': track['album']['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'release_date': track['album']['release_date']
        }
        return track_info
    else:
        return None

# Search for the info
track_infos = {}
for track_name in tracks:
    track_info = get_track_info(track_name)
    time.sleep(1)
    if track_info:
        track_infos[track_name] = track_info
        time.sleep(1)  # Pause to prevent errors
    else:
        track_infos[track_name] = None
        print(f"Information not found: {track_name}")

# Show the results 
for track_name, info in track_infos.items():
    if info:
        print(f'The music: "{track_name}" - Artist: {info["artist"]}, Album: {info["album"]}, Popularity: {info["popularity"]}, Duration: {info["duration_ms"]} ms, Date of release: {info["release_date"]}')
    else:
        print(f'Informations not found "{track_name}"')

# Make it into a CSV file
with open('track_infos.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Track Name', 'Artist', 'Album', 'Popularity', 'Duration (ms)', 'Release Date'])
    for track_name, info in track_infos.items():
        if info:
            writer.writerow([info['name'], info['artist'], info['album'], info['popularity'], info['duration_ms'], info['release_date']])
        else:
            writer.writerow([track_name, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
