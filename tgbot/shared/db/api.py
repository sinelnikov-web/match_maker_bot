import datetime
from typing import List

from django.db.models import Q

from dto import UserDTO
from dto.event import EventDTO, TeamDTO, PaymentDTO
from shared.db import get_or_none
from shared.enums import EventStatus, PaymentStatus
from shared.utils import create_dto
from sport_events.models import Event, Team, Payment
from telegram.models import TelegramUser


async def create_event_model(user: UserDTO, event: EventDTO):
    user_model = await TelegramUser.objects.aget(id=user.id)

    event_model = await Event.objects.acreate(
        name=event.name,
        description=event.description,
        host=user_model,
        date=datetime.datetime.strptime(event.date, "%d.%m.%Y %H:%M"),
        amount=event.amount,
        max_participants=event.max_participants
    )
    await event_model.asave()
    teams = []
    for i in range(len(event.teams)):
        team_model = await Team.objects.acreate(event=event_model)
        await team_model.asave()
        teams.append(
            TeamDTO(id=team_model.id, participants=[], event=event)
        )

    event.teams = teams
    event.id = event_model.id

    return event


async def get_event_by_team(id: str) -> EventDTO:
    team_model = await get_or_none(Team, id=id)

    if team_model is None:
        return

    event = create_dto(team_model.event, EventDTO)
    return event


async def get_event(id: int) -> EventDTO:
    event_model = await get_or_none(Event, id=id)

    if event_model is None:
        return

    event = create_dto(event_model, EventDTO)
    return event


async def add_user_in_team(user_id, team_id) -> TeamDTO:
    team_model = await get_or_none(Team, id=team_id)
    user_model = await get_or_none(TelegramUser, id=user_id)

    team_model.participants.add(user_model)
    await team_model.asave()

    return create_dto(team_model, TeamDTO)


async def remove_user_from_team(user_id, team_id) -> TeamDTO:
    team_model = await get_or_none(Team, id=team_id)
    user_model = await get_or_none(TelegramUser, id=user_id)

    team_model.participants.remove(user_model)
    await team_model.asave()

    return create_dto(team_model, TeamDTO)


async def change_event_status(event_id: int, status: EventStatus) -> EventDTO:
    event_model = await get_or_none(Event, id=event_id)

    event_model.status = status.value

    await event_model.asave()

    return create_dto(event_model, EventDTO)


async def get_active_teams(user: UserDTO) -> List[TeamDTO]:
    user_model = await get_or_none(TelegramUser, id=user.id)
    teams = user_model.teams.exclude(
        Q(event__status=EventStatus.CANCELED.value) | Q(event__date__lt=datetime.datetime.now())
    )
    teams_dto = list(map(lambda x: create_dto(x, TeamDTO), teams))
    return teams_dto


async def get_payment_by_user(user_id: int, event_id: int) -> PaymentDTO:
    payment = await get_or_none(Payment, user__id=user_id, event__id=event_id)
    if payment is None:
        return
    return create_dto(payment, PaymentDTO)


async def change_payment_status(payment_id, status: PaymentStatus) -> PaymentDTO:
    payment = await get_or_none(Payment, id=payment_id)
    payment.status = status.value
    await payment.asave()

    return create_dto(payment, PaymentDTO)