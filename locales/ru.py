# Приветствие
START_MESSAGE = (
    "Привет, {username}! 👋\n\n"
    "Я помогу тебе подключить VPN и управлять подпиской.\n\n"
    "Выберите действие ниже:"
)

# Главное меню
MAIN_MENU = {
    "buy_vpn": "🛒 Купить VPN",
    "my_profile": "👤 Мой профиль",
    "my_config": "📱 Моя конфигурация",
    "referral": "🎁 Реферальная программа",
    "help": "❓ Помощь",
    "support": "💬 Поддержка"
}

# Сообщения про оплату
PAYMENT_MESSAGES = {
    "choose_tariff": (
        "Выберите тариф для оплаты ⭐:\n\n"
        "1️⃣ 1 месяц — 79 ⭐\n"
        "2️⃣ 2 месяца — 129 ⭐\n"
        "3️⃣ 3 месяца — 149 ⭐"
    ),
    "payment_instructions": (
        "Инструкция по оплате:\n"
        "1. Переведите необходимое количество ⭐ на бота.\n"
        "2. Нажмите кнопку 'Оплатил(а)'.\n"
        "После подтверждения вы получите доступ к VPN."
    ),
    "payment_success": "✅ Оплата прошла успешно! Ваш VPN активирован.\n\n"
                       "📩 Ваш VPN ключ и инструкция отправлены ниже.",
    "payment_failed": "❌ Оплата не прошла. Попробуйте снова."
}

# Реферальная система
REFERRAL_MESSAGES = {
    "referral_info": (
        "Приглашайте друзей и зарабатывайте бонусы!\n"
        "🔹 Каждый приглашённый даёт {percent}% от его покупки в виде ⭐.\n"
        "🔹 Минимальная сумма для вывода: {min_payout} ⭐.\n"
        "Ваша персональная ссылка: https://t.me/YourBot?start={user_id}"
    )
}

# Профиль пользователя
PROFILE_MESSAGES = {
    "subscription_info": "Ваша подписка:\nТариф: {plan}\nАктивна до: {expiry_date}",
    "no_subscription": "У вас пока нет активной подписки.",
    "referrals_info": "Приглашено: {invited}\nОплатили: {paid}"
}

# Конфигурация VPN
CONFIG_MESSAGES = {
    "vpn_info": (
        "Ваши VPN данные:\n"
        "IPv4: {ipv4}\n"
        "IPv6: {ipv6}\n\n"
        "Подключение по SSH:\n"
        "ssh root@{ipv4}\n"
        "Пароль: {root_password}\n\n"
        "Файл конфигурации VPN: {client_file}"
    )
}

# Ошибки
ERROR_MESSAGES = {
    "invalid_username": "❌ Некорректный username, попробуйте ещё раз.",
    "unknown_command": "❌ Неизвестная команда.",
    "no_active_subscription": "❌ У вас нет активной подписки."
}

# Кнопки inline
BUTTONS = {
    "buy_vpn": "🛒 Купить VPN",
    "my_profile": "👤 Мой профиль",
    "my_config": "📱 Моя конфигурация",
    "referral": "🎁 Реферальная программа",
    "help": "❓ Помощь",
    "support": "💬 Поддержка",
    "paid": "Оплатил(а)"
}
