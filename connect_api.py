import sys
import pandas as pd
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import config
from skimage import io

if len(sys.argv) > 1:
    username = sys.argv[1]
else: 
    print("Usage %s username" %(sys.argv[0],))
    sys.exit()

VISUALIZED_SONG_WIDTH = 15
VISUALIZED_SONG_HEIGHT_RATIO = 0.625
VISUALIZED_SONG_COLUMNS = 5
def get_id_name(x):
    """
    Pulls playlist and and playlist images

    Parameters:
        x (token): token that is used to authenticate request from spotify api

    Returns:
        Dictionary for playlist with playlist name as key and id as value,
        Dictionary for playlist image with id as key and url of image as value
    """

    id_name = {}
    list_photo = {}
    for i in x.current_user_playlists()['items']:
        id_name[i['name']] = i['uri'].split(':')[2]
        list_photo[i['uri'].split(':')[2]] = i['images'][0]['url']
    return id_name,list_photo

def create_necessary_outputs(playlist_name,id_dic,df,token):
    """
    Pull songs from a specific playlist

    Parameters:
        playlist_name (str): name of the playlist you'd like to pull from spotify API
        id_dic (dic): dictionary that maps playlist_name to playlist_id
        df (pandas dataframe): spotify dataframe
        token (token): token that is used to authenticate request from spotify api
    Returns:
        playlist: all songs in the playlist that are available from Kaggle Dataset
    """

    playlist = pd.DataFrame()
    playlist_name = playlist_name

    for ind, i in enumerate(token.playlist(id_dic[playlist_name])['tracks']['items']):
        playlist.loc[ind,'artist'] = i['track']['artists'][0]['name']
        playlist.loc[ind,'name'] = i['track']['name']
        playlist.loc[ind,'id'] = i['track']['id']
        playlist.loc[ind,'url'] = i['track']['album']['images'][1]['url']
        playlist.loc[ind,'date_added'] = i['added_at']
    
    playlist['date_added'] = pd.to_datetime(playlist['date_added'])
    playlist = playlist[playlist['id'].isin(df['id'].values)].sort_values('date_added',ascending=False)

    return playlist

def visualize_songs(df):
    """
    Visualizes song album imaage

    Parameters:
        playlist dataframe: dataframe of playlist with features

    Returns:
        image of album art of each song in dataframe
    """

    urls = df['url'].values
    plt.figure(figsize=(VISUALIZED_SONG_WIDTH, int(VISUALIZED_SONG_HEIGHT_RATIO* len(urls))))
    columns = VISUALIZED_SONG_COLUMNS
 
    for i, url in enumerate(urls):
        plt.subplot(len(urls) / columns + 1,columns,i + 1)

        image  = io.imread(url)
        plt.imshow(image)
        plt.xticks(color='w',fontsize = 0.1)
        plt.yticks(color='w',fontsize = 0.1)
        plt.xlabel(df['name'].values[i],fontsize = 12)
        plt.tight_layout(h_pad = 0.4,w_pad = 0)
        plt.subplots_adjust(wspace = None,hspace = None)

    plt.show()