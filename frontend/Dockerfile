# frontend/Dockerfile

# 1. Usar una imagen base de Nginx muy ligera ('alpine').
FROM nginx:alpine

# 2. Copiar tu archivo HTML al directorio por defecto donde Nginx sirve contenido estático.
COPY index.html /usr/share/nginx/html/index.html

# 3. Exponer el puerto 80 (puerto por defecto de HTTP).
EXPOSE 80