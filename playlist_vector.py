import pandas as pd

def playlist_vector(complete_feature_set,playlist_df,weight_factor):
    """
    Summarize a user's playlist into a single vector

    Parameters:
        complete_feature_set(panda df): Dataframe including all features for Spotify songs
        playlist_df(panda df): playlist df
        weight_factor(float): float value that represents recency bias. Larger recency bias the most priority sonsgs get.

    Returns:
        playlist_feature_set_weighted_final(panda series): single feature that summarizes playlist
        complete_feature_set_nonplaylist
    """

    complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
    complete_feature_set_playlist = complete_feature_set_playlist.merge(playlist_df[['id','date_added']],on='id',how='inner')
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]

    playlist_feature_set = complete_feature_set_playlist.sort_values('date_added',ascending = False)
    most_recent_date = playlist_feature_set.iloc[0,-1]

    for ind,row in playlist_feature_set.iterrows():
        playlist_feature_set.loc[ind,'months_from_recent'] = int((most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days / 30)
    
    playlist_feature_set['weight'] = playlist_feature_set['months_from_recent'].apply(lambda x: weight_factor **(-x))

    playlist_feature_set_weighted = playlist_feature_set.copy()
    playlist_feature_set_weighted.update(playlist_feature_set_weighted.iloc[:,:-4].mul(playlist_feature_set_weighted.weight,0))
    playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:,:-4]

    return playlist_feature_set_weighted_final.sum(axis=0), complete_feature_set_nonplaylist

