from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CreateEventCallback(CallbackData, prefix="create_event"):
    action: str
    name: str
    description: str
    participants_limit: int
    teams_count: int
    payment_amount: int


defaults = {
    "name": "New Event",
    "description": "",
    "participants_limit": 0,
    "teams_count": 0,
    "payment_amount": 0,
}


class CreateEventAction:
    BACK = 'back'
    SET_NAME = 'set_name'
    SET_DESCRIPTION = 'set_description'
    SET_DATE = 'set_date'
    SET_PARTICIPANTS_LIMIT = 'set_participants_limit'
    SET_TEAMS_COUNT = 'set_teams_count'
    SET_PAYMENT_AMOUNT = 'set_payment_amount'
    CREATE = 'create'


def get_dict_from_data(callback_data: Optional[CreateEventCallback]):
    if callback_data is None:
        return defaults

    return {
        "name": callback_data.name,
        "description": callback_data.description,
        "participants_limit": callback_data.participants_limit,
        "teams_count": callback_data.teams_count,
        "payment_amount": callback_data.payment_amount,
    }


def create_event_name_keyboard(callback_data: Optional[CreateEventCallback] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=CreateEventCallback(
                
                **get_dict_from_data(callback_data), 
                action=CreateEventAction.SET_NAME
            ).pack()
        )
    )

    return builder.as_markup()


def create_event_description_keyboard(callback_data: Optional[CreateEventCallback] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=CreateEventCallback(**get_dict_from_data(callback_data),
                                              action=CreateEventAction.SET_DESCRIPTION).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=CreateEventCallback(
                **get_dict_from_data(callback_data),
                action=CreateEventAction.BACK,
            ).pack()
        )
    )

    return builder.as_markup()

def create_event_date_keyboard(callback_data: Optional[CreateEventCallback] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=CreateEventCallback(**get_dict_from_data(callback_data),
                                              action=CreateEventAction.SET_DATE).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=CreateEventCallback(
                **get_dict_from_data(callback_data),
                action=CreateEventAction.BACK,
            ).pack()
        )
    )

    return builder.as_markup()

def create_event_max_participants_keyboard(callback_data: Optional[CreateEventCallback] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    data = get_dict_from_data(callback_data)
    builder.add(
        InlineKeyboardButton(
            text="+1",
            callback_data=CreateEventCallback(
                **data | {"participants_limit": int(data.get("participants_limit", 0)) + 1},
                action=CreateEventAction.SET_PARTICIPANTS_LIMIT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="+3",
            callback_data=CreateEventCallback(
                **data | {"participants_limit": int(data.get("participants_limit", 0)) + 3},
                action=CreateEventAction.SET_PARTICIPANTS_LIMIT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="+5",
            callback_data=CreateEventCallback(
                **data | {"participants_limit": int(data.get("participants_limit", 0)) + 5},
                action=CreateEventAction.SET_PARTICIPANTS_LIMIT,
            ).pack()
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="-1",
            callback_data=CreateEventCallback(
                **data | {"participants_limit": max(int(data.get("participants_limit", 0)) - 1, 0)},
                action=CreateEventAction.SET_PARTICIPANTS_LIMIT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="-3",
            callback_data=CreateEventCallback(
                **data | {"participants_limit": max(int(data.get("participants_limit", 0)) - 3, 0)},
                action=CreateEventAction.SET_PARTICIPANTS_LIMIT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="-5",
            callback_data=CreateEventCallback(
                **data | {"participants_limit": max(int(data.get("participants_limit", 0)) - 5, 0)},
                action=CreateEventAction.SET_PARTICIPANTS_LIMIT,
            ).pack()
        )
    )
    builder.adjust(3)

    builder.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=CreateEventCallback(
                **data | {"teams_count": int(data.get("teams_count", 0))},
                action=CreateEventAction.SET_TEAMS_COUNT,
            ).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=CreateEventCallback(
                **data,
                action=CreateEventAction.BACK,
            ).pack()
        )
    )

    return builder.as_markup()


def create_event_teams_count_keyboard(callback_data: Optional[CreateEventCallback] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    data = get_dict_from_data(callback_data);
    builder.add(
        InlineKeyboardButton(
            text="+1",
            callback_data=CreateEventCallback(
                **data | {"teams_count": int(data.get("teams_count", 0)) + 1},
                action=CreateEventAction.SET_TEAMS_COUNT,
            ).pack()
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="-1",
            callback_data=CreateEventCallback(
                **data | {"teams_count": int(data.get("teams_count", 0)) - 1},
                action=CreateEventAction.SET_TEAMS_COUNT,
            ).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Далее",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0))},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=CreateEventCallback(
                **data,
                action=CreateEventAction.BACK,
            ).pack()
        )
    )

    return builder.as_markup()


def create_event_payment_amount_keyboard(callback_data: Optional[CreateEventCallback] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    data = get_dict_from_data(callback_data)
    builder.add(
        InlineKeyboardButton(
            text="+10000",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) + 10000},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="+1000",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) + 1000},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="+100",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) + 100},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="+10",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) + 10},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="+1",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) + 1},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="-10000",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) - 10000},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="-1000",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) - 1000},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="-100",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) - 100},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="-10",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) - 10},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="-1",
            callback_data=CreateEventCallback(
                **data | {"payment_amount": int(data.get("payment_amount", 0)) - 1},
                action=CreateEventAction.SET_PAYMENT_AMOUNT,
            ).pack()
        )
    )

    builder.adjust(5)

    builder.row(
        InlineKeyboardButton(
            text="Создать",
            callback_data=CreateEventCallback(
                **data,
                action=CreateEventAction.CREATE,
            ).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=CreateEventCallback(
                **data,
                action=CreateEventAction.BACK,
            ).pack()
        )
    )

    return builder.as_markup()
