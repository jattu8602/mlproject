# Chapter 8: Docker Configuration

## What is Docker?
Docker packages your app + all its dependencies into a **container** — a lightweight, portable unit that runs the same everywhere (your laptop, a server, the cloud).

## Files

### Dockerfile
```dockerfile
FROM python:3.9-slim          # Base image with Python

WORKDIR /app                   # Working directory inside container

COPY requirements.txt .        # Copy requirements first (caching optimization)
RUN pip install -r requirements.txt   # Install dependencies

COPY . .                       # Copy all source code

EXPOSE 5000                    # Tell Docker the app uses port 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:application"]
```

**Why `gunicorn` instead of `app.run()`?**
- `app.run()` is Flask's development server (single-process, not production-safe)
- `gunicorn` is a production WSGI server (multi-worker, handles real traffic)

### .dockerignore
Excludes unnecessary files from the Docker build (keeps the image small):
```
venv/          # Don't copy local virtual env
__pycache__/   # Don't copy bytecode
artifacts/     # Don't copy pickle files (regenerate in container if needed)
.git/          # Don't copy git history
```

## Commands

| Command | What it does |
|---------|-------------|
| `docker build -t mlproject .` | Build the image (tag: mlproject) |
| `docker run -p 5000:5000 mlproject` | Run container, map port 5000 |
| `docker ps` | List running containers |
| `docker stop <container-id>` | Stop a container |
| `docker images` | List built images |

## Why Docker?
- **Consistency** — runs the same on any machine
- **Portability** — deploy to any cloud (AWS ECS, Azure Container Instances, etc.)
- **Isolation** — doesn't interfere with other projects on your machine
