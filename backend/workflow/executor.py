from weather import get_weather


def execute_weather_task(destination):

    print("Executor started...")

    weather_result = get_weather(destination)

    if not weather_result["success"]:
        print("Weather task failed")

        return weather_result

    print("Weather task completed")

    return weather_result