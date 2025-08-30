from aiogram import types

# ------------------------------
# Функция для отправки счета через Stars
# ------------------------------
async def send_stars_invoice(message: types.Message, plan_name: str, price: int):
    """
    Создаёт "счёт" для оплаты через Stars и отправляет пользователю ссылку/кнопку.
    
    :param message: types.Message – объект сообщения от пользователя
    :param plan_name: str – название тарифа, например "1 месяц"
    :param price: int – стоимость в ⭐️
    """
    # Здесь можно интегрировать реальный API Stars
    # Для примера отправим просто кнопку с "заглушкой" оплаты
    keyboard = types.InlineKeyboardMarkup()
    
    # Кнопка оплаты (заглушка)
    pay_url = f"https://stars.example.com/pay?amount={price}&plan={plan_name}"
    keyboard.add(types.InlineKeyboardButton(f"💳 Оплатить {plan_name} ({price}⭐️)", url=pay_url))
    
    await message.answer(
        f"Вы выбрали тариф: {plan_name}\n"
        f"Сумма к оплате: {price}⭐️\n\n"
        f"Нажмите кнопку ниже для оплаты:",
        reply_markup=keyboard
    )
