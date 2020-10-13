-- artists table
{% set tables = ['stg_songplays', 'stg_top_artists', 'stg_top_tracks'] %}

{% for table in tables %}
    select distinct
        artist_id,
        artist_name,
        artist_popularity,
        artist_followers,
        artist_genre,
        artist_genre_others                                     
    from {{ ref(table) }}
    {% if not loop.last -%} union {%- endif %}
{% endfor %}