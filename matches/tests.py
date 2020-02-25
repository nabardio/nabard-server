from datetime import timedelta

from django.utils import timezone


def test__create_new_match(client, sample_game, sample_user, sample_robot):
    a_user = sample_user(prefix="a")
    b_user = sample_user(prefix="b")
    game = sample_game(owner_id=a_user["id"])
    a_robot = sample_robot(owner_id=a_user["id"], game_id=game["id"], prefix="a")
    b_robot = sample_robot(owner_id=b_user["id"], game_id=game["id"], prefix="b")

    client.login(username=a_user["username"], password=a_user["password"])

    match_input = {
        "home_robot": a_robot["id"],
        "away_robot": b_robot["id"],
        "start_at": timezone.now() + timedelta(minutes=5),
    }
    resp = client.post(
        "/api/v1/match/", data=match_input, content_type="application/json"
    )
    robot_result = resp.json()

    assert resp.status_code == 201
    assert robot_result["home_robot"] == a_robot["id"]
    assert robot_result["away_robot"] == b_robot["id"]


def test__create_new_match_with_start_at_right_now(
    client, sample_game, sample_user, sample_robot
):
    a_user = sample_user(prefix="a")
    b_user = sample_user(prefix="b")
    game = sample_game(owner_id=a_user["id"])
    a_robot = sample_robot(owner_id=a_user["id"], game_id=game["id"], prefix="a")
    b_robot = sample_robot(owner_id=b_user["id"], game_id=game["id"], prefix="b")

    client.login(username=a_user["username"], password=a_user["password"])

    match_input = {
        "home_robot": a_robot["id"],
        "away_robot": b_robot["id"],
        "start_at": timezone.now(),
    }
    resp = client.post(
        "/api/v1/match/", data=match_input, content_type="application/json"
    )

    assert resp.status_code == 400


def test__create_new_match_with_robot_not_owned(
    client, sample_game, sample_user, sample_robot
):
    a_user = sample_user(prefix="a")
    b_user = sample_user(prefix="b")
    game = sample_game(owner_id=a_user["id"])
    a_robot = sample_robot(owner_id=a_user["id"], game_id=game["id"], prefix="a")
    b_robot = sample_robot(owner_id=b_user["id"], game_id=game["id"], prefix="b")

    client.login(username=a_user["username"], password=a_user["password"])

    match_input = {
        "home_robot": b_robot["id"],
        "away_robot": a_robot["id"],
        "start_at": timezone.now() + timedelta(minutes=5),
    }
    resp = client.post(
        "/api/v1/match/", data=match_input, content_type="application/json"
    )

    assert resp.status_code == 400


def test__create_new_match_with_robot_both_owned(
    client, sample_game, sample_user, sample_robot
):
    a_user = sample_user(prefix="a")
    game = sample_game(owner_id=a_user["id"])
    a_robot = sample_robot(owner_id=a_user["id"], game_id=game["id"], prefix="a")
    b_robot = sample_robot(owner_id=a_user["id"], game_id=game["id"], prefix="b")

    client.login(username=a_user["username"], password=a_user["password"])

    match_input = {
        "home_robot": a_robot["id"],
        "away_robot": b_robot["id"],
        "start_at": timezone.now() + timedelta(minutes=5),
    }
    resp = client.post(
        "/api/v1/match/", data=match_input, content_type="application/json"
    )

    assert resp.status_code == 400


def test__create_new_match_with_robots_not_playing_the_same_game(
    client, sample_game, sample_user, sample_robot
):
    a_user = sample_user(prefix="a")
    b_user = sample_user(prefix="b")
    a_game = sample_game(owner_id=a_user["id"], prefix="a")
    b_game = sample_game(owner_id=a_user["id"], prefix="b")
    a_robot = sample_robot(owner_id=a_user["id"], game_id=a_game["id"], prefix="a")
    b_robot = sample_robot(owner_id=b_user["id"], game_id=b_game["id"], prefix="b")

    client.login(username=a_user["username"], password=a_user["password"])

    match_input = {
        "home_robot": a_robot["id"],
        "away_robot": b_robot["id"],
        "start_at": timezone.now() + timedelta(minutes=5),
    }
    resp = client.post(
        "/api/v1/match/", data=match_input, content_type="application/json"
    )
    print(resp.json())

    assert resp.status_code == 400


def test__list_matches(client, sample_match):
    match = sample_match(timedelta(minutes=2) + timezone.now())
    resp = client.get("/api/v1/match/", content_type="application/json")

    assert resp.status_code == 200

    result = resp.json()

    for m in result["results"]:
        assert m["home_robot"] == str(match["home_robot"].pk)
        assert m["away_robot"] == str(match["away_robot"].pk)


def test__retrieve_match(client, sample_match):
    match = sample_match(timedelta(minutes=2) + timezone.now())
    resp = client.get(f"/api/v1/match/{match['id']}/", content_type="application/json")

    result = resp.json()
    assert resp.status_code == 200
    assert result["home_robot"] == str(match["home_robot"].pk)
    assert result["away_robot"] == str(match["away_robot"].pk)


def test__delete_match(client, sample_user, sample_match):
    match = sample_match(timedelta(minutes=2) + timezone.now())

    user = sample_user(prefix="a")
    client.login(username=user["username"], password=user["password"])

    resp = client.delete(
        f"/api/v1/match/{match['id']}/", content_type="application/json",
    )

    assert resp.status_code == 204
