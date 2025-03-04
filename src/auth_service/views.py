from rest_framework.views import APIView
from rest_framework.response import Response
from auth_service.factories.login import LoginFactory
from auth_service.factories.register import RegisterFactory
from auth_service.factories.send_mail import SendMailFactory
from auth_service.factories.reset_password import ResetPasswordFactory
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView
from auth_service.models import Profile
from auth_service.serializers import ProfileSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from auth_service.services import jwt_service
from auth_service.services import otp_service, mail_service

# 1. Login User
class LoginUser(APIView):
    
    def post(self, request, format=None):
        # getting the Data from the request
        data = request.data
        
        # validating the user credentials
        user_email : str = data.get('email')
        user_password : str = data.get('password')

        # handle the cred
        if user_email == None or user_password == None:
            raise ValueError('Invalid Credentials')
        
        # Login User token
        factory = LoginFactory(
            email=user_email,
            password=user_password
        )
        token = factory.userLogin()

        # result context
        context = {
            'status' : True,
            'message' : 'Login Successful',
            'token' : token
        }

        # response object
        response = Response(context)

        # setting a cookie
        response.set_cookie('auth-token', token, max_age=30*24*60*60*1000)

        # return response
        return response
    
# 2. Register User
class RegisterUser(APIView):
    
    def post(self, request, format=None):
        # getting the Data from the request
        data = request.data
        
        # validating the user credentials
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        address = data.get('address')
        gender = data.get('gender')
        age = data.get('age')
        state = data.get('state')
        country = data.get('country')
        bio = data.get('bio')
        assistive_device = data.get('assistive_device')

        # handle the cred
        if firstname == None or lastname == None or email == None or password == None or phone == None or address == None or gender == None or age == None or state == None or country == None:
            raise ValueError('Invalid Credentials')
        
        # Register User
        factory = RegisterFactory(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            phone=phone,
            address=address,
            gender=gender,
            age=age,
            state=state,
            country=country,
            bio=bio,
            assistive_device=assistive_device
        )
        context = factory.register()

        # result context
        context = {
            'status' : True,
            'message' : 'Registration Successful',
            'data' : context
        }

        # response object
        response = Response(data=context, status=HTTP_200_OK)
        
        # return response
        return response
    
# 3. Forgot Password
class SendMail(APIView):
    
    def post(self, request, format=None):
        data = request.data

        if data.get('email') is None:
            raise ValueError('Missing email address')
        
        email = data.get('email')
        
        # Send OTP to the user's email
        factory = SendMailFactory(
           email=email
        )
        result = factory.send_otp()

        # get the cookies
        otp = result.get('otp')
        if otp is None:
            raise ValueError('Invalid OTP')
        
        token = result.get('token')
        if otp is None:
            raise ValueError('Token is not generated for this mail address')

        # response object
        response = Response({
            'status' : True,
            'message' : 'OTP sent successfully'
        })
        response.set_cookie('otp', otp)
        response.set_cookie('otp_token', token)
        
        # return response
        return response
    
# Verify Otp
class VerifyOtp(APIView):
    def post(self, request, format=None):
        otp = request.data.get('otp')
        if otp is None:
            raise ValueError('Invalid OTP')
        
        # get the cookies
        response = Response({
            'status' : True,
            'message' : 'OTP verified successfully'
        })

        # Get the OTP from cookies
        otp_from_cookie = request.COOKIES.get('otp')
        if otp_from_cookie is None:
            return Response({'status': False, 'message': 'OTP not found in cookies'}, status=400)
        
        if otp_from_cookie != otp:
            return Response({'status': False, 'message': 'OTP is Incorrect'}, status=400)
        
        response.delete_cookie('otp')
        response.set_cookie('otp_verified', True)

        return response        
# Reset Password
class PasswordReset(APIView):
    def post(self, request, format=None):
        password = request.data.get('newPassword')
        if password is None:
            raise ValueError('Invalid password')
        
        # get the cookies
        response = Response({
            'status' : True,
            'message' : 'Password has been reset successfully',
        })
        is_otp_verified = request.COOKIES.get('otp_verified')

        if is_otp_verified == False or is_otp_verified == None:
            raise UserWarning('token is invalid, try again')
        
        token = request.COOKIES.get('otp_token')
        if token == False or token == None:
            raise UserWarning('token is invalid, try again')
        
        # Reset Password
        instance = ResetPasswordFactory(
            password, token
        )
        instance.reset_password()

        return response

class Logout(APIView):
    def post(self, request, *args, **kwargs):
        response = Response( {
            'status' : True,
            'message' : 'Logged out successfully'
        })
        response.delete_cookie('auth-token')
        response.delete_cookie('otp')
        response.delete_cookie('otp_token')
        response.delete_cookie('otp_verified')

        return response
    
class MFaSteStep1(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('auth-token')
        if token is None:
            raise ValueError('Token is not provided')
        
        instance = jwt_service.JwtService()
        data = instance.verifyToken(
            token=token
        )
        if data is None:
            return Response({
                    'error' : "Token is not valid, resulted in errors"
                })

        otp = otp_service.OtpService().generate_otp()
        message = f"""
        your otp is {otp}
        """
        mail_service.SendMailService(message=message, receiver=data.get('email')).send()
        
        data = {
            'status' : True,
            'message' : "Otp has been sent to your email address"
        }    
        response = Response(data)
        response.set_cookie('mfa_otp', otp)
        return response
    
class MfaSteStep2(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('auth-token')
        if token is None:
            raise ValueError('Token is not provided')
        
        instance = jwt_service.JwtService()
        data = instance.verifyToken(
            token=token
        )
        if data is None:
            return Response({
                    'error' : "Token is not valid, resulted in errors"
                })
    
        otp = request.data.get('otp')
        if otp is None:
            return Response({
                'error' : "Invalid otp"
            }, status=HTTP_400_BAD_REQUEST)
        
        otp_from_browser = request.COOKIES.get('mfa_otp')
        if otp_from_browser is None:
            return Response({
                'error' : "otp is not found in browser"
            }, status=HTTP_400_BAD_REQUEST)
        
        Profile.objects.filter(
            email=data.get('email')
        ).update(mfa=True)
        
        # get the cookies
        response = Response({
            'status' : True,
            'message' : 'Otp verified successfully'
        })
        response.delete_cookie('mfa_otp')
        return response


class UpdateProfile(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class DeleteProfile(RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CurrentUser(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('auth-token')

        if token is None:
            raise ValueError('Token is not provided')
        
        instance = jwt_service.JwtService()

        data = instance.verifyToken(
            token=token
        )
        user_profile = Profile.objects.filter(
            email=data.get("email")
        ).first()
        response = Response({
            'token_encoded' : data,
            'model': {
                'firstname' : user_profile.firstname,
                'lastname' : user_profile.lastname,
                'email' : user_profile.email,
                'phone' : user_profile.phone,
                'state' : user_profile.state,
                'address' : user_profile.address,
                'gender' : user_profile.gender,
                'age' : user_profile.age,
                'country' : user_profile.country,
                'bio' : user_profile.bio,
                'assistive_device' : user_profile.assistive_device,
                'mfa' : user_profile.mfa
            }
        })
        return response