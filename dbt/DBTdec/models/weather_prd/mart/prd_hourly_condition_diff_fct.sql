{{
    config(
        materialized='table'
    )
}}

select
    time,
    temperatureapparent,
    temperature,
    humidity,
    windspeed,
    temperature - LAG(temperature, 1, 0) over (partition by city order by time) as temp_diff,
    humidity - LAG(humidity, 1, 0) over (partition by city order by time) as humidity_diff,
    windspeed - LAG(humidity, 1, 0) over (partition by city order by time) as windspeed_diff
from {{ ref('stg_hourly_des_moines_weather') }}
