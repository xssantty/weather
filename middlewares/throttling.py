from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import asyncio

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 1.0):
        super().__init__()
        self.limit = limit
        self.user_times = {}

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user_id = getattr(event.from_user, "id", None)
        if user_id is None:
            return await handler(event, data)

        now = asyncio.get_event_loop().time()
        last_time = self.user_times.get(user_id, 0)

        if now - last_time < self.limit:
            return  # игнорируем спам
        self.user_times[user_id] = now

        return await handler(event, data)
