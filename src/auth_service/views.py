from rest_framework.views import APIView
from rest_framework.response import Response
from auth_service.factories.login import LoginFactory
from auth_service.factories.register import RegisterFactory
from auth_service.factories.send_mail import SendMailFactory
from auth_service.factories.reset_password import ResetPasswordFactory
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView
from auth_service.models import Profile
from auth_service.serializers import ProfileSerializer
from rest_framework.status import HTTP_200_OK
from auth_service.services import jwt_service

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
        print(context)

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
        print(otp)
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
        print(otp_from_cookie)

        print(otp == otp_from_cookie)
        
        if otp_from_cookie != otp:
            return Response({'status': False, 'message': 'OTP is Incorrect'}, status=400)
        
        response.delete_cookie('otp')
        response.set_cookie('otp_verified', True)

        return response        
# Reset Password
class PasswordReset(APIView):
    def post(self, request, format=None):
        password = request.data.get('password')
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
        
        token = request.COOKIES.get('otp-token')
        if token == False or token == None:
            raise UserWarning('token is invalid, try again')
        
        # Reset Password
        instance = ResetPasswordFactory(
            password, token
        )
        result = instance.reset_password()
        result['password'] = ""

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
        print(data)
        response = Response(data)
        return response