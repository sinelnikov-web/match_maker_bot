from enum import Enum


class EventStatus(Enum):
    PARTICIPANTS_WAIT = 'participants_wait'
    PAYMENT_WAIT = 'payment_wait'
    CANCELED = 'canceled'
    CONDUCTED = 'conducted'
