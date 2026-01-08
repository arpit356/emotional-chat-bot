# Run Instructions (MVP)

1. Create and activate virtual env (Windows):
   - `python -m venv venv`
   - `venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Start backend service:
   - `python -m uvicorn app.main:app --reload --port 8000` (run from the `backend` folder or set `PYTHONPATH` appropriately)
   - Or use the provided script (Windows PowerShell): `./scripts/start-dev.ps1` which opens backend and frontend servers in new windows
4. Open `http://localhost:5500/` in your browser (served by a small static server)

Notes: Serving the frontend via `python -m http.server 5500` is recommended; the frontend will call the backend on port 8000. The frontend script auto-detects a backend running on port 8000 so you should not need to change any code unless you use different ports.
