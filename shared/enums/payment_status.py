from enum import Enum


class PaymentStatus(Enum):
    PENDING = 'pending'
    CANCELED = 'canceled'
    PAID = 'paid'
