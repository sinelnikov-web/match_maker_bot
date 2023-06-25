import json

from aiohttp import ClientSession

from .enums import PaymentServiceApiRoute


class Payment:

    def __init__(self):
        self.session = ClientSession()

    async def close(self):
        await self.session.close()

    async def create_payment(self, amount, redirect_url, callback_url, callback_data, expiration_date):
        request_url = PaymentServiceApiRoute.CREATE_PAYMENT.value
        request_body = {"amount": amount, "redirect_url": redirect_url, "callback_url": callback_url,
                        "callback_data": callback_data, "expiration_date": expiration_date}
        headers = {
            "Content-Type": "application/json"
        }
        print(request_body)
        async with self.session.post(url=request_url, data=json.dumps(request_body), headers=headers) as response:
            return await response.json()

    async def check_status(self, payment_id):
        request_url = PaymentServiceApiRoute.GET_STATUS.value + f"/{payment_id}"
        async with self.session.get(url=request_url) as response:
            return response

    async def get_invoice(self, invoice_id):
        request_url = PaymentServiceApiRoute.GET_INVOICE.value + f"/{invoice_id}"
        async with self.session.get(url=request_url) as response:
            return response
