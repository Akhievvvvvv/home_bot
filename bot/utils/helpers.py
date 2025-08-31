from datetime import datetime, timedelta

# =========================
# ТАРИФЫ В ЗВЁЗДАХ
# =========================
TARIFFS = {
    "1_month": 49,
    "2_months": 89,
    "3_months": 119,
}

# =========================
# ФОРМАТИРОВАНИЕ
# =========================
def format_price_stars(stars: int) -> str:
    """Возвращает цену в звёздах с красивым оформлением."""
    return f"{stars} ⭐"

def format_date(timestamp: int) -> str:
    """Преобразует Unix timestamp в читаемую дату."""
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")

# =========================
# ПРОВЕРКА ЮЗЕРНЕЙМА
# =========================
def validate_username(username: str) -> bool:
    """Простейшая валидация username Telegram."""
    return username.isalnum() and 5 <= len(username) <= 32

# =========================
# ПОДСЧЁТ ОКОНЧАНИЯ ПОДПИСКИ
# =========================
def calculate_subscription_end(start_date: datetime, months: int) -> datetime:
    """Возвращает дату окончания подписки через N месяцев."""
    return start_date + timedelta(days=30 * months)

# =========================
# ПОЛУЧЕНИЕ СТОИМОСТИ ПО ТАРИФУ
# =========================
def get_tariff_price(tariff_name: str) -> int:
    """Возвращает стоимость тарифа в звёздах."""
    return TARIFFS.get(tariff_name, 0)

# =========================
# СООБЩЕНИЕ ДЛЯ ОПЛАТЫ
# =========================
def generate_payment_message(tariff_name: str) -> str:
    """Создает текст для сообщения с оплатой."""
    stars = get_tariff_price(tariff_name)
    return (
        f"Вы выбрали тариф: {tariff_name.replace('_', ' ')}\n"
        f"Стоимость: {format_price_stars(stars)}\n\n"
        "Нажмите кнопку ниже, чтобы оплатить ⭐ и активировать VPN 🚀"
    )

# =========================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ В ХЭНДЛЕРЕ
# =========================
# from bot.utils.helpers import generate_payment_message
# msg = generate_payment_message("1_month")
