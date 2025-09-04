import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "7231676236").split(",")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

VPN_IPV4 = os.getenv("VPN_IPV4", "5.129.197.99")
VPN_ROOT_PASSWORD = os.getenv("VPN_ROOT_PASSWORD", "hP9CsxoHLUnq,3")
VPN_CLIENTS_DIR = os.getenv("VPN_CLIENTS_DIR", "/root/home_bot/clients")
os.makedirs(VPN_CLIENTS_DIR, exist_ok=True)

PLAN_1_MONTH = int(os.getenv("PLAN_1_MONTH", 49))
PLAN_2_MONTH = int(os.getenv("PLAN_2_MONTH", 89))
PLAN_3_MONTH = int(os.getenv("PLAN_3_MONTH", 119))

REFERRAL_BONUS_PERCENT = int(os.getenv("REFERRAL_BONUS_PERCENT", 10))
REFERRAL_MIN_PAYOUT = int(os.getenv("REFERRAL_MIN_PAYOUT", 100))

LANG = "ru"
