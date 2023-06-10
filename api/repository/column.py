from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select
from repository import database
from model.scan import Scan

inspector = inspect(database.engine)

class ScanRepository:

    def find_db_by_id(self,id):
        session = Session(database.engine)
        query = select(Scan).where(Scan.db_id == id)
        result = session.scalars(query).one()
        session.close()
        return result
    
    def save(self,scan):
        session = Session(database.engine, expire_on_commit=False)
        session.add(scan)
        session.commit()
        session.close()
        return scan.id
