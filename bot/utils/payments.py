from aiogram import types
from aiogram.types import LabeledPrice
from bot.config.settings import PROVIDER_TOKEN

async def send_stars_invoice(message: types.Message, plan_name: str, price: int):
    prices = [LabeledPrice(label=plan_name, amount=price*100)]
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title=f"VPN: {plan_name}",
        description=f"Оплата тарифа {plan_name} через ⭐️Stars",
        payload=f"plan_{plan_name}",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="vpn_payment"
    )
