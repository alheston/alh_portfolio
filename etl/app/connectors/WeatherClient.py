import requests 
from datetime import datetime

class WeatherApiClient:
    def __init__(self, api_key_id: str):
        self.base_url = "https://api.tomorrow.io/v4/weather/forecast?"
        if api_key_id is None:
            raise Exception("API key is not there")
        self.api_key_id = api_key_id
        