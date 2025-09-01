from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales.ru import PAYMENT_MESSAGES, CONFIG_MESSAGES, BUTTONS
from bot.utils.vpn import generate_ovpn

async def handle_buy(call, bot):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("1 месяц — 79 ⭐", callback_data="buy_1"),
        InlineKeyboardButton("2 месяца — 129 ⭐", callback_data="buy_2"),
        InlineKeyboardButton("3 месяца — 149 ⭐", callback_data="buy_3")
    )
    await call.message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)

async def handle_payment(call, month, bot):
    user_id = call.from_user.id
    ovpn_file = generate_ovpn(str(user_id))
    
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(BUTTONS["paid"], callback_data=f"paid_{month}"))

    await call.message.answer(
        f"✅ Оплата подтверждена!\nВаш VPN готов.\n\n"
        f"Файл конфигурации: {ovpn_file}\n\n"
        f"Инструкция по подключению:\n"
        f"1️⃣ Установите OpenVPN клиент.\n"
        f"2️⃣ Импортируйте .ovpn файл.\n"
        f"3️⃣ Подключитесь к VPN.\n"
        f"🌐 Теперь вы онлайн безопасно и анонимно!",
        reply_markup=kb
    )
