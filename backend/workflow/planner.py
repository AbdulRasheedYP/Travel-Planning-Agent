


def create_travel_plan(travel_request):
    tasks=[
        {
            "step":1,
            "task":"Get destination weather information"
        },
        {
            "step":2,
            "task":"Generate travel itinerary using Gemni"
        },
        {
            "step":3,
            "task":"Calculate estimated travel expenses"
        },
        {
            "step":4,
            "task":"Validate the travel budget"
        }
    ]
    return{
        "agent":"Travel Planning Agent",
        "travel_request":travel_request,
        "tasks":tasks
    }