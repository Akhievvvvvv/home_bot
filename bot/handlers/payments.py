from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config.settings import PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(buy_vpn_command, commands=["buy"])

async def buy_vpn_command(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"1 месяц - {PLAN_1_MONTH} ⭐", callback_data="buy_1"))
    kb.add(InlineKeyboardButton(f"2 месяца - {PLAN_2_MONTH} ⭐", callback_data="buy_2"))
    kb.add(InlineKeyboardButton(f"3 месяца - {PLAN_3_MONTH} ⭐", callback_data="buy_3"))
    kb.add(InlineKeyboardButton("❓ Инструкция по оплате", callback_data="instructions"))
    await message.answer("Выберите тариф:", reply_markup=kb)
