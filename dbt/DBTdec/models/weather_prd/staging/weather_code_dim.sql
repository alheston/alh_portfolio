{{
    config(
        materialized='table'
    )
}}

select
    weathercode,
    case
        when weathercode = '0' then 'Unknown'
        when weathercode = '1000' then 'Clear'
        when weathercode = '1100' then 'Mostly Clear'
        when weathercode = '1101' then 'Partly Cloudy'
        when weathercode = '1102' then 'Mostly Cloudy'
        when weathercode = '1001' then 'Cloudy'
        when weathercode = '2000' then 'Fog'
        when weathercode = '2100' then 'Light Fog'
        when weathercode = '4000' then 'Drizzle'
        when weathercode = '4001' then 'Rain'
        when weathercode = '4200' then 'Light Rain'
        when weathercode = '4201' then 'Heavy Rain'
        when weathercode = '5000' then 'Snow'
        when weathercode = '5001' then 'Flurries'
        when weathercode = '5100' then 'Light Snow'
        when weathercode = '5101' then 'Heavy Snow'
        when weathercode = '6000' then 'Freezing Drizzle'
        when weathercode = '6001' then 'Freezing Rain'
        when weathercode = '6200' then 'Light Freezing Rain'
        when weathercode = '6201' then 'Heavy Freezing Rain'
        when weathercode = '7000' then 'Ice Pellets'
        when weathercode = '7101' then 'Heavy Ice Pellets'
        when weathercode = '7102' then 'Light Ice Pellets'
        when weathercode = '8000' then 'Thunderstorm'
    end as currentcondition
from {{ source('etl', 'des_moines_weather_hourly') }}
