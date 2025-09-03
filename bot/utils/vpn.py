# bot/utils/cleanup.py

import os
import datetime
from bot.config.settings import VPN_CLIENTS_DIR
from bot.models.database import SessionLocal, VPNKey

def cleanup_expired_vpn_keys():
    """
    Удаляет все VPN ключи и файлы, у которых истёк срок действия.
    """
    now = datetime.datetime.utcnow()
    deleted_keys = 0
    deleted_files = 0

    with SessionLocal() as db:
        expired_keys = db.query(VPNKey).filter(VPNKey.expires_at != None, VPNKey.expires_at < now).all()

        for key in expired_keys:
            # Удаляем файл .ovpn
            file_path = os.path.join(VPN_CLIENTS_DIR, f"{key.key}.ovpn")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    deleted_files += 1
                except Exception as e:
                    print(f"Ошибка удаления файла {file_path}: {e}")

            # Удаляем запись из базы
            db.delete(key)
            deleted_keys += 1

        db.commit()

    print(f"Очистка завершена: удалено {deleted_keys} ключей и {deleted_files} файлов")
    return deleted_keys, deleted_files
