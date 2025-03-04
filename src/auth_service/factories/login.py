from auth_service.services.jwt_service import JwtService
from auth_service.models import Profile
from auth_service.services.bcrypt_service import BcryptService
from auth_service.services.mail_service import SendMailService

class LoginFactory:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password

        self.message = f"Dear {self.email},\n\nYou have successfully logged into the BrunoMed Rehabilitation System. Access your dashboard to track your progress and explore available resources.\n\nIf this wasnt you, please reset your password immediately.\n\nBest regards,\nEmmanuel [Founder of BrunoMed]\njehrtech@gmail.com"


        self.bcrypt_service = BcryptService()
        self.email_service = SendMailService(
                message=self.message,
                receiver=self.email
            )
        self.jwt_service = JwtService()

    def userLogin(self):
        user_data = Profile.objects.filter(email=self.email).first()
        print("User profile: ", user_data)

        if user_data is None:
            raise UserWarning('User not logged in, please register an account')
        
        userPassword = user_data.password  # Use dot notation instead of dictionary access
        checkPassword = self.bcrypt_service.check_password(
            password=self.password,
            hash_value=userPassword
        )
        print(checkPassword)

        if not checkPassword:
            raise UserWarning('Password Incorrect, Try again')
        
        # Create a token using the user profile data
        token = self.jwt_service.genToken({"email": user_data.email, "id": user_data.id})
        
        print(token)
        if token is None:
            raise PermissionError('Token is Invalid')
        
        self.email_service.send()
        return token