{{
    config(
        materialized='table'
    )
}}

select
time,
temperatureapparent,
temperature,
temperature - LAG(temperature, 1, 0) OVER (PARTITION BY City ORDER BY time) as temp_diff,
humidity,
humidity - LAG(humidity, 1, 0) OVER (PARTITION BY City ORDER BY time) as humidity_diff,
windspeed,
windspeed - LAG(humidity, 1, 0) OVER (PARTITION BY City ORDER BY time) as windspeed_diff,
from {{ref('stg_hourly_des_moines_weather')}}
