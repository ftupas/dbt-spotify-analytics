from util import SpotifyUtil
import config
import os

ITEM_LIMIT = 50
DATA_PATH = "data"
DATA_DICT = {
    "current_user_top_artists": "user-top-read",
    "current_user_recently_played": "user-read-recently-played",
    "current_user_top_tracks": "user-top-read",
    "current_user_playlists": "playlist-read-private",
}


def main():

    spotifyutil = SpotifyUtil(
        username=config.USERNAME,
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=config.REDIRECT_URI,
    )

    all_scopes = ""
    for scope in DATA_DICT.values():
        all_scopes += scope + " "

    spotifyutil.setup(scope=all_scopes)

    for query in DATA_DICT.keys():
        print(f"--GETTING {query}--")

        if query == "current_user_playlists":
            df, df_items = spotifyutil.get_spotify_data(query=query, limit=ITEM_LIMIT)

            # Write data to ../data folder
            df.to_csv(
                os.path.join(DATA_PATH, f"{query}.csv"), index=False, encoding="utf-8"
            )
            df_items.to_csv(
                os.path.join(DATA_PATH, "playlist_items.csv"),
                index=False,
                encoding="utf-8",
            )
        else:
            df = spotifyutil.get_spotify_data(query=query, limit=ITEM_LIMIT)

            # Write data to ../data folder
            df.to_csv(
                os.path.join(DATA_PATH, f"{query}.csv"), index=False, encoding="utf-8"
            )


if __name__ == "__main__":
    main()
