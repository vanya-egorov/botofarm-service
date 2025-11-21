from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime

from app.infrastructure.database import Base
from app.infrastructure.types import GUID


class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    login = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(500), nullable=False)
    project_id = Column(GUID(), nullable=False, index=True)
    env = Column(String(50), nullable=False)
    domain = Column(String(50), nullable=False)
    locktime = Column(DateTime, nullable=True)

