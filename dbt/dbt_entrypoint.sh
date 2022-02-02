#!/bin/bash
cp -r /data/. /dbt/data &&
dbt debug --profiles-dir . &&
dbt seed --profiles-dir . &&
dbt deps --profiles-dir . &&
dbt run --profiles-dir . &&
dbt test --profiles-dir .  &&
dbt docs generate --profiles-dir . &&
dbt docs serve --profiles-dir .