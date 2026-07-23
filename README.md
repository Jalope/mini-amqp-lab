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