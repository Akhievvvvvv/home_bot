import logging
from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Регистрируем хендлеры
from bot.handlers import main as main_handlers
main_handlers.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
