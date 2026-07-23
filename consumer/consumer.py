import json
import os
from typing import Any

from proton.handlers import MessagingHandler
from proton.reactor import Container

# Qpid Proton utiliza un modelo dirigido por eventos. Nuestra clase no ejecuta un bucle que pregunte constantemente si hay mensajes, define funciones que Proton invocará cuando ocurra algo
# Los dos eventos más importantes son:
# - on_start: se invoca cuando comienza la aplicación AMQP
# - on_message: se invoca cuando se recibe un mensaje


class TrackConsumer(MessagingHandler):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        queue: str,
    ) -> None:
        super().__init__(auto_accept=True)

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue = queue

        self.connection = None
        self.receiver = None

    def on_start(self, event: Any) -> None:
        connection_url = f"amqp://{self.host}:{self.port}"

        print(f"Conectando a {connection_url}...")

        # Esto no es un contenedor de Docker, es un contenedor de Qpid Proton. Un contenedor es un objeto que administra la conexión y el receptor de mensajes. Cuando se inicia la aplicación, se crea un contenedor y se le pasa nuestra clase TrackConsumer como event driver
        self.connection = event.container.connect(
            connection_url,
            user=self.username,
            password=self.password,
        )

        # El receiver es un objeto que se encarga de recibir mensajes de la cola. Se crea a partir del contenedor y la conexión, y se le pasa el nombre de la cola a la que queremos suscribirnos
        self.receiver = event.container.create_receiver(
            self.connection,
            self.queue,
        )

        print(f"Esperando un mensaje en la cola '{self.queue}'...")

    # Procesamiento del mensaje
    def on_message(self, event: Any) -> None:
        print("\nMensaje recibido:")

        body = event.message.body

        if isinstance(body, bytes):
            body = body.decode("utf-8")

        if isinstance(body, str):
            self._print_text_body(body)
        else:
            print(body)

        print("\nMensaje procesado. Cerrando el consumidor.")

        event.receiver.close()
        event.connection.close()

    def on_transport_error(self, event: Any) -> None:
        print(f"Error de transporte AMQP: {event.transport.condition}")

    @staticmethod
    def _print_text_body(body: str) -> None:
        try:
            parsed_body = json.loads(body)
            print(json.dumps(parsed_body, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(body)


def get_required_environment_variable(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"La variable de entorno obligatoria '{name}' no está definida."
        )

    return value


def main() -> None:
    consumer = TrackConsumer(
        host=get_required_environment_variable("AMQP_HOST"),
        port=int(get_required_environment_variable("AMQP_PORT")),
        username=get_required_environment_variable("AMQP_USER"),
        password=get_required_environment_variable("AMQP_PASSWORD"),
        queue=get_required_environment_variable("AMQP_QUEUE"),
    )

    try:
        Container(consumer).run()
    except KeyboardInterrupt:
        print("\nConsumidor detenido manualmente.")


if __name__ == "__main__":
    main()