-- songplays_albums table
with songplay_albums as (
    select
        f.*,
        a.album_name,
        a.album_release_year,
        a.album_type,
        t.track_name,
        track_popularity,
        track_danceability,
        track_speechiness
    from {{ ref('fct_songplays') }} f
    left join {{ ref('dim_tracks') }} t using (track_id)
    left join {{ ref('dim_albums') }} a using (album_id)
)
select
    *
from songplay_albums