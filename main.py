from operation_user import UserOperation
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from opreation_product import ProductOperation
from io_interface import IOInterface
from model_product import Product
from model_customer import Customer
import os
import csv


def login_control():
    pass


def customer_control():
    IOInterface.customer_menu()
    choice = IOInterface.get_user_input("Enter your choice: ", 1)[0]
    
    while True:    
        if choice == '1':
            CustomerOperation.get_customers_list()
            
        elif choice == '2':       
                CustomerOperation.update_profile()
            
        elif choice == '3':       
                ProductOperation.get_product_list()
            
        elif choice == '4':       
                OrderOperation.get_order_list()
            
        elif choice == '5':
                OrderOperation.generate_all_customers_consumption_figure()

        elif choice == '6':
                 break            
    

def admin_control():
    IOInterface.admin_menu()
    choice = IOInterface.get_user_input("Enter your choice: ", 1)[0]

    while True:
        if choice == '1':
            files = os.listdir('data/product')
            for file_name in files:
                if file_name.endswith('.csv'):
                    file_path = os.path.join('data/product', file_name)
                    with open(file_path, 'r') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            product = Product(pro_name=row['name'])
                            ProductOperation.save_product_to_file(product)
                        return product
                    
        elif choice == '2':
            user_name = input("Enter customer username: ")
            user_password = input("Enter customer password: ")
            user_email = input("Enter customer email: ")
            user_mobile = input("Enter customer mobile: ")
            # print ("Registering admin user if not registered already")
            # AdminOperation.register_admin()  # Call the register_admin() method from AdminOperation
            success = CustomerOperation.register_customer(user_name, user_password, user_email, user_mobile)
            print("customer added successfully:", success)
            if success:
                print("Customer added successfully.")
            else:
                print("Failed to add customer.")
            break
            
        elif choice == '3':       
            CustomerOperation.get_customers_list()
            
        elif choice == '4':       
            OrderOperation.get_order_list()
            
        elif choice == '5':       
            CustomerOperation.generate_test_order_data()
            
        elif choice == '6':
            ProductOperation.generate_category_figure()
                    
        elif choice == '7':
            ProductOperation.delete_all_products()
                
        elif choice == '8':
            break


def main():
     
    #print("Register admin account")
    
    #AdminOperation.register_admin()
    
    #print("Admin user registered successfully")

    while True:
        IOInterface.main_menu()
        choice = IOInterface.get_user_input("Enter your choice: ", 1)[0]

        if choice == '1':
            user_name = input("please input the name of the user:")
            user_password  = input("please input the password of the user:") 
            userdetails = UserOperation.login(user_name, user_password)
            if userdetails is None:
                print("The user needs to be registered in the system.")
            else:
                print("The user login is successful.")
                open("data/users.txt", 'r').readlines()
                if user_name != 'admin':
                    customer_control()
                else:
                    admin_control()
                

        elif choice == '2':
            user_name = input("Enter username: ")
            user_password = input("Enter password: ")
            user_email = input("Enter email: ")
            user_mobile = input("Enter mobile: ")
            # print ("Registering admin user if not registered already")
            # AdminOperation.register_admin()  # Call the register_admin() method from AdminOperation
            success = CustomerOperation.register_customer(user_name, user_password, user_email, user_mobile)
            print("Registration successful:", success)
            if success:
                print("Customer registered successfully.")
            else:
                print("Failed to register customer.")
                
        elif choice == '3':
            break
                

if __name__ == "__main__":
    main()