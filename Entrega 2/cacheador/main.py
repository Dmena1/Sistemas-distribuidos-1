from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from cache import LRUCache, LFUCache
import requests
import os

# Parámetros de entorno
CACHE_SIZE = int(os.getenv("CACHE_SIZE", 100))
CACHE_POLICY = os.getenv("CACHE_POLICY", "LRU").upper()
BACKEND_URL = os.getenv("BACKEND_URL", "http://cache:8001/eventos")

# Selección de política
if CACHE_POLICY == "LFU":
    print("🧠 Usando política de caché: LFU")
    cache = LFUCache(capacity=CACHE_SIZE)
else:
    print("🧠 Usando política de caché: LRU")
    cache = LRUCache(capacity=CACHE_SIZE)

app = FastAPI()

@app.get("/eventos")
def eventos_proxy(request: Request):
    query_str = str(request.url.query)
    cache_key = f"/eventos?{query_str}" if query_str else "/eventos"

    resultado = cache.get(cache_key)
    if resultado:
        return {"cache": True, "resultado": resultado}

    try:
        response = requests.get(BACKEND_URL, params=dict(request.query_params))
        response.raise_for_status()
        data = response.json()
        cache.put(cache_key, data)
        return {"cache": False, "resultado": data}
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": str(e)})

@app.get("/cache/stats")
def estadisticas_cache():
    stats = cache.stats()
    hits = stats["hits"]
    misses = stats["misses"]
    total = hits + misses
    stats["hit_rate"] = round(hits / total * 100, 2) if total > 0 else 0.0
    return stats
