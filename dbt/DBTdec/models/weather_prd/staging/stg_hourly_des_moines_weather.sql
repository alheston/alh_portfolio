{{
    config(
        materialized='table'
    )
}}

select 
    time,
    humidity,
    windspeed,
    temperature, 
    weathercode,
    rainaccumulation,
    precipitationtype,
    temperatureapparent,
    precipitationprobability,
    'DesMoines' as City
from {{ source('etl', 'des_moines_weather_hourly') }}