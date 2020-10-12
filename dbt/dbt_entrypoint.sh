#!/bin/bash
dbt init spotify_analytics &&
cp -r /dbt_init/. /dbt/spotify_analytics &&
cp -r /data/. /dbt/spotify_analytics/data &&
rm -rf /dbt/spotify_analytics/models/example &&
mv /dbt/spotify_analytics/profiles.yml /root/.dbt/profiles.yml
cd /dbt/spotify_analytics &&
dbt debug &&
dbt deps &&
dbt seed &&
dbt run &&
dbt test &&
dbt docs generate &&
dbt docs serve