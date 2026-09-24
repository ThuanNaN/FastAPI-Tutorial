"""Auth endpoint tests — login, /api/auth/me, error cases."""


def test_login_gets_token(client, seeded_db):
    """POST /api/auth/login with valid credentials returns a Bearer token."""
    response = client.post("/api/auth/login", data={"username": "user", "password": "user123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_me_with_token(client, seeded_db):
    """GET /api/auth/me with a valid token returns the current user."""
    login = client.post("/api/auth/login", data={"username": "user", "password": "user123"})
    token = login.json()["access_token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "user"


def test_wrong_password_returns_400(client, seeded_db):
    """POST /api/auth/login with wrong password returns 400."""
    response = client.post("/api/auth/login", data={"username": "user", "password": "wrong"})
    assert response.status_code == 400


def test_missing_credentials_returns_401(client, seeded_db):
    """POST /api/auth/login with no credentials returns 401."""
    response = client.post("/api/auth/login", data={})
    assert response.status_code == 401
