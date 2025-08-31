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
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\nВыбери действие:", 
        reply_markup=kb
    )

# Обработчик callback-кнопок
async def menu_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await callback_query.answer()  # убирает "часики"

    # Главное меню → меню покупки VPN
    if data == "menu_buy":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("1 месяц ⭐", callback_data="buy_1"),
            InlineKeyboardButton("2 месяца ⭐", callback_data="buy_2"),
            InlineKeyboardButton("3 месяца ⭐", callback_data="buy_3"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        await callback_query.message.edit_text("Выберите тариф для оплаты:", reply_markup=kb)

    # Выбор тарифа
    elif data.startswith("buy_"):
        month = data.split("_")[1]
        await callback_query.message.answer(f"Вы выбрали тариф: {month} месяц(ев). Следуйте инструкции для оплаты ⭐")

    # Профиль
    elif data == "menu_profile":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        await callback_query.message.edit_text("Здесь будет информация о вашем профиле", reply_markup=kb)

    # Конфигурация VPN
    elif data == "menu_config":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        await callback_query.message.edit_text("Ваши VPN данные здесь", reply_markup=kb)

    # Реферальная программа
    elif data == "menu_referral":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        await callback_query.message.edit_text("Приглашайте друзей и зарабатывайте бонусы!", reply_markup=kb)

    # Помощь
    elif data == "menu_help":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        help_text = (
            "📝 Как пользоваться ботом:\n"
            "1️⃣ Выберите тариф и оплатите ⭐\n"
            "2️⃣ Получите VPN конфигурацию\n"
            "3️⃣ Подключайтесь и пользуйтесь безопасно\n"
            "4️⃣ Приглашайте друзей и зарабатывайте бонусы"
        )
        await callback_query.message.edit_text(help_text, reply_markup=kb)

    # Поддержка
    elif data == "menu_support":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        await callback_query.message.edit_text("Свяжитесь с техподдержкой: @support_username", reply_markup=kb)

    # Назад в главное меню
    elif data == "back_main":
        await start_command(callback_query.message)
