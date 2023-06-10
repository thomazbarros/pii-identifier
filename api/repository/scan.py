from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select, desc, asc
from repository import database
from model.scan import Scan
from sqlalchemy.orm.exc import NoResultFound
from exception.entitynotfoundexception import EntityNotFoundException


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
        return scan.scan_id
    
    def get_last_scan(self, db_id):
        try:
            session = Session(database.engine)
            query = select(Scan.scan_id).where(Scan.dbcredential_id == db_id).order_by(desc(Scan.scan_id))
            result = session.scalars(query).first()
            session.close()
        except NoResultFound:
            raise EntityNotFoundException("DBCredential not found with id " + id)
        else:
            return result