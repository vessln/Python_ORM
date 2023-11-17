import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Q, Count, Avg, F


# Django queries 1:

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name) if search_name is not None else Q()
    query_nationality = Q(nationality__icontains=search_nationality) if search_nationality is not None else Q()

    searched_directors = Director.objects.filter(query_name & query_nationality).order_by("full_name")

    if not searched_directors:
        return ""

    result = []
    for d in searched_directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")

    return "\n".join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.count_movies}."


def get_top_actor():
    top_actor = Actor.objects.prefetch_related("starring_actor_movies").annotate(
        num_movies=Count("starring_actor_movies")).order_by("-num_movies", "full_name").first()

    if top_actor and top_actor.num_movies > 0:
        avg_rating = top_actor.starring_actor_movies.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        movies = ", ".join(mv.title for mv in top_actor.starring_actor_movies.all())
        return f"Top Actor: {top_actor.full_name}, starring in movies: {movies}, movies average rating: {avg_rating:.1f}"
    else:
        return ""


# Django queries 2:

def get_actors_by_movies_count():
    top_3_actors = Actor.objects.prefetch_related("actors_movies").annotate(
        num_movies=Count("actors_movies")).order_by("-num_movies", "full_name")[:3]

    if top_3_actors:
        result = []
        for a in top_3_actors:
            if a.num_movies:
                result.append(f"{a.full_name}, participated in {a.num_movies} movies")
        return "\n".join(result)
    else:
        return ""


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True
                    ).select_related("starring_actor"
                    ).prefetch_related("actors"
                    ).order_by("-rating", "title").first()

    if top_movie:
        starring_a = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"
        all_actors = ", ".join(a.full_name for a in top_movie.actors.order_by("full_name") if a.full_name)

        return (f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. "
                f"Starring actor: {starring_a}. Cast: {all_actors}.")

    else:
        return ""


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not classic_movies:
        return "No ratings increased."

    num_of_updated_movies = classic_movies.update(rating=F("rating") + 0.1)
    return f"Rating increased for {num_of_updated_movies} movies."



# Director.objects.create(full_name="Akira Kurosawa", years_of_experience=0, birth_date='1910-03-23', nationality='Unknown')
# Director.objects.create(full_name="Francis Ford Coppola", years_of_experience=50, birth_date='1939-04-07', nationality='Unknown')
# Director.objects.create(full_name="Martin Scorsese", years_of_experience=60, birth_date='1942-11-17', nationality='American and Italian')
#
# al_pacino = Actor.objects.create(full_name="Al Pacino", birth_date='1940-04-25', nationality='American')
# robert_duvall = Actor.objects.create(full_name="Robert Duvall", birth_date='1931-01-05', nationality='American')
# joaquin_phoenix = Actor.objects.create(full_name="Joaquin Phoenix", birth_date='1974-10-28', nationality='American')
#
# movie1 = Movie.objects.create(
#     title="The Godfather",
#     release_date="1972-03-24",
#     storyline="Storyline 1",
#     genre=Movie.GenreChoices.Drama,
#     rating=9.2,
#     is_classic=True,
#     director=Director.objects.get(full_name="Francis Ford Coppola"),
#     starring_actor=al_pacino,)
# movie2 = Movie.objects.create(
#     title="Apocalypse Now",
#     release_date="1979-08-15",
#     storyline="Storyline 2",
#     genre=Movie.GenreChoices.Drama,
#     rating=8.5,
#     is_classic=True,
#     director=Director.objects.get(full_name="Francis Ford Coppola"),
#     starring_actor=robert_duvall,)
# movie3 = Movie.objects.create(
#     title="Taxi Driver",
#     release_date="1976-02-08",
#     storyline="Storyline 3",
#     genre=Movie.GenreChoices.Drama,
#     rating=8.3,
#     is_classic=True,
#     director=Director.objects.get(full_name="Martin Scorsese"),
#     starring_actor=robert_duvall,)
# movie4 = Movie.objects.create(
#     title="Joker",
#     release_date="2019-10-04",
#     storyline="Storyline 4",
#     genre=Movie.GenreChoices.Drama,
#     rating=8.4,
#     is_classic=False,
#     director=Director.objects.get(full_name="Martin Scorsese"),
#     starring_actor=joaquin_phoenix,)
#
# movie1.actors.add(al_pacino)
# movie2.actors.add(al_pacino)
# movie2.actors.add(robert_duvall)
# movie3.actors.add(robert_duvall)
# movie4.actors.add(joaquin_phoenix)
