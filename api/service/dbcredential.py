from model.dbcredential import DBCredential
from repository import dbcredential
from service.crypto import CryptoService

crypto_service = CryptoService()

class DBCredentialService:
    def create(self, host, port, username, password):
        if port is None:
            port=3306
        if password is None:
            password=""
        else:
            password = crypto_service.encrypt(password)
        dbCredential = DBCredential(db_host=host, db_port=port, db_username=username, db_password=password)
        return dbcredential.save(dbCredential)