# Sistemas Distribuidos – Scraper de Eventos Waze

Este proyecto aborda el análisis y procesamiento de eventos de tráfico en tiempo real extraídos desde Waze Live Map, dividido en tres etapas consecutivas:

- **Entrega 1**: Scraper automatizado, almacenamiento y consulta de eventos, usando como soporte políticas de caché (LRU y LFU) y simulación de usuarios (distribución uniforme o Poisson).
- **Entrega 2**: Análisis offline de los eventos mediante Apache Pig y un simulador de caché en Python para evaluar eficiencia de políticas sobre datasets.
- **Entrega 3**: Sistema completo de recolección, almacenamiento, consulta y visualización de eventos usando Elasticsearch y Kibana.

---

## Tecnologías Utilizadas

- **Python 3.12**
- **Playwright** 
- **FastAPI** – Backend
- **Apache Pig** – Análisis de datos
- **Elasticsearch** – Almacenamiento e indexación
- **Kibana** – Visualización de datos
- **Docker + Docker Compose**
- **Distribuciones**: Uniforme y Poisson
- **Políticas de Caché**: LRU y LFU

---

## Estructura General del Proyecto
```
Entrega 3
│   analisis_incidentes.pig
│   analisis_limpios.pig
│   docker-compose.yml
│   eventos_convertidos.csv
│   eventos_limpios.csv
│   eventos_region_metropolitana.json
│   filtrar_csv.py
│   geckodriver-v0.36.0-linux64.tar.gz
│   json_a_csv.py
│   main.py
│   requirements.txt
│   simulador_cache.py
│   verificar_datos.py
│   
├───cache
│       api.py
│       Dockerfile
│       requirements.txt
│
├───cacheador
│       cache.py
│       Dockerfile
│       main.py
│       requirements.txt
│
├───data
│   ├───conteo_por_comuna
│   │       part-r-00000
│   │
│   └───conteo_por_tipo
│           part-r-00000
│
├───generador
│       Dockerfile
│       generador.py
│       requirements.txt
│
├───indexer
│       Dockerfile
│       index_data.py
│       requirements.txt
│
├───resultados
│   ├───conteo_por_comuna
│   │       .part-r-00000.crc
│   │       ._SUCCESS.crc
│   │       part-r-00000
│   │       _SUCCESS
│   │
│   └───conteo_por_tipo
│           .part-r-00000.crc
│           ._SUCCESS.crc
│           part-r-00000
│           _SUCCESS
│
└───resultados_limpios
    ├───conteo_por_comuna
    │       .part-r-00000.crc
    │       ._SUCCESS.crc
    │       part-r-00000
    │       _SUCCESS
    │
    └───conteo_por_tipo
            .part-r-00000.crc
            ._SUCCESS.crc
            part-r-00000
            _SUCCESS
```

---

## Entrega 1 – Backend y Simulador

### Componentes:
- **Scraper**: Extrae eventos reales desde el mapa de Waze usando Playwright.
- **Cache**: API REST para almacenar eventos.
- **Cacheador**: Aplica política LRU o LFU a las consultas.
- **Generador**: Simula usuarios generando consultas con distribuciones configurables.

### Instrucciones de ejecución:
```bash
git clone https://github.com/Dmena1/Sistemas-distribuidos-1
cd Sistemas-distribuidos-1/'Entrega 1'
docker-compose up --build
```

- `http://localhost:8002/cache/stats`: Estadísticas del caché.

#### Cambios de configuración:
- **Distribución**: Editar `docker-compose.yml`, comentar líneas 28-29 y descomentar 30-32.
- **Política de Caché**: Cambiar línea 42 en `cacheador/main.py` por "LRU" o "LFU".

---

## Entrega 2 – Análisis Offline

### Scripts:

- `analisis_incidentes.pig`: Procesa eventos sin filtros.
- `analisis_limpios.pig`: Analiza eventos limpios.
- `simulador_cache.py`: Simula políticas de caché con datasets reales.

---

## Entrega 3 – Elasticsearch + Kibana

### Componentes:

- **Elasticsearch** 
- **Kibana** (puerto 5601): Visualización y dashboards.
- **Cache** (puerto 8001): Recibe y sirve eventos.
- **Cacheador** (puerto 8002): Proxy con caché LRU/LFU.
- **Indexer**: Procesa e indexa datos automáticamente.

### Instrucciones:

```bash
cd Sistemas-distribuidos-1/'Entrega 3'
docker-compose up --build
```

#### Verificar servicios:

```bash
curl http://localhost:5601
curl http://localhost:8001/eventos
curl http://localhost:8002/eventos
```

#### Acceso a Kibana:
Visita: [http://localhost:5601](http://localhost:5601)

#### Variables de entorno (`cacheador`):

- `CACHE_SIZE`: Tamaño del caché (default: 100)
- `CACHE_POLICY`: Política ("LRU" o "LFU")
- `BACKEND_URL`: URL del backend (default: http://cache:8001/eventos)

### Datos indexados:

- Índice `conteo_comuna`: Conteo por comuna
- Índice `conteo_tipo`: Conteo por tipo de incidente

---

## Notas Finales

- Elasticsearch puede tardar en inicializarse.
- Kibana requiere que Elasticsearch esté activo para funcionar.
- El servicio `indexer` espera automáticamente la disponibilidad de Elasticsearch.
- Los datos se indexan automáticamente al levantar los servicios.

---

## Integrantes

- Diego Caña  
- Diego Mena
