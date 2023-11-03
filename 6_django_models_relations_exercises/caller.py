import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Registration, Car, \
    Owner
from datetime import timedelta, date


def show_all_authors_with_their_books():
    all_authors = Author.objects.all().order_by("id")

    authors_books = []
    for a in all_authors:
        books = a.book_set.all()
        if books:
            authors_books.append(f"{a.name} has written - {', '.join(b.title for b in books)}!")

    return "\n".join(authors_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


# author1 = Author.objects.create(name="J.K. Rowling")
# author2 = Author.objects.create(name="George Orwell")
# author3 = Author.objects.create(name="Harper Lee")
# author4 = Author.objects.create(name="Mark Twain")
#
# book1 = Book.objects.create(
#     title="Harry Potter and the Philosopher's Stone",
#     price=19.99,
#     author=author1
# )
# book2 = Book.objects.create(
#     title="1984",
#     price=14.99,
#     author=author2
# )
# book3 = Book.objects.create(
#     title="To Kill a Mockingbird",
#     price=12.99,
#     author=author3
# )
#
# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
# delete_all_authors_without_books()
# print(Author.objects.count())


def add_song_to_artist(artist_name: str, song_title: str):
    artist_obj = Artist.objects.get(name=artist_name)
    song_obj = Song.objects.get(title=song_title)

    artist_obj.songs.add(song_obj)

def get_songs_by_artist(artist_name: str):
    artist_obj = Artist.objects.get(name=artist_name)
    songs_obj = artist_obj.songs.all().order_by("-id")

    return songs_obj

def remove_song_from_artist(artist_name: str, song_title: str):
    artist_obj = Artist.objects.get(name=artist_name)
    song_obj = Song.objects.get(title=song_title)

    artist_obj.songs.remove(song_obj)

# artist1 = Artist.objects.create(name="Daniel Di Angelo")
# artist2 = Artist.objects.create(name="Indila")
#
# song1 = Song.objects.create(title="Lose Face")
# song2 = Song.objects.create(title="Tourner Dans Le Vide")
# song3 = Song.objects.create(title="Loyalty")
#
# add_song_to_artist("Daniel Di Angelo", "Lose Face")
# add_song_to_artist("Daniel Di Angelo", "Loyalty")
# add_song_to_artist("Indila", "Tourner Dans Le Vide")
#
# songs = get_songs_by_artist("Daniel Di Angelo")
# for song in songs:
#     print(f"Daniel Di Angelo: {song.title}")
#
# songs = get_songs_by_artist("Indila")
# for song in songs:
#     print(f"Indila: {song.title}")
#
# remove_song_from_artist("Daniel Di Angelo", "Lose Face")
#
# songs = get_songs_by_artist("Daniel Di Angelo")
#
# for song in songs:
#     print(f"Songs by Daniel Di Angelo after removal: {song.title}")


def calculate_average_rating_for_product_by_name(product_name: str):
    product_obj = Product.objects.get(name=product_name)
    reviews_for_product = product_obj.reviews.all()

    avg_rating = (sum(r.rating for r in reviews_for_product)) / reviews_for_product.count()

    return avg_rating

def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)

def get_products_with_no_reviews():
    products = Product.objects.filter(reviews__isnull=True).order_by("-name")

    return products

def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()

# product1 = Product.objects.create(name="Laptop")
# product2 = Product.objects.create(name="Smartphone")
# product3 = Product.objects.create(name="Headphones")
# product4 = Product.objects.create(name="PlayStation 5")
#
# review1 = Review.objects.create(description="Great laptop!", rating=5, product=product1)
# review2 = Review.objects.create(description="The laptop is slow!", rating=2, product=product1)
# review3 = Review.objects.create(description="Awesome smartphone!", rating=5, product=product2)
#
# products_without_reviews = get_products_with_no_reviews()
# print(f"Products without reviews: {', '.join([p.name for p in products_without_reviews])}")
# delete_products_without_reviews()
# print(f"Products left: {Product.objects.count()}")
# print(calculate_average_rating_for_product_by_name("Laptop"))


def calculate_licenses_expiration_dates():
    driving_licenses = DrivingLicense.objects.all().order_by("-license_number")
    result = []
    for l in driving_licenses:
        result.append(f"License with id: {l.license_number} expires on {l.issue_date + timedelta(days=365)}!")

    return "\n".join(result)

def get_drivers_with_expired_licenses(due_date):
    # expiration_cutoff_date = due_date - timedelta(days=365)
    # expired_drivers = Driver.objects.filter(drivinglicense__issue_date__gt=expiration_cutoff_date)
    # return expired_drivers

    result = []
    for d in Driver.objects.all():
        max_date = d.drivinglicense.issue_date + timedelta(days=365)
        if max_date > due_date:
            result.append(d)

    return result


# driver1 = Driver.objects.create(first_name="Tanya", last_name="Petrova")
# driver2 = Driver.objects.create(first_name="Ivan", last_name="Yordanov")
#
# license1 = DrivingLicense.objects.create(license_number="123", issue_date=date(2022, 10, 6), driver=driver1)
# license2 = DrivingLicense.objects.create(license_number="456", issue_date=date(2022, 1, 1), driver=driver2)
#
# expiration_dates = calculate_licenses_expiration_dates()
# print(expiration_dates)
#
# drivers_with_expired_licenses = get_drivers_with_expired_licenses(date(2023, 1, 1))
# for driver in drivers_with_expired_licenses:
#     print(f"{driver.first_name} {driver.last_name} has to renew their driving license!")





