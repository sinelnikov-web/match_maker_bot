import datetime
import json

from match_maker_bot import celery_app, celery_event_loop
from shared.db import get_or_none
from shared.enums import PaymentStatus, EventStatus
from sport_events.models import Payment
from telegram.models import TelegramUser
from tgbot.loader import bot
from tgbot.matchMakingService.lib.event_text import create_event_text
from tgbot.shared.db.api import get_event, get_payment_by_user, change_payment_status, change_event_status
from payment_service.payment import Payment as PaymentService


async def payment_request(event_id: int):
    payment_service = PaymentService()
    event = await get_event(event_id)
    users_count = 0
    for team in event.teams:
        users_count += len(team.participants)

    amount = event.amount / users_count

    for team in event.teams:
        for user in team.participants:
            user_model = await get_or_none(TelegramUser, id=user.id)
            payment_data = await payment_service.create_payment(
                amount=float(amount),
                redirect_url="https://t.me/makeurmatch_bot",
                callback_url="https://f406-67-209-129-23.ngrok-free.app/api/payment_notification/",
                callback_data=json.dumps({"user_id": user.id, "event_id": event.id}),
                expiration_date=str(datetime.datetime.now() + datetime.timedelta(days=7))
            )
            print(payment_data)
            payment = await Payment.objects.acreate(
                id=payment_data.get("id"),
                event_id=event.id,
                user=user_model,
                amount=amount,
                url="http://127.0.0.1/" + payment_data.get("payment_url")
            )

            await bot.send_message(
                chat_id=user.id,
                text=await create_event_text(
                    event,
                    ['show_teams', 'status', 'payment'],
                    payment_link=payment.url,
                    payment_amount=amount
                )
            )
    await payment_service.close()

@celery_app.task()
def send_payment_requests(event_id: int):
    celery_event_loop.run_until_complete(payment_request(event_id))


async def notify_about_cancel(event_id: int):
    event = await get_event(event_id)

    for team in event.teams:
        for user in team.participants:
            user_model = await get_or_none(TelegramUser, id=user.id)

            payment = await Payment.objects.aget(
                user=user_model,
                event_id=event.id,
            )

            if payment.status == PaymentStatus.PAID.value:
                await bot.send_message(
                    chat_id=user.id,
                    text=await create_event_text(
                        event,
                        ['show_teams', 'status', 'cancel', 'refund'],
                        payment_amount=payment.amount
                    )
                )
            else:
                await bot.send_message(
                    chat_id=user.id,
                    text=await create_event_text(
                        event,
                        ['show_teams', 'status', 'cancel'],
                    )
                )

            payment.status = PaymentStatus.CANCELED.value
            await payment.asave()


@celery_app.task()
def send_refund(event_id: int):
    celery_event_loop.run_until_complete(notify_about_cancel(event_id))


async def notify_user_about_payment(data):
    event = await get_event(data.get('event_id'))
    payment = await get_payment_by_user(data.get('user_id'), event.id)

    new_payment = await change_payment_status(payment.id, PaymentStatus.PAID)

    await bot.send_message(
        chat_id=payment.user.id,
        text=await create_event_text(
            new_payment.event,
            ['status', 'show_teams', 'payment'],
            payment_amount=new_payment.amount,
            payment_status=new_payment.status
        ),
    )


@celery_app.task()
def notify_user_about_payment_success(data: dict):
    celery_event_loop.run_until_complete(notify_user_about_payment(data))


async def notify_about_cancel_payment(data: dict):
    event = await get_event(data.get('event_id'))
    payment = await get_payment_by_user(data.get('user_id'), event.id)

    new_payment = await change_payment_status(payment.id, PaymentStatus.CANCELED)
    new_event = await change_event_status(event.id, EventStatus.CANCELED)

    await bot.send_message(
        chat_id=new_payment.user.id,
        text=await create_event_text(
            new_event,
            ['status', 'show_teams', 'payment'],
            payment_amount=new_payment.amount,
            payment_status=new_payment.status
        ),
    )

    await bot.send_message(
        chat_id=new_event.host.id,
        text=await create_event_text(
            new_event,
            ['status', 'show_teams', 'canceled_by'],
            canceled_by=f"{payment.user.full_name} @{payment.user.username}",
        ),
    )

    for team in new_event.teams:
        for participant in team.participants:
            show_data = ['status', 'show_teams', 'canceled_by']
            payment = await get_payment_by_user(participant.id, new_event.id)

            if payment.status == PaymentStatus.PAID:
                show_data += ['refund']

            await bot.send_message(
                chat_id=participant.id,
                text=await create_event_text(
                    new_event,
                    show_data,
                    canceled_by=f"{payment.user.full_name} @{payment.user.username}",
                ),
            )



@celery_app.task()
def notify_about_payment_cancel(data: dict):
    celery_event_loop.run_until_complete(notify_about_cancel_payment(data))
