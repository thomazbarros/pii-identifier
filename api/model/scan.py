from __future__ import annotations
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from repository.database import Base
import datetime
from model.schema import Schema


class Scan(Base):
    __tablename__ = 'scan'
    scan_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = Column(DateTime, default=datetime.datetime.utcnow)
    dbcredential_id: Mapped[INTEGER] = Column(ForeignKey("database_credential.db_id"))
    schemas: Mapped[List["Schema"]] = relationship()