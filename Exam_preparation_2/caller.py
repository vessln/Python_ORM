import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F


# Django queries 1:

def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
        ).annotate(num_orders=Count("profile_orders")).order_by("full_name")

    if profiles:
        result = []
        for p in profiles:
            result.append(f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.num_orders}")
        return "\n".join(result)

    return ""


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles:
        return ""

    return "\n".join(f"Profile: {p.full_name}, orders: {p.number_of_orders}" for p in loyal_profiles)


def get_last_sold_products():
    latest_order = Order.objects.prefetch_related("products_orders").last()

    if latest_order and latest_order.products.all():
        return f"Last sold products: {', '.join(p.name for p in latest_order.products.all().order_by('name'))}"

    return ""


# Django queries 2:

def get_top_products():
    top_products = Product.objects.prefetch_related("products_orders"
                        ).annotate(sold_times=Count("products_orders")
                        ).filter(sold_times__gt=0).order_by("-sold_times", "name")[:5]

    if top_products:
        result = ["Top products:"]
        for p in top_products:
            result.append(f"{p.name}, sold {p.sold_times} times")
        return "\n".join(result)

    return ""


def apply_discounts():
    not_completed_orders = Order.objects.annotate(sold_times=Count("products")
                                ).filter(is_completed=False, sold_times__gt=2)

    if not not_completed_orders:
        num_of_updated_orders = 0
    else:
        num_of_updated_orders = not_completed_orders.update(total_price=F("total_price") * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    first_order = Order.objects.prefetch_related("products"
                ).filter(is_completed=False).order_by("creation_date").first()

    if first_order:
        for product in first_order.products.all():
            product.in_stock -= 1
            if product.in_stock == 0:
                product.is_available = False
            product.save()

        first_order.is_completed = True
        first_order.save()

        return f"Order has been completed!"

    return ""


# adam_smith = Profile.objects.create(full_name="Adam Smith", email="as@test.com", phone_number="001 555 555", address="Adam's Address", is_active=True)
# susan_james = Profile.objects.create(full_name="Susan James", email="sj@test.co.uk", phone_number="0044 333 222", address="Susan's Address", is_active=True)
# vesi_sfm = Profile.objects.create(full_name="Vesi Sfm", email="vesis@test.com", phone_number="001 555 555", address="Vesi's Address", is_active=True)
#
# display_dl = Product.objects.create(name="Display DL", description="Description for Display DL", price=100.0, in_stock=5, is_available=True)
# desk_m = Product.objects.create(name="Desk M", description="Description for Desk M", price=150.0, in_stock=3, is_available=True)
# printer_br_pm = Product.objects.create(name="Printer Br PM", description="Description for Printer Br PM", price=200.0, in_stock=2, is_available=True)
#
# order_adam1 = Order.objects.create(profile=adam_smith, total_price=display_dl.price, is_completed=True)
# order_adam1.products.add(display_dl, printer_br_pm, desk_m)
# order_adam2 = Order.objects.create(profile=adam_smith, total_price=display_dl.price, is_completed=True)
# order_adam2.products.add(printer_br_pm, desk_m)
# order_adam3 = Order.objects.create(profile=adam_smith, total_price=desk_m.price, is_completed=False)
# order_adam3.products.add(display_dl, printer_br_pm)
#
# order_susan = Order.objects.create(profile=susan_james, total_price=desk_m.price, is_completed=False)
# order_susan.products.add(desk_m, printer_br_pm)
#
# order_vesi1 = Order.objects.create(profile=vesi_sfm, total_price=display_dl.price, is_completed=True)
# order_vesi1.products.add(desk_m, printer_br_pm)
# order_vesi2 = Order.objects.create(profile=vesi_sfm, total_price=desk_m.price, is_completed=True)
# order_vesi2.products.add(printer_br_pm, display_dl)
