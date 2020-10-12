-- top_tracks table
with source as (
    select
        *
    from {{ ref('stg_top_tracks') }}
),
fact_top_tracks as (
    select
        track_rank,
        track_id,
        album_id,
        artist_name_others,
        artist_id,
        artist_id_others
    from source
)
select
    *
from fact_top_tracks