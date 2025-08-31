import requests
from bot.config.settings import OUTLINE_API_URL, OUTLINE_CERT_SHA256

def create_access_key(name: str):
    headers = {"Content-Type": "application/json"}
    data = {"name": name}
    response = requests.post(
        f"{OUTLINE_API_URL}/access-keys",
        json=data,
        verify=False  # чтобы обойти self-signed сертификат
    )
    if response.status_code == 200:
        return response.json()
    return None
