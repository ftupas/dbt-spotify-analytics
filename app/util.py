from datetime import datetime
from time import sleep
from typing import Union

import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util


class SpotifyUtil:
    """
    Utility class for accessing Spotify API
    """

    query_dict = {
        "current_user_recently_played": "parse_songplays",
        "current_user_top_artists": "parse_top_artists",
        "current_user_top_tracks": "parse_tracks",
        "current_user_playlists": "parse_playlists",
        "playlist_items": "parse_playlists_items",
    }

    def __init__(
        self, username: str, client_id: str, client_secret: str, redirect_uri: str
    ) -> None:
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.session = ""

    def setup(self, scope: str) -> None:
        """
        Setup Spotify connection and authorization
        """
        print("-- Initializing Spotify connection SETUP")

        token = self.get_token(scope=scope)
        print("token is ready!")

        session = spotipy.Spotify(auth=token)
        self.session = session
        sleep(1)
        print(f"connection and user are ready!")

    def get_spotify_data(
        self, query: str, limit: int = 50, time_range: str = "long_term"
    ) -> pd.DataFrame:
        """
        Retrieves data from Spotify
        """
        if query in ["current_user_top_tracks", "current_user_top_artists"]:
            json = getattr(self.session, query)(limit=limit, time_range=time_range)
        else:
            json = getattr(self.session, query)(limit=limit)

        self.df = getattr(self, self.query_dict[query])(data=json)

        if query == "current_user_playlists":
            items = []

            for index in self.df.index.tolist():
                json_items = getattr(self.session, "playlist_items")(
                    limit=100, playlist_id=self.df.at[index, "playlist_id"]
                )
                if len(json_items["items"]) > 0:
                    playlist_items, columns = getattr(
                        self, self.query_dict["playlist_items"]
                    )(data=json_items, playlist_id=self.df.at[index, "playlist_id"])
                    items.append(playlist_items)

            df_items = pd.concat(items)
            return self.df, df_items

        return self.df

    def get_token(self, scope: str) -> str:
        """
        Obtains the token for user authorization
        """
        token = util.prompt_for_user_token(
            username=self.username,
            scope=scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        return token

    def parse_json(self, data: dict, columns: list, **kwargs) -> pd.DataFrame:
        """
        Parses response data in JSON format
        """
        if not (kwargs.get("result_key") == None):
            data = data[kwargs["result_key"]]
        df = pd.json_normalize(data).reset_index()

        if "id" in columns.values():
            df = df.dropna(subset=["id"])

        df["index"] = df["index"] + 1
        df = df[columns.keys()].rename(columns=columns)

        return df

    def parse_primary_other(self, parse_list: list = []) -> Union[str, str]:
        """
        Parses primary and other values for lists
        """
        parse_list = parse_list.copy()
        try:
            primary = parse_list.pop(0)
        except IndexError:
            primary = None

        others = ", ".join(parse_list)
        return primary, others

    def parse_songplays(self, data: dict, columns: dict = None) -> pd.DataFrame:
        """
        Parses songplays data of user
        """
        # Parse artists
        def parse_artist(artists: list) -> Union[list, list, list, list]:
            # parse primary and other artists
            artist_name, artist_name_others = self.parse_primary_other(
                [artist["name"] for artist in artists]
            )
            artist_id, artist_id_others = self.parse_primary_other(
                [artist["id"] for artist in artists]
            )
            return artist_name, artist_name_others, artist_id, artist_id_others

        # Get release year
        def parse_year(album_release_year: str) -> int:
            try:
                year = pd.to_datetime(album_release_year).year
            except (ValueError, NameError, TypeError):
                year = np.nan
            return year

        # Get features
        def get_features(
            key: str,
            method: str,
            df: pd.DataFrame,
            columns: dict,
            result_key: str = None,
        ) -> pd.DataFrame:
            # clean missing ids
            df = df.dropna(subset=[key])

            for values_list in self.split_in_chunks(df[key].values.tolist(), 50):
                try:
                    features = getattr(self.session, method)(values_list)
                except:
                    print("An error occured when trying to get attributes")
                features_df = self.parse_json(
                    data=features, columns=columns, result_key=result_key
                )
                # Parse genres
                unfold_list_column(
                    df=features_df, key="artist_genres", singular_key="artist_genre"
                )

                features_df.drop_duplicates(subset=key, inplace=True)
                df = df.merge(features_df, how="outer")
            return df

        def unfold_list_column(df: pd.DataFrame, key: str, singular_key: str) -> None:
            """some dataframes contain lists inside columns, this function unfolds those lists

            Args:
                df (pd.DataFrame): dataframe on which to perform the action
                key (str): column name that contain list
                singular_key (str): singular of column name, to name new colunm after unfold
            """
            others_key = f"{singular_key}_others"
            if key in df.columns:
                (df[singular_key], df[others_key]) = zip(
                    *df[key].apply(self.parse_primary_other)
                )
                df.drop(columns=[key], axis=1, inplace=True)

        if columns is None:
            columns = {
                "index": "songplays_id",
                "track.id": "track_id",
                "track.name": "track_name",
                "track.artists": "artists",
                "track.duration_ms": "track_duration",
                "track.explicit": "track_is_explicit",
                "track.popularity": "track_popularity",
                "played_at": "track_played_at",
                "track.album.id": "album_id",
                "track.album.name": "album_name",
                "track.album.release_date": "album_release_year",
                "track.album.type": "album_type",
            }

        track_features_columns = {
            "id": "track_id",
            "danceability": "track_danceability",
            "energy": "track_energy",
            "key": "track_key",
            "loudness": "track_loudness",
            "mode": "track_mode",
            "speechiness": "track_speechiness",
            "acousticness": "track_acousticness",
            "instrumentalness": "track_instrumentalness",
            "liveness": "track_liveness",
            "valence": "track_valence",
        }

        artist_features_columns = {
            "id": "artist_id",
            "genres": "artist_genres",
            "popularity": "artist_popularity",
            "followers.total": "artist_followers",
        }

        songplays = self.parse_json(data=data, columns=columns, result_key="items")

        (
            songplays["artist_name"],
            songplays["artist_name_others"],
            songplays["artist_id"],
            songplays["artist_id_others"],
        ) = zip(*songplays["artists"].apply(parse_artist))

        # Convert timestamp
        try:
            songplays["track_played_at"] = songplays["track_played_at"].apply(
                lambda x: pd.Timestamp(x).strftime("%Y-%m-%d %H:%M:%S")
            )
        except KeyError:
            pass

        # Convert track duration
        songplays["track_duration"] = songplays["track_duration"].apply(
            lambda x: x / 60000
        )

        songplays["album_release_year"] = songplays["album_release_year"].apply(
            lambda x: parse_year(x)
        )
        # Get track features

        songplays = get_features(
            key="track_id",
            method="audio_features",
            df=songplays,
            columns=track_features_columns,
        )

        # Get artist features

        songplays = get_features(
            key="artist_id",
            method="artists",
            df=songplays,
            columns=artist_features_columns,
            result_key="artists",
        )
        # Parse genres
        unfold_list_column(
            df=songplays, key="artist_genres", singular_key="artist_genre"
        )

        return songplays

    def parse_top_artists(self, data: dict) -> pd.DataFrame:
        """
        Parses top artists of user
        """
        columns = {
            "index": "artist_rank",
            "id": "artist_id",
            "name": "artist_name",
            "genres": "artist_genres",
            "popularity": "artist_popularity",
            "followers.total": "artist_followers",
        }

        top_artists = self.parse_json(data=data, columns=columns, result_key="items")
        # Parse genres
        (top_artists["artist_genre"], top_artists["artist_genre_others"]) = zip(
            *top_artists["artist_genres"].apply(self.parse_primary_other)
        )

        top_artists.drop(columns=["artist_genres"], axis=1, inplace=True)
        return top_artists

    def parse_tracks(self, data: dict) -> pd.DataFrame:
        """
        Parses top tracks of user
        """
        columns = {
            "index": "track_rank",
            "id": "track_id",
            "name": "track_name",
            "artists": "artists",
            "duration_ms": "track_duration",
            "explicit": "track_is_explicit",
            "popularity": "track_popularity",
            "album.id": "album_id",
            "album.name": "album_name",
            "album.release_date": "album_release_year",
            "album.type": "album_type",
        }

        top_tracks = self.parse_songplays(data=data, columns=columns)
        return top_tracks

    def parse_playlists(self, data: dict) -> pd.DataFrame:
        """
        Parses playlists of user
        """
        columns = {
            "index": "playlist_rank",
            "id": "playlist_id",
            "name": "playlist_name",
            "tracks.total": "playlist_size",
            "public": "playlist_is_public",
            "collaborative": "playlist_is_collaborative",
        }

        playlists = self.parse_json(data=data, columns=columns, result_key="items")

        return playlists

    def parse_playlists_items(
        self, data: dict, playlist_id: str
    ) -> Union[pd.DataFrame, list]:
        """
        Parses items of a playlist of user
        """

        tmp_list = [item["track"] for item in data["items"]]
        data["items"] = tmp_list

        playlist_items = self.parse_tracks(data=data)
        playlist_items["playlist_id"] = playlist_id
        columns = playlist_items.columns
        return playlist_items, columns

    def split_in_chunks(self, lst: list, n: int) -> list:
        for i in range(0, len(lst), n):
            yield lst[i : i + n]
