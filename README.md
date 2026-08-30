# 🐳 Docker Learning App

A small learning project designed to understand how a **GUI application**, **FastAPI backend**, and **PostgreSQL database** work together.

The project is intentionally kept small so that the architecture and communication between each component are easy to understand.

Docker and Docker Compose will be introduced in the next stage after the non-Docker application is fully understood.

---

## 🎯 Project Goal

The purpose of this project is to learn the fundamentals of building a multi-component application:

* 🖥️ PySide6 GUI
* ⚡ FastAPI backend
* 🐘 PostgreSQL database
* 🐍 Python
* 📦 `uv` for Python dependency management
* 🧪 Pytest for automated testing
* 🐳 Docker
* 🎼 Docker Compose

The application is a simple **Message Manager** supporting CRUD operations:

* ➕ Create messages
* 📥 Get messages
* ✏️ Update messages
* 🗑️ Delete messages

---

# 🏗️ Architecture

## Current Architecture — Before Docker

```text
                         🖥️ USER
                            │
                            ▼
                  ┌──────────────────┐
                  │   🖥️ PySide6 GUI │
                  │                  │
                  │  📥 GET          │
                  │  ➕ CREATE       │
                  │  ✏️ UPDATE       │
                  │  🗑️ DELETE       │
                  └────────┬─────────┘
                           │
                           │ HTTP / JSON
                           ▼
                  ┌──────────────────┐
                  │   ⚡ FastAPI     │
                  │     Backend      │
                  │                  │
                  │ GET /messages    │
                  │ POST /messages   │
                  │ PUT /messages/{id}
                  │ DELETE /messages/{id}
                  └────────┬─────────┘
                           │
                           │ SQL
                           ▼
                  ┌──────────────────┐
                  │ 🐘 PostgreSQL    │
                  │                  │
                  │ docker_learning  │
                  │                  │
                  │   messages       │
                  └──────────────────┘
```

---

# 🔄 Application Flow

The application follows a three-layer architecture:

```text
🖥️ GUI
  │
  │ HTTP / JSON
  ▼
⚡ Backend
  │
  │ SQL
  ▼
🐘 PostgreSQL
```

### Example — Create Message

```text
👤 User
  │
  │ enters "Hello Docker"
  ▼
🖥️ PySide6 GUI
  │
  │ POST /messages
  │
  │ {
  │   "message": "Hello Docker"
  │ }
  ▼
⚡ FastAPI
  │
  │ INSERT INTO messages
  ▼
🐘 PostgreSQL
  │
  │ message stored
  ▼
⚡ FastAPI
  │
  │ JSON response
  ▼
🖥️ PySide6 GUI
  │
  ▼
📋 Message displayed
```

---

# 🔄 CRUD Architecture

The four GUI operations map directly to HTTP operations and SQL operations.

| 🖥️ GUI    | 🌐 HTTP  | ⚡ Backend      | 🐘 PostgreSQL |
| ---------- | -------- | -------------- | ------------- |
| 📥 GET     | `GET`    | Read messages  | `SELECT`      |
| ➕ CREATE   | `POST`   | Create message | `INSERT`      |
| ✏️ UPDATE  | `PUT`    | Update message | `UPDATE`      |
| 🗑️ DELETE | `DELETE` | Delete message | `DELETE`      |

```text
             CRUD
              │
     ┌────────┼────────┐
     │        │        │
   CREATE    READ    UPDATE    DELETE
     │        │        │        │
    POST      GET      PUT     DELETE
     │        │        │        │
     └────────┴────────┴────────┘
                    │
                    ▼
              🐘 PostgreSQL
```

---

# 📁 Project Structure

```text
Docker-Learning-App/
│
├── 📄 README.md
├── 📄 pyproject.toml
├── 📄 uv.lock
├── 📄 .python-version
├── 🔐 .env
│
├── ⚡ backend/
│   ├── 📄 __init__.py
│   └── 📄 main.py
│
├── 🐘 database/
│   ├── 📄 __init__.py
│   ├── 📄 database.py
│   └── 📄 init.sql
│
├── 🖥️ gui/
│   └── 📄 main.py
│
└── 🧪 tests/
    └── 📄 test_database.py
```

---

# 🧩 Components

## 🖥️ GUI — PySide6

Location:

```text
gui/main.py
```

The GUI provides four operations:

```text
📥 GET
➕ CREATE
✏️ UPDATE
🗑️ DELETE
```

It communicates with the backend using HTTP requests.

```text
GUI
 │
 │ HTTP
 ▼
FastAPI
```

The GUI does **not** communicate directly with PostgreSQL.

---

## ⚡ Backend — FastAPI

Location:

