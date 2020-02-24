from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart


def test__create_new_robot(client, sample_user, sample_game):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot_input = {"name": "test-robot", "game": game["id"]}

    client.login(username=user["username"], password=user["password"])
    resp = client.post(
        "/api/v1/robot/", data=robot_input, content_type="application/json"
    )
    robot_result = resp.json()

    assert resp.status_code == 201
    assert robot_result["name"] == robot_input["name"]


def test__list_my_robots(client, sample_user, sample_game, sample_robot):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    client.login(username=user["username"], password=user["password"])
    resp = client.get(
        f"/api/v1/robot/?owner={str(robot['owner'].pk)}",
        content_type="application/json",
    )

    assert resp.status_code == 200

    result = resp.json()
    for item in result["results"]:
        assert item["name"] == robot["name"]


def test__list_robots(client, sample_user, sample_game, sample_robot):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    resp = client.get("/api/v1/robot/", content_type="application/json")

    assert resp.status_code == 200

    result = resp.json()
    for item in result["results"]:
        assert item["name"] == robot["name"]


def test__retrieve_robot(client, sample_user, sample_game, sample_robot):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    resp = client.get(f"/api/v1/robot/{robot['id']}/", content_type="application/json")

    result = resp.json()
    assert resp.status_code == 200
    assert result["name"] == robot["name"]


def test__upload_code_for_robot(
    client, sample_user, sample_game, sample_code, sample_robot
):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    client.login(username=user["username"], password=user["password"])
    resp = client.put(
        f"/api/v1/robot/{robot['id']}/code/",
        encode_multipart(BOUNDARY, {"file": sample_code()}),
        content_type=MULTIPART_CONTENT,
        format="multipart",
    )
    assert resp.status_code == 204


def test__update_robot(client, sample_user, sample_game, sample_robot):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    client.login(username=user["username"], password=user["password"])
    resp = client.put(
        f"/api/v1/robot/{robot['id']}/",
        data={"name": "changed", "game": str(robot["game"].pk)},
        content_type="application/json",
    )
    robot_result = resp.json()

    assert resp.status_code == 200
    assert robot_result["name"] == "changed"


def test__partial_update_robot(client, sample_user, sample_game, sample_robot):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    client.login(username=user["username"], password=user["password"])
    resp = client.patch(
        f"/api/v1/robot/{robot['id']}/",
        data={"name": "changed"},
        content_type="application/json",
    )
    robot_result = resp.json()

    assert resp.status_code == 200
    assert robot_result["name"] == "changed"


def test__delete_robot(client, sample_user, sample_game, sample_robot):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    robot = sample_robot(owner_id=user["id"], game_id=game["id"])

    client.login(username=user["username"], password=user["password"])
    resp = client.delete(
        f"/api/v1/robot/{robot['id']}/", content_type="application/json",
    )

    assert resp.status_code == 204
