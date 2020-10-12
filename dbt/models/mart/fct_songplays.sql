-- songplays table
with source as (
    select
        *
    from {{ ref('stg_songplays') }}
),
fact_songplays as (
    select
        songplays_id,
        track_id,
        track_played_at,
        album_id,
        artist_id,
        artist_id_others,
        artist_name_others
    from source
)
select
    *
from fact_songplays