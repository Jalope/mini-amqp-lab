import json
import os
from datetime import datetime, timezone
from typing import Any

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class TrackProducer(MessagingHandler):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        address: str,
    ) -> None:
        super().__init__()

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.address = address

        self.sent = False

    # Se establece la conexión con el broker y se crea un sender para enviar mensajes a la address especificada.
    def on_start(self, event: Any) -> None:
        connection_url = f"amqp://{self.host}:{self.port}"

        print(f"Conectando a {connection_url}...")

        connection = event.container.connect(
            connection_url,
            user=self.username,
            password=self.password,
        )

        event.container.create_sender(
            connection,
            self.address,
        )

        print(f"Sender creado para la address '{self.address}'.")

    # Este método se llama cuando el sender dispone de crédito y puede transfereir mensajes al broker. 
    def on_sendable(self, event: Any) -> None:
        if self.sent:
            return

        track = {
            "messageId": "track-0002",
            "trackOrigin": "BCN",
            "trackNumber": 5678,
            "callsign": "VLG5678",
            "flightLevel": 280,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        message = Message(
            # Transformamos el diccionario en una cadena JSON.
            body=json.dumps(track),
            # El parámetro durable=True indica que el mensaje debe ser persistente y sobrevivir a reinicios del broker.
            durable=True,
        )

        event.sender.send(message)

        self.sent = True

        print("\nMensaje enviado:")
        print(json.dumps(track, indent=2, ensure_ascii=False))

    # Este método se llama cuando el broker acepta el mensaje enviado.
    def on_accepted(self, event: Any) -> None:
        print("\nArtemis ha aceptado el mensaje.")

        event.sender.close()
        event.connection.close()

    def on_rejected(self, event: Any) -> None:
        print(f"\nArtemis ha rechazado el mensaje: {event.delivery.remote_state}")

        event.sender.close()
        event.connection.close()

    def on_transport_error(self, event: Any) -> None:
        print(f"Error de transporte AMQP: {event.transport.condition}")


def get_required_environment_variable(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"La variable de entorno obligatoria '{name}' no está definida."
        )

    return value


def main() -> None:
    producer = TrackProducer(
        host=get_required_environment_variable("AMQP_HOST"),
        port=int(get_required_environment_variable("AMQP_PORT")),
        username=get_required_environment_variable("AMQP_USER"),
        password=get_required_environment_variable("AMQP_PASSWORD"),
        address=get_required_environment_variable("AMQP_ADDRESS"),
    )

    try:
        Container(producer).run()
    except KeyboardInterrupt:
        print("\nProductor detenido manualmente.")


if __name__ == "__main__":
    main()