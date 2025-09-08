import base64, os, time, io
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from drive_upload import upload_to_drive

load_dotenv()
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.get("/")
def index():
    return render_template("index.html")

def _demo_results(name: str):
    n = name.strip()
    if not n or n.lower() in {"none","nomatch","no match"}:
        return []
    return [
        {"name": f"{n} Holdings LLC", "uei": "UEI123456789", "cage": "1A2B3", "status":"Active", "address":"Chico, CA"},
        {"name": f"{n} Services Inc",   "uei": "UEI987654321", "cage": "9Z8Y7", "status":"Inactive", "address":"Redding, CA"}
    ]

@app.post("/search")
def search():
    name = request.form.get("name","").strip()
    demo = os.getenv("DEMO_MODE","true").lower() == "true"
    # In a production build, replace with real API call if demo==False
    results = _demo_results(name) if demo else _demo_results(name)
    return render_template("results.html", query=name, results=results, demo=demo)

@app.post("/capture")
def capture():
    data_url = request.form.get("imageData","")
    name = request.form.get("name","query").strip().replace(" ", "_")
    if not data_url.startswith("data:image/png;base64,"):
        return jsonify({"ok": False, "error": "Invalid image data"}), 400
    b64 = data_url.split(",",1)[1]
    raw = base64.b64decode(b64)
    ts = time.strftime("%Y%m%d_%H%M%S")
    fname = f"samgov_result_{name}_{ts}.png"
    path = os.path.join("/tmp", fname)
    with open(path, "wb") as f:
        f.write(raw)

    drive_id = None
    folder = os.getenv("DRIVE_TARGET_FOLDER_ID","").strip()
    creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS","").strip()
    if folder and creds and os.path.exists(creds):
        try:
            drive_id = upload_to_drive(path, folder)
        except Exception as e:
            # ignore upload errors in demo
            drive_id = None

    # Return the file directly for download as well
    return jsonify({"ok": True, "filename": fname, "driveFileId": drive_id})

@app.get("/download/<path:fname>")
def download(fname):
    full = os.path.join("/tmp", fname)
    if not os.path.exists(full):
        return "Not found", 404
    return send_file(full, mimetype="image/png", as_attachment=True, download_name=fname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
