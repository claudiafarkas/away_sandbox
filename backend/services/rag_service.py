def generate_itinerary(context: dict) -> dict:
    # TODO: Integrate embedding store and LLM orchestration.
    return {
        "status": "pending",
        "itinerary": [],
        "context": context,
    }
