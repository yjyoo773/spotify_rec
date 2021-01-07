import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
scope = 'user-library-read'

auth_manager = SpotifyClientCredentials(client_id = client_id,client_secret = client_secret)
sp = spotipy.Spotify(auth_manager = auth_manager)
token = util.prompt_for_user_token(scope,client_id = client_id,client_secret = client_secret,redirect_uri = "http://localhost:8881/")
sp = spotipy.Spotify(auth = token)