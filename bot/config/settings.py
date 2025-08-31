import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Outline VPN
OUTLINE_API_URL = os.getenv("OUTLINE_API_URL")
OUTLINE_CERT_SHA256 = os.getenv("OUTLINE_CERT_SHA256")

VPN_IPV4 = os.getenv("VPN_IPV4")
VPN_IPV6 = os.getenv("VPN_IPV6")

# Тарифы (звёзды)
PLAN_1_MONTH = int(os.getenv("PLAN_1_MONTH", 49))
PLAN_2_MONTH = int(os.getenv("PLAN_2_MONTH", 89))
PLAN_3_MONTH = int(os.getenv("PLAN_3_MONTH", 119))

# Реферальная система
REFERRAL_BONUS_PERCENT = int(os.getenv("REFERRAL_BONUS_PERCENT", 10))
REFERRAL_MIN_PAYOUT = int(os.getenv("REFERRAL_MIN_PAYOUT", 100))
