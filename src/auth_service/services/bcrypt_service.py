import bcrypt

class BcryptService:
    """Handles password hashing and verification using bcrypt."""

    @staticmethod
    def generate_hash(password: str) -> str:
        # converting password to array of bytes 
        bytes = password.encode('utf-8') 
        # generating the salt 
        salt = bcrypt.gensalt() 
        # Hashing the password 
        hash = bcrypt.hashpw(bytes, salt) 
        return hash

    @staticmethod
    def check_password(password: str, hash_value: str) -> bool:
        # Encoding user input password to bytes
        userBytes = password.encode('utf-8') 

        # Ensure the stored hash is also in bytes
        if isinstance(hash_value, str):
            hash_value = hash_value.encode('utf-8')  # Convert string to bytes

        # Checking the password
        return bcrypt.checkpw(userBytes, hash_value)