# Mini AMQP Lab

Laboratorio local para aprender AMQP 1.0 utilizando Apache ActiveMQ Artemis y Python.

## Arquitectura actual

### Distribución a clientes externos

```text
Productor AMQP
      │
      ▼
Address: tracks.distribution
      │ MULTICAST
      ├── Queue: client-a.tracks
      └── Queue: client-b.tracks
```

Cada cola representa a un cliente externo y recibe una copia independiente de cada mensaje publicado.

### Procesamiento repartido

```text
Productor AMQP
      │
      ▼
Address: tracks.processing
      │ ANYCAST
      ├── Queue: worker-a.tracks
      └── Queue: worker-b.tracks
```

Cada mensaje se enruta a una sola cola compatible.

## Tecnologías

- Docker Compose
- Apache ActiveMQ Artemis
- Python
- Apache Qpid Proton

## Arranque

```bash
docker compose up -d artemis
```

Consola de Artemis:

```text
http://localhost:8161
```

## Ejecutar el productor

Publicación en la address multicast configurada por defecto:

```bash
docker compose run --rm producer
```

Publicación en la address anycast:

```bash
docker compose run --rm -e "AMQP_ADDRESS=tracks.processing" producer
```

## Ejecutar el consumidor

Consumir de la cola configurada por defecto:

```bash
docker compose run --rm consumer
```

Consumir de una cola concreta:

```bash
docker compose run --rm \
  -e "AMQP_QUEUE=tracks.distribution::client-b.tracks" \
  consumer
```

El consumidor accede a una cola mediante su Fully Qualified Queue Name:

```text
address::queue
```

Ejemplo:

```text
tracks.distribution::client-a.tracks
```

La imagen de productor y consumidor incluye `cyrus-sasl-plain` para permitir la autenticación mediante usuario y contraseña.

## Conceptos comprobados

- Diferencia entre address y queue.
- Publicación del productor en una address.
- Consumo desde una cola concreta.
- Colas y mensajes durables.
- Persistencia de mensajes tras reiniciar Artemis.
- Confirmación del productor mediante `accepted`.
- Confirmación del consumidor mediante acknowledgement.
- Routing `MULTICAST`: una copia por cada cola.
- Consumidores competidores dentro de una misma cola.
- Selección de cola mediante variables de entorno.
- Routing `ANYCAST`: cada mensaje se almacena en una sola cola compatible.

## Estado actual

El laboratorio dispone de:

- Dos colas multicast para clientes externos.
- Dos colas anycast para workers equivalentes.
- Productor AMQP reutilizable.
- Consumidor AMQP reutilizable.
- Mensajes con identificador dinámico y cuerpo JSON.
