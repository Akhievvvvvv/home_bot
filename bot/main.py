import asyncio
from aiogram import Bot, Dispatcher, types
from bot.config.settings import BOT_TOKEN
from bot.handlers import main as main_handlers
from bot.locales.ru import START_MESSAGE, MAIN_MENU

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*(types.KeyboardButton(text) for text in MAIN_MENU.values()))
    await message.answer(START_MESSAGE.format(username=message.from_user.username), reply_markup=kb)

# Подключаем callback handlers
# Здесь подключаются все функции из handlers/main.py
# например: dp.callback_query_handler(main_handlers.handle_buy, lambda c: c.data.startswith("buy_"))

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
