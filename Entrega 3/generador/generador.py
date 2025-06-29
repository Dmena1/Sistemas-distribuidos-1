import time
import random
import requests
import os

# Configuraciones desde variables de entorno
URL_CONSULTA = os.getenv("URL_CONSULTA", "http://cache:8001/eventos")
DISTRIBUCION = os.getenv("DISTRIBUCION", "uniforme")
TASA_POISSON = float(os.getenv("TASA_POISSON", 1.0))
INTERVALO_MIN = float(os.getenv("INTERVALO_MIN", 1.0))
INTERVALO_MAX = float(os.getenv("INTERVALO_MAX", 3.0))

TIPOS = ["HAZARD", "JAM", "WEATHER", "ROAD_CLOSED"]
CIUDADES = ["Santiago", "Providencia", "Ñuñoa", "Renca", "La Florida", "Maipú", "Estación Central"]

def obtener_intervalo():
    if DISTRIBUCION == "poisson":
        return random.expovariate(TASA_POISSON)
    else:
        return random.uniform(INTERVALO_MIN, INTERVALO_MAX)

def construir_url():
    params = []
    if random.random() < 0.6:
        tipo = random.choice(TIPOS)
        params.append(f"tipo={tipo}")
    if random.random() < 0.6:
        ciudad = random.choice(CIUDADES)
        params.append(f"ciudad={ciudad}")
    query = "&".join(params)
    return f"{URL_CONSULTA}?{query}" if query else URL_CONSULTA

def simular_usuario():
    while True:
        url = construir_url()
        try:
            response = requests.get(url)
            print(f"Consulta a {url} → {response.status_code}")
        except Exception as e:
            print(f"Error al consultar {url}: {e}")
        intervalo = obtener_intervalo()
        print(f"Esperando {intervalo:.2f} segundos...\n")
        time.sleep(intervalo)

if __name__ == "__main__":
    print(f"Generador iniciado con distribución: {DISTRIBUCION}")
    simular_usuario()
