from django.db import models
from django.db.models import Count, Max, Min, Avg
from django.forms import DecimalField


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price, max_price):
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        return self.values("location").annotate(count_loc=Count("location")).order_by("id")[:2]


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre):
        return self.filter(genre=genre)

    def recently_released_games(self, year):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.annotate(max_rating=Max("rating")).order_by("-max_rating").first()

        # max_r = self.aggregate(max_rating=Max("rating"))["max_rating"]
        # return self.filter(rating=max_r).first()

    def lowest_rated_game(self):
        return self.annotate(min_rating=Min("rating")).order_by("min_rating").first()

        # min_r = self.aggregate(min_rating=Min("rating"))["min_rating"]
        # return self.filter(rating=min_r).first()

    def average_rating(self):
        avg_rating_games = self.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        return f"{avg_rating_games:.1f}"
