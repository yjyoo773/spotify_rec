import pandas as pd
import data_prep
import feature_engineering
import sp
from connect_api import get_id_name,create_necessary_outputs, visualize_songs
from playlist_vector import playlist_vector
from create_rec import create_playlist_rec

spotify_df = pd.read_csv("data.csv")
data_w_genre = pd.read_csv("data_w_genres.csv")

spotify_df = data_prep.data_prep(spotify_df,data_w_genre,pop_split = 5)
complete_feature_set = feature_engineering.create_feature_set(spotify_df)

id_name,list_photo = get_id_name(sp.sp)
playlist_popedm = create_necessary_outputs('poppish edm',id_name,spotify_df,sp.sp)

complete_feature_set_popedm, complete_feature_set_nonplaylist_popedm = playlist_vector(complete_feature_set,playlist_popedm,1.09)
popedm_top40 = create_playlist_rec(spotify_df,complete_feature_set_popedm,complete_feature_set_nonplaylist_popedm)
visualize_songs(popedm_top40)