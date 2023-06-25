from enum import Enum


class PaymentServiceApiRoute(Enum):
    CREATE_PAYMENT = 'http://127.0.0.1/api/payments/invoice/'
    GET_STATUS = 'http://127.0.0.1/api/payments/invoice/'
    GET_INVOICE = 'http://127.0.0.1/api/billing/'
