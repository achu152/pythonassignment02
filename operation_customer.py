import re
import time
import json
from operation_user import UserOperation
from model_customer import Customer

class CustomerOperation:
    @staticmethod
    def validate_email(user_email):
        # Use regular expression to validate email format
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(email_pattern, user_email):
            return True
        return False

    @staticmethod
    def validate_mobile(user_mobile):
        # Validate mobile number format
        if re.match(r'^0[34]\d{8}$', user_mobile):
            return True
        return False

    @staticmethod
    def register_customer(user_name, user_password, user_email, user_mobile):
        # Check if username already exists
        if UserOperation.check_username_exist(user_name):
            return False

        # Validate email and mobile number
        if not CustomerOperation.validate_email(user_email) or not CustomerOperation.validate_mobile(user_mobile):
            return False

        # Generate unique user ID
        user_id = UserOperation.generate_unique_user_id()

        # Get current time
        current_time = time.strftime("%d-%m-%Y_%H:%M:%S")

        # Create a customer object
        customer = Customer(user_id=user_id, user_name=user_name, user_password=user_password, user_role='customer',user_email=user_email, user_mobile=user_mobile)

        # Save customer information to data/users.txt file
        with open("data/users.txt", "a") as file:
            file.write(str(customer) + "\n")

        return True

    @staticmethod
    def update_profile(attribute_name, value, customer_object):
        # Validate and update the given attribute value of the customer object
        if attribute_name == 'user_name':
            if not UserOperation.validate_username(value):
                return False
            customer_object.user_name = value
        elif attribute_name == 'user_password':
            if not UserOperation.validate_password(value):
                return False
            customer_object.user_password = value
        elif attribute_name == 'user_email':
            if not CustomerOperation.validate_email(value):
                return False
            customer_object.user_email = value
        elif attribute_name == 'user_mobile':
            if not CustomerOperation.validate_mobile(value):
                return False
            customer_object.user_mobile = value
        else:
            return False

        # Update the changes in the data/users.txt file
        UserOperation.update_user_info_file(customer_object)

        return True

    @staticmethod
    def delete_customer(customer_id):
        # Delete the customer from data/users.txt based on the customer_id
        users = UserOperation.get_users_from_file()
        updated_users = []
        deleted = False

        for user in users:
            if isinstance(user, Customer) and user.user_id == customer_id:
                deleted = True
            else:
                updated_users.append(user)

        if deleted:
            UserOperation.write_users_to_file(updated_users)
            return True
        else:
            return False

    @staticmethod
    def get_customer_list(page_number):
        # Retrieve one page of customers from data/users.txt
        users = UserOperation.get_users_from_file()
        customers = [user for user in users if isinstance(user, Customer)]
        total_pages = (len(customers) + 9) // 10

        start_index = (page_number - 1) * 10
        end_index = start_index + 10

        customers_page = customers[start_index:end_index]

        return customers_page, page_number, total_pages
        
    @staticmethod
    def get_customers_list():
        customers = []

        with open("data/users.txt", "r") as file:
            for line in file:
                user_info = json.loads(line.strip())

                if user_info.get("user_role") == "customer":
                    customer = Customer(
                       user_id=user_info.get("user_id"),
                       user_name=user_info.get("user_name"),
                       user_password=user_info.get("user_password"),
                       user_register_time=user_info.get("user_register_time"),
                       user_role=user_info.get("user_role"),
                       user_email=user_info.get("user_email"),
                       user_mobile=user_info.get("user_mobile")
                     )
                    customers.append(customer)

        return customers
        

    @staticmethod
    def delete_all_customers():
        # Remove all customers from data/users.txt file
        users = UserOperation.get_users_from_file()
        updated_users = [user for user in users if not isinstance(user, Customer)]

        # Write the updated users list back to the file
        with open('data/users.txt', 'w') as file:
            for user in updated_users:
                file.write(str(user) + '\n')
