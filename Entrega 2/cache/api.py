from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os

app = FastAPI()

eventos = []  # Guardamos en memoria

# Permitir CORS para pruebas locales (opcional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/eventos")
async def recibir_evento(request: Request):
    data = await request.json()
    eventos.append(data)
    print(f"🟢 Evento recibido. Total: {len(eventos)}")

    # Guardar en disco cada vez que se agrega (opcional)
    with open("eventos_guardados.json", "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)

    return {"mensaje": "Evento recibido", "total": len(eventos)}

# 🆕 NUEVA RUTA PARA CONSULTAS
@app.get("/eventos")
def obtener_eventos(
    tipo: Optional[str] = Query(None),
    ciudad: Optional[str] = Query(None),
    limite: int = Query(100)
):
    filtrados = eventos

    if tipo:
        filtrados = [e for e in filtrados if e.get("type") == tipo]

    if ciudad:
        filtrados = [e for e in filtrados if e.get("city") == ciudad]

    return {"total": len(filtrados[:limite]), "eventos": filtrados[:limite]}
