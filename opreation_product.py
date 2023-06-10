import csv
import os
import matplotlib.pyplot as plt
from model_product import Product

class ProductOperation:
    def extract_products_from_files():
        # Clear existing product data
        ProductOperation.delete_all_products()

        # Extract product information from csv files
        files = os.listdir('data/product')
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join('data/product', file_name)
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        product = Product(
                            pro_id=row['id'],
                            pro_model=row['model'],
                            pro_category=row['category'],
                            pro_name=row['name'],
                            pro_current_price=row['current_price'],
                            pro_raw_price=row['raw_price'],
                            pro_discount=row['discount'],
                            pro_likes_count=row['likes_count']
                        )
                        ProductOperation.save_product_to_file(product)
                        return product

    @staticmethod
    def save_product_to_file(product):
        with open('data/products.txt', 'a') as file:
            file.write(str(product) + '\n')

    @staticmethod
    def get_product_list(page_number):
        products = ProductOperation.extract_products_from_files()
        total_pages = (len(products) + 9) // 10
        start_index = (page_number - 1) * 10
        end_index = start_index + 10
        return products[start_index:end_index], page_number, total_pages

    @staticmethod
    def delete_product(product_id):
        products = ProductOperation.extract_products_from_files()
        filtered_products = [product for product in products if product.pro_id != product_id]
        if len(products) == len(filtered_products):
            return False
        ProductOperation.save_products_to_file(filtered_products)
        return True

    @staticmethod
    def get_product_list_by_keyword(keyword):
        products = ProductOperation.extract_products_from_files()
        filtered_products = [product for product in products if keyword.lower() in product.pro_name.lower()]
        return filtered_products

    @staticmethod
    def get_product_by_id(product_id):
        products = ProductOperation.extract_products_from_files()
        for product in products:
            if product.pro_id == product_id:
                return product
        return None

    @staticmethod
    def generate_category_figure():
        products = ProductOperation.extract_products_from_files()
        categories = {}
        for product in products:
            if product.pro_category in categories:
                categories[product.pro_category] += 1
            else:
                categories[product.pro_category] = 1

        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        x = [category[0] for category in sorted_categories]
        y = [category[1] for category in sorted_categories]

        plt.figure(figsize=(10, 6))
        plt.bar(x, y)
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.title('Product Categories')
        plt.savefig('data/figure/category_figure.png')
        plt.close()

    @staticmethod
    def generate_discount_figure():
        products = ProductOperation.extract_products_from_files()
        less_than_30 = 0
        between_30_and_60 = 0
        greater_than_60 = 0
        for product in products:
            discount = int(product.pro_discount)
            if discount < 30:
                less_than_30 += 1
            elif 30 <= discount <= 60:
                between_30_and_60 += 1
            else:
                greater_than_60 += 1

        labels = ['Less than 30', 'Between 30 and 60', 'Greater than 60']
        sizes = [less_than_30, between_30_and_60, greater_than_60]
        explode = (0, 0, 0.1)

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Product Discount Distribution')
        plt.savefig('data/figure/discount_figure.png')
        plt.close()

    @staticmethod
    def generate_likes_count_figure():
        products = ProductOperation.extract_products_from_files()
        categories = {}
        for product in products:
            if product.pro_category in categories:
                categories[product.pro_category] += int(product.pro_likes_count)
            else:
                categories[product.pro_category] = int(product.pro_likes_count)

        sorted_categories = sorted(categories.items(), key=lambda x: x[1])
        x = [category[0] for category in sorted_categories]
        y = [category[1] for category in sorted_categories]

        plt.figure(figsize=(10, 6))
        plt.bar(x, y)
        plt.xlabel('Category')
        plt.ylabel('Total Likes Count')
        plt.title('Total Likes Count for Each Category')
        plt.savefig('data/figure/likes_count_figure.png')
        plt.close()

    @staticmethod
    def generate_discount_likes_count_figure():
        products = ProductOperation.extract_products_from_files()
        discounts = [int(product.pro_discount) for product in products]
        likes_counts = [int(product.pro_likes_count) for product in products]

        plt.figure(figsize=(10, 6))
        plt.scatter(discounts, likes_counts, alpha=0.5)
        plt.xlabel('Discount')
        plt.ylabel('Likes Count')
        plt.title('Relationship between Discount and Likes Count')
        plt.savefig('data/figure/discount_likes_count_figure.png')
        plt.close()

    @staticmethod
    def delete_all_products():
        file_path = 'data/products.txt'
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False
