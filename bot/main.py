# bot/main.py
import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

from bot.config.settings import (
    BOT_TOKEN,
    PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH,
    REFERRAL_BONUS_PERCENT, REFERRAL_MIN_PAYOUT,
)
from bot.locales.ru import START_MESSAGE, MAIN_MENU, PAYMENT_MESSAGES, BUTTONS
from bot.utils.vpn import generate_ovpn
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
async def start_handler(message: types.Message):
    await message.answer(
        START_MESSAGE.format(username=message.from_user.username or message.from_user.id),
        reply_markup=main_menu_kb()
    )

# -------------------- Основные callback кнопки --------------------
async def buy_vpn_handler(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"1 месяц — {PLAN_1_MONTH} ⭐", callback_data="buy_1")],
        [InlineKeyboardButton(text=f"2 месяца — {PLAN_2_MONTH} ⭐", callback_data="buy_2")],
        [InlineKeyboardButton(text=f"3 месяца — {PLAN_3_MONTH} ⭐", callback_data="buy_3")],
    ])
    await call.message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)
    await call.answer()


async def profile_handler(call: types.CallbackQuery):
    await call.message.answer(
        f"👤 Профиль пользователя {call.from_user.username or call.from_user.id}\n"
        f"Подписка: 1 месяц\n"
        f"Дата окончания: 01.10.2025\n"
        f"Рефералы: 5\n"
        f"Оплачено рефералами: 2\n"
    )
    await call.answer()


async def config_handler(call: types.CallbackQuery):
    try:
        ovpn_file = generate_ovpn(str(call.from_user.id))
        with open(ovpn_file, "rb") as file:
            await call.message.answer_document(file, caption="📎 Ваша VPN-конфигурация")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка получения конфига: {e}")
    await call.answer()


async def referral_handler(call: types.CallbackQuery):
    bot_info = await bot.me()
    referral_link = f"https://t.me/{bot_info.username}?start={call.from_user.id}"
    await call.message.answer(
        f"🎁 Реферальная система\n\n"
        f"Приглашайте друзей и получайте {REFERRAL_BONUS_PERCENT}% от их оплаты ⭐.\n"
        f"Минимальная выплата: {REFERRAL_MIN_PAYOUT} ⭐\n\n"
        f"Ваша ссылка:\n{referral_link}"
    )
    await call.answer()


async def help_handler(call: types.CallbackQuery):
    await call.message.answer("ℹ️ Здесь будет подробная инструкция и FAQ.")
    await call.answer()


async def support_handler(call: types.CallbackQuery):
    await call.message.answer("👨‍💻 Поддержка: @YourSupportUsername")
    await call.answer()

# -------------------- Регистрация callback --------------------
def register_callbacks(dp: Dispatcher):
    dp.callback_query.register(buy_vpn_handler, F.data == "buy_vpn")
    dp.callback_query.register(profile_handler, F.data == "my_profile")
    dp.callback_query.register(config_handler, F.data == "my_config")
    dp.callback_query.register(referral_handler, F.data == "referral")
    dp.callback_query.register(help_handler, F.data == "help")
    dp.callback_query.register(support_handler, F.data == "support")

# -------------------- Подключение дополнительных роутеров --------------------
def register_all_handlers():
    register_callbacks(dp)
    dp.include_router(payments.router)
    dp.include_router(admin.admin_router)

# -------------------- Запуск --------------------
async def main():
    register_all_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
