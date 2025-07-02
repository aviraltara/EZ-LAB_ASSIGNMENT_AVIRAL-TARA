def test_create_duplicate_user(client):
    response = client.post("/users/signup", json={"email": "client1@example.com", "password": "testpass"})
    assert response.status_code == 400
