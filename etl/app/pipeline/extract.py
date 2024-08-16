import yaml
from dotenv import load_dotenv
import os
from pathlib import Path
from connectors.WeatherClient import WeatherApiClient
from connectors.PostgresClient import PostgresClient
from assets.WeatherData import get_weather, weather_data_to_df, load
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, TIMESTAMP, DateTime
from connectors.Airbyte import Airbyte
import schedule
import time


def pipeline(config):
    load_dotenv()
    ##postgres conn
    host_name = os.environ.get("host_name")
    database_name = os.environ.get("database_name")
    username = os.environ.get("username")
    password = os.environ.get("password")
    port = os.environ.get("port")
    airbyte_connection_id = os.environ.get("airbyte_connection_id")
    airbyte_username = os.environ.get("airbyte_username")
    airbyte_password = os.environ.get("airbyte_password")
    airbyte_server_name=os.environ.get("airbyte_server_name")
    print("pstgres + airbyte connection details loaded")

    ## weather api parameters moving to config in __main__ entry point
    api_key = os.environ.get("api_key")
    ## pg client
    postgres_client = PostgresClient(
    host_name = host_name,
    database_name = database_name,
    username = username,
    password = password,
    port = port)
    print(postgres_client)
    print("pstgres client details loaded")
    ## api client
    weather_client = WeatherApiClient(
        api_key_id=api_key
    )
    ## get weather data api
    print("extracting from weather api for hourly metrics")
    data_hourly = get_weather(
        weather_api_client=weather_client,
        location=config.get("location_hourly"),
        units=config.get("units_hourly"),
        timesteps=config.get("timesteps_hourly")
    )
    print("extracting from weather api for daily metrics")
    data_daily = get_weather(
        weather_api_client=weather_client,
        location=config.get("location_daily"),
        units=config.get("units_daily"),
        timesteps=config.get("timesteps_daily")

    )
    print("extracting from weather api done")
    ## transform weather data
    
    df_hourly = weather_data_to_df(data_hourly, frequency="hourly")
    df_daily = weather_data_to_df(data_daily, frequency="daily")
    # df_daily['sunriseTime'] = df_daily['sunriseTime'].astype('timestamp')
    # df_daily['sunsetTime'] = df_daily['sunsetTime'].astype('timestamp')

    print(f"weather df: {df_hourly}")
    print(f"daily df dtypes: {df_daily.dtypes}")
    ## define postgres table to pass 
    metadata = MetaData()
    
    table_hourly = Table(
    "des_moines_weather_hourly",
    metadata,
    Column("time", DateTime, primary_key=True),
    Column("temperature", Float),
    Column("humidity", Float),
    Column("temperatureApparent", Float),
    Column("windSpeed", Float),
    Column("precipitationProbability", Float),
    Column("precipitationType", Float),
    Column("rainAccumulation", Float),
    Column("weatherCode", String),
    )

    table_daily = Table(
    "des_moines_weather_daily",
    metadata,
    Column("time", DateTime, primary_key=True),
    Column("temperature", Float),
    Column("uvIndex", Integer),
    Column("uvHealthConcern", Integer),
    Column("thunderstormProbability", Float),
    Column("evapotranspiration", Float),
    Column("sunriseTime", DateTime),
    Column("sunsetTime", DateTime),
    Column("weatherCodeDay", String),
    Column("weatherCodeNight", Float)
    )


    print("starting load of hourly")
    load(
    df = df_hourly,
    postgres_client = postgres_client,
    table = table_hourly,
    metadata = metadata,
    load_method = os.environ.get("load_method")
    )

    print("starting load of daily")
    load(
    df = df_daily,
    postgres_client = postgres_client,
    table = table_daily,
    metadata = metadata,
    load_method = os.environ.get("load_method")
    )

    print("load to postgres done")

    print("starting airbyte connection")
    airbyte_client = Airbyte(
        server_name=airbyte_server_name,
        username=airbyte_username,
        password=airbyte_password
    )

    print("triggering sync from postgres to snowflake")
    
    if airbyte_client.valid_connection():
        airbyte_client.trigger_sync(
            connection_id=airbyte_connection_id
        )
        
    print(f"check airbyte UI for successfull sync {airbyte_connection_id}")


if __name__ == "__main__":
    yaml_file_path = __file__.replace(".py", ".yaml")
    if Path(yaml_file_path).exists():
        with open(yaml_file_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
            print("Loaded config:", config)
    else:
        raise Exception(
            f"Missing {yaml_file_path} file! Please create the yaml file with at least a `name` key for the pipeline name."
        )
    
    pipeline(config['config'])
    print("Pipeline executed successfully.")


