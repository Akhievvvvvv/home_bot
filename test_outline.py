import os
import requests

# Загружаем данные из окружения
API_URL = os.getenv("OUTLINE_API_URL")
CERT_SHA256 = os.getenv("OUTLINE_CERT_SHA256")

if not API_URL or not CERT_SHA256:
    print("❌ Нет переменных OUTLINE_API_URL или OUTLINE_CERT_SHA256")
    exit(1)

headers = {
    "Content-Type": "application/json",
    "Access-Token": CERT_SHA256
}

# Создаем новый access key
url = f"{API_URL}/access-keys"
response = requests.post(url, headers=headers)

if response.status_code == 201:
    key = response.json()
    print("✅ Новый VPN ключ создан:")
    print(key["accessUrl"])
else:
    print("❌ Ошибка при создании ключа")
    print(response.status_code, response.text)
