import json
import os
from datetime import datetime

import boto3
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


def lambda_handler(event, context):

    load_dotenv()
    spotify_client_id = os.getenv("spotify_client_id")
    spotify_client_secret = os.getenv("spotify_client_secret")
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")

    client_credentials_manager = SpotifyClientCredentials(
        client_id=spotify_client_id, client_secret=spotify_client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists("spotify")

    
    playlist_link = "https://open.spotify.com/playlist/xxxx"
    playlist_id = playlist_link.split("/")[-1]

    spotify_data = sp.playlist_tracks(playlist_id)

    cilent = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="ap-southeast-2",
    )

    filename = "spotify_raw_" + str(datetime.now()) + ".json"

    cilent.put_object(
        Bucket="spotify-phungntm",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(spotify_data),
    )


if __name__ == "__main__":
    lambda_handler(None, None)
