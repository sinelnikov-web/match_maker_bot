import datetime

from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.methods import DeleteMessage
from aiogram.types import Message, CallbackQuery

from dto import UserDTO
from dto.event import EventDTO, TeamDTO
from tgbot.shared.db.api import create_event_model
from tgbot.shared.keyboards import KeyboardManager, Keyboards
from tgbot.shared.keyboards.create_event import create_event_name_keyboard, CreateEventCallback, CreateEventAction, \
    create_event_description_keyboard, create_event_max_participants_keyboard, create_event_teams_count_keyboard, \
    create_event_payment_amount_keyboard, create_event_date_keyboard
from tgbot.shared.keyboards.start_event import approve_event_keyboard
from .router import router
from ...lib.event_text import create_event_text
from ...states.create_event import CreateEventState
from ...usecases.user.create_event import start_create_event

def get_keyboard_by_state(state):
    kb_dict = {
        "name": create_event_name_keyboard,
        "description": create_event_description_keyboard,
        "date": create_event_date_keyboard,
        "participants_limit": create_event_max_participants_keyboard,
        "teams_count": create_event_teams_count_keyboard,
        "payment_amount": create_event_payment_amount_keyboard,
    }

    return kb_dict.get(state)

def get_prev_state(state):
    states_dict = {
        "description": "name",
        "date": "description",
        "participants_limit": "date",
        "teams_count": "participants_limit",
        "payment_amount": "teams_count",
    }

    return states_dict.get(state)


@router.message(Text(
    KeyboardManager.get(Keyboards.MAIN_KEYBOARD).get_button_text("CREATE_EVENT")
))
async def create_event(message: Message, user: UserDTO, state: FSMContext):
    await start_create_event(message, user, state)


@router.callback_query(CreateEventCallback.filter(F.action == 'back'))
async def back_handler(call: CallbackQuery, user: UserDTO, state: FSMContext, callback_data: CreateEventCallback):
    await call.answer()

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    prev_state = get_prev_state(data.get('state'))

    await call.message.edit_text(await create_event_text(event, [prev_state]), reply_markup=get_keyboard_by_state(prev_state)(callback_data))

    await state.update_data({
        "event": event.to_json(),
        "state": prev_state
    })


@router.message(CreateEventState.name)
async def input_name(message: Message, user: UserDTO, state: FSMContext):
    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    message_id = data.get("event_msg_id")

    event.name = message.text
    event_msg = await message.answer(await create_event_text(event, ['name']), reply_markup=create_event_name_keyboard())

    await DeleteMessage(message_id=message_id, chat_id=message.from_user.id)

    await state.update_data({
        "event": event.to_json(),
        "event_msg_id": event_msg.message_id,
        "state": "name"
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.SET_NAME))
async def set_name(call: CallbackQuery, user: UserDTO, state: FSMContext, callback_data: CreateEventCallback):
    await call.answer()
    await state.set_state(CreateEventState.description)

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))

    await call.message.edit_text(await create_event_text(event, ['description']),
                                 reply_markup=create_event_description_keyboard(callback_data))

    await state.update_data({
        "state": "description",
    })


@router.message(CreateEventState.description)
async def input_description(message: Message, user: UserDTO, state: FSMContext):
    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    message_id = data.get("event_msg_id")

    event.description = message.text
    event_msg = await message.answer(await create_event_text(event, ['description']),
                                     reply_markup=create_event_description_keyboard())

    await DeleteMessage(message_id=message_id, chat_id=message.from_user.id)

    await state.update_data({
        "event": event.to_json(),
        "event_msg_id": event_msg.message_id,
        "state": "description",
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.SET_DESCRIPTION))
async def set_description(call: CallbackQuery, user: UserDTO, state: FSMContext, callback_data: CreateEventCallback):
    await call.answer()
    await state.set_state(CreateEventState.date)

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))

    await call.message.edit_text(await create_event_text(event, ['date']),
                                 reply_markup=create_event_date_keyboard(callback_data))

    await state.update_data({
        "state": "date"
    })


@router.message(CreateEventState.date)
async def input_date(message: Message, user: UserDTO, state: FSMContext):
    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    message_id = data.get("event_msg_id")

    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except:
        await message.answer("Неверный формат даты!")
        return

    event.date = message.text
    event_msg = await message.answer(await create_event_text(event, ['date']), reply_markup=create_event_date_keyboard())

    await DeleteMessage(message_id=message_id, chat_id=message.from_user.id)

    await state.update_data({
        "event": event.to_json(),
        "event_msg_id": event_msg.message_id,
        "state": "date"
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.SET_DATE))
async def set_description(call: CallbackQuery, user: UserDTO, state: FSMContext, callback_data: CreateEventCallback):
    await call.answer()
    await state.set_state(CreateEventState.date)

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))

    await call.message.edit_text(await create_event_text(event, ['participants_limit']),
                                 reply_markup=create_event_max_participants_keyboard(callback_data))

    await state.update_data({
        "state": "participants_limit"
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.SET_PARTICIPANTS_LIMIT))
async def change_participants_limit(call: CallbackQuery, user: UserDTO, state: FSMContext,
                                    callback_data: CreateEventCallback):
    await call.answer()
    await state.set_state(CreateEventState.other)

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    event.max_participants = callback_data.participants_limit

    await call.message.edit_text(await create_event_text(event, ['participants_limit']),
                                 reply_markup=create_event_max_participants_keyboard(callback_data))

    await state.update_data({
        "event": event.to_json(),
        "state": "participants_limit"
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.SET_TEAMS_COUNT))
async def set_teams_count(call: CallbackQuery, user: UserDTO, state: FSMContext, callback_data: CreateEventCallback):
    await call.answer()

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    event.teams = [TeamDTO(id=i, event=None, participants=[]) for i in range(callback_data.teams_count)]

    await call.message.edit_text(await create_event_text(event, ['teams_count']),
                                 reply_markup=create_event_teams_count_keyboard(callback_data))

    await state.update_data({
        "event": event.to_json(),
        "state": "teams_count"
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.SET_PAYMENT_AMOUNT))
async def set_teams_count(call: CallbackQuery, user: UserDTO, state: FSMContext, callback_data: CreateEventCallback):
    await call.answer()

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))
    event.amount = callback_data.payment_amount

    await call.message.edit_text(await create_event_text(event, ['payment_amount']),
                                 reply_markup=create_event_payment_amount_keyboard(callback_data))

    await state.update_data({
        "event": event.to_json(),
        "state": "payment_amount"
    })


@router.callback_query(CreateEventCallback.filter(F.action == CreateEventAction.CREATE))
async def create(call: CallbackQuery, user: UserDTO, state: FSMContext):
    await call.answer()

    data = await state.get_data()
    event = EventDTO.from_json(data.get("event"))

    new_event = await create_event_model(user, event)

    await call.message.edit_text(await create_event_text(new_event, ['links', 'show_teams', 'status']),
                                 reply_markup=approve_event_keyboard(new_event.id))

    await state.clear()
