from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger, func, DateTime,
)

from database.database import Base


class DonorTargetChatID(Base):
    """Таблица с ID чатов доноров и целевых каналов"""
    id = Column(Integer, autoincrement=True)
    donor_chat_id = Column(BigInteger, primary_key=True)
    target_chat_id = Column(BigInteger, primary_key=True)
    date = Column(DateTime, default=datetime.now, server_default=func.now())


class DonorTargetMsgID(Base):
    """Таблица с ID сообщений доноров и целевых каналов"""
    id = Column(Integer, autoincrement=True, primary_key=True)
    donor_chat_id = Column(BigInteger, nullable=False)
    target_chat_id = Column(BigInteger, nullable=False)
    donor_msg_id = Column(BigInteger, nullable=False)
    target_msg_id = Column(BigInteger, nullable=False)
    date = Column(DateTime, default=datetime.now, server_default=func.now())
