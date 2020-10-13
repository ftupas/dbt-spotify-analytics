-- albums table
{% set tables = ['stg_songplays', 'stg_top_tracks'] %}

{% for table in tables %}
    select distinct
        album_id,
        album_name,
        album_release_year,
        album_type                                   
    from {{ ref(table) }}
    {% if not loop.last -%} union {%- endif %}
{% endfor %}