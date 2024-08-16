import requests
from connectors.WeatherClient import WeatherApiClient
from connectors.PostgresClient import PostgresClient
import pandas as pd
from sqlalchemy import Table, MetaData

base_url = "https://api.tomorrow.io/v4/weather/forecast?"

import requests

def get_weather(
        weather_api_client: WeatherApiClient, location: str, 
        units: str, 
        timesteps: str
    ) -> list[dict]:
    
    base_url = "https://api.tomorrow.io/v4/weather/forecast"
    params = {
        "location": location,
        "units": units,
        "timesteps": timesteps,
        "apikey": weather_api_client.api_key_id
    }
    
    headers = {
        "accept": "application/json"
    }
    
    response = requests.get(url=base_url, params=params, headers=headers)
    
    if response.status_code == 200: 
        return response.json()
    else:
        print(f"URL: {response.url}")
        print(f"Response status code: {response.status_code}")
        print(f"Error: {response.status_code} - {response.content.decode('utf-8')}")
        response.raise_for_status()


# api_key = "AZnrEq4L5h4lIl9cMWkvL3TnDdc3bRx1"
# weather_client = WeatherApiClient(api_key_id=api_key)
# location='41.5868, 93.6250'
# units='imperial'
# timesteps='1h'
# weather_data = get_weather(
#     weather_api_client=weather_client,
#     location=location,
#     units=units,
#     timesteps=timesteps
# )


def weather_data_to_df(data: list[dict], frequency: str) -> pd.DataFrame:
  rows = []
  if frequency == "hourly":
     selected_fields = ['temperature', 
                        'humidity', 
                        'temperatureApparent', 
                        'windSpeed', 
                        'precipitationProbability',
                        'precipitationType', 
                        'rainAccumulation', 
                        'weatherCode'
                        ]
     intervals = data['timelines']['hourly']
  elif frequency == 'daily':
     selected_fields = [
                        'temperature', 
                        'uvIndex', 
                        'uvHealthConcern', 
                        'thunderstormProbability', 
                        'evapotranspiration', 
                        'sunriseTime', 
                        'sunsetTime', 
                        'weatherCodeDay', 
                        'weatherCodeNight'
                    ]
     intervals = data['timelines']['daily']
  for interval in intervals:
     record = {
                  'time': interval['time']
               }
     for field in selected_fields:
          record[field] = interval['values'].get(field)
          
     rows.append(record)
    
  df = pd.DataFrame(rows)
  return df

def load(
    df: pd.DataFrame,
    postgres_client: PostgresClient,
    table: Table,
    metadata: MetaData,
    load_method: str = "overwrite"
    ) -> None: 
     if load_method == "insert":
          postgres_client.insert(
               data = df.to_dict(orient="records"), table=table, metadata=metadata
          )
     elif load_method == "overwrite":
          postgres_client.overwrite(
               data = df.to_dict(orient="records"), table=table, metadata=metadata
          )
     elif load_method == "upsert":
          postgres_client.upsert(
               data = df.to_dict(orient="records"), table=table, metadata=metadata
          )

