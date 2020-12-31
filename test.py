import pandas as pd
from data_prep import data_prep
import feature_engineering
import sp
from connect_api import get_id_name,create_necessary_outputs, visualize_songs
from playlist_vector import playlist_vector
from create_rec import create_playlist_rec




spotify_df = pd.read_csv("data.csv")
data_w_genre = pd.read_csv("data_w_genres.csv")

float_cols = spotify_df.dtypes[spotify_df.dtypes == 'float64'].index.values
ohe_cols = 'popularity'

spotify_df = data_prep(spotify_df,data_w_genre)
complete_feature_set = feature_engineering.create_feature_set(spotify_df,float_cols=float_cols)

id_name,list_photo = get_id_name(sp.sp)
playlist_popedm = create_necessary_outputs('poppish edm',id_name,spotify_df)
# visualize_songs(playlist_popedm)

complete_feature_set_popedm, complete_feature_set_nonplaylist_popedm = playlist_vector(complete_feature_set,playlist_popedm,1.09)
popedm_top40 = create_playlist_rec(spotify_df,complete_feature_set_popedm,complete_feature_set_nonplaylist_popedm)
