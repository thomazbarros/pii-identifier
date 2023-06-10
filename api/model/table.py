from __future__ import annotations
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from repository.database import Base
from model.tablecolumn import TableColumn


class Table(Base):
    __tablename__ = 'table'
    table_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    table_name: Mapped[String] = Column(String(255), nullable=False)
    schema_id: Mapped[INTEGER] = Column(ForeignKey("schema.schema_id"))
    is_pii: Mapped[BOOLEAN] = Column(BOOLEAN, nullable=False, default=False)
    columns: Mapped[List["TableColumn"]] = relationship()
