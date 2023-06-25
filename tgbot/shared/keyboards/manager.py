import os
import re

import django
from aiogram.filters.callback_data import CallbackData


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ektu_bot_v2.settings")
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


setup_django()

from typing import Dict, Any

from interface import Interface, implements

from telegram.models import Keyboard as KeyboardModel
from tgbot.shared.enums import KeyboardType
from tgbot.shared.keyboards import Keyboard


class IKeyboardProvider(Interface):

    @staticmethod
    def raw_data() -> Dict[str, Any]:
        pass


class DatabaseKeyboardProvider(implements(IKeyboardProvider)):

    @staticmethod
    def raw_data() -> Dict[str, Any]:
        keyboards = KeyboardModel.objects.all()
        raw_keyboards = {}

        for keyboard in keyboards:
            raw_keyboard = {
                "key": keyboard.key,
                "type": keyboard.type,
                "buttons": {}
            }
            if keyboard.type == KeyboardType.REPLY:
                buttons = keyboard.reply_buttons.filter(hidden=False)
            else:
                buttons = keyboard.inline_buttons.filter(hidden=False)
            for button in buttons:
                button_raw = {
                    "text_ru": button.text_ru,
                    "text_kz": button.text_kz,
                }
                if keyboard.type == KeyboardType.REPLY:
                    button_raw['request_location'] = button.request_location
                    button_raw['request_contact'] = button.request_contact
                else:
                    button_raw['url_ru'] = button.url_ru
                    button_raw['url_kz'] = button.url_kz
                    button_raw['callback_data'] = button.callback_data
                    if button.callback_data is not None:
                        prefix = button.callback_data.split(":")[0]
                        callback_args = {key: "None" for key in
                                         re.findall(r'\{(\w+)}', button.callback_data)}
                        CallbackDataClass = type(
                            "DynamicCallbackData",
                            (CallbackData,),
                            callback_args,
                            prefix=prefix
                        )
                        button_raw['CallbackData'] = CallbackDataClass
                raw_keyboard.get('buttons')[button.key] = button_raw
            raw_keyboards[keyboard.key] = raw_keyboard
        return raw_keyboards


class KeyboardManager:
    provider: IKeyboardProvider = DatabaseKeyboardProvider
    raw_keyboards: Dict[str, Any]

    def __init__(self, keyboard_provider: IKeyboardProvider = None):
        if keyboard_provider:
            self.provider = keyboard_provider
        self.raw_keyboards = self.provider.raw_data()

    def get(self, key: str) -> Keyboard:
        return Keyboard(self.raw_keyboards[key])

    def get_callback(self, key: str, button_key) -> CallbackData:
        return self.raw_keyboards[key]["buttons"].get(button_key).get("CallbackData")

    def reinitialize(self):
        self.raw_keyboards = self.provider.raw_data()


km = KeyboardManager()
