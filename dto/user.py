from __future__ import annotations
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from shared.enums import LanguageCode


@dataclass_json
@dataclass
class UserDTO:
    id: int
    username: str
    full_name: str
    phone: str
    email: str
    language: LanguageCode
