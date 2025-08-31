from aiogram import types, Dispatcher
from bot.config.settings import ADMIN_IDS
from bot.models.database import SessionLocal, User, Subscription, VPNKey

# Регистрация хэндлеров
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=["admin"])
    dp.register_message_handler(list_users, commands=["users"])
    dp.register_message_handler(list_subscriptions, commands=["subs"])
    dp.register_message_handler(list_keys, commands=["keys"])
    dp.register_message_handler(broadcast_start, commands=["broadcast"])
    dp.register_message_handler(broadcast_send, state="broadcast:message")


async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет доступа к админ-панели")
        return

    text = (
        "👑 <b>Админ-панель Home Bot</b>\n\n"
        "Команды:\n"
        "/users - список пользователей\n"
        "/subs - список подписок\n"
        "/keys - VPN ключи\n"
        "/broadcast - массовая рассылка\n"
    )
    await message.answer(text, parse_mode="HTML")


async def list_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    if not users:
        await message.answer("Пользователей пока нет.")
        return

    text = "<b>Список пользователей:</b>\n"
    for u in users:
        text += f"ID: {u.id} | Username: @{u.username} | Stars: {u.stars}\n"
    await message.answer(text, parse_mode="HTML")


async def list_subscriptions(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    db = SessionLocal()
    subs = db.query(Subscription).all()
    db.close()

    if not subs:
        await message.answer("Подписок пока нет.")
        return

    text = "<b>Список подписок:</b>\n"
    for s in subs:
        text += f"User ID: {s.user_id} | Тариф: {s.plan_months} мес | Статус: {s.status}\n"
    await message.answer(text, parse_mode="HTML")


async def list_keys(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    db = SessionLocal()
    keys = db.query(VPNKey).all()
    db.close()

    if not keys:
        await message.answer("VPN ключей пока нет.")
        return

    text = "<b>Список VPN ключей:</b>\n"
    for k in keys:
        text += f"Ключ: {k.key} | Пользователь ID: {k.user_id} | Активен: {k.active}\n"
    await message.answer(text, parse_mode="HTML")


# Массовая рассылка
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot

class BroadcastStates(StatesGroup):
    message = State()

async def broadcast_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("Введите текст для рассылки всем пользователям:")
    await BroadcastStates.message.set()

async def broadcast_send(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    sent = 0
    for u in users:
        try:
            await message.bot.send_message(u.id, message.text)
            sent += 1
        except:
            continue

    await message.answer(f"✅ Рассылка завершена! Отправлено: {sent}/{len(users)}")
    await state.finish()
