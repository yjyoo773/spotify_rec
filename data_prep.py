import pandas as pd
import numpy as np
import re
import itertools

spotify_df = pd.read_csv("data.csv")
data_w_genre = pd.read_csv("data_w_genres.csv")

def data_prep(spotify_df,data_w_genre):
    # Normalize genre column for data_w_genre
    data_w_genre['genres_upd'] = data_w_genre['genres'].\
        apply(lambda x:[re.sub(" ","_",i) for i in re.findall(r"'([^']*)'",x)])

    # Normalize artists column in spotify_df
    spotify_df['artists_v1'] = spotify_df['artists'].apply(lambda x: re.findall(r"'([^']*)'",x))

    # Normalize artists column that v1 missed
    spotify_df['artists_v2'] = spotify_df['artists'].apply(lambda x: re.findall('\"(.*?)\"',x))

    # Combine v1 and v2
    spotify_df['artists_final'] = np.where(spotify_df['artists_v1'].apply(lambda x: not x),spotify_df['artists_v2'],spotify_df['artists_v1'])

    # Create identifier column combining artist to song
    spotify_df['artist_song'] = spotify_df.apply(lambda row: row['artists_final'][0]+'_'+row['name'],axis=1)

    spotify_df.drop_duplicates('artist_song',inplace = True)

    # Explode df based on artists_final column
    artists_explode = spotify_df[['artists_final','id']].explode('artists_final')

    # Merge exploded df with genre df
    artists_explode_merge = artists_explode.merge(data_w_genre,how='left',left_on='artists_final',right_on='artists')
    artists_explode_merge_nonnull = artists_explode_merge[~artists_explode_merge.genres_upd.isnull()]

    # Group each song and lists its genre with the given dataset we created
    artists_genres_consolidated = artists_explode_merge_nonnull.groupby('id')['genres_upd'].apply(list).reset_index()

    artists_genres_consolidated['consolidate_genre_lists'] = artists_genres_consolidated['genres_upd'].apply(lambda x:list(set(list(itertools.chain.from_iterable(x)))))

    spotify_df = spotify_df.merge(artists_genres_consolidated[['id','consolidate_genre_lists']],on='id',how='left')

    # Create release year column
    spotify_df['year'] = spotify_df['release_date'].apply(lambda x: x.split('-')[0])

    # Divide popularity column into five parts
    spotify_df['pop_red'] = spotify_df['popularity'].apply(lambda x: int(x/5))

    # Replace null values with empty list
    spotify_df['consolidate_genre_lists'] = spotify_df['consolidate_genre_lists'].apply(lambda x: x if isinstance(x,list) else [])

    return spotify_df

spotify_df = data_prep(spotify_df,data_w_genre)