from auth_service.services.bcrypt_service import BcryptService
from auth_service.services.mail_service import SendMailService
from auth_service.models import Profile
from auth_service.serializers import ProfileSerializer

class RegisterFactory:
    def __init__(self, firstname: str, lastname: str, email: str, password: str, phone: str, address: str, 
                 gender: str, age: int, state: str, country: str, bio: str, assistive_device: str) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password  # Consider hashing before storing
        self.phone = phone
        self.address = address
        self.gender = gender
        self.age = age
        self.state = state
        self.country = country
        self.bio = bio
        self.assistive_device = assistive_device

        self.message = f"""
        Dear {self.firstname} {self.lastname},

        Welcome to BrunoMed!

        We are delighted to have you join our community dedicated to helping individuals in their rehabilitation journey.

        Here are your registration details:
        ----------------------------------------
        Name: {self.firstname} {self.lastname}
        Email: {self.email}
        Phone: {self.phone}
        Address: {self.address}, {self.state}, {self.country}
        Gender: {self.gender}
        Age: {self.age}
        Assistive Device: {self.assistive_device if self.assistive_device else 'N/A'}
        ----------------------------------------

        Your account has been successfully created. Please keep your credentials secure. If you ever need to reset your password, you can do so through our website.

        If you have any questions or need support, feel free to reach out to us.

        Best regards,  
        BrunoMed Team  
        jehrtech@gmail.com  
        """

        # services
        self.bcrypt_service = BcryptService()
        self.email_service = SendMailService(
            message=self.message,
            receiver=self.email
        )

    def __str__(self):
        return f"{self.firstname} {self.lastname}, {self.email}, {self.phone}, {self.country}"
    
    def register(self):
        # find if user already registered
        user_data = Profile.objects.filter(
            email = self.email
        ).first()

        if user_data is not None:
            raise ValueError(f"User with email {self.email} already exists.")
        
        # encrypt the password
        hashedpassword = self.bcrypt_service.generate_hash(
            password=self.password
        )
        if hashedpassword == None:
            raise ValueError("Failed to hash password.")
        
        # Ensure hashed_password is a string, not bytes
        if isinstance(hashedpassword, bytes):
            hashedpassword = hashedpassword.decode("utf-8")
        
         # Prepare user data
        user_data = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": hashedpassword,
            "phone": self.phone,
            "address": self.address,
            "gender": self.gender,
            "age": self.age,
            "state": self.state,
            "country": self.country,
            "bio": self.bio,
            "assistive_device": self.assistive_device
        }

        # Serialize and validate data
        user_profile = ProfileSerializer(data=user_data)
        
        if user_profile.is_valid():
            user_profile.save()

            # Send welcome email
            self.email_service.send()

            # Return response
            return {
                'status': True,
                'message': 'Registration Successful'
            }
        else:
            print(user_profile.errors)  # Debugging step
            raise ValueError("Failed to create user profile.")