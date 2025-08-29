from aiogram import types, Dispatcher
from bot.utils.payments import send_stars_invoice

async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("1 месяц - 49⭐️", callback_data="plan_1"))
    keyboard.add(types.InlineKeyboardButton("2 месяца - 89⭐️", callback_data="plan_2"))
    keyboard.add(types.InlineKeyboardButton("3 месяца - 119⭐️", callback_data="plan_3"))
    await message.answer("👋 Привет! Я бот для продажи VPN через ⭐️Stars.\n\nВыбери тариф:", reply_markup=keyboard)

async def process_plan(callback_query: types.CallbackQuery):
    plan_map = {
        "plan_1": ("1 месяц", 49),
        "plan_2": ("2 месяца", 89),
        "plan_3": ("3 месяца", 119),
    }
    plan_name, price = plan_map[callback_query.data]
    await send_stars_invoice(callback_query.message, plan_name, price)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start","buy"])
    dp.register_callback_query_handler(process_plan, lambda c: c.data.startswith("plan_"))
