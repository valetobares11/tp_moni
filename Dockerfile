# Utiliza la imagen base de Python 3.8.10
FROM python:3.8.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor en /app
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app/

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
