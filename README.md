# Sistemas distribuidos pt.1
Scraper de Eventos Waze
Este proyecto aborda el análisis y procesamiento de eventos de tráfico en tiempo real extraídos desde Waze Live Map. Dividiendose por el momento en dos etapas:

Entrega 1: Scraper automatizado, almacenamiento y consulta de eventos usando un backend REST, con soporte para políticas de caché (LRU y LFU) y simulación de usuarios (distribución uniforme o poisson).

Entrega 2: Análisis offline de los eventos mediante scripts de Apache Pig y un simulador de caché en Python para optimización de consultas sobre datasets.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Estructura
Entrega1/ ├── scraper/ → Automatiza navegador y extrae eventos reales (Playwright) ├── cache/ → Backend REST que almacena eventos recibidos ├── cacheador/ → Proxy con política de caché (LRU o LFU) ├── generador/ → Simula usuarios realizando consultas (uniforme o poisson) ├── docker-compose.yml

¿Cómo correr el sistema?
Clona el repositorio y entra al directorio:
  git clone https://github.com/tuusuario/tareasd.git
  cd tareasd
Inicia todo el sistema con Docker:
  sudo docker-compose up --build
  //Si usa windows: docker-compose up --build
Esto levantará automáticamente: 

scraper: ejecutará el script para capturar y enviar 10.000 eventos

cache: servidor de almacenamiento (/eventos)

cacheador: recibe consultas del generador y verifica si estas ya se encuentran en su memoria caché. Si es así, se considera un HIT en caso contrario, consulta al backend, almacena la respuesta y se registra como un MISS. En caso de que la caché esté llena, se aplica una política de reemplazo.

Registra estadísticas: cuántos hits, misses, tamaño de caché, etc. (http://localhost:8002/cache/stats)

generador: envía consultas al cacheador 

cambio de sistema de distribución: Para realizar el cambio entre la distibución poisson y uniforme, se debe descomentar las lineas 30 a la 32 del archivo docker-compose.yml y comentar las lineas 28 y 29.

Cambio de política de caché: Para cambiar entre las políticas LRU y LFU, se debe modificar la línea 42 del código, seleccionando la que se desea utilizar.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Análisis con Apache Pig (Entrega 2)

Descripción de scripts:
analisis_incidentes.pig: Realiza análisis de eventos sin filtrar.

analisis_limpios.pig: Análisis enfocado en eventos filtrados y limpios.

simulador_cache.py: Herramienta Python que emula políticas de caché y evalúa eficiencia sobre datasets.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Tecnologías Utilizadas
Python 3.12

Playwright – Automatización del navegador para el scraper

FastAPI – Backend REST

Apache Pig – Procesamiento masivo de datos

Docker + Docker Compose

Distribuciones: Uniforme y Poisson

Políticas de Caché: LRU y LFU

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Integrantes: -Diego Caña
             -Diego Mena
