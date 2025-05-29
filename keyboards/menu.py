from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales.loader import get_text
from storage.user_data import get_favorites

def main_menu_keyboard(context=None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🌤 {get_text('menu_weather', context)}", callback_data="menu_weather")],
        [InlineKeyboardButton(text=f"⭐ {get_text('menu_favorites', context)}", callback_data="menu_favorites")],
        [InlineKeyboardButton(text=f"🌐 {get_text('menu_language', context)}", callback_data="menu_language")],
        [InlineKeyboardButton(text=f"ℹ️ {get_text('menu_help', context)}", callback_data="menu_help")]
    ])

def favorites_keyboard(user_id: int) -> InlineKeyboardMarkup:
    favorites = get_favorites(user_id)
    if not favorites:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Нет избранных", callback_data="none")]
        ])
    buttons = [
        [InlineKeyboardButton(text=f"❌ {city}", callback_data=f"remove_fav:{city}")]
        for city in favorites
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
