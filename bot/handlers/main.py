from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales.ru import PAYMENT_MESSAGES, CONFIG_MESSAGES, BUTTONS
from bot.utils.vpn import generate_ovpn

# Кнопки выбора тарифа
def create_tariff_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("1 месяц — 79 ⭐", callback_data="buy_1"),
        InlineKeyboardButton("2 месяца — 129 ⭐", callback_data="buy_2"),
        InlineKeyboardButton("3 месяца — 149 ⭐", callback_data="buy_3")
    )
    return kb

# Обработка покупки (показываем тарифы)
async def handle_buy(call, bot):
    kb = create_tariff_kb()
    await call.message.answer(
        PAYMENT_MESSAGES["choose_tariff"],
        reply_markup=kb
    )

# Обработка подтверждённой оплаты
async def handle_payment(call, month, bot):
    user_id = str(call.from_user.id)
    
    # Генерация .ovpn файла для пользователя
    ovpn_file = generate_ovpn(user_id)
    
    # Кнопка "Оплатил(а)" после оплаты (если нужна повторная проверка)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(BUTTONS["paid"], callback_data=f"paid_{month}"))

    # Отправка сообщения с файлом и инструкцией
    await call.message.answer(
        f"✅ Оплата подтверждена!\n\n"
        f"Ваш VPN готов.\n"
        f"Файл конфигурации: {ovpn_file}\n\n"
        f"Инструкция по подключению:\n"
        f"1️⃣ Установите OpenVPN клиент (например, OpenVPN Connect).\n"
        f"2️⃣ Импортируйте .ovpn файл.\n"
        f"3️⃣ Подключитесь к VPN.\n"
        f"🌐 Теперь вы онлайн безопасно и анонимно!",
        reply_markup=kb
    )
