# Entrega 3 - Sistema Distribuido con Elasticsearch

Esta entrega implementa un sistema completo de recolección, almacenamiento y consulta de eventos de tráfico con Elasticsearch y Kibana.

## Arquitectura

El sistema está compuesto por los siguientes servicios:

- **Elasticsearch**: Base de datos NoSQL para indexar y buscar datos
- **Kibana**: Interfaz web para visualizar y consultar datos
- **Cache**: API REST para recibir eventos de tráfico
- **Cacheador**: Proxy con caché LRU/LFU para optimizar consultas
- **Indexer**: Servicio para indexar datos procesados en Elasticsearch

## Servicios

### 1. Elasticsearch (Puerto 9200)
Base de datos NoSQL para almacenar y buscar eventos indexados.

### 2. Kibana (Puerto 5601)
Interfaz web para visualizar datos y crear dashboards.

### 3. Cache (Puerto 8001)
API REST que recibe eventos de tráfico y los almacena en memoria.

**Endpoints:**
- `POST /eventos` - Recibe un evento de tráfico
- `GET /eventos` - Consulta eventos con filtros opcionales

### 4. Cacheador (Puerto 8002)
Proxy con caché que optimiza las consultas al backend.

**Endpoints:**
- `GET /eventos` - Consulta eventos con caché
- `GET /cache/stats` - Estadísticas del caché

### 5. Indexer
Servicio que indexa datos procesados en Elasticsearch.

## Instalación y Uso

### 1. Levantar los servicios
```bash
docker-compose up -d
```

### 2. Verificar que los servicios estén funcionando
```bash
# Elasticsearch
curl http://localhost:9200/_cluster/health

# Kibana
curl http://localhost:5601

# Cache
curl http://localhost:8001/eventos

# Cacheador
curl http://localhost:8002/eventos
```

### 3. Recolectar eventos (opcional)
```bash
python main.py
```

### 4. Acceder a Kibana
Abrir http://localhost:5601 en el navegador.

## Configuración

### Variables de entorno del Cacheador:
- `CACHE_SIZE`: Tamaño del caché (default: 100)
- `CACHE_POLICY`: Política de caché - "LRU" o "LFU" (default: "LFU")
- `BACKEND_URL`: URL del backend (default: http://cache:8001/eventos)

### Datos indexados:
- **Índice `conteo_comuna`**: Conteo de incidentes por comuna
- **Índice `conteo_tipo`**: Conteo de incidentes por tipo

## Consultas de ejemplo

### Desde el caché:
```bash
# Consultar eventos por tipo
curl "http://localhost:8002/eventos?tipo=JAM"

# Consultar eventos por ciudad
curl "http://localhost:8002/eventos?ciudad=Santiago"

# Ver estadísticas del caché
curl "http://localhost:8002/cache/stats"
```

### Desde Elasticsearch:
```bash
# Consultar conteo por comuna
curl "http://localhost:9200/conteo_comuna/_search"

# Consultar conteo por tipo
curl "http://localhost:9200/conteo_tipo/_search"
```

## Estructura de archivos

```
Entrega 3/
├── docker-compose.yml          # Configuración de servicios
├── main.py                     # Recolector de eventos
├── cache/                      # Servicio de cache
│   ├── api.py
│   ├── Dockerfile
│   └── requirements.txt
├── cacheador/                  # Servicio de caché
│   ├── main.py
│   ├── cache.py
│   ├── Dockerfile
│   └── requirements.txt
├── indexer/                    # Servicio de indexación
│   ├── index_data.py
│   ├── Dockerfile
│   └── requirements.txt
└── data/                       # Datos procesados
    ├── conteo_por_comuna/
    └── conteo_por_tipo/
```

## Notas importantes

1. **Elasticsearch** puede tardar unos minutos en estar completamente listo
2. **Kibana** necesita que Elasticsearch esté funcionando
3. El **indexer** espera automáticamente a que Elasticsearch esté listo
4. Los datos se indexan automáticamente al levantar los servicios 