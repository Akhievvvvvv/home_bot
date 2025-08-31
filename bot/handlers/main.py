from aiogram import types, Dispatcher
from bot.config.settings import PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])

async def start_command(message: types.Message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Выбери действие:\n"
        "🛒 Купить VPN\n"
        "👤 Мой профиль\n"
        "📱 Моя конфигурация\n"
        "🎁 Реферальная программа\n"
        "❓ Помощь\n"
        "💬 Поддержка"
    )
    await message.answer(text)
