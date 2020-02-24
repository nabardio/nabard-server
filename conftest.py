from io import BytesIO

import pytest
from django.core.files import File

from games.models import Game
from robots.models import Robot


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def sample_user(django_user_model):
    def _generate_sample_user(prefix=""):
        try:
            user = django_user_model.objects.get(username=f"{prefix}_test")
            return user
        except django_user_model.DoesNotExist:
            pass

        user_input = {
            "first_name": f"{prefix}_test",
            "last_name": f"{prefix}_test",
            "username": f"{prefix}_test",
            "email": f"{prefix}_test@test.tld",
            "password": "P@ss4Test",
        }

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
