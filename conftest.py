from io import BytesIO

import pytest
from django.core.files import File

from games.models import Game
from robots.models import Robot


def generate_sample_file():
    f = BytesIO("print('hello, world!')".encode())
    f.name = "test.py"
    f.seek(0)
    return f


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def sample_user(django_user_model):
    user_input = {
        "first_name": "test",
        "last_name": "test",
        "username": "test",
        "email": "test@test.tld",
        "password": "P@ss4Test",
    }

    django_user_model.objects.create_user(**user_input)
    return user_input


@pytest.fixture
def logged_in_client(sample_user, client):
    client.login(username=sample_user["username"], password=sample_user["password"])
    return client


@pytest.fixture
def sample_code():
    return generate_sample_file()


@pytest.fixture
def sample_game(django_user_model, sample_user):
    code = generate_sample_file()

    owner = django_user_model.objects.get(username=sample_user["username"])
    game_input = {
        "name": "test_game",
        "description": "description for test_game",
        "instruction": "long text describing how the game works and what to do?",
        "code": File(code),
        "owner": owner,
    }

    game = Game.objects.create(**game_input)
    game_input["id"] = str(game.pk)

    return game_input


@pytest.fixture
def sample_robot(django_user_model, sample_user, sample_game):
    code = generate_sample_file()

    owner = django_user_model.objects.get(username=sample_user["username"])
    game = Game.objects.get(pk=sample_game["id"])
    robot_input = {
        "name": "test_robot",
        "game": game,
        "code": File(code),
        "owner": owner,
    }

    robot = Robot.objects.create(**robot_input)
    robot_input["id"] = str(robot.pk)

    return robot_input
