from aiogram import types

async def send_stars_invoice(message: types.Message, plan_name: str, price: int):
    """
    Создаёт счет для оплаты через Stars
    """
    keyboard = types.InlineKeyboardMarkup()
    pay_url = f"https://stars.example.com/pay?amount={price}&plan={plan_name}"
    keyboard.add(types.InlineKeyboardButton(f"💳 Оплатить {plan_name} ({price}⭐️)", url=pay_url))
    
    await message.answer(
        f"Вы выбрали тариф: {plan_name}\n"
        f"Сумма к оплате: {price}⭐️\n\n"
        "Нажмите кнопку ниже для оплаты:",
        reply_markup=keyboard
    )
