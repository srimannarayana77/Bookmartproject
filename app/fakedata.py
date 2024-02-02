from faker import Faker
from .models import User
import random
from django.contrib.auth.hashers import make_password

fake = Faker()

def generate_fake_users(num_users):
    users = []

    for _ in range(num_users):
        user_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(), 
            'email': fake.email(),
            "password": make_password("123"),
            'user_type': random.choice(['PUBLISHER', 'CUSTOMER']),
            'password': fake.password(),
        }
        user = User(**user_data)
        user.save()  # Save the user to the database
        users.append(user)

    return users

