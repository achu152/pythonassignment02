import random
import string
from model_admin import Admin
from model_customer import Customer

class UserOperation:
    @staticmethod
    def generate_unique_user_id():
        user_id = ''.join(random.choices(string.digits, k=10))
        return f"u_{user_id}"
    
    @staticmethod
    def encrypt_password(user_password):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=len(user_password)*2))
        encrypted_password = "^^"
        for i, char in enumerate(user_password):
            encrypted_password += random_string[2*i] + char
        encrypted_password += random_string[-1] + "$$"
        return encrypted_password
    
    @staticmethod
    def decrypt_password(encrypted_password):
        password = encrypted_password[2:-2:3]
        return password
    
    @staticmethod
    def check_username_exist(user_name):
        with open('data/users.txt', 'r') as file:
            for line in file:
                user_data = eval(line)
                if user_data['user_name'] == user_name:
                    return True
        return False
    
    @staticmethod
    def validate_username(user_name):
        if len(user_name) < 5:
            return False
        if not user_name.isalnum() and "_" not in user_name:
            return False
        return True
    
    @staticmethod
    def validate_password(user_password):
        if len(user_password) < 5:
            return False
        if not any(char.isalpha() for char in user_password):
            return False
        if not any(char.isdigit() for char in user_password):
            return False
        return True
    
    @staticmethod
    def login(user_name, user_password):
        with open('data/users.txt', 'r') as file:
            for line in file:
                user_data = eval(line)
                if user_data['user_name'] == user_name and user_data['user_password'] == user_password:
                    if user_data['user_role'] == 'admin':
                        return Admin(user_data['user_id'], user_data['user_name'], user_data['user_password'], user_data['user_register_time'])
                    else:
                        return Customer(user_data['user_id'], user_data['user_name'], user_data['user_password'], user_data['user_register_time'], user_data['user_email'], user_data['user_mobile'])
        return None
