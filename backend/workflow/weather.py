import requests


def get_weather(destination):

    # Step 1: Find destination coordinates

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": destination,
        "count": 1,
        "language": "en",
        "countryCode": "IN"
    }

    try:
        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        locations = geo_data.get("results")

        if not locations:
            return {
                "success": False,
                "error": "Destination not found"
            }

        location = locations[0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get weather forecast

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        return {
            "success": True,
            "destination": location["name"],
            "weather": weather_data["current"]
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }