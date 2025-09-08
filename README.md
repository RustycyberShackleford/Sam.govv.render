# SAM.gov Search Demo (Render/Cloud Run friendly)

This app lets a user enter a name, shows demo results, and creates a **PNG screenshot** of the results **in the browser**. The server then saves the PNG to `/tmp` and returns a download link. Optional: upload the PNG to Google Drive.

## Quick Start (Local)
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` (leave `DEMO_MODE=true`).
3. `python webapp.py`
4. Open `http://127.0.0.1:8080`
5. Enter a name → **Capture & Save Screenshot** → click the **Download PNG** link.

> If you get “file not found,” make sure you clicked **Capture & Save Screenshot** first. The file is saved to `/tmp` and the link is returned by the server after capture.

---

## Deploy to Render (Dockerfile)
1. Push this folder to a GitHub repo.
2. In Render, create **New → Web Service → Build & deploy from a repo**. Render will detect the **Dockerfile**.
3. **Environment Variables** (Settings → Environment):
   - `DEMO_MODE` = `true` (keeps demo data; no external APIs needed)
   - *(Optional, for Drive uploads)*
     - `GOOGLE_APPLICATION_CREDENTIALS` = `/opt/render/project/src/.render-secrets/service-account.json`
     - `DRIVE_TARGET_FOLDER_ID` = `<your-drive-folder-id>`

4. **Secret Files** (Settings → Secret Files → Add Secret File) — *only if you want Drive uploads now*:
   - **Name**: `service-account.json`  *(just the filename; no slashes)*
   - **Contents**: paste the JSON key you downloaded from Google Cloud (service account key).
   - After saving, Render makes it available at:
     `/opt/render/project/src/.render-secrets/service-account.json`
   - Make sure your Drive folder is **shared** with the service account email in that JSON (`client_email`) as **Editor**.

5. **Deploy**. When live, open your Render URL, enter a name, click **Capture & Save Screenshot**, then click **Download PNG**.

**Health check:** `GET /healthz` should return `ok`.

### Where did my file go?
- Files are saved to `/tmp` inside the container. Use `/download/<filename>` to fetch them immediately.
- For debugging, you can view a quick list at **`/files`** (added below).

---

## Deploy to Cloud Run (no JSON file needed)
You can run without embedding a JSON key by attaching a **service account** to the Cloud Run service and using **Application Default Credentials**.

1. Build & push the Docker image, then deploy:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud builds submit --tag gcr.io/$PROJECT_ID/samgov-demo
   gcloud run deploy samgov-demo      --image gcr.io/$PROJECT_ID/samgov-demo      --allow-unauthenticated      --set-env-vars DEMO_MODE=true      --port=8080
   ```
2. Share your Drive folder with the Cloud Run **service account email** if you add Drive uploads later.
3. Open the Cloud Run URL → test like above.

---

## Environment Variables (explained)
- `DEMO_MODE`  
  - `true`: show synthetic results. No external APIs required. Best for demos.
  - `false`: you would add your real SAM.gov query logic (not included here).
- `GOOGLE_APPLICATION_CREDENTIALS` *(Render + Drive uploads only)*  
  - Must point to Render’s secret file path:
    `/opt/render/project/src/.render-secrets/service-account.json`
- `DRIVE_TARGET_FOLDER_ID` *(Drive uploads only)*  
  - The ID from your Drive folder URL: `https://drive.google.com/drive/folders/<THIS_ID>`

---

## Endpoints
- `GET /` – form to enter name.
- `POST /search` – shows results page.
- `POST /capture` – receives base64 PNG from browser and saves to `/tmp`.
- `GET /download/<filename>` – downloads the PNG saved in `/tmp`.
- `GET /files` – lists saved files in `/tmp` (debug helper).
- `GET /healthz` – returns `ok`.

---

## Common issues
- **“file not found” when downloading**  
  You must click **Capture & Save Screenshot** first so the server creates the file and returns the generated filename. Then click the **Download PNG** link that appears.
- **Drive upload fails**  
  Double-check:
  - `GOOGLE_APPLICATION_CREDENTIALS` path matches the Render Secret File location.
  - Drive folder is shared with the service account’s `client_email` as **Editor**.
  - `DRIVE_TARGET_FOLDER_ID` is correct.
