from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales.ru import MAIN_MENU, BUTTONS

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_callback_query_handler(menu_callback)

# Главное меню
async def start_command(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(MAIN_MENU["buy_vpn"], callback_data="menu_buy"),
        InlineKeyboardButton(MAIN_MENU["my_profile"], callback_data="menu_profile"),
        InlineKeyboardButton(MAIN_MENU["my_config"], callback_data="menu_config"),
        InlineKeyboardButton(MAIN_MENU["referral"], callback_data="menu_referral"),
        InlineKeyboardButton(MAIN_MENU["help"], callback_data="menu_help"),
        InlineKeyboardButton(MAIN_MENU["support"], callback_data="menu_support")
    )
    await message.answer(f"👋 Привет, {message.from_user.first_name}!\n\nВыбери действие:", reply_markup=kb)

# Обработчик callback-кнопок
async def menu_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await callback_query.answer()  # убирает "часики" у кнопки

    if data == "menu_buy":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("1 месяц ⭐", callback_data="buy_1"),
            InlineKeyboardButton("2 месяца ⭐", callback_data="buy_2"),
            InlineKeyboardButton("3 месяца ⭐", callback_data="buy_3"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        await callback_query.message.edit_text("Выберите тариф для оплаты:", reply_markup=kb)

    elif data.startswith("buy_"):
        month = data.split("_")[1]
        await callback_query.message.answer(f"Вы выбрали тариф: {month} месяц(ев). Следуйте инструкции для оплаты.")

    elif data == "menu_profile":
        await callback_query.message.answer("Здесь будет информация о вашем профиле.")

    elif data == "menu_config":
        await callback_query.message.answer("Здесь ваши VPN данные.")

    elif data == "menu_referral":
        await callback_query.message.answer("Приглашайте друзей и зарабатывайте бонусы!")

    elif data == "menu_help":
        await callback_query.message.answer("📝 Как пользоваться ботом:\n1️⃣ Выберите тариф и оплатите ⭐\n2️⃣ Получите VPN конфигурацию\n3️⃣ Подключайтесь.")

    elif data == "menu_support":
        await callback_query.message.answer("Свяжитесь с техподдержкой: @support_username")

    elif data == "back_main":
        await start_command(callback_query.message)
