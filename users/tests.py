def test__register_new_user(client, django_user_model):
    user_input = {
        "first_name": "test",
        "last_name": "test",
        "username": "test",
        "email": "test@test.tld",
        "password": "P@ss4Test",
    }

    resp = client.post(
        "/api/v1/user/", data=user_input, content_type="application/json"
    )
    user_result = resp.json()

    assert resp.status_code == 201

    user_input.pop("password")
    for k, v in user_input.items():
        assert user_result[k] == v
    
    # Check for user that isn't active
    assert not django_user_model.objects.get(id=user_result["id"]).is_active


def test__register_new_user_with_simple_password(client):
    user_input = {
        "first_name": "test",
        "last_name": "test",
        "username": "test",
        "email": "test@test.tld",
        "password": "simple",
    }

    resp = client.post(
        "/api/v1/user/", data=user_input, content_type="application/json"
    )

    assert resp.status_code == 400


def test__activate_user(client, sample_no_login_user, generate_uid_and_token):
    user = sample_no_login_user("active_user")
    uid, token = generate_uid_and_token(user["id"])

    resp = client.get(
        f"/api/v1/user/auth/activate/{uid}/{token}/",
        content_type="application/json",
    )

    assert resp.status_code == 204


def test__activate_user_with_wrong_uid(client, sample_no_login_user, generate_uid_and_token):
    user = sample_no_login_user()
    _, token = generate_uid_and_token(user["id"])

    resp = client.get(
        f"/api/v1/user/auth/activate/UIDB64/{token}/",
        content_type="application/json",
    )

    assert resp.status_code == 400


def test__activate_user_with_wrong_token(client, sample_no_login_user, generate_uid_and_token):
    user = sample_no_login_user()
    uid, _ = generate_uid_and_token(user["id"])

    resp = client.get(
        f"/api/v1/user/auth/activate/{uid}/TOKEN/",
        content_type="application/json",
    )

    assert resp.status_code == 400


def test__activate_user_with_wrong_data(client):
    resp = client.get(
        "/api/v1/user/auth/activate/UIDB64/TOKEN/",
        content_type="application/json",
    )

    assert resp.status_code == 400


def test__login_user_with_username(client, sample_user):
    user = sample_user()
    resp = client.post(
        "/api/v1/user/auth/",
        data={"username": user["username"], "password": user["password"]},
        content_type="application/json",
    )

    assert resp.status_code == 200


def test__login_not_active_user_with_username(client, sample_no_login_user):
    user = sample_no_login_user()

    resp = client.post(
        "/api/v1/user/auth/",
        data={"username": user["username"], "password": user["password"]},
        content_type="application/json",
    )

    assert resp.status_code == 403


def test__login_user_with_email(client, sample_user):
    user = sample_user()
    resp = client.post(
        "/api/v1/user/auth/",
        data={"email": user["email"], "password": user["password"]},
        content_type="application/json",
    )

    assert resp.status_code == 200


def test__login_not_active_user_with_email(client, sample_no_login_user):
    user = sample_no_login_user()

    resp = client.post(
        "/api/v1/user/auth/",
        data={"email": user["email"], "password": user["password"]},
        content_type="application/json",
    )

    assert resp.status_code == 403


def test__login_user_with_wrong_username(client, sample_user):
    user = sample_user()
    resp = client.post(
        "/api/v1/user/auth/",
        data={"username": "wrong", "password": user["password"]},
        content_type="application/json",
    )

    assert resp.status_code == 404


def test__login_user_with_wrong_password(client, sample_user):
    user = sample_user()
    resp = client.post(
        "/api/v1/user/auth/",
        data={"username": user["username"], "password": "wrong-password"},
        content_type="application/json",
    )

    assert resp.status_code == 403


def test__login_with_empty_request_body(client):
    user_input = {}

    resp = client.post(
        "/api/v1/user/auth/", data=user_input, content_type="application/json"
    )

    assert resp.status_code == 400


def test__logout_user(client, sample_user):
    user = sample_user()
    client.login(username=user["username"], password=user["password"])
    resp = client.delete("/api/v1/user/auth/", content_type="application/json")

    assert resp.status_code == 204


def test__retrieve_user(client, sample_user):
    user = sample_user()
    client.login(username=user["username"], password=user["password"])
    resp = client.get(
        f"/api/v1/user/{user['username']}/", content_type="application/json"
    )

    assert resp.status_code == 200


def test__get_profile(client, sample_user):
    user = sample_user()
    client.login(username=user["username"], password=user["password"])
    resp = client.get("/api/v1/user/", content_type="application/json")

    assert resp.status_code == 200


def test__get_profile_unauthenticated(client):
    resp = client.get("/api/v1/user/", content_type="application/json")

    assert resp.status_code == 403


def test__update_user(client, sample_user):
    user = sample_user()
    client.login(username=user["username"], password=user["password"])
    resp = client.put(
        f"/api/v1/user/{user['username']}/",
        data={
            "first_name": "changed",
            "last_name": "changed",
            "username": user["username"],
            "email": user["email"],
            "password": user["password"],
        },
        content_type="application/json",
    )
    user_result = resp.json()

    assert resp.status_code == 200
    assert user_result["first_name"] == "changed"
    assert user_result["last_name"] == "changed"


def test__partial_update_user(client, sample_user):
    user = sample_user()
    client.login(username=user["username"], password=user["password"])
    resp = client.patch(
        f"/api/v1/user/{user['username']}/",
        data={"first_name": "changed", "last_name": "changed"},
        content_type="application/json",
    )
    user_result = resp.json()

    assert resp.status_code == 200
    assert user_result["first_name"] == "changed"
    assert user_result["last_name"] == "changed"
