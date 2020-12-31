import sys
import pandas as pd
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import config
from skimage import io

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else: 
    print("Usage %s username" %(sys.argv[0],))
    sys.exit()

auth_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(auth_manager = auth_manager)
token = util.prompt_for_user_token(scope,client_id = client_id,client_secret=client_secret,redirect_uri= "http://localhost:8881/")
sp =spotipy.Spotify(auth=token)

# id_name = {}
# list_photo = {}
# for i in sp.current_user_playlists()['items']:
#     id_name[i['name']] = i['uri'].split(':')[2]
#     list_photo[i['uri'].split(':')[2]] = i['images'][0]['url']

def get_id_name(x):
    id_name = {}
    list_photo = {}
    for i in x.current_user_playlists()['items']:
        id_name[i['name']] = i['uri'].split(':')[2]
        list_photo[i['uri'].split(':')[2]] = i['images'][0]['url']
    return id_name,list_photo

def create_necessary_outputs(playlist_name,id_dic,df):
    """
    Pull songs from a specific playlist

    Parameters:
        playlist_name (str): name of the playlist you'd like to pull from spotify API
        id_dic (dic): dictionary that maps playlist_name to playlist_id
        df (pandas dataframe): spotify dataframe
    
    Returns:
        playlist: all songs in the playlist that are available from Kaggle Dataset
    """

    playlist = pd.DataFrame()
    playlist_name = playlist_name

    for ind, i in enumerate(sp.playlist(id_dic[playlist_name])['tracks']['items']):
        playlist.loc[ind,'artist'] = i['track']['artists'][0]['name']
        playlist.loc[ind,'name'] = i['track']['name']
        playlist.loc[ind,'id'] = i['track']['id']
        playlist.loc[ind,'url'] = i['track']['album']['images'][1]['url']
        playlist.loc[ind,'date_added'] = i['added_at']
    
    playlist['date_added'] = pd.to_datetime(playlist['date_added'])
    playlist = playlist[playlist['id'].isin(df['id'].values)].sort_values('date_added',ascending=False)

    return playlist

def visualize_songs(df):
    temp = df['url'].values
    plt.figure(figsize=(15,int(0.625*len(temp))))
    columns = 5
 
    for i,url in enumerate(temp):
        plt.subplot(len(temp)/columns+1,columns,i+1)

        image  = io.imread(url)
        plt.imshow(image)
        plt.xticks(color='w',fontsize = 0.1)
        plt.yticks(color='w',fontsize = 0.1)
        plt.xlabel(df['name'].values[i],fontsize= 12)
        plt.tight_layout(h_pad=0.4,w_pad=0)
        plt.subplots_adjust(wspace=None,hspace=None)

    plt.show()