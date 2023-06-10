from __future__ import annotations
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from repository.database import Base
import datetime
from model.scan import Scan


class DBCredential(Base):
    __tablename__ = 'database_credential'
    db_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), default=0)
    db_host: Mapped[String] = Column(String(15), nullable=False)
    db_port: Mapped[INTEGER] = Column(INTEGER(unsigned=True), default=3306)
    db_username: Mapped[String] = Column(String(255), nullable=False)
    db_password: Mapped[String] = Column(String(255), default="")
    scans: Mapped[List["Scan"]] = relationship()

