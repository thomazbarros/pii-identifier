from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select
from repository import database
from model.tablecolumn import TableColumn
from sqlalchemy.orm.exc import NoResultFound

inspector = inspect(database.engine)

class TableColumnRepository:

    def find_db_by_id(self,id):
        session = Session(database.engine)
        query = select(TableColumn).where(TableColumn.db_id == id)
        result = session.scalars(query).one()
        session.close()
        return result
    
    def save(self,obj):
        session = Session(database.engine, expire_on_commit=False)
        session.add(obj)
        session.commit()
        session.close()
        return obj.table_id
    
    def find_by_table_id(self, table_id):
        try:
            session = Session(database.engine)
            query = select(TableColumn).where(TableColumn.table_id==table_id)
            result = session.scalars(query).all()
            session.close()
        except NoResultFound:
            return None
        else:
            return result
