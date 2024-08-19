{{
    config(
        materialized='table'
    )
}}

select
    hourly.time,
    hourly.humidity,
    hourly.windspeed,
    hourly.temperature,
    hourly.weathercode,
    hourly.rainaccumulation,
    hourly.precipitationtype,
    hourly.temperatureapparent,
    hourly.precipitationprobability,
    hourly.city,
    daily.sunrisetime,
    daily.sunsettime
from {{ ref('stg_hourly_des_moines_weather') }} as hourly
inner join {{ ref('stg_daily_des_moines_weather') }} as daily
    on date(hourly.time) = date(daily.time)
