# Hello‑World Flask App — Docker & Docker Compose Guide

This project is a simple Flask application that reads text from a file located in the `data/` directory. The app is fully containerized using Docker and supports live file updates through a bind‑mounted volume.

<img width="1283" height="743" alt="screenshot-app" src="https://github.com/user-attachments/assets/95104793-723e-4c2f-a598-2db8099ea39b" />

## Project Structure

```text
hello-world/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── index.html
└── data/
    └── text.txt
```

> [!NOTE]
> The `data/` folder should not be baked into the production Docker image. It is mounted at runtime so changes on your host machine appear instantly inside the container.

---

## Build & Run with Docker (Local)

### 1. Build the Docker Image
Run the following command from inside the project root folder:
```bash
docker build -t hello-world-app .
```

### 2. Run the Container with a Volume
To avoid Git Bash path mangling on Windows and accurately target the application's working directory, run:
```bash
MSYS_NO_PATHCONV=1 docker run -p 5000:5000 \
  -v "$(pwd)/data:/data" \
  --name hello-world \
  hello-world
```

### 3. Access the App
Open your web browser and navigate to:
```text
http://localhost:5000
```

### 4. Verify Live Updates
Edit `data/text.txt` on your host machine and refresh the webpage—your changes will appear instantly.

---

## Run with Docker Compose

Using Docker Compose eliminates terminal path compatibility issues entirely by handling the mount internally.

### 1. Create a `docker-compose.yml` File
Ensure your `docker-compose.yml` is configured as follows:
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: hello-world
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
    environment:
      - FLASK_DEBUG=1
      - WATCHFILES_FORCE_POLLING=true
```

### 2. Start the Application
```bash
docker compose up --build
```

---

## Enter the Running Container (Optional)

To inspect the internal file structure of your running container:
```bash
docker exec -it hello-world bash
```

Inside the container terminal, verify the live mount point:
```bash
cat data/text.txt
```

---

## `.dockerignore` Recommendation

Create a `.dockerignore` file in your root directory to prevent local runtime assets and cache files from inflating your image size:
```text
data/
__pycache__/
*.pyc
.env
.git
```
