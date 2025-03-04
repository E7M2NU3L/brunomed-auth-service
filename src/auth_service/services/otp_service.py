import random

class OtpService:
    def __init__(self) -> None:
        self.length = 6
    
    def generate_otp(self) -> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(self.length))