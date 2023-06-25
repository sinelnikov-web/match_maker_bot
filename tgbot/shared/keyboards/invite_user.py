from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InviteCallback(CallbackData, prefix="invite"):
    action: str
    team: str


class LeaveCallback(CallbackData, prefix="leave"):
    action: str
    team: str


def create_invite_keyboard(team_id: str):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="Принять",
            callback_data=InviteCallback(action='accept', team=team_id).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Отклонить",
            callback_data=InviteCallback(action='decline', team=team_id).pack()
        )
    )

    return builder.as_markup()


def cancel_invite_keyboard(team_id: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Выйти",
            callback_data=LeaveCallback(action='decline', team=team_id).pack()
        )
    )

    return builder.as_markup()
