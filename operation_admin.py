from operation_user import UserOperation
from model_admin import Admin

class AdminOperation:
    @staticmethod
    def register_admin():
        # Check if admin account already exists in the database
        if UserOperation.check_username_exist('admin'):
            return

        # Generate unique user ID for the admin
        user_id = UserOperation.generate_unique_user_id()

        # Create an admin object
        admin = Admin(user_id=user_id, user_name='admin', user_password='admin123', user_register_time='00-00-0000_00:00:00', user_role='admin')

        # Write admin information to the data/users.txt file
        with open('data/users.txt', 'a') as file:
            file.write(str(admin) + '\n')
