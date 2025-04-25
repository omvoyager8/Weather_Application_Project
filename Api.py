import requests
import datetime as dt

class Api:
    def __init__(self):
        self.api_key = "b9681bef4a95328a9953b50a21b032f7"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_info_by_city_name(self, city):
        """Fetch and return weather information for a given city."""
        try:
            # Make the API request
            response = requests.get(self.base_url, params={'q': city, 'appid': self.api_key})
            data = response.json()

            # Check if the request was successful and contains required data
            if response.status_code == 200 and self._is_valid_response(data):
                return self._format_weather_data(data)
            else:
                return {"error": "City not found or invalid response from API"}
        except requests.RequestException as e:
            return {"error": f"Request failed: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

    def _is_valid_response(self, data):
        """Check if the response data contains the necessary fields."""
        required_fields = ["main", "weather", "sys"]
        return all(field in data for field in required_fields)

    def _format_weather_data(self, data):
        """Format the weather data into a readable format."""
        return {
            "current_temperature": f"{round(data['main']['temp'] - 273.15, 1)}°C",
            "weather": data['weather'][0]['main'],
            "humidity": f"{data['main']['humidity']}%",
            "sunrise": dt.datetime.fromtimestamp(data['sys']['sunrise']).strftime("%A, %B %d, %Y %I:%M:%S %p"),
            "sunset": dt.datetime.fromtimestamp(data['sys']['sunset']).strftime("%A, %B %d, %Y %I:%M:%S %p"),
            "country": data['sys']['country']
        }
    def get_info_by_coordinates(self, lat, lon):
        """Fetch and return weather info using latitude and longitude."""
        try:
            lat = float(lat)
            lon = float(lon)
            response = requests.get(self.base_url, params={
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            })
            data = response.json()

            if response.status_code == 200 and self._is_valid_response(data):
                return self._format_weather_data(data)
            else:
                return {"error": "Invalid coordinates or response from API"}
        except requests.RequestException as e:
            return {"error": f"Request failed: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}
        