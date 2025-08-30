from aiogram import types, Dispatcher
from bot.utils.payments import send_stars_invoice

# ------------------------------
# Стартовое сообщение
# ------------------------------
async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Тарифы
    keyboard.add(
        types.InlineKeyboardButton("🛒 1 месяц - 49⭐️", callback_data="plan_1"),
        types.InlineKeyboardButton("🛒 2 месяца - 89⭐️", callback_data="plan_2"),
        types.InlineKeyboardButton("🛒 3 месяца - 119⭐️", callback_data="plan_3")
    )
    
    # Профиль и конфигурации
    keyboard.add(
        types.InlineKeyboardButton("👤 Мой профиль", callback_data="profile"),
        types.InlineKeyboardButton("📱 Моя конфигурация", callback_data="config")
    )
    
    # Реферальная программа и помощь
    keyboard.add(
        types.InlineKeyboardButton("🎁 Реферальная программа", callback_data="referral"),
        types.InlineKeyboardButton("❓ Помощь", callback_data="help")
    )
    
    # Поддержка
    keyboard.add(
        types.InlineKeyboardButton("💬 Поддержка", callback_data="support")
    )
    
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🚀 Я — твой VPN-бот для безопасного и быстрого подключения к интернету!\n\n"
        "✨ Что я умею:\n"
        "🛒 Купить VPN подписку на 1, 2 или 3 месяца через ⭐️Stars\n"
        "📱 Получить готовые конфигурации WireGuard\n"
        "👤 Личный кабинет — отслеживайте свои подписки\n"
        "🎁 Реферальная программа — зарабатывайте с друзьями\n"
        "💬 Поддержка — всегда на связи\n\n"
        "Выбери действие ниже ⬇️"
    )
    
    await message.answer(welcome_text, reply_markup=keyboard)


# ------------------------------
# Обработка тарифов
# ------------------------------
async def process_plan(callback_query: types.CallbackQuery):
    plan_map = {
        "plan_1": ("1 месяц", 49),
        "plan_2": ("2 месяца", 89),
        "plan_3": ("3 месяца", 119),
    }
    plan_name, price = plan_map[callback_query.data]
    await send_stars_invoice(callback_query.message, plan_name, price)


# ------------------------------
# Профиль пользователя
# ------------------------------
async def handle_profile(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "👤 Ваш профиль:\n"
        "Тариф: нет активных подписок.\n"
        "Срок действия: —"
    )


# ------------------------------
# Конфигурации VPN
# ------------------------------
async def handle_config(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "📱 Здесь вы сможете скачать ваши VPN конфигурации."
    )


# ------------------------------
# Реферальная программа
# ------------------------------
async def handle_referral(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🎁 Реферальная программа:\n"
        "Отправляйте ссылку друзьям и получайте бонусы."
    )


# ------------------------------
# Инструкция и помощь
# ------------------------------
async def handle_help(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "❓ Инструкции по использованию бота:\n"
        "1. Выберите тариф\n"
        "2. Оплатите через ⭐️Stars\n"
        "3. Получите VPN конфигурацию"
    )


# ------------------------------
# Связь с поддержкой
# ------------------------------
async def handle_support(callback_query: types.CallbackQuery):
    await callback_query.message.answer("💬 Поддержка: @akhievvvvv")


# ------------------------------
# Регистрация всех обработчиков
# ------------------------------
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", "buy"])
    dp.register_callback_query_handler(process_plan, lambda c: c.data.startswith("plan_"))
    dp.register_callback_query_handler(handle_profile, lambda c: c.data=="profile")
    dp.register_callback_query_handler(handle_config, lambda c: c.data=="config")
    dp.register_callback_query_handler(handle_referral, lambda c: c.data=="referral")
    dp.register_callback_query_handler(handle_help, lambda c: c.data=="help")
    dp.register_callback_query_handler(handle_support, lambda c: c.data=="support")
