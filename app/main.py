from util import SpotifyUtil
import config
import os

ITEM_LIMIT=50
DATA_PATH='data'
DATA_DICT = {
    'songplays': {'current_user_recently_played': 'user-read-recently-played'},
    'top_artists': {'current_user_top_artists': 'user-top-read'},
    'top_tracks': {'current_user_top_tracks': 'user-top-read'}
}

def main():

    # Instantiate a SpotifyUtil object 
    spotifyutil = SpotifyUtil(username=config.USERNAME,
                              client_id=config.CLIENT_ID,
                              client_secret=config.CLIENT_SECRET,
                              redirect_uri=config.REDIRECT_URI)
    
    # Retrieve data from Spotify
    for data, scope_dict in DATA_DICT.items():
        print(f'--GETTING {data}--')
        for query, scope in scope_dict.items():
            df = spotifyutil.getSpotifyData(scope=scope, query=query, limit=ITEM_LIMIT)

            # Write data to spotify_analytics/data
            spotifyutil.writeCSV(df=df, path=os.path.join(DATA_PATH, f'{data}.csv'))
            DATA_DICT[data] = df
    
if __name__ == '__main__':
    main()