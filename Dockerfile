# Usa una imagen oficial de Playwright con todos los navegadores y librerías necesarias
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos al contenedor
COPY . /app

# Instala las dependencias desde requirements_render.txt
RUN pip install --no-cache-dir -r requirements_render.txt

# Instala los navegadores de Playwright
RUN playwright install

# Ejecuta el bot al iniciar el contenedor
CMD ["python", "bot_render.py"]
