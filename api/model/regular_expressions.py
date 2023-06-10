from __future__ import annotations
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped
from typing import List
from repository.database import Base
import datetime
from model.schema import Schema


class Regular_Expression(Base):
    __tablename__ = 'regular_expression'
    # reg_ex_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = Column(DateTime, default=datetime.datetime.utcnow,nullable=False)
    reg_ex_name: Mapped[String] = Column(String(255), primary_key=True, nullable=False)
    reg_ex: Mapped[String] = Column(String(400), nullable=False)