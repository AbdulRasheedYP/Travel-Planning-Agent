from weather import get_weather
from llm_service import generate_itinerary
from validator import validate_itinerary


def execute_weather_task(destination):

    try:
        result = get_weather(destination)

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Weather unavailable")
            }

        return result

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def execute_itinerary_task(travel_request, weather_data=None):

    try:
        result = generate_itinerary(
            travel_request,
            weather_data
        )

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "AI generation failed")
            }

        return result

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def execute_travel_workflow(travel_request):

    # Step 1: Get weather information

    weather_result = execute_weather_task(
        travel_request["destination"]
    )

    weather_data = None
    warnings = []

    if weather_result["success"]:
        weather_data = weather_result["weather"]
    else:
        warnings.append("Weather information unavailable")

    # Step 2: Generate itinerary using Gemini

    itinerary_result = execute_itinerary_task(
        travel_request,
        weather_data
    )

    if not itinerary_result["success"]:
        return {
            "success": False,
            "stage": "itinerary_generation",
            "error": itinerary_result["error"]
        }

    # Step 3: Validate itinerary

    itinerary = itinerary_result["itinerary"]

    validation = validate_itinerary(
        itinerary,
        travel_request["duration"]
    )

    if not validation["valid"]:
        return {
            "success": False,
            "stage": "validation",
            "errors": validation["errors"]
        }

    # Step 4: Return final result

    return {
        "success": True,
        "itinerary": itinerary,
        "weather": weather_data,
        "warnings": warnings
    }