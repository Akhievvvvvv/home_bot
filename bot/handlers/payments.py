from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales.ru import PAYMENT_MESSAGES, BUTTONS
from bot.utils.vpn import generate_ovpn

router = Router()

# --- Создание кнопок тарифов ---
def create_tariff_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц — 79 ⭐", callback_data="buy_1")],
        [InlineKeyboardButton(text="2 месяца — 129 ⭐", callback_data="buy_2")],
        [InlineKeyboardButton(text="3 месяца — 149 ⭐", callback_data="buy_3")]
    ])

# --- Команда /buy или нажатие кнопки "Купить VPN" ---
@router.message(F.text.in_({"🛒 Купить VPN", "/buy"}))
async def handle_buy(message: types.Message):
    kb = create_tariff_kb()
    await message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)

# --- Обработка выбора тарифа (callback) ---
@router.callback_query(F.data.in_({"buy_1", "buy_2", "buy_3"}))
async def handle_payment(call: types.CallbackQuery):
    # Определяем месяц по callback
    month = int(call.data.split("_")[1])
    user_id = str(call.from_user.id)

    # Генерируем .ovpn
    try:
        ovpn_path = generate_ovpn(user_id)
    except Exception as e:
        await call.message.answer(f"❌ Ошибка генерации VPN: {e}")
        await call.answer()
        return

    # Кнопка "Оплатил(а)" на случай проверки
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTONS["paid"], callback_data=f"paid_{month}")]
    ])

    # Отправляем инструкцию
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
        with open(ovpn_path, "rb") as f:
            await call.message.answer_document(f, caption="📎 Ваш .ovpn файл")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка отправки файла: {e}")

    await call.answer()  # закрываем "часики" у callback
