from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# --- База ---
Base = declarative_base()
engine = create_engine("sqlite:///vpn_bot.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

# --- Модель пользователя ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    referral_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    vpn_keys = relationship("VPNKey", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"

# --- Модель подписки ---
class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_months = Column(Integer, nullable=False)
    paid_stars = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="subscriptions")

    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, plan={self.plan_months} мес)>"

# --- Модель VPN ключа ---
class VPNKey(Base):
    __tablename__ = "vpn_keys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="vpn_keys")

    def __repr__(self):
        return f"<VPNKey(user_id={self.user_id}, key={self.key})>"

# --- Создание всех таблиц ---
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("База данных и таблицы созданы успешно!")
