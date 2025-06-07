# main.py

import os
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Import router Anda dari file yang sudah ada
from src.api.v1.sentiment import router as sentiment_router

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Sentiment Analysis API with Cache")

# Ambil URL Redis dari environment variable (penting untuk Kubernetes)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379") # <-- DITAMBAHKAN

@app.on_event("startup")
async def startup():
    """
    Fungsi ini dijalankan saat aplikasi startup untuk koneksi ke Redis.
    """
    try:
        # Koneksi ke Redis menggunakan URL yang sudah ditentukan
        r = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        await r.ping()
        # Inisialisasi cache menggunakan backend Redis
        FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
        print(f"Successfully connected to Redis at {REDIS_URL}")
    except Exception as e:
        print(f"Could not connect to Redis: {e}")
        print("Caching will be disabled.")
# --- AKHIR BAGIAN TAMBAHAN ---

# Include router Anda, sama seperti sebelumnya
app.include_router(sentiment_router, prefix="/api/v1", tags=["sentiment"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentiment Analysis API"}

# Bagian ini bisa tetap ada untuk development lokal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)