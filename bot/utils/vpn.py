import subprocess
import os
from bot.config.settings import VPN_CLIENTS_DIR

def generate_ovpn(client_name: str) -> str:
    client_file = os.path.join(VPN_CLIENTS_DIR, f"{client_name}.ovpn")

    if os.path.exists(client_file):
        return client_file

    command = f"sudo ./openvpn-install.sh --client {client_name} --output {VPN_CLIENTS_DIR}"
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Ошибка генерации клиента: {result.stderr.decode()}")

    return client_file
