from pydantic import BaseModel
from domain.event.table import Event

class EventResponse(BaseModel) :
    id: int
    image_url: str

def create_event_response(event: Event) :
    return EventResponse(
        id = event.id,
        image_url = event.image_url
    )