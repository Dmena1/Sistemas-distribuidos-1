import csv
import time

archivo = "eventos_limpios.csv"
cache = {}  # caché en memoria

def contar_por_tipo(tipo):
    if tipo in cache:
        print("🧠 Respuesta desde CACHÉ")
        return cache[tipo]

    print("🐢 Consultando SIN caché...")
    inicio = time.time()
    conteo = 0

    with open(archivo, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila["tipo"] == tipo:
                conteo += 1

    tiempo = time.time() - inicio
    cache[tipo] = conteo
    print(f"Resultado: {conteo} eventos [{tiempo:.4f} s]")
    return conteo

def contar_por_comuna(comuna):
    key = f"comuna:{comuna}"
    if key in cache:
        print("🧠 Respuesta desde CACHÉ")
        return cache[key]

    print("🐢 Consultando SIN caché...")
    inicio = time.time()
    conteo = 0

    with open(archivo, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila["comuna"] == comuna:
                conteo += 1

    tiempo = time.time() - inicio
    cache[key] = conteo
    print(f"Resultado: {conteo} eventos [{tiempo:.4f} s]")
    return conteo

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        print("\n📊 Consulta de eventos")
        print("1. Consultar por tipo")
        print("2. Consultar por comuna")
        print("0. Salir")
        opcion = input("Selecciona opción: ")

        if opcion == "0":
            break
        elif opcion == "1":
            tipo = input("Tipo de evento (ej: JAM): ").strip().upper()
            contar_por_tipo(tipo)
        elif opcion == "2":
            comuna = input("Nombre exacto de la comuna (ej: Ñuñoa): ").strip()
            contar_por_comuna(comuna)
        else:
            print("Opción inválida.")
