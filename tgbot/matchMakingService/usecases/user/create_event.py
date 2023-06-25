import dataclasses

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from dto import UserDTO
from dto.event import EventDTO
from tgbot.matchMakingService.lib.event_text import create_event_text
from tgbot.matchMakingService.states.create_event import CreateEventState
from tgbot.shared.keyboards.create_event import create_event_name_keyboard


async def start_create_event(msg: Message, user: UserDTO, state: FSMContext):
    new_event = EventDTO(name="New Event", host=user)
    await state.set_state(CreateEventState.name)
    event_msg = await msg.answer(await create_event_text(new_event, 'name'), reply_markup=create_event_name_keyboard())
    await state.update_data({
        "event": new_event.to_json(),
        "event_msg_id": event_msg.message_id,
        "state": "name"
    })