
# Secure File Sharing System

A secure file-sharing API built with FastAPI and PostgreSQL that supports two types of users:

* **Ops User**: Can login and upload files (`pptx`, `docx`, `xlsx` only).
* **Client User**: Can sign up, verify email, login, list files, and download files via secure encrypted URLs.

---

## Features

* User authentication with JWT tokens
* Email verification for Client Users
* Role-based access control (Ops vs Client)
* File upload with file type restrictions (only pptx, docx, xlsx)
* Secure encrypted download links for Client Users
* PostgreSQL database integration with SQLAlchemy ORM
* Fully tested with automated test cases

---

## Getting Started

### Prerequisites

* Python 3.10+
* PostgreSQL installed and running
* Virtual environment (recommended)

### Setup Steps

1. **Clone the repo and navigate to the project:**

   ```bash
   git clone <your-repo-url>
   cd secure_file_sharing
   ```

2. **Create and activate virtual environment:**

   Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Rename `.env.example` to `.env` and update values (especially `DATABASE_URL` and email settings).

5. **Create PostgreSQL database:**

   Connect to PostgreSQL and run:

   ```sql
   CREATE DATABASE filedb;
   ```

6. **Run database migrations (if applicable)**

7. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

---

## Accessing the API

* Open API docs at: `http://127.0.0.1:8000/docs`
* Use the interactive UI to test endpoints or
* Use the provided Postman collection for easier testing.

---

## Postman Collection

Import `secure_file_sharing_postman_collection.json` from the repo into Postman to test all API endpoints with ready-made requests.

---

## Running Tests

Run all automated test cases with:

```bash
pytest
```

Tests cover user signup, login, file upload, download, and authorization.
