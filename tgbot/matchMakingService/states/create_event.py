from aiogram.fsm.state import StatesGroup, State


class CreateEventState(StatesGroup):
    name = State()
    description = State()
    date = State()
    other = State()

