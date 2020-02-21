import pytest
from games.models import Game
from django.core.files import File
from io import BytesIO


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
    file = BytesIO("print('hello, world!')".encode())
    file.name = "test.py"
    file.seek(0)
    return file


@pytest.fixture
def sample_game(django_user_model, sample_user, sample_code):
    owner = django_user_model.objects.get(username=sample_user["username"])
    game_input = {
        "name": "test_game",
        "description": "description for test_game",
        "instruction": "long text describing how the game works and what to do?",
        "code": File(sample_code),
        "owner": owner,
    }

    game = Game.objects.create(**game_input)
    game_input["id"] = game.pk

    return game_input
