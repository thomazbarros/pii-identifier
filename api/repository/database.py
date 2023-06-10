import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

internal_user = os.environ['INTERNAL_DB_USER']
internal_passwd = os.environ['INTERNAL_DB_PASSWD']
internal_host = os.environ['INTERNAL_DB_HOST']
internal_port = os.environ['INTERNAL_DB_PORT']
internal_database = os.environ['INTERNAL_DB']

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_connection(user, password, host, port, database):
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
            ) 
    )


engine = get_connection(internal_user, internal_passwd, internal_host, internal_port, internal_database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def build_inspector(db_user, db_password, db_host, db_port, db_database):
    local_engine = get_connection(db_user, db_password, db_host, db_port, db_database)
    return engine, inspect(local_engine)