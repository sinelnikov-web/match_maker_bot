from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class HostEventCallback(CallbackData, prefix='host_event'):
    action: str
    event_id: int


def approve_event_keyboard(event_id, accept=True):
    builder = InlineKeyboardBuilder()

    accept_row = []

    if accept:
        accept_row.append(
            InlineKeyboardButton(
                text="Утвердить",
                callback_data=HostEventCallback(action='accept', event_id=event_id).pack()
            )
        )

    accept_row.append(
        InlineKeyboardButton(
            text="Отменить",
            callback_data=HostEventCallback(action='decline', event_id=event_id).pack()
        ),
    )

    builder.row(*accept_row)

    builder.row(
        InlineKeyboardButton(
            text="Обновить",
            callback_data=HostEventCallback(action='refresh', event_id=event_id).pack()
        ),
    )

    return builder.as_markup()
