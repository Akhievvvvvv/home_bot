from datetime import datetime, timedelta

# =========================
# ТАРИФЫ В ЗВЁЗДАХ
# =========================
TARIFFS = {
    "1_month": 49,
    "2_months": 89,
    "3_months": 119,
}

TARIFF_LABELS = {
    "1_month": "1 месяц",
    "2_months": "2 месяца",
    "3_months": "3 месяца",
}

# =========================
# ФОРМАТИРОВАНИЕ
# =========================
def format_price_stars(stars: int) -> str:
    return f"{stars} ⭐"

def format_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

# =========================
# ПРОВЕРКА ЮЗЕРНЕЙМА
# =========================
def validate_username(username: str) -> bool:
    if not username:
        return False
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    return all(c in allowed for c in username) and 5 <= len(username) <= 32

# =========================
# ПОДСЧЁТ ОКОНЧАНИЯ ПОДПИСКИ
# =========================
def calculate_subscription_end(start_date: datetime, months: int) -> datetime:
    return start_date + timedelta(days=30 * months)

# =========================
# СТОИМОСТЬ ТАРИФА
# =========================
def get_tariff_price(tariff_name: str) -> int:
    return TARIFFS.get(tariff_name, 0)

def get_tariff_label(tariff_name: str) -> str:
    return TARIFF_LABELS.get(tariff_name, "Неизвестный тариф")

# =========================
# СООБЩЕНИЕ ДЛЯ ОПЛАТЫ
# =========================
def generate_payment_message(tariff_name: str) -> str:
    stars = get_tariff_price(tariff_name)
    if not stars:
        return "❌ Неверный тариф!"
    return (
        f"Вы выбрали тариф: <b>{get_tariff_label(tariff_name)}</b>\n"
        f"Стоимость: {format_price_stars(stars)}\n\n"
        "Нажмите кнопку ниже, чтобы оплатить ⭐ и активировать VPN 🚀"
    )
