# A custom Spotify Wrapped whenever you want, instead of waiting for the end of each year.

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime
import gspread
import os


# Credentials found in Spotify Dev Portal - CLEAN BEFORE YOU SHARE.
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URL = 'http://localhost:8888/callback'
SCOPE = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URL,
                                               scope=SCOPE))

# Top Tracks

top_tracks_short = sp.current_user_top_tracks(limit=10, offset=0, time_range="short_term")

# Get track ids for songs in certain time frame
def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

# Gather track info

def get_track_features(id):
    meta = sp.track(id)
    # meta data
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info


#Insert into sheet
def insert_to_gsheet(track_ids):
    # Loop over track ids
    tracks = []
    for i in range (len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)
    # Create dataframe
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
    # insert into google sheet
    gc = gspread.service_account(filename=r'<your JSON download location')
    sh = gc.open('Name of the gpsread file you made')
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print('Done')
    return tracks

time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_track_ids(top_tracks)
    insert_to_gsheet(track_ids)






