from auth_service.services.mail_service import SendMailService
from auth_service.services.otp_service import OtpService
from auth_service.services.jwt_service import JwtService
from auth_service.models import Profile

class SendMailFactory:
    def __init__(self, email) -> None:
        # get the email address to work with
        self.email = email
        self.jwt_service = JwtService()

        # generate the otp
        self.otp_service = OtpService()
        self.otp = self.otp_service.generate_otp()
        
        # sending message
        self.message = f"""
        Dear User,

        Your One-Time Password (OTP) for verification is: **{self.otp}**

        Please use this OTP to complete your authentication process. Do not share this code with anyone.

        If you did not request this OTP, please ignore this email.

        Best regards,  
        BrunoMed Support Team  
        jehrtech@gmail.com
        """

    def send_otp(self) -> dict:
        # get user
        user_data = Profile.objects.get(
            email = self.email
        )
        if user_data is None:
            raise ValueError('No user Found with this email address')

        token = self.jwt_service.genToken(
            payload={"email": user_data.email, "id": user_data.id}
        )

        SendMailService(self.message, self.email).send()

        # return response
        context = {
            'otp': self.otp,
            'token' : token,
            'status': True,
            'message': 'OTP sent successfully'
        }
        print(context)
        return context