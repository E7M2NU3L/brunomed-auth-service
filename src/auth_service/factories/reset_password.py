from auth_service.services.jwt_service import JwtService
from auth_service.services.bcrypt_service import BcryptService
from auth_service.services.mail_service import SendMailService 
from auth_service.models import Profile

class ResetPasswordFactory:
    def __init__(self, password : str, token : str) -> None:
        self.password = password
        self.token = token

        self.bcrypt_service = BcryptService()
        self.jwt_service = JwtService()

    def reset_password(self):
        encoded = self.jwt_service.verifyToken(
            token=self.token
        )
        user_email = encoded.get('email')
        hashed_password = self.bcrypt_service.generate_hash(
            password=self.password
        )
        
        # Update the password in the database
        updated_user = Profile.objects.filter(
            email=user_email
        ).update(
            password=hashed_password
        )

        message = f"""
            Dear User,

            Your password for the BrunoMed Rehabilitation System has been successfully updated.

            If you made this change, no further action is required. However, if you did not request this update, please reset your password immediately and contact our support team.

            For security reasons, we recommend using a strong and unique password.

            Best regards,  
            BrunoMed Support Team  
            jehrtech@gmail.com
        """
        mail_service = SendMailService(
            message=message,
            receiver=user_email
        )
        mail_service.send()
        return updated_user