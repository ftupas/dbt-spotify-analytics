-- top_artists table
with source as (
    select
        *
    from {{ ref('stg_top_artists') }}
),
fact_top_artists as (
    select
        artist_rank,
        artist_id
    from source
)
select
    *
from fact_top_artists