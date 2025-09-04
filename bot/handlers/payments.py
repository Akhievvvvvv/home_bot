from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.vpn import generate_ovpn
from bot.locales.ru import PAYMENT_MESSAGES
from bot.config.settings import PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH

router = Router()

def create_tariff_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"1 месяц — {PLAN_1_MONTH} ⭐", callback_data="buy_1")],
        [InlineKeyboardButton(text=f"2 месяца — {PLAN_2_MONTH} ⭐", callback_data="buy_2")],
        [InlineKeyboardButton(text=f"3 месяца — {PLAN_3_MONTH} ⭐", callback_data="buy_3")],
    ])

@router.message(F.text.in_({"🛒 Купить VPN", "/buy"}))
async def handle_buy(message: types.Message):
    kb = create_tariff_kb()
    await message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)

@router.callback_query(F.data.in_({"buy_1", "buy_2", "buy_3"}))
async def handle_payment(call: types.CallbackQuery):
    month = int(call.data.split("_")[1])
    user_id = str(call.from_user.id)
    try:
        ovpn_path = generate_ovpn(user_id)
    except Exception as e:
        await call.message.answer(f"❌ Ошибка генерации VPN: {e}")
        await call.answer()
        return
    await call.message.answer(
        f"✅ Оплата подтверждена!\n\n"
        f"Ваш VPN активирован на <b>{month} мес.</b>\n\n"
        f"📖 Инструкция по подключению:\n"
        f"1️⃣ Установите <b>OpenVPN Connect</b> (или другой клиент).\n"
        f"2️⃣ Импортируйте присланный .ovpn файл.\n"
        f"3️⃣ Подключитесь к VPN.\n\n"
        f"🌍 Теперь вы в сети <b>безопасно и анонимно</b> 🔒",
        parse_mode="HTML"
    )
    try:
        with open(ovpn_path, "rb") as f:
            await call.message.answer_document(f, caption="📎 Ваш персональный .ovpn файл")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка отправки файла: {e}")
    await call.answer()
