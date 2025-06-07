# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del backend
COPY . .

# Expone el puerto que usará Flask (Render lo detecta automáticamente)
EXPOSE 5000

# Comando para correr la aplicación
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flaskr.app:app"]
