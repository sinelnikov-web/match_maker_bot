from aiogram.types import CallbackQuery

from dto import UserDTO
from sport_events.tasks import send_payment_requests, send_refund
from tgbot.shared.db.api import get_event_by_team, get_event
from tgbot.shared.keyboards.start_event import HostEventCallback, approve_event_keyboard
from .router import router
from ...lib.event_text import create_event_text
from ...usecases.user.approve_event import approve_event, decline_event


@router.callback_query(HostEventCallback.filter())
async def host_handler(call: CallbackQuery, user: UserDTO, callback_data: HostEventCallback):
    await call.answer()

    if callback_data.action == 'refresh':
        event = await get_event(callback_data.event_id)
        await call.message.edit_text(
            await create_event_text(event, ['show_teams', 'links', 'status']),
            reply_markup=approve_event_keyboard(callback_data.event_id)
        )
    elif callback_data.action == 'accept':
        # TODO: notify all users
        new_event = await approve_event(event=await get_event(callback_data.event_id))
        send_payment_requests.delay(new_event.id)
        await call.message.edit_text(
            await create_event_text(new_event, ['show_teams', 'status']),
            reply_markup=approve_event_keyboard(callback_data.event_id)
        )
    else:
        # TODO: refund money
        new_event = await decline_event(event=await get_event(callback_data.event_id))
        send_refund.delay(new_event.id)
        await call.message.edit_text(
            await create_event_text(new_event, ['show_teams', 'status']),
        )
