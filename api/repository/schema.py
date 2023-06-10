from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select
from repository import database
from model.schema import Schema
from sqlalchemy.orm.exc import NoResultFound

inspector = inspect(database.engine)

class SchemaRepository:

    def find_db_by_id(self,id):
        session = Session(database.engine)
        query = select(Schema).where(Schema.db_id == id)
        result = session.scalars(query).one()
        session.close()
        return result
    
    def save(self,obj):
        session = Session(database.engine, expire_on_commit=False)
        session.add(obj)
        session.commit()
        session.close()
        return obj.schema_id

    def find_by_scan_id(self, scan_id):
        try:
            session = Session(database.engine, expire_on_commit=False)
            query = select(Schema).where(Schema.scan_id==scan_id)
            result = session.scalars(query).all()
            session.close()
        except NoResultFound:
            return None
        else:
            return result
