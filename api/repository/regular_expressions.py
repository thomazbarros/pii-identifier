from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select
from repository import database
from model.regular_expressions import Regular_Expression
from sqlalchemy.orm.exc import NoResultFound

inspector = inspect(database.engine)

class Regular_Expression_Repository:

    def find_by_id(self,name):
        session = Session(database.engine)
        query = select(Regular_Expression).where(Regular_Expression.reg_ex_name == name)
        result = session.scalars(query).first()
        session.close()
        return result
    
    def save(self,obj):
        session = Session(database.engine, expire_on_commit=False)
        session.add(obj)
        session.commit()
        session.close()
        return obj.reg_ex_id
    
    def find_all(self):
        try:
            session = Session(database.engine)
            query = select(Regular_Expression)
            result = session.scalars(query).all()
            session.close()
        except NoResultFound:
            return None
        else:
            return result
    


