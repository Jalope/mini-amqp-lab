# Mini AMQP Lab

Laboratorio local para aprender AMQP 1.0 utilizando Apache ActiveMQ Artemis y Python.

## Arquitectura actual

```text
Productor AMQP
      │
      ▼
Address: tracks.distribution
      │ MULTICAST
      ▼
Queue: client-a.tracks
      │
      ▼
Consumidor Python
```

La address representa el destino donde publica el AMQP Distribution Service.

La queue representa la cola asignada a un cliente externo.

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

## Ejecutar el consumidor

```bash
docker compose run --rm consumer
```

El consumidor accede a la cola mediante su Fully Qualified Queue Name:

```text
tracks.distribution::client-a.tracks
```

La imagen del consumidor incluye `cyrus-sasl-plain` para permitir la autenticación mediante usuario y contraseña.

## Estado actual

- Address multicast creada.
- Cola durable creada.
- Mensaje enviado manualmente.
- Consumidor AMQP implementado.
- Mensaje recibido y confirmado correctamente.
- Productor creado y mensaje distribuido por el broker a la única cola existente
