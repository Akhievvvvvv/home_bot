from aiogram import Bot, Dispatcher, executor, types
from bot.config.settings import BOT_TOKEN
from bot.handlers.main import register_handlers

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
register_handlers(dp)

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    plan = message.successful_payment.total_amount // 100
    await message.answer(f"✅ Оплата прошла! Твой тариф: {plan}⭐️\n\n🎉 Вот твой VPN-конфиг (заглушка).")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
