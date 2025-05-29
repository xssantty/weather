from aiogram.filters import BaseFilter
from aiogram.types import Message

class LengthFilter(BaseFilter):
    def __init__(self, min_len: int = 1, max_len: int = 100):
        self.min_len = min_len
        self.max_len = max_len

    async def __call__(self, message: Message) -> bool:
        length = len(message.text or "")
        return self.min_len <= length <= self.max_len
