from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.config.settings import ADMIN_IDS
from bot.models.database import SessionLocal, User, Subscription, VPNKey

# Создаем роутер для админских команд
admin_router = Router()


# --- FSM для рассылки ---
class BroadcastStates(StatesGroup):
    message = State()


# --- Хэндлеры ---
@admin_router.message(F.text == "/admin")
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


@admin_router.message(F.text == "/users")
async def list_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    with SessionLocal() as db:
        users = db.query(User).all()

    if not users:
        await message.answer("Пользователей пока нет.")
        return

    text = "<b>Список пользователей:</b>\n"
    for u in users:
        username = f"@{u.username}" if u.username else "—"
        text += f"ID: {u.id} | Username: {username} | Stars: {u.stars}\n"

    await message.answer(text[:4096], parse_mode="HTML")


@admin_router.message(F.text == "/subs")
async def list_subscriptions(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    with SessionLocal() as db:
        subs = db.query(Subscription).all()

    if not subs:
        await message.answer("Подписок пока нет.")
        return

    text = "<b>Список подписок:</b>\n"
    for s in subs:
        text += f"User ID: {s.user_id} | Тариф: {s.plan_months} мес | Статус: {s.status}\n"

    await message.answer(text[:4096], parse_mode="HTML")


@admin_router.message(F.text == "/keys")
async def list_keys(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    with SessionLocal() as db:
        keys = db.query(VPNKey).all()

    if not keys:
        await message.answer("VPN ключей пока нет.")
        return

    text = "<b>Список VPN ключей:</b>\n"
    for k in keys:
        text += f"Ключ: {k.key} | Пользователь ID: {k.user_id} | Активен: {k.active}\n"

    await message.answer(text[:4096], parse_mode="HTML")


# --- Массовая рассылка ---
@admin_router.message(F.text == "/broadcast")
async def broadcast_start(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer("Введите текст для рассылки всем пользователям:")
    await state.set_state(BroadcastStates.message)


@admin_router.message(BroadcastStates.message)
async def broadcast_send(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    with SessionLocal() as db:
        users = db.query(User).all()

    sent = 0
    for u in users:
        try:
            await message.bot.send_message(u.id, message.text)
            sent += 1
        except Exception:
            continue

    await message.answer(f"✅ Рассылка завершена! Отправлено: {sent}/{len(users)}")
    await state.clear()
