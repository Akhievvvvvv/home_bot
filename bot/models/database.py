from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# --- База ---
DATABASE_URL = "sqlite:///vpn_bot.db"  # можно заменить на PostgreSQL
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Модель пользователя ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    referral_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    vpn_keys = relationship("VPNKey", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} tg_id={self.telegram_id} username={self.username}>"

    def __str__(self):
        return f"User({self.telegram_id}, {self.username})"


# --- Модель подписки ---
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_months = Column(Integer, nullable=False)
    paid_stars = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="subscriptions")

    def __repr__(self):
        return f"<Subscription user_id={self.user_id} {self.plan_months} мес>"

    def __str__(self):
        return f"Sub({self.user_id}, {self.plan_months} мес)"


# --- Модель VPN ключа ---
class VPNKey(Base):
    __tablename__ = "vpn_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="vpn_keys")

    def __repr__(self):
        return f"<VPNKey user_id={self.user_id} key={self.key}>"

    def __str__(self):
        return f"VPNKey({self.user_id})"


# --- Утилита для подключения ---
def get_db():
    """Контекстный менеджер для работы с сессией БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Создание всех таблиц ---
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ База данных и таблицы созданы успешно!")
