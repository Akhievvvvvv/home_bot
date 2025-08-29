from aiogram import Bot, Dispatcher, types, executor

BOT_TOKEN = "8253356529:AAG5sClokG30SlhqpP3TNMdl6TajExIE7YU"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "buy"])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("1 месяц - 49⭐️", callback_data="plan_1"))
    keyboard.add(types.InlineKeyboardButton("2 месяца - 89⭐️", callback_data="plan_2"))
    keyboard.add(types.InlineKeyboardButton("3 месяца - 119⭐️", callback_data="plan_3"))
    await message.answer("👋 Привет! Это демо бота @home_vpn_bot_bot.\nВыбери тариф:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("plan_"))
async def plan_callback(callback_query: types.CallbackQuery):
    plan_map = {
        "plan_1": "1 месяц - 49⭐️",
        "plan_2": "2 месяца - 89⭐️",
        "plan_3": "3 месяца - 119⭐️",
    }
    plan = plan_map.get(callback_query.data)
    await callback_query.message.answer(f"Вы выбрали тариф: {plan}\n💡 Оплата через Stars пока демо.")
    await callback_query.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
