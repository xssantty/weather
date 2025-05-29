from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.weather_states import WeatherStates
from services.api_client import WeatherAPI
from utils.formatters import format_weather
from keyboards.menu import main_menu_keyboard, favorites_keyboard
from locales.loader import get_text
from storage.user_data import (
    add_user,
    add_favorite,
    remove_favorite,
    set_language,
    get_language
)

router = Router()
api = WeatherAPI()

@router.message(Command("start"))
async def start(message: Message):
    add_user(message.from_user.id)
    await message.answer(get_text("start", message), reply_markup=main_menu_keyboard(message))

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(get_text("help", message))

@router.message(Command("language"))
async def language_cmd(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
        ]
    )
    await message.answer(get_text("choose_language", message), reply_markup=kb)

@router.callback_query(F.data == "menu_language")
async def cb_lang(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
        ]
    )
    await callback.message.answer(get_text("choose_language", callback), reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    set_language(callback.from_user.id, lang)
    await callback.message.answer(get_text("language_updated", callback))
    await callback.message.answer(get_text("start", callback), reply_markup=main_menu_keyboard(callback))
    await callback.answer()

@router.message(Command("weather"))
async def weather_cmd(message: Message, state: FSMContext):
    await message.answer(get_text("enter_city", message))
    await state.set_state(WeatherStates.waiting_for_city)

@router.message(WeatherStates.waiting_for_city)
async def handle_city(message: Message, state: FSMContext):
    city = message.text.strip()
    try:
        lang = get_language(message.from_user.id)
        data = await api.get_weather(city, lang=lang)
        add_favorite(message.from_user.id, city)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🔄 {get_text('refresh', message)}", callback_data=f"refresh_{city}")],
            [InlineKeyboardButton(text=f"🔙 {get_text('back', message)}", callback_data="back_to_menu")]
        ])
        await message.answer(format_weather(data, lang), reply_markup=kb)
    except Exception as e:
        await message.answer(str(e))
    await state.clear()

@router.callback_query(F.data.startswith("refresh_"))
async def refresh_weather(callback: CallbackQuery):
    city = callback.data.replace("refresh_", "")
    try:
        lang = get_language(callback.from_user.id)
        data = await api.get_weather(city, lang=lang, force_refresh=True)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🔄 {get_text('refresh', callback)}", callback_data=f"refresh_{city}")],
            [InlineKeyboardButton(text=f"🔙 {get_text('back', callback)}", callback_data="back_to_menu")]
        ])
        await callback.message.edit_text(format_weather(data, lang), reply_markup=kb)
        await callback.answer(get_text("updated", callback))
    except Exception:
        await callback.answer(get_text("error_refresh", callback), show_alert=True)

@router.callback_query(F.data == "menu_weather")
async def cb_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(get_text("enter_city", callback))
    await state.set_state(WeatherStates.waiting_for_city)
    await callback.answer()

@router.callback_query(F.data == "menu_help")
async def cb_help(callback: CallbackQuery):
    await callback.message.answer(get_text("help", callback))
    await callback.answer()

@router.callback_query(F.data == "menu_favorites")
async def cb_favorites(callback: CallbackQuery):
    await callback.message.answer(get_text("favorites_title", callback), reply_markup=favorites_keyboard(callback.from_user.id, callback))
    await callback.answer()

@router.callback_query(F.data.startswith("remove_fav:"))
async def cb_remove_favorite(callback: CallbackQuery):
    city = callback.data.split(":")[1]
    remove_favorite(callback.from_user.id, city)
    await callback.message.edit_reply_markup(reply_markup=favorites_keyboard(callback.from_user.id, callback))
    await callback.answer(get_text("favorite_removed", callback).format(city=city))

@router.callback_query(F.data == "back_to_menu")
async def cb_back_to_menu(callback: CallbackQuery):
    await callback.message.answer(get_text("back_to_menu", callback), reply_markup=main_menu_keyboard(callback))
    await callback.answer()
