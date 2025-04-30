from playwright.sync_api import sync_playwright 
import json
import time
import requests

# CONFIGURACIÓN INICIAL
MAX_EVENTOS = 10000
ZOOM_SCROLL = 300
ZOOM_OUT_INICIAL = 1
INTERVALO = 4
PIXEL_POR_KM = 11

# DIVISION DE LA REGIÓN METROPOLITANA
ANCHO_GRILLA = 6
ALTO_GRILLA = 8
ESPACIADO_KM_X = 10
ESPACIADO_KM_Y = 10
ESPACIADO_PX_X = ESPACIADO_KM_X * PIXEL_POR_KM # x pixel
ESPACIADO_PX_Y = ESPACIADO_KM_Y * PIXEL_POR_KM # x pixel

# CAMPOS A ELIMINAR
keys_to_remove = [
    "comments", "reportDescription", "nThumbsUp", "reportBy",
    "reportByMunicipalityUser", "reportRating", "reportMood",
    "fromNodeId", "toNodeId", "magvar", "additionalInfo", "wazeData"
]

eventos_acumulados = []
uuids_vistos = set()

def remove_keys_from_dict(data, keys_to_remove):
    if isinstance(data, list):
        for item in data:
            remove_keys_from_dict(item, keys_to_remove)
    elif isinstance(data, dict):
        for key in keys_to_remove:
            if key in data:
                del data[key]
        for key in data:
            if isinstance(data[key], (dict, list)):
                remove_keys_from_dict(data[key], keys_to_remove)

def procesar_eventos(data):
    global eventos_acumulados, uuids_vistos
    alerts = data.get("alerts", [])
    remove_keys_from_dict(alerts, keys_to_remove)
    nuevos = 0
    for evento in alerts:
        uuid = evento.get("uuid")
        if uuid and uuid not in uuids_vistos:
            eventos_acumulados.append(evento)
            uuids_vistos.add(uuid)
            nuevos += 1
    return nuevos

def mover_mapa(page, dx, dy):
    center_x, center_y = 600, 300
    print(f"Moviendo mapa a dx={dx}, dy={dy}")
    page.mouse.move(center_x, center_y)
    page.mouse.down()
    page.mouse.move(center_x + dx, center_y + dy, steps=20)
    page.mouse.up()
    time.sleep(1)

def zoom(page, sentido="out", veces=1):
    center_x, center_y = 600, 300
    page.mouse.move(center_x, center_y)
    time.sleep(0.2)
    for _ in range(int(veces)):
        delta = -ZOOM_SCROLL if sentido == "in" else ZOOM_SCROLL
        page.mouse.wheel(0, delta)
        time.sleep(0.6)

def capturar(page):
    print("Capturando eventos")
    time.sleep(INTERVALO)

def generar_grilla():
    grilla = [
        (col * ESPACIADO_PX_X - (ANCHO_GRILLA // 2 * ESPACIADO_PX_X),
         row * ESPACIADO_PX_Y - (ALTO_GRILLA // 2 * ESPACIADO_PX_Y))
        for row in range(ALTO_GRILLA)
        for col in range(ANCHO_GRILLA)
    ]
    return grilla

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        def handle_response(response):
            if "georss" in response.url and response.status == 200:
                try:
                    data = response.json()
                    nuevos = procesar_eventos(data)
                    print(f"Nuevos eventos encontrados: {nuevos} | Total encontrados hasta el momento: {len(eventos_acumulados)}")
                except Exception as e:
                    print(f"Error: {e}")

        page.on("response", handle_response)

        print("Abriendo Waze...")
        page.goto("https://www.waze.com/es-419/live-map?ll=-33.075484,-70.932070&zoom=9") #URL DE INICIO DE WAZE (ESQUINA DE EL AREA A BUSCAR)

        try:
            page.wait_for_selector("//button[contains(text(), 'Entendido')]", timeout=15000)
            page.locator("//button[contains(text(), 'Entendido')]").click()
            print("Popup cerrado")
        except:
            print("No apareció ningun popup")

        time.sleep(10)

        zoom(page, "out", ZOOM_OUT_INICIAL)

        zonas = generar_grilla()
        ciclo = 0

        while len(eventos_acumulados) < MAX_EVENTOS:
            ciclo += 1
            print(f"\n N° {ciclo} de division recorrida")

            for dx, dy in zonas:
                if len(eventos_acumulados) >= MAX_EVENTOS:
                    break
                mover_mapa(page, dx, dy)
                capturar(page)

        # Guardar localmente
        with open("eventos_region_metropolitana.json", "w", encoding="utf-8") as f:
            json.dump({"alerts": eventos_acumulados}, f, indent=2, ensure_ascii=False)

        print(f"\nBusqueda completada. Total de eventos encontrados: {len(eventos_acumulados)}")

        # Enviar al backend
        print("Enviando eventos al backend")
        enviados = 0
        for evento in eventos_acumulados:
            try:
                response = requests.post("http://cache:8001/eventos", json=evento)
                response.raise_for_status()
                enviados += 1
            except Exception as e:
                print(f"Error: {e}")
        print(f"Se enviaron {enviados} eventos a http://cache:8001/eventos")

        browser.close()

if __name__ == "__main__":
    main()
