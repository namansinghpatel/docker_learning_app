# 🐳 Docker Learning App

A small learning project for understanding how a **GUI**, a **backend API**, and a **database**
work together — first without Docker, then with it.

**Stack:** PySide6 (GUI) → FastAPI (backend) → PostgreSQL (database), using `psycopg` and
managed with `uv`.

The app is a simple **Message Manager** with full CRUD: Create, Read, Update, Delete.

---

## 🏗️ Architecture

```text
🖥️ PySide6 GUI  --HTTP/JSON-->  ⚡ FastAPI Backend  --SQL-->  🐘 PostgreSQL
```

| GUI action | HTTP        | Backend        | SQL      |
| ---------- | ----------- | -------------- | -------- |
| 📥 GET     | `GET`       | Read messages  | `SELECT` |
| ➕ CREATE  | `POST`      | Create message | `INSERT` |
| ✏️ UPDATE  | `PUT`       | Update message | `UPDATE` |
| 🗑️ DELETE | `DELETE`    | Delete message | `DELETE` |

## 📁 Project Structure

```text
docker_learning_app/
├── README.md
├── pyproject.toml / uv.lock
├── .env                    # DB credentials (used for local + docker compose)
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   └── main.py             # FastAPI app
├── database/
│   ├── database.py         # psycopg data access layer
│   └── init.sql            # auto-creates the `messages` table in Postgres
├── gui/
│   ├── Dockerfile
│   └── main.py             # PySide6 app
└── tests/
    └── test_database.py
```

The backend exposes `GET/POST /messages`, `PUT/DELETE /messages/{id}`. Interactive docs
are at `/docs` (Swagger) and `/redoc`.

---

## 🐍 Run Locally (no Docker)

Requires PostgreSQL running locally and `uv` installed.

```bash
# 1) install deps (everything - backend + gui + dev tools)
uv sync --all-extras

# 2) create DB, user, and table (once)
sudo -u postgres psql -c "CREATE DATABASE docker_learning;"
sudo -u postgres psql -c "CREATE USER learning_user WITH PASSWORD 'learning_password';"
sudo -u postgres psql -d docker_learning -c "GRANT ALL PRIVILEGES ON DATABASE docker_learning TO learning_user;"
psql -U learning_user -d docker_learning -h localhost -f database/init.sql

# 3) run backend
uv run uvicorn backend.main:app --reload
# → browser: http://localhost:8000/docs   (see "Testing it" below for more)

# 4) run GUI (separate terminal)
uv run python gui/main.py

# 5) run tests
uv run python -m pytest -v
```

`.env` (used automatically by `python-dotenv`):

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=docker_learning
POSTGRES_USER=learning_user
POSTGRES_PASSWORD=learning_password
```

⚠️ Don't commit `.env` — it's already in `.gitignore`.

### 🌐 Testing it (once the backend from step 3 is running)

You don't need the GUI to try the API — the backend alone is enough.

**Browser:**

- **http://localhost:8000/docs** — Swagger UI, interactive: expand an endpoint, "Try it
  out", fill the body, "Execute".
- **http://localhost:8000/redoc** — read-only API reference.
- **http://localhost:8000/** — plain health check (`{"message": "..."}`).

**curl:**

```bash
curl http://localhost:8000/                 # health check
curl http://localhost:8000/messages          # GET all messages

curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Docker"}'           # CREATE

curl -X PUT http://localhost:8000/messages/1 \
  -H "Content-Type: application/json" \
  -d '{"message": "Updated via curl"}'       # UPDATE id=1

