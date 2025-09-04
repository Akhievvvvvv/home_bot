from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.config.settings import ADMIN_IDS
from bot.models.database import SessionLocal, User, Subscription, VPNKey

admin_router = Router()

class BroadcastStates(StatesGroup):
    message = State()

@admin_router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас нет доступа к админ-панели")
        return
    text = "👑 <b>Админ-панель Home Bot</b>\n\nКоманды:\n/users\n/subs\n/keys\n/broadcast"
    await message.answer(text, parse_mode="HTML")

# остальной код с выводом пользователей, подписок и VPN ключей
