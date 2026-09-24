"""Upload endpoint tests — file upload."""


def test_upload_file(client):
    """POST /api/upload with a file returns 200."""
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", b"hello world", "text/plain")},
        data={"book_id": "1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["content_type"] == "text/plain"
    assert data["size"] == 11
