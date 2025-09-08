
import base64, os, time, json
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv

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
    results = _demo_results(name)
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
    return jsonify({"ok": True, "filename": fname, "driveFileId": None})

@app.get("/download/<path:fname>")
def download(fname):
    full = os.path.join("/tmp", fname)
    if not os.path.exists(full):
        return "Not found", 404
    return send_file(full, mimetype="image/png", as_attachment=True, download_name=fname)

@app.get("/files")
def list_files():
    # Debug helper: list files currently saved in /tmp
    entries = []
    for fn in os.listdir("/tmp"):
        p = os.path.join("/tmp", fn)
        if os.path.isfile(p):
            entries.append({"name": fn, "bytes": os.path.getsize(p)})
    return jsonify(entries)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
