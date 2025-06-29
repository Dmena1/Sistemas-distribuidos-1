import csv

input_file = "eventos_convertidos.csv"
output_file = "eventos_limpios.csv"

vistos = set()

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    campos = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=campos)
    writer.writeheader()

    for fila in reader:
        uuid = fila["uuid"]
        tipo = fila["tipo"]
        comuna = fila["comuna"]
        lat = fila["latitud"]
        lon = fila["longitud"]

        # Eliminar duplicados por UUID
        if uuid in vistos:
            continue
        vistos.add(uuid)

        # Validar campos esenciales
        if not tipo or not comuna or not lat or not lon:
            continue

        writer.writerow(fila)

print(f"✔ Archivo limpio generado: {output_file}")
