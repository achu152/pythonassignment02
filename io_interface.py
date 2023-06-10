class IOInterface:
    @staticmethod
    def get_user_input(message, num_of_args):
        user_input = input(message).split()
        result = user_input[:num_of_args]
        if len(result) < num_of_args:
            result.extend([''] * (num_of_args - len(result)))
        return result
    
    @staticmethod
    def main_menu():
        print("1. Login")
        print("2. Register")
        print("3. Quit")
    
    @staticmethod
    def admin_menu():
        print("1. Show products")
        print("2. Add customers")
        print("3. Show customers")
        print("4. Show orders")
        print("5. Generate test data")
        print("6. Generate all statistical figures")
        print("7. Delete all data")
        print("8. Logout")
    
    @staticmethod
    def customer_menu():
        print("1. Show profile")
        print("2. Update profile")
        print("3. Show products")
        print("4. Show history orders")
        print("5. Generate all consumption figures")
        print("6. Logout")
    
    @staticmethod
    def show_list(user_role, list_type, object_list):
        if user_role == 'admin' or list_type in ['Product', 'Order']:
            items, page_number, total_page = object_list
            print(f"List Type: {list_type}")
            print(f"Page: {page_number}/{total_page}")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {str(item)}")
        else:
            print("You are not authorized to view this list.")
    
    @staticmethod
    def print_error_message(error_source, error_message):
        print(f"Error in {error_source}: {error_message}")
    
    @staticmethod
    def print_message(message):
        print(message)
    
    @staticmethod
    def print_object(target_object):
        print(str(target_object))