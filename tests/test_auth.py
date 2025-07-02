def test_ops_login_invalid_user(client):
    response = client.post("/auth/login", data={"username": "no@user.com", "password": "123456"})
    assert response.status_code == 400

def test_client_signup_and_verify(client):
    # Signup
    response = client.post("/users/signup", json={"email": "client1@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert "verification_url" in response.json()

    # Extract token from URL and verify
    token = response.json()["verification_url"].split("token=")[1]
    verify_response = client.get(f"/users/verify-email?token={token}")
    assert verify_response.status_code == 200

def test_client_login_success(client):
    response = client.post("/auth/login", data={"username": "client1@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
