from aiogram import types

async def send_stars_invoice(message: types.Message, plan_name: str, price: int):
    prices = [types.LabeledPrice(label=plan_name, amount=price*100)]
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title=f"Подписка VPN - {plan_name}",
        description=f"VPN доступ на {plan_name}",
        payload="vpn_subscription",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="vpn-stars-payment"
    )
