import os
import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Product, Category, Customer, Order, OrderProduct


# def add_records_to_database():
#     food_category = Category.objects.create(name='Food')
#     drinks_category = (Category.objects.create(name='Drinks'))
#
#     product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99, category=food_category, is_available=False)
#     product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99, category=food_category, is_available=False)
#     product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99, category=food_category, is_available=True)
#     product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49, category=food_category, is_available=True)
#     product5 = Product.objects.create(name='Pasta and Sauce Bundle', description='Package containing pasta and a jar of pasta sauce', price=6.99, category=food_category, is_available=False)
#     product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99, category=food_category, is_available=True)
#     product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs', price=3.49, category=food_category, is_available=True)
#     product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99, category=food_category, is_available=False)
#     product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49, category=food_category, is_available=True)
#
#     product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99, category=drinks_category, is_available=True)
#     product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49, category=drinks_category, is_available=False)
#     product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water', price=4.99, category=drinks_category, is_available=True)
#     product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49, category=drinks_category, is_available=True)
#     product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99, category=drinks_category, is_available=False)
#     product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49, category=drinks_category, is_available=True)
#
#     customer1 = Customer.objects.create(username='john_doe')
#     customer2 = Customer.objects.create(username='alex_alex')
#     customer3 = Customer.objects.create(username='peter132')
#     customer4 = Customer.objects.create(username='k.k.')
#     customer5 = Customer.objects.create(username='peter_smith')
#
#     order1 = Order.objects.create(customer=customer1)
#     order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
#     order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
#     order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
#     order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)
#
#     order2 = Order.objects.create(customer=customer3)
#     order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
#     order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)
#
#     order3 = Order.objects.create(customer=customer1)
#     order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
#     order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
#     return "All data entered!"
#
# print(add_records_to_database())


# print('All Products:')
# print(Product.objects.all())
# print()
# print('All Available Products:')
# print(Product.objects.available_products())
# print()
# print('All Available Food Products:')
# print(Product.objects.available_products_in_category("Food"))


def product_quantity_ordered():
    result = []
    quantity_per_product = Product.objects.annotate(
        total_ordered_quantity=Sum("orderproduct__quantity")
            ).exclude(total_ordered_quantity=None).order_by("-total_ordered_quantity")

    for p in quantity_per_product:
        result.append(f"Quantity ordered of {p.name}: {p.total_ordered_quantity}")

    return "\n".join(result)

# print(product_quantity_ordered())


def ordered_products_per_customer():
    result = []
    orders = Order.objects.prefetch_related("orderproduct_set__product__category").order_by("id")

    for order in orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")
        for prd in order.products.all():
            result.append(f"- Product: {prd.name}, Category: {prd.category.name}")

    return "\n".join(result)

# print(ordered_products_per_customer())


def filter_products():
    result = []
    av_products_price_greater_3 = Q(is_available=True) & Q(price__gt=3.00)
    filtered_products = Product.objects.filter(av_products_price_greater_3).order_by("-price", "name")

    for product in filtered_products:
        result.append(f"{product.name}: {product.price}lv.")

    return "\n".join(result)

# print(filter_products())


def give_discount():
    result = []
    av_products_price_greater_3 = Q(is_available=True) & Q(price__gt=3.00)
    filtered_products = Product.objects.filter(av_products_price_greater_3).order_by("-price", "name")

    filtered_products.update(price=F("price") * 0.7)

    for p in Product.objects.available_products().order_by("-price", "name"):
        result.append(f"{p.name}: {p.price}lv.")

    return "\n".join(result)

# print(give_discount())


