import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Токен и админы
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "7231676236").split(",")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# VPN
VPN_IPV4 = os.getenv("VPN_IPV4", "5.129.197.99")
VPN_ROOT_PASSWORD = os.getenv("VPN_ROOT_PASSWORD", "hP9CsxoHLUnq,3")
VPN_CLIENTS_DIR = os.getenv("VPN_CLIENTS_DIR", "/root/home_bot/clients")

# Тарифы
PLAN_1_MONTH = int(os.getenv("PLAN_1_MONTH", 79))
PLAN_2_MONTH = int(os.getenv("PLAN_2_MONTH", 129))
PLAN_3_MONTH = int(os.getenv("PLAN_3_MONTH", 149))

# Рефералы
REFERRAL_BONUS_PERCENT = int(os.getenv("REFERRAL_BONUS_PERCENT", 10))
REFERRAL_MIN_PAYOUT = int(os.getenv("REFERRAL_MIN_PAYOUT", 50))

# Язык
LANG = 'ru'
