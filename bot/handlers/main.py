from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales.ru import PAYMENT_MESSAGES, BUTTONS
from bot.utils.vpn import generate_ovpn


# --- Кнопки выбора тарифа ---
def create_tariff_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц — 79 ⭐", callback_data="buy_1")],
        [InlineKeyboardButton(text="2 месяца — 129 ⭐", callback_data="buy_2")],
        [InlineKeyboardButton(text="3 месяца — 149 ⭐", callback_data="buy_3")]
    ])


# --- Покупка: показ тарифов ---
async def handle_buy(call: types.CallbackQuery):
    await call.message.answer(
        PAYMENT_MESSAGES["choose_tariff"],
        reply_markup=create_tariff_kb()
    )
    await call.answer()  # закрывает "часики" у кнопки


# --- Оплата подтверждена ---
async def handle_payment(call: types.CallbackQuery, month: int):
    user_id = str(call.from_user.id)

    # Генерация .ovpn файла
    ovpn_path = generate_ovpn(user_id)

    # Кнопка "Оплатил(а)" (если нужна доп. проверка)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTONS["paid"], callback_data=f"paid_{month}")]
    ])

    # Отправляем сообщение
    await call.message.answer(
        f"✅ Оплата подтверждена!\n\n"
        f"Ваш VPN готов.\n\n"
        f"Инструкция по подключению:\n"
        f"1️⃣ Установите OpenVPN клиент (например, OpenVPN Connect).\n"
        f"2️⃣ Импортируйте .ovpn файл.\n"
        f"3️⃣ Подключитесь к VPN.\n\n"
        f"🌐 Теперь вы онлайн безопасно и анонимно!",
        reply_markup=kb
    )

    # Отправляем сам .ovpn файл
    try:
        with open(ovpn_path, "rb") as file:
            await call.message.answer_document(file, caption="📎 Ваш .ovpn файл")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка отправки файла: {e}")

    await call.answer()
