import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config.settings import (
    BOT_TOKEN,
    PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH,
    REFERRAL_BONUS_PERCENT, REFERRAL_MIN_PAYOUT,
)
from bot.locales.ru import START_MESSAGE, MAIN_MENU
from bot.handlers import payments, admin

# -------------------- Логирование --------------------
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# -------------------- Главное меню --------------------
def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=MAIN_MENU["buy_vpn"], callback_data="buy_vpn")],
        [InlineKeyboardButton(text=MAIN_MENU["my_profile"], callback_data="my_profile")],
        [InlineKeyboardButton(text=MAIN_MENU["my_config"], callback_data="my_config")],
        [InlineKeyboardButton(text=MAIN_MENU["referral"], callback_data="referral")],
        [InlineKeyboardButton(text=MAIN_MENU["help"], callback_data="help")],
        [InlineKeyboardButton(text=MAIN_MENU["support"], callback_data="support")],
    ])

# -------------------- /start --------------------
@dp.message(CommandStart())
async def start_handler(message):
    await message.answer(
        START_MESSAGE.format(username=message.from_user.username or message.from_user.id),
        reply_markup=main_menu_kb()
    )

# -------------------- Подключение роутеров --------------------
def register_all_routers():
    dp.include_router(payments.router)
    dp.include_router(admin.admin_router)

# -------------------- Запуск бота --------------------
async def main():
    register_all_routers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
