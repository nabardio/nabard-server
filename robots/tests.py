from django.test.client import MULTIPART_CONTENT, BOUNDARY, encode_multipart


def test__register_new_user(logged_in_client, sample_game):
    robot_input = {"name": "test-robot", "game": sample_game["id"]}

    resp = logged_in_client.post(
        "/api/v1/robot/", data=robot_input, content_type="application/json"
    )
    robot_result = resp.json()

    assert resp.status_code == 201
    assert robot_result["name"] == robot_input["name"]


def test__list_my_robots(logged_in_client, sample_robot):
    resp = logged_in_client.get(
        f"/api/v1/robot/?owner={str(sample_robot['owner'].pk)}",
        content_type="application/json",
    )

    assert resp.status_code == 200

    result = resp.json()
    for item in result["results"]:
        assert item["name"] == sample_robot["name"]


def test__list_robots(client, sample_robot):
    resp = client.get("/api/v1/robot/", content_type="application/json")

    assert resp.status_code == 200

    result = resp.json()
    for item in result["results"]:
        assert item["name"] == sample_robot["name"]


def test__retrieve_robot(client, sample_robot):
    resp = client.get(
        f"/api/v1/robot/{sample_robot['id']}/", content_type="application/json"
    )

    result = resp.json()
    assert resp.status_code == 200
    assert result["name"] == sample_robot["name"]


def test__upload_code_for_robot(logged_in_client, sample_code, sample_robot):
    resp = logged_in_client.put(
        f"/api/v1/robot/{sample_robot['id']}/code/",
        encode_multipart(BOUNDARY, {"file": sample_code}),
        content_type=MULTIPART_CONTENT,
        format="multipart",
    )
    assert resp.status_code == 204


def test__update_robot(logged_in_client, sample_robot):
    resp = logged_in_client.put(
        f"/api/v1/robot/{sample_robot['id']}/",
        data={"name": "changed", "game": str(sample_robot["game"].pk)},
        content_type="application/json",
    )
    robot_result = resp.json()

    assert resp.status_code == 200
    assert robot_result["name"] == "changed"


def test__partial_update_user(logged_in_client, sample_robot):
    resp = logged_in_client.patch(
        f"/api/v1/robot/{sample_robot['id']}/",
        data={"name": "changed"},
        content_type="application/json",
    )
    robot_result = resp.json()

    assert resp.status_code == 200
    assert robot_result["name"] == "changed"


def test__delete_robot(logged_in_client, sample_robot):
    resp = logged_in_client.delete(
        f"/api/v1/robot/{sample_robot['id']}/", content_type="application/json",
    )

    assert resp.status_code == 204