```text
backend/main.py
```

The backend exposes REST API endpoints.

Responsibilities:

* 🌐 Receive HTTP requests
* ✅ Validate input
* 🧠 Handle application logic
* 🐘 Call the database layer
* 📦 Return JSON responses

---

## 🐘 Database Layer

Location:

```text
database/database.py
```

Responsibilities:

* 🔌 PostgreSQL connection
* ➕ Insert messages
* 📥 Read messages
* ✏️ Update messages
* 🗑️ Delete messages

The database layer uses:

```text
psycopg
```

to communicate with PostgreSQL.

---

# 🗄️ Database Design

Database:

```text
docker_learning
```

Schema:

```text
public
```

Table:

```text
messages
```

Table structure:

```text
┌─────────────────────────┐
│       messages          │
├─────────────────────────┤
│ id       SERIAL  PK     │
│ message  TEXT    NOT NULL│
└─────────────────────────┘
```

Example:

```text
 id | message
----+-------------------------------
  1 | Hello from PostgreSQL
  2 | Hello from Python
  3 | Learning Docker
```

---

# 🔐 Environment Configuration

Database configuration is stored in:

```text
.env
```

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=docker_learning
POSTGRES_USER=learning_user
POSTGRES_PASSWORD=learning_password
```

⚠️ **Do not commit `.env` to Git.**

Add it to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
```

---

# 🐍 Python Environment

This project uses:

```text
uv
```

instead of `pip`.

`uv` manages:

* 🐍 Python environment
* 📦 Dependencies
* 🔒 Lock file
* ⚡ Fast package installation

The project has a single:

```text
pyproject.toml
```

at the project root.

```text
Docker-Learning-App/
│
└── pyproject.toml
```

There are **no separate `pyproject.toml` files** for the backend or GUI.

---

# 📦 Install Dependencies

From the project root:

```bash
cd ~/MyWorkSpace/Docker-Learning-App
```

Install/synchronize dependencies:

```bash
uv sync
```

If adding a new dependency:

```bash
uv add <package>
```

Example:

```bash
uv add requests
```

For development dependencies:

```bash
uv add --dev pytest
```

---

# 🐘 PostgreSQL Setup

## Check PostgreSQL

```bash
psql --version
```

Check the PostgreSQL service:

```bash
sudo service postgresql status
```

Start PostgreSQL if required:

```bash
sudo service postgresql start
```

---

## Connect as PostgreSQL administrator

```bash
sudo -u postgres psql
```

---

## Create database

```sql
CREATE DATABASE docker_learning;
```

---

## Create application user

```sql
CREATE USER learning_user
WITH PASSWORD 'learning_password';
```

Grant database access:

```sql
GRANT ALL PRIVILEGES
ON DATABASE docker_learning
TO learning_user;
```

Grant schema permissions:

```sql
\c docker_learning

GRANT USAGE, CREATE
ON SCHEMA public
TO learning_user;
```

---

# 🗃️ Create Database Table

Connect as the application user:

```bash
psql \
    -U learning_user \
    -d docker_learning \
    -h localhost
```

Then:

```sql
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL
);
```

Verify:

```sql
\dt
```

Check the table:

```sql
\d messages
```

---

# 🧪 Database Tests

Database tests are located at:

```text
tests/test_database.py
```

Run all tests:

```bash
uv run python -m pytest
```

Run with verbose output:

```bash
uv run python -m pytest -v
```

Example:

```text
============================= test session starts =============================

tests/test_database.py::test_get_connection PASSED
tests/test_database.py::test_create_message PASSED
tests/test_database.py::test_get_messages PASSED
tests/test_database.py::test_create_and_get_message PASSED
tests/test_database.py::test_create_multiple_messages PASSED
tests/test_database.py::test_update_message PASSED
tests/test_database.py::test_update_nonexistent_message PASSED
tests/test_database.py::test_delete_message PASSED
tests/test_database.py::test_delete_nonexistent_message PASSED

============================== 9 passed ==============================
```

Current database test coverage includes:

```text
🔌 Connection
➕ Create
📥 Read
✏️ Update
🗑️ Delete
🔁 Multiple records
❌ Non-existent update
❌ Non-existent delete
```

---

# ⚡ Run the Backend

From the project root:

