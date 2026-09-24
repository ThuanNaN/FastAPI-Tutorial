"""Books endpoint tests — listing, creating, retrieval, 404."""


def test_list_books(client):
    """GET /api/books returns 200 and a list."""
    response = client.get("/api/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_book_with_auth(client, seeded_db):
    """POST /api/books with a valid token creates a book and returns 201."""
    login = client.post("/api/auth/login", data={"username": "user", "password": "user123"})
    token = login.json()["access_token"]
    book_data = {"title": "Test Book", "author": "Test Author", "price": 10.0}
    response = client.post("/api/books", json=book_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"


def test_get_book_by_id(client, seeded_db):
    """GET /api/books/{id} with an existing book returns 200."""
    # Seed a book via the auth-required create endpoint
    login = client.post("/api/auth/login", data={"username": "user", "password": "user123"})
    token = login.json()["access_token"]
    book_data = {"title": "My Book", "author": "Author", "price": 5.0}
    create = client.post("/api/books", json=book_data, headers={"Authorization": f"Bearer {token}"})
    book_id = create.json()["id"]

    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "My Book"


def test_get_book_404(client):
    """GET /api/books/{id} for a non-existent book returns 404."""
    response = client.get("/api/books/9999")
    assert response.status_code == 404
