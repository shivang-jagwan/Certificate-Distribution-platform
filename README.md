# Certificate Project (Render.com Ready)

FastAPI-based Certificate Distribution System that verifies a student from a CSV file and generates a downloadable PDF certificate.

## Required Structure

This repository is structured to deploy as a **Render Web Service**:

```
certificate-project/
 app/
    main.py
    certificate_generator.py
    csv_handler.py
 data/
    students.csv
 templates/
    index.html
 certificates/
 requirements.txt
 runtime.txt
 render.yaml
```

## Production Server (Gunicorn + Uvicorn Workers)

Render start command (required):

```
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

## Environment Variables

You can configure the service using environment variables (Render  Service  Environment):

- `CSV_PATH` (default: `data/students.csv`) — path to the CSV file.
- `CERTIFICATES_DIR` (default: `certificates`) — folder where PDFs are stored.
- `CERTIFICATE_TEMPLATE_IMAGE` (default: `templates/certificate_template.jpg`) — optional background image. If missing, the PDF is generated with a simple background.
- `CERTIFICATE_ID_PREFIX` (default: `CERT`) — prefix used for generated certificate IDs.
- `ADMIN_KEY` (default: empty) — if set, `/generate-all` requires `admin_key` to match.
- `CORS_ALLOW_ORIGINS` (default: `*`) — comma-separated list of allowed origins.

## API Endpoints

- `GET /` — serves the HTML portal from `templates/index.html`
- `GET /health` — returns JSON status
- `GET /verify?name=...&student_id=...` — validates the student from CSV
- `GET /certificate?name=...&student_id=...` — generates (if needed) and downloads the PDF
- `GET /generate-all?admin_key=...` — bulk-generate PDFs (optional admin key)

## Local Development

1) Install dependencies

```
pip install -r requirements.txt
```

2) Run locally

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## Deploy to Render (Web Service)

1) Push this repository to GitHub.

2) In Render:
- Dashboard  **New**  **Web Service**
- Connect your GitHub repo

3) Settings:
- **Runtime**: Python
- **Build Command**:
  ```
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```
  gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
  ```

4) Deploy.

## If Render shows Python 3.13 in logs

This repo pins Python via `runtime.txt` (python-3.10.13). If your Render build log shows something like `.venv/lib/python3.13/...`, Render is not using the repo root.

- In your Render service settings, ensure **Root Directory** is empty (repo root), and that `runtime.txt` exists at the repo root.
- Redeploy after changing Root Directory.

### Using render.yaml (recommended)

This repo includes `render.yaml`. You can use Render Blueprint deploy, or just keep it for documentation; Render will read it during blueprint deployments.
