import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()



from main_app.models import Author, Article, Review

from django.db.models import Q, Count, Avg


# django queries 1:

def get_authors(search_name=None, search_email=None): # 2
    if search_name is None and search_email is None:
        return ""

    query_name = Q(full_name__icontains=search_name) if search_name is not None else Q()
    query_email = Q(email__icontains=search_email) if search_email is not None else Q()

    searched_authors = Author.objects.filter(query_name & query_email).order_by("-full_name")

    if searched_authors:
        result = []
        for author in searched_authors:
            result.append(f"Author: {author.full_name}, email: {author.email}, "
                          f"status: {'Banned' if author.is_banned else 'Not Banned'}")
        return "\n".join(result)

    return ""


def get_top_publisher(): # 2
    best_publisher = Author.objects.get_authors_by_article_count().first()

    if best_publisher is None or best_publisher.count_articles == 0:
        return ""

    return f"Top Author: {best_publisher.full_name} with {best_publisher.count_articles} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(num_reviews=Count("reviews_author")
                    ).filter(num_reviews__gt=0).order_by("-num_reviews", "email").first()

    if top_reviewer is None:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."


# django queries 2:

# def get_latest_art():
#     last_article = Article.objects.prefetch_related("authors").annotate(
#         num_reviews=Count("reviews_article"),
#         avg_rating=Avg("reviews_article__rating")
#     ).order_by("-published_on").first()
#
#     if last_article.exists():
#         author_names = ", ".join(author.full_name for author in last_article.authors.all().order_by('full_name'))
#
#         if last_article.num_reviews <= 0:
#             average_rating = 0
#         else:
#             average_rating = f"{last_article.avg_rating:.2f}"
#
#         return (f"The latest article is: {last_article.title}. "
#                 f"Authors: {author_names}. "
#                 f"Reviewed: {last_article.num_reviews} times. "
#                 f"Average Rating: {average_rating}.")
#     else:
#         return ""

def get_latest_article(): # 2
    latest_article = Article.objects.prefetch_related("authors").annotate(
        num_reviews=Count("reviews_article"),
        avg_rating=Avg("reviews_article__rating")
        ).order_by("-published_on").first()

    if latest_article:
        average_rating = 0
        if latest_article.num_reviews > 0:
            average_rating = latest_article.avg_rating

        all_authors = ", ".join([a.full_name for a in latest_article.authors.all()])

        return (f"The latest article is: {latest_article.title}. Authors: {all_authors}. "
                f"Reviewed: {latest_article.num_reviews} times. Average Rating: {average_rating:.2f}.")

    return ""


def get_top_rated_article():
    best_article = Article.objects.prefetch_related("reviews_article").annotate(
        num_reviews=Count("reviews_article"),
        avg_ratings=Avg("reviews_article__rating")
        ).filter(num_reviews__gt=0).order_by("-avg_ratings", "title").first()

    if best_article:
        return (f"The top-rated article is: {best_article.title}, "
                f"with an average rating of {best_article.avg_ratings:.2f}, "
                f"reviewed {best_article.num_reviews} times.")

    return ""


def ban_author(email=None):
    if email is not None:

        author_to_ban = Author.objects.filter(email__exact=email
                    ).annotate(num_reviews=Count("reviews_author")).first()

        if author_to_ban:
            author_to_ban.is_banned = True
            author_to_ban.save()
            author_to_ban.reviews_author.all().delete()
            return f"Author: {author_to_ban.full_name} is banned! {author_to_ban.num_reviews} reviews deleted."

    return "No authors banned."



# anna_williams = Author.objects.create(
#     full_name="Anna Williams",
#     email="aw@test.com",
#     is_banned=False,
#     birth_year=1990,
#     website="http://annawilliams.com"
# )
# adam_smith = Author.objects.create(
#     full_name="Adam Smith",
#     email="as@dev.com",
#     is_banned=False,
#     birth_year=1985,
#     website="http://adamsmith.com"
# )
# test_article = Article.objects.create(
#     title="Test Article",
#     content="This is a test article content.",
#     category=Article.CategoryChoices.Technology
# )
# second_test_article = Article.objects.create(
#     title="Second Test Article",
#     content="This is another test article by Anna Williams.",
#     category=Article.CategoryChoices.Science
# )
# test_article.authors.add(anna_williams, adam_smith)
# second_test_article.authors.add(anna_williams)
#
# review_1 = Review.objects.create(
#     content="Great article!",
#     rating=5.0,
#     author=adam_smith,
#     article=test_article
# )
# review_2 = Review.objects.create(
#     content="Interesting read.",
#     rating=4.8,
#     author=adam_smith,
#     article=test_article
# )
# review_3 = Review.objects.create(
#     content="Cool!",
#     rating=4.9,
#     author=anna_williams,
#     article=second_test_article
# )
