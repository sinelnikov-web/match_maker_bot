from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class MessageTextDTO:
    text_ru: str
    text_kz: str
    key: str