curl -X DELETE http://localhost:8000/messages/1   # DELETE id=1
```

**Database (Postgres directly, port 5432):**

Useful to confirm what the API actually wrote, independent of the app:

```bash
psql -U learning_user -d docker_learning -h localhost -p 5432
```
```sql
SELECT * FROM messages;
```

---

## 🐳 Run with Docker

Each layer runs in its **own container**: `db`, `backend`, `gui`. Nothing about the code
above changes — the same `.env` file is reused, and `docker-compose.yml` just points
`backend`/`gui` at the `db` service by container name instead of `localhost`.

> ⚠️ First time only: run `uv lock` locally after pulling this change (dependencies were
> just split by service — see "What each Dockerfile does" below) so `uv.lock` matches
> `pyproject.toml` before building images.

### 🔁 Day-to-day workflow (read this first)

You only need `--build` when Docker actually needs to redo work — a fresh image, changed
code, or changed dependencies. Once images exist, starting and stopping the app is just:

```bash
docker compose up -d     # start everything in the background
docker compose down      # stop everything
```

That pair is what you'll use almost every day. `--build` is the exception, not the rule:

| Situation                                                        | Command                     |
| ------------------------------------------------------------------ | ---------------------------- |
| **Very first run**, or you pulled new code                       | `docker compose up -d --build` |
| You edited `backend/*.py`, `gui/*.py`, `database/*.py`             | `docker compose up -d --build` |
| You edited `pyproject.toml`, `uv.lock`, or a `Dockerfile`          | `docker compose up -d --build` |
| Just starting your day, nothing changed since last time            | `docker compose up -d`      |
| Done for the day                                                  | `docker compose down`       |
| You changed `docker-compose.yml` only (ports, env vars, volumes)   | `docker compose up -d` (no rebuild needed — compose re-reads the file) |

Why a rebuild is needed for code changes: your source files are **copied into the image**
at build time (`COPY backend/ ./backend/`, etc.), not mounted live. `docker compose up`
without `--build` reuses the image exactly as it was last built, so it won't see edits
until you rebuild.

### Run everything

```bash
docker compose up -d --build   # first time / after code changes: build + start, detached
docker compose up -d           # every other time: just start, detached
docker compose up --build      # attached instead of -d — logs stream in this terminal
```

- Backend → http://localhost:8000 (docs at `/docs`)
- Postgres → `localhost:5432` (same credentials as `.env`)
- GUI window opens on your screen (see X11 note below)

### 🌐 Testing the API — Browser & curl

Once `db` + `backend` are up (`docker compose up -d db backend`), you don't need the GUI
to exercise the API.

> **Port depends on `BACKEND_HOST_PORT`.** The URLs below assume you left it unset
> (default `8000`). If you set `BACKEND_HOST_PORT=8001` (e.g. to run alongside the native
> app — see "Running native + Docker at the same time" further down), substitute `8001`
> for `8000` everywhere below.

**Browser (Swagger UI):**

Open **http://localhost:8000/docs** — FastAPI's interactive docs. Expand any endpoint,
click "Try it out", fill in the body, and click "Execute". An alternative read-only view
is at **http://localhost:8000/redoc**, and a plain health check is at
**http://localhost:8000/**. FastAPI serves both `/docs` and `/redoc` automatically — the
project doesn't disable either — so if one loads, the other will too (see
Troubleshooting below if *neither* loads).

**curl:**

```bash
# health check
curl http://localhost:8000/

# GET all messages
curl http://localhost:8000/messages

# CREATE a message
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Docker"}'

# UPDATE message with id=1
curl -X PUT http://localhost:8000/messages/1 \
  -H "Content-Type: application/json" \
  -d '{"message": "Updated via curl"}'

# DELETE message with id=1
curl -X DELETE http://localhost:8000/messages/1
```

`GET`/`POST` return JSON you can pretty-print by piping to `python3 -m json.tool` or `jq`.

**Database (Postgres directly):**

Same idea as the local setup, just note the port depends on `POSTGRES_HOST_PORT`
(default `5432`, unless you changed it to avoid a conflict with a native Postgres):

```bash
psql -U learning_user -d docker_learning -h localhost -p 5432
```
```sql
SELECT * FROM messages;
```

Or without installing `psql` on the host at all — run it inside the `db` container:

```bash
docker compose exec db psql -U learning_user -d docker_learning -c "SELECT * FROM messages;"
```

### Run containers independently

```bash
docker compose up -d db          # just the database
docker compose up -d backend     # backend (+ starts db if not running)
docker compose up gui            # gui (+ starts backend/db if not running)
```

`-d` runs a service in the background (detached) so you get your terminal back — useful
for `db`/`backend`, which you'll usually leave running while you iterate on the GUI or
poke the API from a browser/curl. `gui` is left attached above since it's an interactive
desktop window, not something you'd want backgrounded.

Each service can also be stopped, rebuilt, or inspected on its own:

```bash
docker compose stop gui
docker compose build backend       # rebuild just this one image
docker compose logs -f backend
docker compose exec backend uv run python -m pytest -v   # tests against the db container
```

### Stop / clean up

```bash
docker compose down       # stop containers
docker compose down -v    # also delete the postgres volume (wipes data)
```

### 🔌 How the services find each other (`.env` vs `docker-compose.yml`)

There are two *different* URLs the GUI/backend can use to reach each other, depending on
whether you're running natively or in Docker — this is why you won't find `BACKEND_URL`
in `.env`: it's set only in `docker-compose.yml`, not shared config like the DB
credentials are.

| Variable         | Native (`uv run ...`)                          | Docker Compose                                   |
| ----------------- | ------------------------------------------------ | --------------------------------------------------- |
| `POSTGRES_HOST`  | `localhost` (from `.env`)                        | `db` — overridden in `docker-compose.yml`          |
| `BACKEND_URL`    | `http://127.0.0.1:8000` (default in `gui/main.py`, `.env` not involved) | `http://backend:8000` — set in `docker-compose.yml` |

- **`http://backend:8000`** only works *from inside another container on the same Docker
  network* (`app_network`). It's Docker's built-in DNS: any container can reach service
  `backend` by that service's name from `docker-compose.yml`. It will **not** work if you
  paste it into your host browser or a native `curl` — from your machine, the backend is
  always `http://localhost:8000` (because `docker-compose.yml` publishes port 8000 to
  the host).
- **You don't need to add `BACKEND_URL` to `.env`.** It only matters to the `gui`
  container, is already set correctly in `docker-compose.yml`, and its default
  (`http://127.0.0.1:8000`) already covers running the GUI natively.

### 🖥️ GUI container note (X11)

The GUI is a desktop app, so its container needs access to a display server:

- **Linux:** run `xhost +local:docker` once per session before `docker compose up gui`.
- **macOS/Windows:** install an X server (XQuartz / VcXsrv), point `DISPLAY` at it, and
  adjust the `gui` service's `volumes`/`environment` in `docker-compose.yml` accordingly.
- **Simplest option:** run `db` + `backend` in Docker and the GUI natively
  (`uv run python gui/main.py`) — it already respects `BACKEND_URL` (defaults to
  `http://127.0.0.1:8000`, matching the backend's published port).

### What each Dockerfile does

- `backend/Dockerfile` — `python:3.13-slim` + `uv`, installs `libpq5` (required by
  `psycopg` at runtime), installs only the `backend` dependency group, copies only
  `backend/` + `database/`, runs `uvicorn`.
- `gui/Dockerfile` — same base, adds the Qt/X11 runtime libraries PySide6 needs,
  installs only the `gui` dependency group, copies only `gui/`, runs `python gui/main.py`.

**Dependencies are split by service**, not shared wholesale. `pyproject.toml` still has
one `[project]` section (one project, one lockfile — that part of the original design is
worth keeping), but the actual packages are declared as two independent
`[project.optional-dependencies]` groups:

```toml
[project.optional-dependencies]
backend = ["fastapi", "psycopg", "python-dotenv", "uvicorn[standard]"]
gui = ["pyside6", "requests"]
```

Each Dockerfile installs only the extra it needs (`uv sync --extra backend` /
`uv sync --extra gui`), so:

- the **backend image never contains PySide6/Qt** — it's a pure API image,
- the **GUI image never contains FastAPI/psycopg/uvicorn** — it's a pure client image,
- either one can be built, shipped, and run **standalone**, independent of the other.

For local full-stack development you still get everything in one environment with
`uv sync --all-extras`; for a single service, `uv sync --extra backend` (or `--extra gui`)
mirrors exactly what its Docker image installs.

> ⚠️ **One-time step:** since the dependency groups changed, run `uv lock` once to
> regenerate `uv.lock` before your first `docker compose up --build` (or local `uv sync`).

### Docker concepts this adds on top of the local setup

```text
📦 Image           → backend/Dockerfile, gui/Dockerfile, postgres:16-alpine
🚢 Container        → db, backend, gui (one process each)
🌐 Network          → app_network (containers reach each other by service name)
💾 Volume           → db_data (Postgres data survives container restarts)
🎼 Compose          → docker-compose.yml wires all three together
```

### 🩺 Troubleshooting

**`localhost:5432` (or `:8000`) refuses to connect:**

1. Check the containers are actually running: `docker compose ps` — status should say
   `running` (or `healthy` for `db`), not `Exit` / `Restarting`.
2. Check logs for the failing service: `docker compose logs db` or `docker compose logs backend`.
3. **Most common cause:** a Postgres already running natively on your machine (e.g. from
   the "Run Locally" section above, or a system service) is already using port 5432, so
   Docker can't bind it. Check for the conflict:
   ```bash
   sudo lsof -i :5432        # Linux/macOS
   # or, on Windows: netstat -ano | findstr :5432
   ```
   Either stop the native service (`sudo service postgresql stop`), or run Docker on a
   different host port instead — see "Running native + Docker at the same time" below.
4. If you just ran `docker compose up -d` and it's been only a couple of seconds, `db`
   may still be starting — `backend` waits for it (`depends_on: condition:
   service_healthy`), so give it a moment and re-check `docker compose ps`.

**`/docs` or `/redoc` won't load:**

Same checklist as above — this is almost always the backend container not being up yet
or not being reachable, not the docs feature itself (nothing in this project disables
`/redoc`). Confirm with `docker compose logs backend`, and once you see uvicorn's
"Application startup complete", retry the browser.

### 🔀 Running native + Docker at the same time (different ports)

This is a port-mapping choice, not a limit of the app — `docker-compose.yml` just
defaults to publishing the same ports the native app uses (5432, 8000), for convenience.
Change the **host** side of the mapping and both can run simultaneously without touching
each other:

```bash
# either edit .env (uncomment/add these two lines), or pass them inline like this:
POSTGRES_HOST_PORT=5433 BACKEND_HOST_PORT=8001 docker compose up -d --build
```

Now:

| Service              | Native                          | Docker (with the ports above)     |
| --------------------- | ---------------------------------- | ------------------------------------ |
| Postgres              | `localhost:5432` (unchanged)       | `localhost:5433`                    |
| Backend               | `localhost:8000` (unchanged)       | `localhost:8001` — docs at `localhost:8001/docs` |

Nothing internal changes: inside Docker, `backend` still talks to `db` on port `5432`
(the container's *internal* port never moves), and the `gui` container still reaches the
backend at `http://backend:8000` — both are container-to-container, unrelated to which
host port you chose. The only other thing to update is if you run the **GUI natively**
against the **Dockerized** backend on an alternate port — point it at the new port
explicitly:

```bash
BACKEND_URL=http://localhost:8001 uv run python gui/main.py
```

---

## 🧪 Tests

```bash
uv sync --extra backend                              # if not already installed
uv run python -m pytest -v                            # local
docker compose exec backend uv run python -m pytest -v # inside the backend container
```

---

## ⭐ Philosophy

Keep it small, understand every layer, then containerize it.
