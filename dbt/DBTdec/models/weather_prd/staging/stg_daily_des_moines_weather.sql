{{
    config(
        materialized='table'
    )
}}

select 
    time,
    sunrisetime,
    sunsettime,
    'DesMoines' as City
from {{ source('etl', 'des_moines_weather_daily') }}