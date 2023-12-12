import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Q, Count


# novak = TennisPlayer.objects.create(full_name="Novak Djokovic", birth_date="1987-05-22", country="SRB", ranking=1)
# grigor = TennisPlayer.objects.create(full_name="Grigor Dimitrov", birth_date="1991-05-16", country="BUL", ranking=15)
# coco = TennisPlayer.objects.create(full_name="Coco Vandeweghe", birth_date="1991-12-06", country="USA", ranking=300)
# ella = TennisPlayer.objects.create(full_name="Ella Seidel", birth_date="1999-03-18", country="GER", ranking=150)
#
# australian_open_2024 = Tournament.objects.create(name="Australian Open 2024", location="Australia", prize_money=1000000, start_date="2024-01-15")
# us_open_2023 = Tournament.objects.create(name="US Open 2023", location="USA", prize_money=900000, start_date="2023-08-22")
#
# match_us_open_1 = Match.objects.create(score="7:6(7:4) 6:3 6:4", summary="Stunning!", date_played="2023-08-31 22:00:00+00:00", tournament=us_open_2023)
# match_us_open_1.players.set([grigor, novak])
# match_us_open_1.winner = grigor
# match_us_open_1.save()
#
# match_suspended = Match.objects.create(score="7:6(7:4) 4:3 (suspended)", date_played="2023-06-10 19:00:00+00:00")
# match_suspended.players.set([grigor, novak])
#
# match_june_8 = Match.objects.create(score="7:6(11:9) 4:6 6:3 6:4", date_played="2023-06-08 19:00:00+00:00", tournament=us_open_2023, winner=novak)
# match_june_8.players.set([coco, novak])


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    q_name = Q(full_name__icontains=search_name) if search_name is not None else Q()
    q_country = Q(country__icontains=search_country) if search_country is not None else Q()

    players = TennisPlayer.objects.filter(q_name & q_country).order_by("ranking")

    if players:
        result = []
        for p in players:
            result.append(f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}")

        return "\n".join(result)

    return ""


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_player is None:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.num_wins} wins."


def get_tennis_player_by_matches_count():
    t_player = TennisPlayer.objects.annotate(num_matches=Count("matches_players")
                ).filter(num_matches__gt=0).order_by("-num_matches", "ranking").first()

    if t_player is None:
        return ""

    return f"Tennis Player: {t_player.full_name} with {t_player.num_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    searched_tournaments = Tournament.objects.prefetch_related("matches_tournament"
                            ).annotate(num_matches=Count("matches_tournament")
                            ).filter(surface_type__icontains=surface).order_by("-start_date")

    if searched_tournaments:
        result = []
        for t in searched_tournaments:
            result.append(f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}")

        return "\n".join(result)

    return ""


def get_latest_match_info():
    last_match = Match.objects.prefetch_related("players"
                ).order_by("-date_played", "-id").first()

    if last_match:
        players_last_match = last_match.players.order_by("full_name").all()
        player1_name = players_last_match[0]
        player2_name = players_last_match[1]
        winner_name = last_match.winner.full_name if last_match.winner is not None else "TBA"

        return (f"Latest match played on: {last_match.date_played}, "
                f"tournament: {last_match.tournament.name}, "
                f"score: {last_match.score}, players: {player1_name} vs {player2_name}, "
                f"winner: {winner_name}, summary: {last_match.summary}")

    return ""


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is not None:

        matches_by_tournament = Match.objects.prefetch_related("tournament"
            ).filter(tournament__name__exact=tournament_name).order_by('-date_played')

        if matches_by_tournament:
            result = []
            for m in matches_by_tournament:
                winner_name = m.winner.full_name if m.winner is not None else "TBA"
                result.append(f"Match played on: {m.date_played}, score: {m.score}, winner: {winner_name}")

            return "\n".join(result)

    return "No matches found."








