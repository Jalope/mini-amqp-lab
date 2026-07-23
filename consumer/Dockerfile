# Construimos una imagen capaz de ejectura el consumidor AMQP def en consumer.py

# Este tipo de archivos se ejecutan en dos fases: 1. La primera vez hay que construirlo mediante el comando de docker "build": <docker build -t amqp-consumer .> 2. A partir de aqui lo que hacemos es arrancar el contenedor mediante el comando "run" de docker: <docker run amqp-consumer> 

# Instalación mínima de distro linux 
FROM fedora:43

#dfn es la palabra clave en fedora para gestionar paquetes (el apt de ubuntu) "-y para responder que si a las preguntas de instalación."
RUN dnf install -y \
        # Paquete de python
        python3 \
        # Biblioteca de python que permite comunicarse mediante AMQP 1.0
        python3-qpid-proton \
        # mecanismo SASL (Capa de Autenticación y Seguridad Simple) compatible con el broker Artemis
        cyrus-sasl-plain \
    # Limpiamos cache descargada por dfn. "&& => que solo ejecuta esta linea si el anterior dfn funcionó"
    && dnf clean all

# Crea o selecciona /app como directorio de trabajo dentro del contenedor (Hace algo como un: cd app)
WORKDIR /app

# Copia el archivo de python con el cliente (el punto le dice que en el directorio actual de trabajo)
COPY consumer.py .

# Docker ejecuta python sin pasar por consolas intermedias
CMD ["python3", "consumer.py"]