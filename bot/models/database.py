from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# База
Base = declarative_base()
engine = create_engine("sqlite:///vpn_bot.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    referral_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Модель подписки
class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    plan_months = Column(Integer)
    paid_stars = Column(Integer)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)

# Заглушка VPNKey, чтобы импорт работал
class VPNKey(Base):
    __tablename__ = "vpn_keys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    key = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

# Создаём все таблицы
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("База данных и таблицы созданы успешно!")
