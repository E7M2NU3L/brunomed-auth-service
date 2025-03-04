from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=2550, blank=True)  # Hash before storing
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    assistive_device = models.CharField(max_length=100, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    last_login = models.DateTimeField(auto_now=True)  # Update on every login

    def __str__(self) -> str:
        return super().__str__()