from dto.event import EventDTO
from shared.enums import EventStatus
from tgbot.shared.db.api import change_event_status


async def approve_event(event: EventDTO):
    return await change_event_status(event.id, EventStatus.PAYMENT_WAIT)


async def decline_event(event: EventDTO):
    return await change_event_status(event.id, EventStatus.CANCELED)
