# app.py — full-stack demo: FastAPI backend + serves the website + APK download.
# Local run:  python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
# On Render:  gunicorn/uvicorn reads the PORT env var automatically (see start command).

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

app = FastAPI(title="ShopDemo")

# ---- Fake "database" of products (later this becomes PostgreSQL) ----
PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 199.00, "emoji": "🎧"},
    {"id": 2, "name": "Smart Watch",        "price": 149.00, "emoji": "⌚"},
    {"id": 3, "name": "Bluetooth Speaker",  "price": 89.00,  "emoji": "🔊"},
    {"id": 4, "name": "Laptop Stand",       "price": 45.00,  "emoji": "💻"},
    {"id": 5, "name": "Mechanical Keyboard","price": 129.00, "emoji": "⌨️"},
    {"id": 6, "name": "USB-C Hub",          "price": 59.00,  "emoji": "🔌"},
]


# ---- API endpoint: the frontend calls this to get products ----
@app.get("/api/products")
def get_products():
    return {"status": "success", "products": PRODUCTS}


# ---- Serve the single HTML page (the website) ----
@app.get("/", response_class=HTMLResponse)
def home():
    return Path("index.html").read_text(encoding="utf-8")


# ---- Serve the Android app for the "Download App" button ----
# Put the built APK next to app.py as "shopdemo.apk" for this to work.
@app.get("/download-app")
def download_app():
    apk = Path("shopdemo.apk")
    if apk.exists():
        return FileResponse(
            apk,
            media_type="application/vnd.android.package-archive",
            filename="ShopDemo.apk",
        )
    return {"status": "error", "msg": "APK not uploaded yet"}
