
from sqlalchemy.orm import Session
from sqlalchemy import select
from model.user import User
from repository import database

class UserRepository: 
    def find_by_id(self, id):
        session = Session(database.engine)
        stmt = select(User).where(User.id == id)
        return session.scalars(stmt).one_or_none()
    
    def search_users(self, name=None, age=None, email=None):
        session = Session(database.engine)
        query = session.query(User)  # User is your SQLAlchemy model class representing the user table
        
        if name:
            query = query.filter(User.name == name)
        if age:
            query = query.filter(User.age == age)
        if email:
            query = query.filter(User.email == email)
        
        results = query.all()
        return results

    def find(self, name = None, username = None):
        session = Session(database.engine)
        query = session.query(User)
        if name:
            search = "%{}%".format(name)
            query = query.filter(User.name.like(search))
        if username:
            query = query.filter(User.username == username)
        return query.all()

    def create_user(self, user): 
        session = Session(database.engine, expire_on_commit=False)
        session.add(user)
        session.commit()
        session.close()
        return user.id
            

