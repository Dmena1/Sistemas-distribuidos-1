# Sistemas distribuidos pt.1
Scraper de Eventos Waze
Este proyecto extrae eventos en tiempo real desde Waze Live Map, los almacena en un backend, simula consultas y utiliza un cache.

Estructura
tareasd/ ├── scraper/ → Automatiza navegador y extrae eventos reales (Playwright) ├── cache/ → Backend REST que almacena eventos recibidos ├── cacheador/ → Proxy con política de caché (LRU o LFU) ├── generador/ → Simula usuarios realizando consultas (uniforme o poisson) ├── docker-compose.yml

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

generador: envía consultas al cacheador 

Tecnologías utilizadas
Python 3.12

Playwright (automatización de navegador)

FastAPI (API REST)

Docker + Docker Compose
   
Distribuciones: Poisson y Uniforme

Políticas de caché: LRU y LFU

Integrantes: -Diego Caña
             -Diego Mena
