from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sp
def create_playlist_rec(df,features,nonplaylist_features):
    """
    Pull songs from specfic playlist

    Parameters:
        df (pandas dataframe): spotify dataframe
        features (pandas series): summarized playlist features
        nonplaylist_features (pandas dataframe): feature set of songs that are not in the selected playlist

    Returns:
        non_playlist_df_top 40: Top 40 recommendations for that playlist
    """

    non_playlist_df = df[df['id'].isin(nonplaylist_features['id'].values)]
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id',axis=1).values,features.values.reshape(1,-1))[:,0]
    nonplaylist_df_top_40 = non_playlist_df.sort_values('sim',ascending=False).head(40)
    nonplaylist_df_top_40['url'] = nonplaylist_df_top_40['id'].apply(lambda x: sp.sp.track(x)['album']['images'][1]['url'])

    return nonplaylist_df_top_40