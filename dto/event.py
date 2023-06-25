from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json

from dto import UserDTO
from shared.enums import EventStatus, PaymentStatus


@dataclass_json
@dataclass
class TeamDTO:
    id: str
    event: EventDTO
    participants: List[UserDTO]


@dataclass_json
@dataclass
class EventDTO:
    host: UserDTO
    name: str
    status: EventStatus = EventStatus.PARTICIPANTS_WAIT
    teams: List[TeamDTO] = field(default_factory=list)
    id: Optional[int] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[str] = None
    max_participants: Optional[int] = None

    def has_participant(self, user_id: int):
        for team in self.teams:
            for user in team.participants:
                if user.id == user_id:
                    return True
        return False


@dataclass_json
@dataclass
class PaymentDTO:
    id: str
    event: EventDTO
    user: UserDTO
    status: PaymentStatus
    amount: float
