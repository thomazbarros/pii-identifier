
from datetime import datetime, timedelta
import jwt
import os

JWT_SECRET = os.getenv('JWT_SECRET')  # Replace with your secure secret key
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = timedelta(minutes=120)

class TokenService:
    def create_jwt_token(self, username: str) -> str:
        payload = {
            "sub": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + JWT_EXPIRATION,
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    def decode(self, x_token):
        return  jwt.decode(x_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM, ])