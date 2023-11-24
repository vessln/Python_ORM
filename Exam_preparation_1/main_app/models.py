from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from main_app.managers import DirectorManager
from main_app.mixins import MixinLastUpdated, MixinIsAwarded

class BasePerson(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )
    birth_date = models.DateField(
        default='1900-01-01',
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )

    objects = DirectorManager()

class Actor(MixinIsAwarded, MixinLastUpdated, BasePerson):
    pass

class Movie(MixinIsAwarded, MixinLastUpdated):
    class GenreChoices(models.TextChoices):
        Action = 'Action',
        Comedy = 'Comedy',
        Drama = 'Drama',
        Other = 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )
    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices.choices,
        default=GenreChoices.Other,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0,
    )
    is_classic = models.BooleanField(
        default=False,
    )
    director = models.ForeignKey(
        to="Director",
        on_delete=models.CASCADE,
        related_name="director_movies",
    )
    starring_actor = models.ForeignKey(
        to="Actor",
        on_delete=models.SET_NULL,
        related_name="starring_actor_movies",
        null=True, blank=True,
    )
    actors = models.ManyToManyField(
        to="Actor",
        related_name="actors_movies"
    )

