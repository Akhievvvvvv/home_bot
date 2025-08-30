import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS","").split(",")]

# Настройки VPN (для будущей интеграции)
VPN_SERVER = os.getenv("VPN_SERVER_URL", "5.129.197.99")
VPN_API_KEY = os.getenv("VPN_API_KEY", "")
