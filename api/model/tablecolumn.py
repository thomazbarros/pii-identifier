from __future__ import annotations
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship
from repository.database import Base


class TableColumn(Base):
    __tablename__ = 'table_column'
    column_id: Mapped[INTEGER] = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    column_name: Mapped[String] = Column(String(255), nullable=False)
    column_type: Mapped[String] = Column(String(255), nullable=False)
    is_pii: Mapped[BOOLEAN] = Column(BOOLEAN, nullable=False, default=False)
    table_id: Mapped[INTEGER] = Column(ForeignKey("table.table_id"))
