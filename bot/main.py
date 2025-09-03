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
from bot.locales.ru import START_MESSAGE, MAIN_MENU, PAYMENT_MESSAGES, BUTTONS, CONFIG_MESSAGES
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


# -------------------- Покупка VPN --------------------
@dp.callback_query(F.data == "buy_vpn")
async def buy_vpn_handler(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"1 месяц — {PLAN_1_MONTH} ⭐", callback_data="buy_1")],
        [InlineKeyboardButton(text=f"2 месяца — {PLAN_2_MONTH} ⭐", callback_data="buy_2")],
        [InlineKeyboardButton(text=f"3 месяца — {PLAN_3_MONTH} ⭐", callback_data="buy_3")],
    ])
    await call.message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)
    await call.answer()


@dp.callback_query(F.data.startswith("buy_"))
async def handle_payment(call: types.CallbackQuery):
    month_map = {
        "buy_1": ("1", PLAN_1_MONTH),
        "buy_2": ("2", PLAN_2_MONTH),
        "buy_3": ("3", PLAN_3_MONTH),
    }
    month, stars = month_map[call.data]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTONS["paid"], callback_data=f"paid_{month}")]
    ])

    await call.message.answer(
        f"⭐ Вы выбрали тариф на {month} месяц(-ев) за {stars} ⭐\n\n"
        f"{PAYMENT_MESSAGES['payment_instructions']}",
        reply_markup=kb
    )
    await call.answer()


@dp.callback_query(F.data.startswith("paid_"))
async def paid_handler(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    month = call.data.split("_")[1]

    try:
        ovpn_file = generate_ovpn(user_id)

        await call.message.answer(
            f"✅ Оплата подтверждена!\nВаш VPN готов.\n\n"
            f"Инструкция по подключению:\n"
            f"1️⃣ Установите OpenVPN клиент.\n"
            f"2️⃣ Импортируйте .ovpn файл.\n"
            f"3️⃣ Подключитесь к VPN.\n\n"
            f"🌐 Теперь вы онлайн безопасно и анонимно!"
        )

        with open(ovpn_file, "rb") as file:
            await call.message.answer_document(file, caption="📎 Ваш .ovpn файл")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка генерации конфигурации: {e}")

    await call.answer()


# -------------------- Профиль --------------------
@dp.callback_query(F.data == "my_profile")
async def profile_handler(call: types.CallbackQuery):
    await call.message.answer(
        f"👤 Профиль пользователя {call.from_user.username or call.from_user.id}\n"
        f"Подписка: 1 месяц\n"
        f"Дата окончания: 01.10.2025\n"
        f"Рефералы: 5\n"
        f"Оплачено рефералами: 2\n"
    )
    await call.answer()


# -------------------- Конфиг --------------------
@dp.callback_query(F.data == "my_config")
async def config_handler(call: types.CallbackQuery):
    try:
        ovpn_file = generate_ovpn(str(call.from_user.id))
        with open(ovpn_file, "rb") as file:
            await call.message.answer_document(file, caption="📎 Ваша VPN-конфигурация")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка получения конфига: {e}")
    await call.answer()


# -------------------- Реферальная система --------------------
@dp.callback_query(F.data == "referral")
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


# -------------------- Help / Support --------------------
@dp.callback_query(F.data == "help")
async def help_handler(call: types.CallbackQuery):
    await call.message.answer("ℹ️ Здесь будет подробная инструкция и FAQ.")
    await call.answer()


@dp.callback_query(F.data == "support")
async def support_handler(call: types.CallbackQuery):
    await call.message.answer("👨‍💻 Поддержка: @YourSupportUsername")
    await call.answer()


# -------------------- Регистрация дополнительных хэндлеров --------------------
def register_all_handlers():
    payments.register_handlers(dp)
    admin.register_handlers(dp)


# -------------------- Запуск бота --------------------
async def main():
    register_all_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
