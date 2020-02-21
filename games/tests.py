def test__list_games(logged_in_client, sample_game):
    resp = logged_in_client.get("/api/v1/game/", content_type="application/json")

    assert resp.status_code == 200

    result = resp.json()
    for item in result["results"]:
        assert item["name"] == sample_game["name"]


def test__retrieve_activity(logged_in_client, sample_game):
    resp = logged_in_client.get(
        f"/api/v1/game/{sample_game['id']}/", content_type="application/json"
    )

    result = resp.json()
    assert resp.status_code == 200
    assert result["name"] == sample_game["name"]
