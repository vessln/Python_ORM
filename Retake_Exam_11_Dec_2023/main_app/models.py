from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator

from main_app.managers import TennisPlayerManager


class TennisPlayer(models.Model):
    full_name = models.CharField(max_length=120,
                validators=[MaxLengthValidator(120), MinLengthValidator(5)])

    birth_date = models.DateField()

    country = models.CharField(max_length=100,
                validators=[MaxLengthValidator(100), MinLengthValidator(2)])

    ranking = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)])

    is_active = models.BooleanField(default=True)

    objects = TennisPlayerManager()

    def __str__(self):
        return self.full_name


class Tournament(models.Model):
    SURFACE_CHOICES = [
        ('Not Selected', 'Not Selected'),
        ('Clay', 'Clay'),
        ('Grass', 'Grass'),
        ('Hard Court', 'Hard Court'),
    ]

    name = models.CharField(max_length=150,
        validators=[MaxLengthValidator(150), MinLengthValidator(2)], unique=True)

    location = models.CharField(max_length=100,
        validators=[MaxLengthValidator(100), MinLengthValidator(2)])

    prize_money = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()

    surface_type = models.CharField(max_length=12, choices=SURFACE_CHOICES,
            validators=[MaxLengthValidator(12)], default="Not Selected")


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"

    score = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])

    summary = models.TextField(validators=[MinLengthValidator(5)])

    date_played = models.DateTimeField()

    tournament = models.ForeignKey(to="Tournament", on_delete=models.CASCADE,
                                   related_name="matches_tournament")

    players = models.ManyToManyField(to="TennisPlayer", related_name="matches_players")

    winner = models.ForeignKey(to="TennisPlayer", on_delete=models.SET_NULL,
                               null=True, blank=True, related_name="match_winner")


