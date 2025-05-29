from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config.settings import settings
from states.admin_states import AdminStates
from storage.user_data import get_all_users, ban_user
from locales.loader import get_text

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in settings.ADMINS:
        await message.answer(get_text("no_access", message))
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("admin_stats", message), callback_data="admin_stats")],
        [InlineKeyboardButton(text=get_text("admin_broadcast", message), callback_data="admin_broadcast")],
        [InlineKeyboardButton(text=get_text("admin_ban", message), callback_data="admin_ban")]
    ])
    await message.answer(get_text("admin_welcome", message), reply_markup=kb)

@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    if callback.from_user.id not in settings.ADMINS:
        await callback.answer(get_text("no_access", callback), show_alert=True)
        return
    count = len(get_all_users())
    await callback.message.answer(f"👥 {count}")
    await callback.answer()

@router.callback_query(F.data == "admin_broadcast")
async def ask_broadcast(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in settings.ADMINS:
        await callback.answer(get_text("no_access", callback), show_alert=True)
        return
    await callback.message.answer(get_text("admin_enter_broadcast", callback))
    await state.set_state(AdminStates.waiting_for_broadcast_text)
    await callback.answer()

@router.message(AdminStates.waiting_for_broadcast_text)
async def do_broadcast(message: Message, state: FSMContext):
    text = message.text
    count = 0
    for uid in get_all_users():
        try:
            await message.bot.send_message(uid, text)
            count += 1
        except:
            continue
    await message.answer(get_text("admin_broadcast_done", message).format(count=count))
    await state.clear()

@router.callback_query(F.data == "admin_ban")
async def ask_ban(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in settings.ADMINS:
        await callback.answer(get_text("no_access", callback), show_alert=True)
        return
    await callback.message.answer(get_text("admin_enter_ban_id", callback))
    await state.set_state(AdminStates.waiting_for_ban_id)
    await callback.answer()

@router.message(AdminStates.waiting_for_ban_id)
async def do_ban(message: Message, state: FSMContext):
    try:
        uid = int(message.text.strip())
        ban_user(uid)
        await message.answer(get_text("admin_ban_success", message).format(uid=uid))
    except:
        await message.answer(get_text("admin_ban_invalid", message))
    await state.clear()