```bash
uv run uvicorn backend.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

or:

```text
http://localhost:8000
```

---

# 📚 FastAPI Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

You'll see:

```text
GET     /messages
POST    /messages
PUT     /messages/{message_id}
DELETE  /messages/{message_id}
```

There is also an alternative documentation interface:

```text
http://localhost:8000/redoc
```

---

# 🌐 API Endpoints

## 📥 GET Messages

```http
GET /messages
```

Example response:

```json
[
    {
        "id": 1,
        "message": "Hello Docker"
    },
    {
        "id": 2,
        "message": "Learning PostgreSQL"
    }
]
```

---

## ➕ CREATE Message

```http
POST /messages
```

Request:

```json
{
    "message": "Hello Docker"
}
```

Response:

```json
{
    "id": 3,
    "message": "Hello Docker"
}
```

---

## ✏️ UPDATE Message

```http
PUT /messages/3
```

Request:

```json
{
    "message": "Learning Docker Compose"
}
```

Response:

```json
{
    "id": 3,
    "message": "Learning Docker Compose"
}
```

---

## 🗑️ DELETE Message

```http
DELETE /messages/3
```

Response:

```json
{
    "id": 3,
    "message": "Message deleted successfully."
}
```

---

# 🖥️ Run the GUI

Make sure PostgreSQL is running.

Also make sure the FastAPI backend is running.

### Terminal 1 — Backend

```bash
cd ~/MyWorkSpace/Docker-Learning-App

uv run uvicorn backend.main:app --reload
```

### Terminal 2 — GUI

```bash
cd ~/MyWorkSpace/Docker-Learning-App

uv run python gui/main.py
```

---

# 🖥️ GUI Workflow

The GUI provides four buttons:

```text
┌──────────────────────────────────────────┐
│       🐳 Docker Learning App             │
│                                          │
│ Message:                                 │
│ ┌──────────────────────────────────────┐ │
│ │ Hello Docker                         │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ [📥 GET] [➕ CREATE] [✏️ UPDATE] [🗑️ DELETE] │
│                                          │
│ 📋 All Messages                          │
│ ┌──────────────────────────────────────┐ │
│ │ 1 | Hello PostgreSQL                 │ │
│ │ 2 | Learning Python                  │ │
│ │ 3 | Hello Docker                     │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ Status: ✅ Loaded 3 message(s)           │
└──────────────────────────────────────────┘
```

---

# 🔄 GUI Request Flow

## 📥 GET

```text
🖥️ User
  │
  │ Click 📥 GET
  ▼
🖥️ PySide6
  │
  │ GET /messages
  ▼
⚡ FastAPI
  │
  │ SELECT
  ▼
🐘 PostgreSQL
  │
  │ rows
  ▼
⚡ FastAPI
  │
  │ JSON
  ▼
🖥️ PySide6
  │
  ▼
📋 Display messages
```

---

## ➕ CREATE

```text
🖥️ User
  │
  │ Enter message
  │
  │ Click ➕ CREATE
  ▼
🖥️ PySide6
  │
  │ POST /messages
  ▼
⚡ FastAPI
  │
  │ INSERT
  ▼
🐘 PostgreSQL
  │
  │ New record
  ▼
⚡ FastAPI
  │
  ▼
🖥️ PySide6
  │
  ▼
📋 Refresh messages
```

---

## ✏️ UPDATE

```text
🖥️ User
  │
  │ Select message
  │ Edit text
  │
  │ Click ✏️ UPDATE
  ▼
🖥️ PySide6
  │
  │ PUT /messages/{id}
  ▼
⚡ FastAPI
  │
  │ UPDATE
  ▼
🐘 PostgreSQL
  │
  ▼
⚡ FastAPI
  │
  ▼
🖥️ PySide6
  │
  ▼
📋 Refresh messages
```

---

## 🗑️ DELETE

```text
🖥️ User
  │
  │ Select message
  │
  │ Click 🗑️ DELETE
  ▼
🖥️ PySide6
  │
  │ DELETE /messages/{id}
  ▼
⚡ FastAPI
  │
  │ DELETE
  ▼
🐘 PostgreSQL
  │
  ▼
⚡ FastAPI
  │
  ▼
🖥️ PySide6
  │
  ▼
📋 Refresh messages
```

---

# 🧪 Testing Architecture

The project currently tests the database layer.

```text
                 🧪 Pytest
                    │
                    ▼
             database/database.py
                    │
                    │ psycopg
                    ▼
             🐘 PostgreSQL
```

Future testing layers:

```text
                    🧪 Tests
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
     🐘 Database    ⚡ API       🖥️ GUI
       Tests        Tests        Tests
```

---

# 🛠️ Development Workflow

A typical development session:

```text
1️⃣ Start PostgreSQL
       │
       ▼
2️⃣ Start FastAPI
       │
       ▼
3️⃣ Start PySide6 GUI
       │
       ▼
4️⃣ Test CRUD operations
       │
       ▼
