from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger, func, DateTime,
)

from database.database import Base


class DonorTargetID(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    donor_id = Column(BigInteger, nullable=False)
    target_id = Column(BigInteger, nullable=False)
    date = Column(DateTime, default=datetime.now, server_default=func.now())
