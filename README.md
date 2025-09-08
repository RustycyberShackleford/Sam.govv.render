# SAM.gov Search Demo (Auto Screenshot)

Now auto-captures the results as soon as the results page loads—no button click required.

## Local
1) pip install -r requirements.txt
2) python webapp.py
3) http://127.0.0.1:8080
4) Choose search type, enter query, submit.
5) The page will auto-capture, save to /tmp, and show a Download link.

## Render
- Deploy via Dockerfile.
- Env: DEMO_MODE=true
- (Optional) Drive vars as before.
