from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def home(request):

    return Response({
        "message": "Travel Planning Agent API is running",
        "status": "success"
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .executor import execute_travel_workflow


@api_view(["POST"])
def generate_trip(request):

    data = request.data

    required_fields = [
        "starting_location",
        "destination",
        "budget",
        "duration",
        "travelers"
    ]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"{field} is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    try:
        travel_request = {
            "starting_location": data["starting_location"],
            "destination": data["destination"],
            "budget": int(data["budget"]),
            "duration": int(data["duration"]),
            "travelers": int(data["travelers"])
        }

        if (
            not travel_request["starting_location"].strip()
            or not travel_request["destination"].strip()
            or travel_request["budget"] <= 0
            or travel_request["duration"] <= 0
            or travel_request["travelers"] <= 0
        ):
            raise ValueError("Invalid travel details")

    except (ValueError, TypeError, AttributeError):
        return Response(
            {"error": "Please provide valid travel details"},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = execute_travel_workflow(travel_request)

    if not result["success"]:
        return Response(
            result,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return Response(result, status=status.HTTP_200_OK)