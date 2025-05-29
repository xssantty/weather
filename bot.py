import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher
from config.settings import settings
from routers.handlers.main import router as main_router
from routers.handlers.admin import router as admin_router
from middlewares.throttling import ThrottlingMiddleware
from utils.logger import setup_logger

setup_logger()

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
dp.message.middleware(ThrottlingMiddleware())

dp.include_router(main_router)
dp.include_router(admin_router)

async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())

