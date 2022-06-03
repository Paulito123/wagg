"""Declare models and relationships."""
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from config import Config
from database import engine, session

Base = declarative_base()


class AccountStat(Base):
    __tablename__ = "accountstat"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    balance = Column(Integer, nullable=False, default=0)
    towerheight = Column(Integer, nullable=False, default=0)
    proofsinepoch = Column(Integer, nullable=False, default=0)
    lastepochmined = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class MinerHistory(Base):
    __tablename__ = "minerhistory"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    epoch = Column(Integer, nullable=False, default=0)
    proofssubmitted = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class PaymentEvent(Base):
    __tablename__ = "paymentevent"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    height = Column(Integer, nullable=False, default=0)
    type = Column(String(100), nullable=False, default="Received Reward")
    amount = Column(Integer, nullable=False, default=0)
    sender = Column(String(100))
    recipient = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


class ChainEvent(Base):
    __tablename__ = "chainevent"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    height = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime, nullable=False, default=func.now())
    type = Column(String(100), nullable=False, default="")
    status = Column(String(100), nullable=False, default="")
    sender = Column(String(100))
    recipient = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())


def init_db():
    counter = 1
    for accm in Config.account_list:
        a = AccountStat(
           address=f"{accm}",
           name=f"Account {counter}")
        session.add(a)
        counter = counter + 1
    session.commit()


Base.metadata.create_all(engine)
