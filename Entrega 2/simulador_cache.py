import csv
import time

archivo = "eventos_limpios.csv"
cache = {}  # caché en memoria

def contar_por_tipo(tipo):
    if tipo in cache:
        print("Respuesta desde CACHÉ")
        return cache[tipo]

    print("Consultando SIN caché...")
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
        print("Respuesta desde CACHÉ")
        return cache[key]

    print("Consultando SIN caché...")
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
    import time as t

    print("\nConsulta SIN caché:")
    start1 = t.time()
    contar_por_tipo("JAM")
    contar_por_comuna("Ñuñoa")
    end1 = t.time()
    print(f"Total sin caché: {end1 - start1:.6f} s")

    print("\nConsulta CON caché:")
    start2 = t.time()
    contar_por_tipo("JAM")
    contar_por_comuna("Ñuñoa")
    end2 = t.time()
    print(f"Total con caché: {end2 - start2:.6f} s")

