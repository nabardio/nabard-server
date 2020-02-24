def test__list_games(client, sample_user, sample_game):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    client.login(username=user["username"], password=user["password"])

    resp = client.get("/api/v1/game/", content_type="application/json")

    assert resp.status_code == 200

    result = resp.json()
    for item in result["results"]:
        assert item["name"] == game["name"]


def test__retrieve_game(client, sample_user, sample_game):
    user = sample_user()
    game = sample_game(owner_id=user["id"])
    client.login(username=user["username"], password=user["password"])

    resp = client.get(f"/api/v1/game/{game['id']}/", content_type="application/json")

    result = resp.json()
    assert resp.status_code == 200
    assert result["name"] == game["name"]
