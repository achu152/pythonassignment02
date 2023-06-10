import os
import random
import string
import time
import matplotlib.pyplot as plt

class OrderOperation:
    @staticmethod
    def generate_unique_order_id():
        file_path = 'data/orders.txt'
        unique_id = None
        while unique_id is None or OrderOperation.check_duplicate_order_id(unique_id, file_path):
            unique_id = 'o_' + ''.join(random.choices(string.digits, k=5))
        return unique_id

    @staticmethod
    def check_duplicate_order_id(order_id, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    order = eval(line)
                    if order['order_id'] == order_id:
                        return True
        return False

    @staticmethod
    def create_an_order(customer_id, product_id, create_time=None):
        order_id = OrderOperation.generate_unique_order_id()
        if create_time is None:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        order_data = {'order_id': order_id, 'customer_id': customer_id, 'product_id': product_id, 'create_time': create_time}
        file_path = 'data/orders.txt'
        with open(file_path, 'a') as file:
            file.write(str(order_data) + '\n')
        return True

    @staticmethod
    def delete_order(order_id):
        file_path = 'data/orders.txt'
        temp_file = 'data/temp_orders.txt'
        deleted = False
        if os.path.exists(file_path):
            with open(file_path, 'r') as file, open(temp_file, 'w') as temp:
                for line in file:
                    order = eval(line)
                    if order['order_id'] != order_id:
                        temp.write(line)
                    else:
                        deleted = True
            os.remove(file_path)
            os.rename(temp_file, file_path)
        return deleted

    @staticmethod
    def get_order_list(customer_id, page_number):
        orders_per_page = 10
        file_path = 'data/orders.txt'
        orders = []
        total_pages = 0
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                total_orders = len(lines)
                total_pages = (total_orders + orders_per_page - 1) // orders_per_page
                start_index = (page_number - 1) * orders_per_page
                end_index = min(start_index + orders_per_page, total_orders)
                for line in lines[start_index:end_index]:
                    order = eval(line)
                    if order['customer_id'] == customer_id:
                        orders.append(order)
        return orders, page_number, total_pages

    @staticmethod
    def generate_test_order_data():
        customers = ['c_1', 'c_2', 'c_3', 'c_4', 'c_5', 'c_6', 'c_7', 'c_8', 'c_9', 'c_10']
        products = ProductOperation.extract_products_from_files()
        
        for customer_id in customers:
            order_count = random.randint(50, 200)
            for _ in range(order_count):
                product = random.choice(products)
                product_id = product['pro_id']
                create_time = OrderOperation.generate_random_order_time()
                OrderOperation.create_an_order(customer_id, product_id, create_time)

    @staticmethod
    def generate_random_order_time():
        now = time.time()
        months_ago = random.randint(0, 11)
        past_time = now - (months_ago * 30 * 24 * 60 * 60)
        random_time = random.uniform(past_time, now)
        order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(random_time))
        return order_time
    
    @staticmethod
    def generate_single_customer_consumption_figure(customer_id):
        orders = OrderOperation.get_order_list(customer_id)[0]
        monthly_consumption = {}
        
        for order in orders:
            month = int(order.create_time.split('-')[1])
            if month in monthly_consumption:
                monthly_consumption[month] += order.product_price
            else:
                monthly_consumption[month] = order.product_price
        
        months = range(1, 13)
        consumption = [monthly_consumption.get(month, 0) for month in months]
        
        plt.bar(months, consumption)
        plt.xlabel('Month')
        plt.ylabel('Consumption')
        plt.title('Monthly Consumption for Customer ' + customer_id)
        plt.savefig('data/figure/generate_single_customer_consumption_figure.png')
        plt.close()
    
    @staticmethod
    def generate_all_customers_consumption_figure():
        all_customers = ['c_1', 'c_2', 'c_3', 'c_4', 'c_5', 'c_6', 'c_7', 'c_8', 'c_9', 'c_10']
        monthly_consumption = {}
        
        for customer_id in all_customers:
            orders = OrderOperation.get_order_list(customer_id)[0]
            for order in orders:
                month = int(order.create_time.split('-')[1])
                if month in monthly_consumption:
                    monthly_consumption[month] += order.product_price
                else:
                    monthly_consumption[month] = order.product_price
        
        months = range(1, 13)
        consumption = [monthly_consumption.get(month, 0) for month in months]
        
        plt.plot(months, consumption, marker='o')
        plt.xlabel('Month')
        plt.ylabel('Consumption')
        plt.title('Monthly Consumption for All Customers')
        plt.savefig('data/figure/generate_all_customers_consumption_figure.png')
        plt.close()
    
    @staticmethod
    def generate_all_top_10_best_sellers_figure():
        orders = OrderOperation.get_all_orders()
        product_sales = {}
        
        for order in orders:
            if order.product_id in product_sales:
                product_sales[order.product_id] += 1
            else:
                product_sales[order.product_id] = 1
        
        top_10 = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:10]
        products, sales = zip(*top_10)
        
        plt.bar(products, sales)
        plt.xlabel('Product ID')
        plt.ylabel('Sales')
        plt.title('Top 10 Best-selling Products')
        plt.savefig('data/figure/generate_all_top_10_best_sellers_figure.png')
        plt.close()
    
    @staticmethod
    def delete_all_orders():
        orders_file = 'data/orders.txt'
        if os.path.exists(orders_file):
            os.remove(orders_file)
    pass