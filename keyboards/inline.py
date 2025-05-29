from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def weather_inline(city: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_{city}")
        ]]
    )
