import pandas as pd
from data_prep import spotify_df
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler


float_cols = spotify_df.dtypes[spotify_df.dtypes == 'float64'].index.values
ohe_cols = 'popularity'
YEAR_SCALER = 0.5
POPULARITY_SCALER = 0.15
FLOAT_SCALER = 0.2

def ohe_prep(df,column,new_name):
    """
    Creates One Hot Encoded features of a specific column

    Parameters: 
        df (pandas df): Spotify Dataframe
        column (str): column to be proceeded
        new_name (str): new column name to be used
    """

    tf_df = pd.get_dummies(df[column])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop = True, inplace = True)
    return tf_df


def create_feature_set(df,float_cols):
    """
    Process spotify df to create a final set of feautures that will be used to generate recommendations
    Parameters:
        df (pandas dataframe): Spotify Dataframe
        float_cols ( list(str)): List of float columns that needs to be scaled
    Returns:
        finalized set of features
    """
    # tfidf genre lists
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['consolidate_genre_lists'].apply(lambda x:" ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + '|' + i for i in tfidf.get_feature_names()]
    genre_df.reset_index(drop = True, inplace = True)

    # explicitly_ohe = ohe_prep(df,'explicit','exp)
    year_ohe = ohe_prep(df,'year','year') * YEAR_SCALER
    popularity_ohe = ohe_prep(df,'pop_red','pop') * POPULARITY_SCALER

    # scale float columns 
    floats = df[float_cols].reset_index(drop = True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats),columns = floats.columns) * FLOAT_SCALER

    # Concatenate all features
    final = pd.concat([genre_df,floats_scaled,popularity_ohe,year_ohe],axis = 1)

    # Add song id
    final['id'] = df['id'].values

    return final

complete_feature_set = create_feature_set(spotify_df,float_cols = float_cols)
