import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ru")

VPN_IPV4 = os.getenv("VPN_IPV4")
VPN_IPV6 = os.getenv("VPN_IPV6")
VPN_API_KEY = os.getenv("VPN_API_KEY")
