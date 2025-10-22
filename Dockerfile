# Usar imagen oficial de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py .
COPY tests/ tests/

# Exponer el puerto
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]