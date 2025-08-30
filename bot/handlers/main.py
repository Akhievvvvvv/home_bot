from aiogram import types, Dispatcher
from bot.config.settings import ADMIN_IDS

async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        "👑 Панель администратора:\n"
        "1. Управление пользователями\n"
        "2. Мониторинг платежей\n"
        "3. Управление VPN ключами\n"
        "4. Логи и статистика"
    )

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=["admin"])
