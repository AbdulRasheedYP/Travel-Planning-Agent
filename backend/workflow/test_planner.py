from planner import create_travel_plan


travel_request={
    "starting_location":"Kochi",
    "destination":"Munnar",
    "budget":15000,
    "duration":3,
    "travelers":2
}

result=create_travel_plan(travel_request)

print(result)