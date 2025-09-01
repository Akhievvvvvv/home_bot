import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from bot.config.settings import BOT_TOKEN, ADMIN_IDS, PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH, VPN_IPV4, VPN_ROOT_PASSWORD, VPN_CLIENTS_DIR, REFERRAL_BONUS_PERCENT, REFERRAL_MIN_PAYOUT
from bot.locales.ru import START_MESSAGE, BUTTONS, PAYMENT_MESSAGES, REFERRAL_MESSAGES, PROFILE_MESSAGES, CONFIG_MESSAGES

import os
import json
from datetime import datetime, timedelta

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Простая база пользователей (json)
DB_FILE = "bot/users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

db = load_db()

# Inline-кнопки главного меню
def main_menu_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(BUTTONS["buy_vpn"], callback_data="buy_vpn"),
        InlineKeyboardButton(BUTTONS["my_profile"], callback_data="my_profile"),
        InlineKeyboardButton(BUTTONS["my_config"], callback_data="my_config"),
        InlineKeyboardButton(BUTTONS["referral"], callback_data="referral"),
        InlineKeyboardButton(BUTTONS["help"], callback_data="help"),
        InlineKeyboardButton(BUTTONS["support"], callback_data="support")
    )
    return kb

# Inline-кнопки оплаты
def payment_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(f"1 месяц — {PLAN_1_MONTH} ⭐", callback_data="plan_1"),
        InlineKeyboardButton(f"2 месяца — {PLAN_2_MONTH} ⭐", callback_data="plan_2"),
        InlineKeyboardButton(f"3 месяца — {PLAN_3_MONTH} ⭐", callback_data="plan_3")
    )
    return kb

# Inline кнопка "Оплатил(а)"
def paid_button():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(BUTTONS["paid"], callback_data="paid"))
    return kb

# Старт
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in db:
        db[user_id] = {
            "username": message.from_user.full_name,
            "subscription": None,
            "referrals": [],
            "earned": 0
        }
        save_db(db)
    await message.answer(START_MESSAGE.format(username=message.from_user.full_name), reply_markup=main_menu_kb())

# Обработка inline кнопок
@dp.callback_query_handler(lambda c: True)
async def inline_handler(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    data = callback.data

    if data == "buy_vpn":
        await bot.send_message(user_id, PAYMENT_MESSAGES["choose_tariff"], reply_markup=payment_kb())
    elif data.startswith("plan_"):
        plan = int(data.split("_")[1])
        db[user_id]["subscription_plan"] = plan
        db[user_id]["subscription_active"] = False
        save_db(db)
        await bot.send_message(user_id, PAYMENT_MESSAGES["payment_instructions"], reply_markup=paid_button())
    elif data == "paid":
        # Проверка оплаты (эмуляция)
        if user_id in db:
            plan = db[user_id].get("subscription_plan", 1)
            db[user_id]["subscription_active"] = True
            db[user_id]["subscription_start"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            db[user_id]["subscription_end"] = (datetime.now() + timedelta(days=30*plan)).strftime("%Y-%m-%d %H:%M")
            save_db(db)

            # Создаём конфиг VPN (файл)
            client_file = f"{VPN_CLIENTS_DIR}/{user_id}.ovpn"
            os.makedirs(VPN_CLIENTS_DIR, exist_ok=True)
            with open(client_file, "w") as f:
                f.write(f"# Конфиг VPN для {user_id}\n")

            await bot.send_message(user_id, PAYMENT_MESSAGES["payment_success"])
            await bot.send_message(user_id, CONFIG_MESSAGES["vpn_info"].format(
                ipv4=VPN_IPV4,
                ipv6="",
                root_password=VPN_ROOT_PASSWORD,
                client_file=client_file
            ))
    elif data == "my_profile":
        user = db.get(user_id, {})
        subscription = user.get("subscription_plan")
        active = user.get("subscription_active")
        start = user.get("subscription_start", "-")
        end = user.get("subscription_end", "-")
        await bot.send_message(user_id, PROFILE_MESSAGES["subscription_info"].format(
            plan=f"{subscription} месяц(ев)" if subscription else "-",
            expiry_date=end if active else "Нет"
        ) + "\n" + PROFILE_MESSAGES["referrals_info"].format(
            invited=len(user.get("referrals", [])),
            paid=sum([1 for r in user.get("referrals", []) if r.get("paid")])
        ))
    elif data == "referral":
        user = db.get(user_id, {})
        await bot.send_message(user_id, REFERRAL_MESSAGES["referral_info"].format(
            percent=REFERRAL_BONUS_PERCENT,
            min_payout=REFERRAL_MIN_PAYOUT,
            user_id=user_id
        ))
    await callback.answer()
