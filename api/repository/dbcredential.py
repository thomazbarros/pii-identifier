from sqlalchemy.orm import Session
from sqlalchemy import inspect,  select
from repository import database
from model.dbcredential import DBCredential
from exception.entitynotfoundexception import EntityNotFoundException

inspector = inspect(database.engine)

def find_db_by_id(id):
    try: 
        session = Session(database.engine)
        query = select(DBCredential).where(DBCredential.db_id == id)
        result = session.scalars(query).one()
        session.close()
        return result
    except Exception as ex:
        raise EntityNotFoundException("Error searching dbcredential: " + str(ex.args))


def get_database_schemas(db_user, db_password, db_host, db_port):
    engine, local_inspector = database.build_inspector(db_user, db_password, db_host, db_port, "")
    schemas = local_inspector.get_schema_names()
    engine.dispose()
    return schemas


def get_schema_tables(db_user, db_password, db_host, db_port, db_database):
    engine, local_inspector = database.build_inspector(db_user, db_password, db_host, db_port, "")
    tables = local_inspector.get_table_names(db_database)
    engine.dispose()
    return tables


def get_table_columns(db_user, db_password, db_host, db_port, db_database, db_table):
    engine, local_inspector = database.build_inspector(db_user, db_password, db_host, db_port, db_database)
    columns = local_inspector.get_columns(db_table, db_database)
    engine.dispose()
    return columns

def get_schema_info(db_user, db_password, db_host, db_port, db_database):
    engine, local_inspector = database.build_inspector(db_user, db_password, db_host, db_port, db_database)
    tables = local_inspector.get_multi_columns(db_database)
    engine.dispose()
    return tables

def save(dbcredential):
    session = Session(database.engine, expire_on_commit=False)
    session.add(dbcredential)
    session.commit()
    session.close()
    return dbcredential.db_id