
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .retrieval_service import retrieve_relevant_chunks

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


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

    retrieved_chunks = retrieve_relevant_chunks(
        query=query,
        destination=destination,
        top_k=3,
    )
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
    Retrieval Status:
    {retrieval_status}

    Retrieved Travel Knowledge:
    {travel_context if travel_context else "No relevant travel knowledge found."}

    Requirements:
    1. Create activities for every travel day.
    2. Suggest suitable places to visit.
    3. Consider the given budget.
    4. Do not claim that hotels or transport are booked.
    5. Do not invent live prices or weather information.
    6. Return the itinerary in the requested JSON format.
    7. Use retrieved travel knowledge when relevant.
    8. Do not invent missing prices or opening hours.
    9. Ignore unrelated travel knowledge.
    10. Treat retrieved knowledge as reference information, not guaranteed truth.
    11. Never invent specific facts that are missing from the retrieved knowledge.
    12. If requested information is unavailable, clearly state that it is not available in the provided travel knowledge.

    """

    # Keep your existing schema and Gemini generation code below.