5️⃣ Run automated tests
```

Commands:

### 1️⃣ PostgreSQL

```bash
sudo service postgresql start
```

### 2️⃣ Backend

```bash
uv run uvicorn backend.main:app --reload
```

### 3️⃣ GUI

Open another terminal:

```bash
uv run python gui/main.py
```

### 4️⃣ Tests

```bash
uv run python -m pytest -v
```

---

# 🛑 Stop the Application

## Stop FastAPI

In the backend terminal:

```text
Ctrl + C
```

## Stop GUI

In the GUI terminal:

```text
Ctrl + C
```

The GUI has been configured to handle `Ctrl+C` and terminate gracefully.

## Stop PostgreSQL

```bash
sudo service postgresql stop
```

---

# 🧠 What We Have Learned So Far

This project currently demonstrates:

### 🐍 Python

* Python project structure
* Virtual environments
* Dependencies
* `uv`

### 🖥️ PySide6

* GUI windows
* Widgets
* Buttons
* Signals and slots
* Event handling
* HTTP requests from GUI

### ⚡ FastAPI

* REST API
* Routes
* HTTP methods
* JSON
* Request models
* Response handling
* API documentation

### 🐘 PostgreSQL

* Database
* Schema
* Tables
* SQL
* CRUD operations
* Database users
* Permissions

### 🌐 Application Communication

```text
GUI
 │
 │ HTTP / JSON
 ▼
FastAPI
 │
 │ SQL
 ▼
PostgreSQL
```

### 🧪 Testing

* Pytest
* Database integration tests
* CRUD testing
* Positive and negative test cases

---

# 🐳 Docker — Next Stage

Docker has **not yet been introduced** into the current application.

The current application runs directly on the development environment:

```text
🖥️ Windows
    │
    ▼
🐧 WSL / Ubuntu
    │
    ├── 🖥️ PySide6
    │
    ├── ⚡ FastAPI
    │
    └── 🐘 PostgreSQL
```

The next stage will introduce Docker.

---

# 🐳 Target Docker Architecture

After Dockerization, we will move toward:

```text
                       🎼 Docker Compose
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
       🖥️ GUI Container  ⚡ Backend       🐘 PostgreSQL
                            Container          Container
              │               │               │
              └───────────────┼───────────────┘
                              │
                         Docker Network
```

The important learning progression will be:

```text
1️⃣ Understand application without Docker
        ↓
2️⃣ Dockerize PostgreSQL
        ↓
3️⃣ Dockerize FastAPI
        ↓
4️⃣ Understand Docker networking
        ↓
5️⃣ Understand volumes
        ↓
6️⃣ Introduce Docker Compose
        ↓
7️⃣ Run the complete application
```

---

# 🎓 Learning Objective

The final goal is not just to make the application run.

The goal is to understand **why containers are useful**.

We will compare:

```text
❌ Without Docker

"Install PostgreSQL"
"Configure PostgreSQL"
"Install Python"
"Install dependencies"
"Configure environment"
"Start backend"
"Start GUI"
```

with:

```text
🐳 With Docker

docker compose up
```

while understanding what Docker is actually doing behind the scenes.

---

# 📌 Current Status

```text
✅ Project created with uv
✅ Root pyproject.toml
✅ Backend created
✅ FastAPI API created
✅ PostgreSQL configured
✅ Database layer created
✅ CRUD implemented
✅ GUI created
✅ GUI CRUD operations implemented
✅ GUI logging added
✅ Ctrl+C support added
✅ Database tests added
⬜ API tests
⬜ GUI tests
⬜ Dockerfile
⬜ Docker image
⬜ Docker container
⬜ Docker networking
⬜ Docker volume
⬜ Docker Compose
```

---

# 🚀 Quick Start

For an already-configured development environment:

### Start PostgreSQL

```bash
sudo service postgresql start
```

### Start Backend

```bash
uv run uvicorn backend.main:app --reload
```

### Start GUI

In another terminal:

```bash
uv run python gui/main.py
```

### Run Tests

```bash
uv run python -m pytest -v
```

### API Documentation

Open:

```text
http://localhost:8000/docs
```

---

# 🐳 Coming Next

**Dockerize this application step by step.**

We'll learn:

```text
🐳 What is Docker?
📦 What is an Image?
🚢 What is a Container?
🌐 What is a Docker Network?
💾 What is a Docker Volume?
📝 What is a Dockerfile?
🎼 What is Docker Compose?
```

Then we'll transform:

```text
🖥️ GUI
   ↓
⚡ FastAPI
   ↓
🐘 PostgreSQL
```

into a reproducible Docker-based application.

---

## ⭐ Project Philosophy

> **Keep it small. Understand every layer. Then containerize it.**

This project is intentionally simple so that Docker concepts can be learned through a real application rather than isolated examples.
