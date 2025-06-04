FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo los archivos necesarios
COPY simulador_cache.py .
COPY eventos_limpios.csv .
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el simulador de caché
CMD ["python", "simulador_cache.py"]
