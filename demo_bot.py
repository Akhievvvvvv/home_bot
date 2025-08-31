# demo_bot.py
from bot.config.settings import LANG

# Настройки тарифов
TARIFFS = {
    1: {"name": "1 месяц", "stars": 49},
    2: {"name": "2 месяца", "stars": 89},
    3: {"name": "3 месяца", "stars": 119},
}

# VPN конфигурация
VPN_INFO = {
    "IPv4": "5.129.197.99",
    "IPv6": "2a03:6f00:a::cbe1",
    "SSH": "ssh root@5.129.197.99",
    "Password": "********",
    "Closed_ports": [2525, 3389, 389, 53413, 465, 25, 587]
}

def show_menu():
    print("""
=== Главное меню Home VPN Bot ===
1. 🛒 Купить VPN
2. 👤 Мой профиль
3. 📱 Моя конфигурация
4. 🎁 Реферальная программа
5. ❓ Помощь
6. 💬 Поддержка
0. Выйти
""")

def buy_vpn():
    print("Выберите тариф для покупки через звёзды:")
    for key, plan in TARIFFS.items():
        print(f"{key}. {plan['name']} — {plan['stars']} ⭐")
    choice = input("Ваш выбор: ")
    try:
        choice = int(choice)
        if choice in TARIFFS:
            print(f"Вы выбрали {TARIFFS[choice]['name']} за {TARIFFS[choice]['stars']} ⭐")
            print("Инструкция по оплате через Telegram-звёзды:")
            print("1. Перейдите в раздел покупки звёзд в Telegram.")
            print("2. Пополните баланс.")
            print("3. Нажмите 'Оплатить' в боте.")
            print("✅ Оплата принята, подписка активирована!")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Введите число.")

def show_profile():
    print("=== Профиль пользователя ===")
    print("Подписок пока нет (демо).")
    print("Реферальные бонусы: 0 ⭐")

def show_vpn_config():
    print("=== Ваша VPN-конфигурация ===")
    for key, value in VPN_INFO.items():
        print(f"{key}: {value}")

def show_referral():
    print("=== Реферальная программа ===")
    print("Вы получаете 10% с каждой покупки друга!")

def show_support():
    print("Связь с поддержкой: @home_vpn_support_bot")

def show_help():
    print("Помощь по боту: выберите пункт меню и следуйте инструкциям.")

def run_demo():
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ")
        if choice == "1":
            buy_vpn()
        elif choice == "2":
            show_profile()
        elif choice == "3":
            show_vpn_config()
        elif choice == "4":
            show_referral()
        elif choice == "5":
            show_help()
        elif choice == "6":
            show_support()
        elif choice == "0":
            print("Выход из демо. Спасибо!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    print("=== Демонстрация Home VPN Bot ===")
    run_demo()
