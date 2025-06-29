import json
import csv
from datetime import datetime

# Ruta al archivo JSON
json_path = "eventos_region_metropolitana.json"
# Ruta al archivo CSV de salida
csv_path = "eventos_convertidos.csv"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

alerts = data.get("alerts", [])

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["uuid", "tipo", "subtipo", "descripcion", "latitud", "longitud", "comuna", "timestamp"])

    for alert in alerts:
        uuid = alert.get("uuid", "")
        tipo = alert.get("type", "")
        subtipo = alert.get("subtype", "")
        descripcion = alert.get("street", "")
        lat = alert.get("location", {}).get("y", "")
        lon = alert.get("location", {}).get("x", "")
        comuna = alert.get("city") or alert.get("nearBy", "")
        millis = alert.get("pubMillis", 0)

        # Convertir timestamp de milisegundos a datetime legible
        timestamp = ""
        if millis:
            timestamp = datetime.utcfromtimestamp(millis / 1000).strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow([uuid, tipo, subtipo, descripcion, lat, lon, comuna, timestamp])

print(f"Exportación completada: {csv_path}")
