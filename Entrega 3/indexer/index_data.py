import requests
import time

ELASTIC_URL = "http://elasticsearch:9200"  # Nombre del contenedor, no localhost

def wait_for_elasticsearch():
    """Espera a que Elasticsearch esté listo"""
    print("Esperando a que Elasticsearch esté listo...")
    while True:
        try:
            response = requests.get(f"{ELASTIC_URL}/_cluster/health")
            if response.status_code == 200:
                print("Elasticsearch está listo!")
                break
        except:
            pass
        time.sleep(5)

def clean_data_line(line):
    """Limpia una línea de datos removiendo comillas extra"""
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]
    return line

def index_comuna():
    print("Indexando conteo por comuna...")
    with open("data/conteo_por_comuna/part-r-00000", "r", encoding="utf-8") as f:
        for line in f:
            try:
                line = clean_data_line(line)
                if ',' in line:
                    comuna, cantidad = line.split(",", 1)
                    doc = {
                        "comuna": comuna.strip(),
                        "cantidad": int(cantidad.strip())
                    }
                    response = requests.post(f"{ELASTIC_URL}/conteo_comuna/_doc",
                                             json=doc)
                    print(f"Indexado: {comuna} - {cantidad}")
            except Exception as e:
                print(f"Error procesando línea: {line} -> {e}")

def index_tipo():
    print("Indexando conteo por tipo...")
    with open("data/conteo_por_tipo/part-r-00000", "r", encoding="utf-8") as f:
        for line in f:
            try:
                line = clean_data_line(line)
                if ',' in line:
                    tipo, cantidad = line.split(",", 1)
                    doc = {
                        "tipo_incidente": tipo.strip(),
                        "cantidad": int(cantidad.strip())
                    }
                    response = requests.post(f"{ELASTIC_URL}/conteo_tipo/_doc",
                                             json=doc)
                    print(f"Indexado: {tipo} - {cantidad}")
            except Exception as e:
                print(f"Error procesando línea: {line} -> {e}")

if __name__ == "__main__":
    wait_for_elasticsearch()
    index_comuna()
    index_tipo()
    print("Indexación completa.")