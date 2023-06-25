from dto.message import MessageTextDTO
from shared.enums import LanguageCode
from shared.utils import create_dto
from telegram.models import MessageText


class MessageStorageService:

    @staticmethod
    async def get(key: str) -> MessageTextDTO:
        message_text_model = await MessageText.objects.aget(key=key)
        return create_dto(message_text_model, MessageTextDTO)

    @staticmethod
    async def get_text(key: str, lang: LanguageCode) -> str:
        message = await MessageStorageService.get(key)
        text = getattr(message, f'text_{lang.value}')
        if len(text.strip()) > 0:
            return text
        else:
            return message.text_ru