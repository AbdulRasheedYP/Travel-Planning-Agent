import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def generate_itinerary(travel_request, weather_data=None):

    if not API_KEY:
        return {
            "success": False,
            "error": "Gemini API key not configured"
        }

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
    You are a professional Kerala travel planner.

    Create a realistic day-wise travel itinerary.

    Travel details:
    Starting location: {travel_request['starting_location']}
    Destination: {travel_request['destination']}
    Duration: {travel_request['duration']} days
    Budget: {travel_request['budget']} INR
    Travellers: {travel_request['travelers']}

    Weather information:
    {weather_data if weather_data else "Not available"}

    Requirements:
    1. Create activities for every travel day.
    2. Suggest suitable places to visit.
    3. Consider the given budget.
    4. Do not claim that hotels or transport are booked.
    5. Do not invent live prices or weather information.
    6. Return the itinerary in the requested JSON format.
    """

    schema = {
        "type": "OBJECT",
        "properties": {
            "trip_title": {
                "type": "STRING"
            },
            "days": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "day": {"type": "INTEGER"},
                        "title": {"type": "STRING"},
                        "activities": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        }
                    },
                    "required": ["day", "title", "activities"]
                }
            }
        },
        "required": ["trip_title", "days"]
    }

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )

        itinerary = json.loads(response.text)

        return {
            "success": True,
            "itinerary": itinerary
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }