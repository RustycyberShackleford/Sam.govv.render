# SAM.gov Search Demo (Render-friendly)

A tiny Flask app that accepts a name, shows demo (or API) results, and uses **html2canvas** in the browser
to create a **screenshot PNG** of the results section. The PNG can be downloaded by the user, and optionally
uploaded to **Google Drive** via the Drive API (no headless browser needed).

## Why this works well on Render
- No Playwright/Selenium. All "screenshot" work happens **in the browser** with html2canvas.
- Server receives the base64 PNG, saves it, and (optionally) uploads to Drive.

## Quick Start (Local)
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and adjust as needed (`DEMO_MODE=true` is fine).
3. `python webapp.py`
4. Open http://127.0.0.1:5000

## Deploy to Render
**Option A (Dockerfile):**
- Push this folder to a GitHub repo.
- Create a new **Web Service** on Render, choose **Docker**.
- Add any secrets in Render > Environment:
  - `DEMO_MODE=true`
  - (Optional) `DRIVE_TARGET_FOLDER_ID`
  - (Optional) `GOOGLE_APPLICATION_CREDENTIALS=/opt/render/project/src/service-account.json`
- Add your `service-account.json` as a Render Secret File (path `/opt/render/project/src/service-account.json`).

**Option B (Native Python):**
- Use the `Procfile` start command: `gunicorn webapp:app --bind 0.0.0.0:$PORT`

## Using Google Drive Upload (Optional)
- Create a Google Service Account; download its JSON key as `service-account.json`.
- Share your target Drive folder with the service account's email.
- Set env vars: `GOOGLE_APPLICATION_CREDENTIALS` and `DRIVE_TARGET_FOLDER_ID`.

## Endpoints
- `GET /` — Form to enter name
- `POST /search` — Renders results page
- `POST /capture` — Accepts base64 PNG from browser; saves and (optionally) uploads to Drive
- `GET /healthz` — Simple health check
