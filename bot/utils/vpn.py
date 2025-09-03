import subprocess
import os
from bot.config.settings import VPN_CLIENTS_DIR

def generate_ovpn(client_name: str) -> str:
    """
    Генерирует .ovpn файл для клиента.
    Если файл уже существует, возвращает его путь.
    """
    # Путь к файлу клиента
    client_file = os.path.join(VPN_CLIENTS_DIR, f"{client_name}.ovpn")

    # Создаём папку для клиентов, если её нет
    os.makedirs(VPN_CLIENTS_DIR, exist_ok=True)

    # Если файл уже существует, возвращаем его путь
    if os.path.exists(client_file):
        return client_file

    # Запуск скрипта генерации клиента
    command = f"sudo ./openvpn-install.sh --client {client_name}"
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Ошибка генерации клиента:\n{result.stderr.decode()}")

    # Скрипт создаёт файл в /root, перемещаем его в папку клиентов
    default_ovpn = f"/root/{client_name}.ovpn"
    if os.path.exists(default_ovpn):
        os.rename(default_ovpn, client_file)
    else:
        raise Exception("Файл .ovpn не найден после генерации!")

    return client_file
