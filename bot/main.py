from aiogram import Bot, Dispatcher, types, executor
import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv("/root/home_bot/.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS").split(",")]

# Тарифы через Stars
TARIFFS = {
    "1_month": {"price_stars": 49, "label": "1 месяц"},
    "2_month": {"price_stars": 89, "label": "2 месяца"},
    "3_month": {"price_stars": 119, "label": "3 месяца"}
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    for key, tariff in TARIFFS.items():
        kb.add(types.InlineKeyboardButton(
            text=f"{tariff['label']} — {tariff['price_stars']}⭐️",
            callback_data=f"buy_{key}"
        ))
    await message.reply("🌟 Выберите тариф VPN:", reply_markup=kb)

# Обработка нажатия кнопки тарифа
@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def process_buy(callback_query: types.CallbackQuery):
    plan_key = callback_query.data[4:]
    if plan_key not in TARIFFS:
        await callback_query.answer("❌ Некорректный тариф")
        return
    tariff = TARIFFS[plan_key]
    # Здесь можно интегрировать Stars оплату
    await callback_query.answer(f"Вы выбрали тариф: {tariff['label']} за {tariff['price_stars']}⭐️")
    # TODO: Добавить выдачу VPN-конфигурации

# Тестовая команда /status (для админов)
@dp.message_handler(commands=["status"])
async def status(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.reply("✅ Бот работает и готов к продажам VPN")
    else:
        await message.reply("❌ У вас нет доступа")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
