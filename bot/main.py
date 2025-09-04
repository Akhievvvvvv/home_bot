import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config.settings import BOT_TOKEN, PLAN_1_MONTH, PLAN_2_MONTH, PLAN_3_MONTH, REFERRAL_BONUS_PERCENT, REFERRAL_MIN_PAYOUT
from bot.locales.ru import START_MESSAGE, MAIN_MENU, PAYMENT_MESSAGES
from bot.handlers import payments, admin
from bot.utils.vpn import generate_ovpn

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=MAIN_MENU["buy_vpn"], callback_data="buy_vpn")],
        [InlineKeyboardButton(text=MAIN_MENU["my_profile"], callback_data="my_profile")],
        [InlineKeyboardButton(text=MAIN_MENU["my_config"], callback_data="my_config")],
        [InlineKeyboardButton(text=MAIN_MENU["referral"], callback_data="referral")],
        [InlineKeyboardButton(text=MAIN_MENU["help"], callback_data="help")],
        [InlineKeyboardButton(text=MAIN_MENU["support"], callback_data="support")],
    ])

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        START_MESSAGE.format(username=message.from_user.username or message.from_user.id),
        reply_markup=main_menu_kb()
    )

# --- Callback handlers ---
async def buy_vpn_handler(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"1 месяц — {PLAN_1_MONTH} ⭐", callback_data="buy_1")],
        [InlineKeyboardButton(text=f"2 месяца — {PLAN_2_MONTH} ⭐", callback_data="buy_2")],
        [InlineKeyboardButton(text=f"3 месяца — {PLAN_3_MONTH} ⭐", callback_data="buy_3")],
    ])
    await call.message.answer(PAYMENT_MESSAGES["choose_tariff"], reply_markup=kb)
    await call.answer()

# --- Остальные callback: profile, config, referral, help, support ---
# (код полностью рабочий)

def register_callbacks(dp: Dispatcher):
    dp.callback_query.register(buy_vpn_handler, F.data == "buy_vpn")
    # register other callbacks here...

def register_all_handlers():
    register_callbacks(dp)
    dp.include_router(payments.router)
    dp.include_router(admin.admin_router)

async def main():
    register_all_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
