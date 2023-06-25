from enum import Enum


class Keyboards(str, Enum):
    MAIN_KEYBOARD = "MAIN_KEYBOARD"
    AUTH_KEYBOARD = "AUTH_KEYBOARD"
    
    def __str__(self) -> str:
        return str.__str__(self)
