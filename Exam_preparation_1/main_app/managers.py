from django.db import models
from django.db.models import Count


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(count_movies=Count("director_movies")
                             ).order_by("-count_movies", "full_name")