from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales.ru import PAYMENT_MESSAGES
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
async def handle_payment(call: types.CallbackQuery):
    user_id = str(call.from_user.id)

    # Из callback_data достаём срок (1 / 2 / 3)
    month = call.data.split("_")[1]

    # Генерация .ovpn файла
    ovpn_path = generate_ovpn(user_id)

    # Сообщение с инструкцией
    await call.message.answer(
        f"✅ Оплата подтверждена!\n\n"
        f"Ваш VPN готов на {month} мес.\n\n"
        f"Инструкция по подключению:\n"
        f"1️⃣ Установите OpenVPN клиент (например, OpenVPN Connect).\n"
        f"2️⃣ Импортируйте .ovpn файл.\n"
        f"3️⃣ Подключитесь к VPN.\n\n"
        f"🌐 Теперь вы онлайн безопасно и анонимно!"
    )

    # Отправляем сам .ovpn файл
    try:
        with open(ovpn_path, "rb") as file:
            await call.message.answer_document(file, caption="📎 Ваш .ovpn файл")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка отправки файла: {e}")

    await call.answer()
