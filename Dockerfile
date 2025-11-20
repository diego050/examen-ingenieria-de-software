# Dockerfile (para el backend)

# 1. Usar una imagen base oficial de Python. 'slim' es una versión ligera.
FROM python:3.9-slim

WORKDIR /app

# ----> AÑADE ESTA LÍNEA AQUÍ <----
# Le dice a Python que incluya el directorio /app en su ruta de búsqueda de módulos.
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

EXPOSE 5000

CMD ["python", "src/infrastructure/adapters/api.py"]