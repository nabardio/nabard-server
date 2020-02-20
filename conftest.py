import pytest


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
