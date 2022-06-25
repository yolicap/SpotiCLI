from collections import Counter

import spotipy
import sys
import os
from rich.console import Console
from spotipy.oauth2 import SpotifyOAuth

console = Console()
spotify = None
scope = 'user-read-currently-playing,user-read-playback-state,user-modify-playback-state,user-top-read'


def analyze_user(user_id=None):
    if user_id is None:
        user = spotify.current_user()

    else:
        user = spotify.user(user_id)

    print()
    console.print(f'Analyzing user {user["display_name"]}...', style='dark_blue')
    console.print(f'Number of followers: {user["followers"]["total"]}', style='dark_blue')
    console.print(f'Profile picture: {user["images"][0]["url"]}', style='dark_blue')

    if user_id is None:
        top_tracks = spotify.current_user_top_tracks(limit=10, time_range='long_term', offset=0)
        top_artists = Counter()
        console.print('All time top 10 tracks:', style='dark_green underline')
        for i in range(0, top_tracks['limit']):
            track = top_tracks['items'][i]
            for artist in track["artists"]:
                top_artists[artist["name"]] += 1
            console.print(f'\t[{i}] \"{track["name"]}\" by {track["artists"][0]["name"]}', style='dark_green')
        console.print(f'Top all time artist: {top_artists.most_common()[0][0]}', style='dark_green underline')

        print()
        recent_tracks = spotify.current_user_top_tracks(limit=10, time_range='short_term', offset=0)
        recent_artists = Counter()
        console.print('Recent top 10 tracks:', style='dark_green underline')
        for i in range(0, recent_tracks['limit']):
            track = recent_tracks['items'][i]
            for artist in track["artists"]:
                recent_artists[artist["name"]] += 1
            console.print(f'\t[{i}] \"{track["name"]}\" by {track["artists"][0]["name"]}', style='dark_green')
        console.print(f'Top recent artist: {recent_artists.most_common()[0][0]}', style='dark_green underline')


def analyze_playlist(playlist_id):
    pass


def playback(command, argv):
    pass


def main(argv):
    global spotify
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.environ['SPOTIPY_CLIENT_ID'],
            client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
            scope=scope
        )
    )

    if argv[0] == '-a' or argv[0] == '-analyze':
        if argv[1] == '-U' or argv[1] == '-user':
            if argv[2] == '--self':
                analyze_user()
            else:
                analyze_user(argv[2])
        elif argv[1] == '-P' or argv[1] == '-playlist':
            analyze_playlist(argv[2])

    print('Done.')


if __name__ == '__main__':
    print('Starting SpotiCLI')
    # sys.argv = ['SpoitCLI.py', '-a', '-U', '--self']
    main(sys.argv[1:])

# -a --analyze (prints out general analysis of object)
# -p --player (for player commands)
# --pause, --play, --skip
# -P --playlist <playlist-id>
# -U --user <user-id>

# Usage example :
# > -a -U <user-id>
# > -a -U --self
# > -a -P <playlist-id>
