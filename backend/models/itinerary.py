from pydantic import BaseModel


class ItineraryItem(BaseModel):
    # TODO: Add start/end time windows and geo-coordinates.
    title: str
    description: str
