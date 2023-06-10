from repository.user import UserRepository
from model.user import User
from service.crypto import CryptoService
from dto.user import UserDTO
from exception.entityalreadyexistsexception import EntityAlreadyExistsException

crypto_service = CryptoService()
user_repository = UserRepository()

class UserService:
    
    def find(self, name = None, username = None): 
        users = user_repository.find(name, username)
        return list(map(self.__convert_to_dto, users))

    def create_user(self, name, username, password): 
        existing_user = user_repository.find(username = username)
        print(existing_user)
        if len(existing_user) > 0:
            raise EntityAlreadyExistsException("User with username " + username + "already exists")
        
        encripted_password = crypto_service.encrypt(password)
        print("password= ", password, "\nencrypted= ", encripted_password)
        new_user = User(name, username, encripted_password)
        return user_repository.create_user(new_user)
        

    def get_user_by_id(self, id):
        user = user_repository.find_by_id(id)
        if user:
            return self.__convert_to_dto(user)
        else:
            return None
    
    def login(self, username, password):
        users = user_repository.find(username = username)
        print(users)
        if (len(users) == 0): 
            raise ValueError("Username or password are incorrect")
        user = users[0]
        decrypted_password_db = crypto_service.decrypt(user.password)
        if (password != decrypted_password_db):
            raise ValueError("Username or password are incorrect")

    def __convert_to_dto(self, user):
        return UserDTO(id= user.id, name= user.name, username= user.username)
