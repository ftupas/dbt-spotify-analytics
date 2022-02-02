-- stage_top_artists
with source as (
    select
        *
    from {{ source('spotify', 'current_user_top_artists') }}
),

stage_top_artists as (
    select
        artist_rank,
        artist_id,
        artist_name,
        artist_popularity,
        artist_followers,
        artist_genre,
        artist_genre_others
    from source
)
select
    *
from stage_top_artists