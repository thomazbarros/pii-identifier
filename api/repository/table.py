from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select
from repository import database
from model.table import Table
from sqlalchemy.orm.exc import NoResultFound

inspector = inspect(database.engine)

class TableRepository:

    def find_db_by_id(self,id):
        session = Session(database.engine)
        query = select(Table).where(Table.db_id == id)
        result = session.scalars(query).one()
        session.close()
        return result
    
    def save(self,obj):
        session = Session(database.engine, expire_on_commit=False)
        session.add(obj)
        session.commit()
        session.close()
        return obj.table_id

    def find_by_schema_id(self, schema_id):
        try:
            session = Session(database.engine)
            query = select(Table).where(Table.schema_id==schema_id)
            result = session.scalars(query).all()
            session.close()
        except NoResultFound:
            return None
        else:
            return result
