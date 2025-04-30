FROM python:3.12-slim

# Instalar librerías del sistema que necesita Playwright para funcionar
RUN apt-get update && apt-get install -y \
    wget gnupg libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 libxss1 \
    libasound2 libatk-bridge2.0-0 libx11-xcb1 libdrm2 libgbm1 libu2f-udev \
    && apt-get clean

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores necesarios para Playwright
RUN python -m playwright install --with-deps

# Ejecución del script
CMD ["python", "main.py"]
