import jwt
import os
from dotenv import load_dotenv

load_dotenv()

class JwtService:
    # generates a token for a given payload
    @staticmethod
    def genToken(payload : dict) -> str:
        secret = os.getenv('SECRET_KEY')
        token : str = jwt.encode(
            payload=payload,
            key=secret,
            algorithm="HS256"
        )
        return token
    
    # verifies a token and returns the decoded payload
    @staticmethod
    def verifyToken(token : str) -> dict:
        secret = os.getenv('SECRET_KEY')
        encoded : dict = jwt.decode(
            jwt=token,
            key=secret,
            algorithms=['HS256']
        )
        return encoded