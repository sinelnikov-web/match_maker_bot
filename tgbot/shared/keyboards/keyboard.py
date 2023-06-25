import re
from typing import List, Dict, Any, Union, Type

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from shared.enums import LanguageCode
from tgbot.shared.enums import KeyboardType


class Keyboard:
    raw_keyboard: Dict[str, Any] = {}
    is_reply: bool = False

    def __init__(self, raw_keyboard: dict):
        self.raw_keyboard = raw_keyboard
        self.is_reply = self.raw_keyboard.get('type') == KeyboardType.REPLY

    def generate_keyboard(self, lang: LanguageCode = LanguageCode.RU, adjust=1, callback_data: dict = {}, **kwargs: Dict[str, Any]) -> Union[
        ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        raw_keyboard = self.raw_keyboard
        buttons = raw_keyboard.get('buttons')
        keyboard = self._get_keyboard_instance()
        button_constructor = self._get_button_constructor()
        buttons_keys = raw_keyboard.get('buttons').keys()

        for button_key in buttons_keys:
            data = buttons[button_key].copy()
            for key in data.keys():
                if key == 'callback_data' and type(data[key]) == str:
                    callback_args = {key: callback_data
                        .get(button_key, {})
                        .get(key, "None") for key in re.findall(r'\{(\w+)}', data[key])
                    }
                    data[key] = data[key].format(**callback_args)
                elif type(data[key]) == str:
                    data[key] = data[key].format(**kwargs)
            button = self._create_button(button_constructor, data, lang)
            keyboard.add(button)
            keyboard.adjust(adjust)

        markup = keyboard.as_markup()
        markup.resize_keyboard = True
        return markup

    def _create_button(self, constructor: Union[Type[InlineKeyboardButton], Type[KeyboardButton]], data: Dict[str, Any],
                       lang: LanguageCode):
        reply_button_kwargs = ('request_contact', 'request_location')
        inline_button_kwargs = ('url:lang', 'callback_data')
        current_kwargs = reply_button_kwargs if self.is_reply else inline_button_kwargs
        text = data.get(f'text_{lang.value}')
        config = {}
        for kwarg in current_kwargs:
            if len(kwarg.split(':')) == 2:
                key, _ = kwarg.split(':')
                data_key = f'{key}_{lang.value}'
                value = data[data_key] if data.get(data_key) is not None else data[f'{key}_ru']
                config[key] = value
                continue
            config[kwarg] = data[kwarg]

        return constructor(
            text=text if text is not None else data.get('text_ru'),
            **config
        )

    def _get_keyboard_instance(self) -> Union[ReplyKeyboardBuilder, InlineKeyboardBuilder]:
        return ReplyKeyboardBuilder() if self.is_reply else InlineKeyboardBuilder()

    def _get_button_constructor(self) -> Union[Type[InlineKeyboardButton], Type[KeyboardButton]]:
        return KeyboardButton if self.is_reply else InlineKeyboardButton

    def get_button_text(self, key: str) -> List[str]:
        translations: List[str] = []

        btn = self.raw_keyboard['buttons'].get(key)
        if btn is None:
            raise Exception(f'Button with key {key} not found!')

        translations.append(btn['text_ru'])

        if btn.get('text_kz') is not None:
            translations.append(btn.get('text_kz'))
        return translations
