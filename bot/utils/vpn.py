import os
import subprocess
import datetime
from bot.config.settings import VPN_CLIENTS_DIR
from bot.models.database import SessionLocal, VPNKey

def generate_ovpn(client_name: str) -> str:
    client_file = os.path.join(VPN_CLIENTS_DIR, f"{client_name}.ovpn")
    os.makedirs(VPN_CLIENTS_DIR, exist_ok=True)
    if os.path.exists(client_file):
        return client_file

    command = f"sudo ./openvpn-install.sh --client {client_name}"
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(result.stderr.decode())

    default_ovpn = f"/root/{client_name}.ovpn"
    if os.path.exists(default_ovpn):
        os.rename(default_ovpn, client_file)
    else:
        raise Exception(".ovpn файл не найден после генерации!")
    return client_file

def cleanup_expired_vpn_keys():
    now = datetime.datetime.utcnow()
    deleted_keys = 0
    deleted_files = 0
    with SessionLocal() as db:
        expired = db.query(VPNKey).filter(VPNKey.expires_at != None, VPNKey.expires_at < now).all()
        for key in expired:
            file_path = os.path.join(VPN_CLIENTS_DIR, f"{key.key}.ovpn")
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files += 1
            db.delete(key)
            deleted_keys += 1
        db.commit()
    print(f"Удалено {deleted_keys} ключей и {deleted_files} файлов")
    return deleted_keys, deleted_files
