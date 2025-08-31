import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config.settings import BOT_TOKEN, LOG_LEVEL
from bot.handlers import main, payments, admin

logging.basicConfig(level=LOG_LEVEL)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Регистрация хэндлеров
main.register_handlers(dp)
payments.register_handlers(dp)
admin.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
