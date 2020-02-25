from io import BytesIO

import pytest
from django.core.files import File

from games.models import Game
from robots.models import Robot
from matches.models import Match


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def sample_user(django_user_model):
    def _generate_sample_user(prefix=""):
        user_input = {
            "first_name": f"{prefix}_test",
            "last_name": f"{prefix}_test",
            "username": f"{prefix}_test",
            "email": f"{prefix}_test@test.tld",
            "password": "P@ss4Test",
        }

        try:
            user = django_user_model.objects.get(username=f"{prefix}_test")
        except django_user_model.DoesNotExist:
            user = django_user_model.objects.create_user(**user_input)

        user_input["id"] = str(user.pk)
        return user_input

    return _generate_sample_user


@pytest.fixture
def sample_code():
    def _generate_sample_code(filename="test.py"):
        f = BytesIO("print('hello, world!')".encode())
        f.name = filename
        f.seek(0)
        return f

    return _generate_sample_code


@pytest.fixture
def sample_game(django_user_model, sample_user, sample_code):
    def _generate_sample_game(owner_id, prefix=""):
        code = sample_code()
        game_input = {
            "name": f"{prefix}_game",
            "description": f"description for {prefix}_game",
            "instruction": "long text describing how the game works and what to do?",
            "code": File(code),
            "owner": django_user_model.objects.get(pk=owner_id),
        }

        game = Game.objects.create(**game_input)
        game_input["id"] = str(game.pk)
        return game_input

    return _generate_sample_game


@pytest.fixture
def sample_robot(django_user_model, sample_user, sample_game, sample_code):
    def _generate_sample_robot(game_id, owner_id, prefix=""):
        code = sample_code()
        robot_input = {
            "name": f"{prefix}_robot",
            "game": Game.objects.get(pk=game_id),
            "code": File(code),
            "owner": django_user_model.objects.get(pk=owner_id),
        }

        robot = Robot.objects.create(**robot_input)
        robot_input["id"] = str(robot.pk)
        return robot_input

    return _generate_sample_robot


@pytest.fixture
def sample_match(sample_user, sample_game, sample_robot):
    def _generate_sample_match(start_at):
        a_user = sample_user(prefix="a")
        b_user = sample_user(prefix="b")
        game = sample_game(owner_id=a_user["id"])
        a_robot = sample_robot(owner_id=a_user["id"], game_id=game["id"], prefix="a")
        b_robot = sample_robot(owner_id=b_user["id"], game_id=game["id"], prefix="b")

        match_input = {
            "home_robot": Robot.objects.get(pk=a_robot["id"]),
            "away_robot": Robot.objects.get(pk=b_robot["id"]),
            "start_at": start_at,
            "game": Game.objects.get(pk=game["id"]),
        }

        match = Match.objects.create(**match_input)
        match_input["id"] = str(match.pk)
        return match_input

    return _generate_sample_match
