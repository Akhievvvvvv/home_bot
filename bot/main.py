# bot/main.py
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from bot.config.settings import BOT_TOKEN, ADMIN_IDS, PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH, VPN_CLIENTS_DIR
from bot.locales.ru import START_MESSAGE, MAIN_MENU, PAYMENT_MESSAGES, BUTTONS, CONFIG_MESSAGES
from bot.utils.vpn import generate_ovpn

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# -------------------- Главное меню --------------------
def main_menu_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(MAIN_MENU["buy_vpn"], callback_data="buy_vpn"),
        InlineKeyboardButton(MAIN_MENU["my_profile"], callback_data="my_profile"),
        InlineKeyboardButton(MAIN_MENU["my_config"], callback_data="my_config"),
        InlineKeyboardButton(MAIN_MENU["referral"], callback_data="referral"),
        InlineKeyboardButton(MAIN_MENU["help"], callback_data="help"),
        InlineKeyboardButton(MAIN_MENU["support"], callback_data="support")
    )
    return kb

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(START_MESSAGE.format(username=message.from_user.username), reply_markup=main_menu_kb())

# -------------------- Обработка кнопок --------------------
@dp.callback_query_handler(lambda c: c.data == "buy_vpn")
async def buy_vpn_handler(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(f"1 месяц — {PLAN_1_MONTH} ⭐", callback_data="buy_1"),
        InlineKeyboardButton(f"2 месяца — {PLAN_2_MONTH} ⭐", callback_data="buy_2"),
        InlineKeyboardButton(f"3 месяца — {PLAN_3_MONTH} ⭐", callback_data="buy_3"),
    )
    await call.message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def handle_payment(call: types.CallbackQuery):
    month_map = {"buy_1": PLAN_1_MONTH, "buy_2": PLAN_2_MONTH, "buy_3": PLAN_3_MONTH}
    month = call.data.split("_")[1]
    stars = month_map[call.data]
    
    # Кнопка "Оплатил(а)"
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(BUTTONS["paid"], callback_data=f"paid_{month}"))
    
    await call.message.answer(
        f"⭐ Вы выбрали тариф на {month} месяц(-ев) за {stars} ⭐\n\n"
        f"{PAYMENT_MESSAGES['payment_instructions']}",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith("paid_"))
async def paid_handler(call: types.CallbackQuery):
    month = call.data.split("_")[1]
    user_id = call.from_user.id
    
    # Генерация VPN .ovpn
    ovpn_file = generate_ovpn(str(user_id))
    
    await call.message.answer(
        f"✅ Оплата подтверждена!\nВаш VPN готов.\n\n"
        f"Файл конфигурации: {ovpn_file}\n\n"
        f"Инструкция по подключению:\n"
        f"1️⃣ Установите OpenVPN клиент.\n"
        f"2️⃣ Импортируйте .ovpn файл.\n"
        f"3️⃣ Подключитесь к VPN.\n"
        f"🌐 Теперь вы онлайн безопасно и анонимно!"
    )

# -------------------- Мой профиль --------------------
@dp.callback_query_handler(lambda c: c.data == "my_profile")
async def profile_handler(call: types.CallbackQuery):
    # Здесь должна быть интеграция с базой данных
    # Для примера покажем статическую информацию
    await call.message.answer(
        f"👤 Профиль пользователя {call.from_user.username}\n"
        f"Подписка: 1 месяц\n"
        f"Дата окончания: 01.10.2025\n"
        f"Рефералы: 5\n"
        f"Оплачено рефералами: 2\n"
    )

# -------------------- Моя конфигурация --------------------
@dp.callback_query_handler(lambda c: c.data == "my_config")
async def config_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    # Генерация VPN конфигурации
    ovpn_file = generate_ovpn(str(user_id))
    await call.message.answer(
        CONFIG_MESSAGES["vpn_info"].format(
            ipv4="5.129.197.99",
            ipv6="2a03:6f00:a::cbe1",
            root_password="hP9CsxoHLUnq,3"
        ) + f"\nФайл .ovpn: {ovpn_file}"
    )

# -------------------- Реферальная программа --------------------
@dp.callback_query_handler(lambda c: c.data == "referral")
async def referral_handler(call: types.CallbackQuery):
    referral_link = f"https://t.me/home_vpn_bot_bot?start={call.from_user.id}"
    await call.message.answer(
        f"🎁 Реферальная система\n\n"
        f"Пригласите друзей и получите {REFERRAL_BONUS_PERCENT}% от их оплаты ⭐.\n"
        f"Минимальная выплата: {REFERRAL_MIN_PAYOUT} ⭐\n"
        f"Ваша личная ссылка для приглашений:\n{referral_link}"
    )

# -------------------- Запуск бота --------------------
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
