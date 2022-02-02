-- stage_top_tracks
with source as (
    select
        *
    from {{ source('spotify', 'current_user_top_tracks') }}
),

stage_top_tracks as (
    select
        track_rank,
        track_id,
    	track_name,
        track_duration,
        track_is_explicit,
        track_popularity,
        album_id,
        album_name,
        album_release_year,
        album_type,
        artist_name,
        artist_name_others,
        artist_id,
        artist_id_others,
        track_danceability,
        track_energy,
        track_key,
        track_loudness,
        track_mode,
        track_speechiness,
        track_acousticness,
        track_instrumentalness,
        track_liveness,
        track_valence,
        artist_popularity,
        artist_followers,
        artist_genre,
        artist_genre_others
    from source
)
select
    *
from stage_top_tracks