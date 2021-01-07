import pandas as pd
import numpy as np
import re
import itertools

spotify_df = pd.read_csv("data.csv")
data_w_genre = pd.read_csv("data_w_genres.csv")
def normalize_genre(genre_df):
    """
    Normalize text for genres in genre dataframe

    Parameters:
        genre_df (pandas dataframe): spotify song genre dataframe

    Returns:
        panda dataframe with new normalized column named 'genres_upd'
    """
    data_w_genre['genres_upd'] = data_w_genre['genres'].\
        apply(lambda x:[re.sub(" ","_",i) for i in re.findall(r"'([^']*)'",x)])
    return genre_df

def normalize_artists(spotify_df):
    """
    Normalize text for artists in spotify dataframe

    Parameters:
        spotify_df (pandas dataframe): spotify dataframe

    Returns:
        panda dataframe with new normalized column named 'artists_final'
    """

    # Normalize artists column in spotify_df
    spotify_df['artists_v1'] = spotify_df['artists'].apply(lambda x: re.findall(r"'([^']*)'",x))
    # Normalize artists column that v1 missed
    spotify_df['artists_v2'] = spotify_df['artists'].apply(lambda x: re.findall('\"(.*?)\"',x))

    # Combine v1 and v2
    spotify_df['artists_final'] = np.where(spotify_df['artists_v1'].apply(lambda x: not x),spotify_df['artists_v2'],spotify_df['artists_v1'])
    return spotify_df

def song_artist_identifier(spotify_df):
    """
    Creates column that matches artist to song name

    Parameters:
        spotify_df (pandas dataframe): spotify dataframe

    Returns:
        panda dataframe with new column named 'artist_song'
    """
    spotify_df['artist_song'] = spotify_df.apply(lambda row: row['artists_final'][0] + '_' + row['name'],axis=1)
    spotify_df.drop_duplicates('artist_song',inplace = True)
    return spotify_df

def combine_dataframes(spotify_df,genre_df):
    """
    Creates an dataframe using spotify_df which explodes artists_final column. Using that dataframe merges with
    genre_df to identify each artists genre. Merge that dataframe with original spotify_df to include genres to
    spotify_df

    Parameters:
        spotify_df (pandas dataframe): spotify dataframe
        genre_df (pandas dataframe): spotify song genre dataframe
    Returns:
        spotify_df panda dataframe including genres
    """

    artists_explode = spotify_df[['artists_final','id']].explode('artists_final')

    # Merge exploded df with genre df
    artists_explode_merge = artists_explode.merge(genre_df, how ='left', left_on = 'artists_final', right_on = 'artists')
    artists_explode_merge_nonnull = artists_explode_merge[~artists_explode_merge.genres_upd.isnull()]

    # Group each song and lists its genre with the given dataset we created
    artists_genres_consolidated = artists_explode_merge_nonnull.groupby('id')['genres_upd'].apply(list).reset_index()
    artists_genres_consolidated['consolidate_genre_lists'] = artists_genres_consolidated['genres_upd'].apply(lambda x:list(set(list(itertools.chain.from_iterable(x)))))
    spotify_df = spotify_df.merge(artists_genres_consolidated[['id','consolidate_genre_lists']],on ='id',how ='left')

    return spotify_df

def split_pop_year(spotify_df,pop_split):
    """
    Creates two columns for spotify dataframe, year column and popularity column which is divided into buckets.
    Also replaces null values into empty lists

    Parameters:
        spotify_df (pandas dataframe): spotify dataframe

    Returns:
        updated spotify_df
    """

    spotify_df['year'] = spotify_df['release_date'].apply(lambda x: x.split('-')[0])

    # Divide popularity column into a number of parts
    spotify_df['pop_red'] = spotify_df['popularity'].apply(lambda x: int(x/pop_split))

    # Replace null values with empty list
    spotify_df['consolidate_genre_lists'] = spotify_df['consolidate_genre_lists'].apply(lambda x: x if isinstance(x,list) else [])

    return spotify_df

def data_prep(spotify_df,genre_df):
    """
    Executes normalize_genre, normalize_artists, song_artitst_identifier, combine_dataframes, split_pop_year
    functions

    Parameters:
        spotify_df (pandas dataframe): spotify dataframe

    Returns:
        finalized spotify_df
    """
    genre_df = normalize_genre(genre_df)
    spotify_df = combine_dataframes(song_artist_identifier(normalize_artists(spotify_df)),genre_df)
    return split_pop_year(spotify_df,5)