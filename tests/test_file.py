import io
from app.auth.routes import get_db
from app.auth.utils import hash_password
from app.models import User

def login(client, email, password):
    return client.post("/auth/login", data={"username": email, "password": password})

def upload_file(client, token, filename, content, mime_type):
    return client.post(
        "/files/upload",
        files={"file": (filename, io.BytesIO(content.encode()), mime_type)},
        headers={"Authorization": f"Bearer {token}"}
    )

def test_ops_user_upload_and_client_download(client):
    # 1. Create ops user directly in DB
    db = next(client.app.dependency_overrides[get_db]())
    ops_user = User(email="ops@example.com", password=hash_password("opspass"), role="ops", is_verified=True)
    db.add(ops_user)
    db.commit()

    # 2. Login as ops
    ops_login = login(client, "ops@example.com", "opspass")
    ops_token = ops_login.json()["access_token"]

    # 3. Upload valid file
    upload_response = upload_file(client, ops_token, "report.docx", "hello world", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert upload_response.status_code == 200

    # 4. Login as client
    client_login = login(client, "client1@example.com", "testpass")
    client_token = client_login.json()["access_token"]

    # 5. List files
    list_response = client.get("/files/list", headers={"Authorization": f"Bearer {client_token}"})
    assert list_response.status_code == 200
    file_id = list_response.json()[0]["id"]

    # 6. Get secure download link
    download_link_res = client.get(f"/files/download-file/{file_id}", headers={"Authorization": f"Bearer {client_token}"})
    assert download_link_res.status_code == 200
    assert "download-link" in download_link_res.json()

    # 7. Follow the download link
    token_url = download_link_res.json()["download-link"].split("/secure-download/")[1]
    final_response = client.get(f"/files/secure-download/{token_url}")
    assert final_response.status_code == 200
    assert final_response.content == b"hello world"
