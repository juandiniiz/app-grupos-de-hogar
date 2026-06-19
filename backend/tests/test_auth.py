def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_login_success(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "admin1234"})
    assert res.status_code == 200


def test_login_wrong_password(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "wrong"})
    assert res.status_code == 401


def test_login_wrong_email(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "nobody@test.com", "password": "admin1234"})
    assert res.status_code == 401


def test_login_returns_token(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "admin1234"})
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 10


def test_get_me_success(client, admin_token):
    res = client.get("/api/auth/me", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["email"] == "admin@test.com"
    assert body["rol"] == "admin"


def test_get_me_no_token_returns_401(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401


def test_get_me_invalid_token_returns_401(client):
    res = client.get("/api/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert res.status_code == 401


def test_register_admin_only(client, admin_token, supervisor_token):
    res = client.post(
        "/api/auth/register",
        json={"email": "new@test.com", "password": "pass1234", "nombre": "New User", "rol": "responsable"},
        headers=auth(supervisor_token),
    )
    assert res.status_code == 403


def test_register_creates_user(client, admin_token):
    res = client.post(
        "/api/auth/register",
        json={"email": "newuser@test.com", "password": "newpass1234", "nombre": "New User", "rol": "responsable"},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["email"] == "newuser@test.com"
    assert body["rol"] == "responsable"

    res2 = client.post(
        "/api/auth/register",
        json={"email": "newuser@test.com", "password": "newpass1234", "nombre": "New User", "rol": "responsable"},
        headers=auth(admin_token),
    )
    assert res2.status_code == 400
