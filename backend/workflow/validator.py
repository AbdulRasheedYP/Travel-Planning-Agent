def validate_itinerary(itinerary, duration):

    errors = []

    days = itinerary.get("days", [])

    if len(days) != duration:
        errors.append("Incorrect itinerary duration")

    for day in days:

        if not day.get("activities"):
            errors.append(
                f"Activities missing on day {day.get('day')}"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_budget(estimated_cost, budget):

    if estimated_cost > budget:
        return {
            "valid": False,
            "message": "Budget exceeded",
            "exceeded_amount": estimated_cost - budget
        }

    return {
        "valid": True,
        "message": "Budget is within the limit",
        "remaining_budget": budget - estimated_cost
    }