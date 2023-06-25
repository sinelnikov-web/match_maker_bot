from aiogram import F
from aiogram.filters import Text
from aiogram.methods import DeleteMessage
from aiogram.types import CallbackQuery, Message

from dto import UserDTO
from shared.enums import EventStatus, PaymentStatus
from tgbot.shared.db.api import get_event_by_team, get_active_teams, get_payment_by_user
from tgbot.shared.filters.event import ActiveEvent
from tgbot.shared.keyboards.invite_user import InviteCallback, cancel_invite_keyboard, LeaveCallback, \
    create_invite_keyboard
from tgbot.shared.keyboards import KeyboardManager, Keyboards
from .router import router
from ...lib.event_text import create_event_text
from ...usecases.user.invite import accept_invite, leave_from_team


@router.callback_query(InviteCallback.filter(), ActiveEvent())
async def invite_handler(call: CallbackQuery, user: UserDTO, callback_data: InviteCallback):
    await call.answer()

    if callback_data.action == 'accept':
        event = await get_event_by_team(callback_data.team)
        await accept_invite(user, callback_data.team)
        await call.message.edit_text(
            await create_event_text(event, ['show_teams', 'status']),
            reply_markup=cancel_invite_keyboard(callback_data.team)
        )
    else:
        await DeleteMessage(message_id=call.message.message_id, chat_id=call.from_user.id)


@router.callback_query(LeaveCallback.filter(), ActiveEvent())
async def invite_handler(call: CallbackQuery, user: UserDTO, callback_data: LeaveCallback):
    await call.answer()

    await leave_from_team(user, callback_data.team)
    event = await get_event_by_team(callback_data.team)
    await call.message.edit_text(
        await create_event_text(event, ['show_teams', 'status']),
        reply_markup=create_invite_keyboard(callback_data.team)
    )


@router.message(
    Text(KeyboardManager.get(Keyboards.MAIN_KEYBOARD).get_button_text("ACTIVE_EVENTS"))
)
async def show_active_events(message: Message, user: UserDTO):
    active_teams = await get_active_teams(user)
    data = ['status', 'show_teams']
    for team in active_teams:
        extended_data = []
        payment = await get_payment_by_user(user.id, team.event.id)
        if payment is not None and team.event.status == EventStatus.PAYMENT_WAIT and payment.status != PaymentStatus.PAID:
            extended_data = ['payment']
        await message.answer(
            await create_event_text(team.event, data + extended_data, payment_link=payment.url if payment else "", payment_amount=payment.amount if payment else 0),
            reply_markup=cancel_invite_keyboard(str(team.id)) if team.event.status == EventStatus.PARTICIPANTS_WAIT else None
        )