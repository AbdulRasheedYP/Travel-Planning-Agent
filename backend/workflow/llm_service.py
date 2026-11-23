
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .retrieval_service import retrieve_relevant_chunks

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()


def generate_itinerary(travel_request, weather_data=None):

    if not API_KEY:
        return {
            "success": False,
            "error": "Gemini API key not configured"
        }

    destination = travel_request.get("destination", "")

    query = (
        f"Travel attractions, activities and sightseeing "
        f"information for {destination}. "
        f"Trip request: {travel_request}"
    )

    try:
        retrieved_chunks = retrieve_relevant_chunks(
            query=query,
            destination=destination,
            top_k=3,
        )
    except Exception:
        retrieved_chunks = []

    if retrieved_chunks:
        travel_context = "\n\n".join(
            item.content for item in retrieved_chunks
        )
        retrieval_status = "Relevant knowledge found"
    else:
        travel_context = "No relevant travel knowledge found."
        retrieval_status = "No relevant knowledge available"

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
    You are an expert travel planner creating a personalized, day-wise travel itinerary.

    Create a realistic, well-paced day-wise itinerary with engaging sightseeing, activities, and local experiences.

    Travel Details:
    - Starting Location: {travel_request['starting_location']}
    - Destination: {travel_request['destination']}
    - Duration: {travel_request['duration']} days
    - Total Budget: ₹{travel_request['budget']} INR
    - Travellers: {travel_request['travelers']}

    Destination Weather Forecast:
    {weather_data if weather_data else "Weather information currently unavailable"}

    Curated Destination Knowledge (RAG):
    {travel_context if travel_context else "No specific destination knowledge found. Use general destination knowledge."}

    Planning Guidelines:
    1. Each day must feature engaging, specific sightseeing activities (key tourist attractions, scenic viewpoints, nature walks, cultural highlights, and local food).
    2. Deeply utilize the retrieved destination knowledge to include genuine local attractions, activities, and route advice.
    3. Group nearby attractions logically to minimize travel time between spots.
    4. Adapt the itinerary to the destination weather conditions (e.g., plan scenic outdoor walks on clear days, indoor/museum visits or relaxing drives during rain).
    5. Keep activities realistic within the specified duration and budget.
    6. Return the response strictly adhering to the JSON schema.
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
