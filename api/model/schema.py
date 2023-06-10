from __future__ import annotations
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from repository.database import Base
from model.table import Table

class Schema(Base):
    __tablename__ = 'schema'
    schema_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    schema_name: Mapped[String] = Column(String(255), nullable=False)
    scan_id: Mapped[INTEGER] = Column(ForeignKey("scan.scan_id"))
    tables: Mapped[List["Table"]] = relationship()