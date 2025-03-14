import logging
import socket

# Binded port
PORT = 8000
# Maximum connections allowed
MAX_CONN = 5

class Server:
    """Server class to interact with clients"""

    def __init__(self, protocol: str):
        self.logger = logging.getLogger("server")
        self.protocol = protocol
        self.server = None
        self.host = None

        match self.protocol:
            case "TCP":
                # Get host by hostname
                self.host = socket.gethostbyname(socket.gethostname())
                # Type: TCP - Stream
                self.socket_type = socket.SOCK_STREAM

            case "UDP":
                self.host = "0.0.0.0"
                # UDP - Diagram
                self.socket_type = socket.SOCK_DGRAM

            case other:
                raise Exception(f"Unknown protocol {other}")

        self.address = (self.host, PORT)

    def init_server(self) -> None:
        # Family: Internet
        self.server = socket.socket(socket.AF_INET, self.socket_type)

        if self.protocol == "TCP":
            self.tcp_setup()
        elif self.protocol == "UDP":
            self.udp_setup()

    def tcp_setup(self):
        # Bind the server to the desired address
        self.server.bind(self.address)

        # Listen connections
        self.server.listen(MAX_CONN)
        self.logger.info("Server UP!")

        while True:
            # Accept returns the communication socket and the address
            client, address = self.server.accept()
            self.logger.info(f"Received connection on {address}")

            # When we communicate, we send bytes of information, so we need to decode them
            message = client.recv(1024).decode("utf-8")
            self.logger.info(f"Received message: {message}")

            reply = f"Goodbye {address}!"
            client.send(reply.encode("utf-8"))

            client.close()
            self.logger.info(f"Closed connection on {address}")

            break

    def udp_setup(self):
        # Bind the server to the desired address
        self.server.bind(self.address)

        # Listen connections
        self.logger.info("Server UP!")

        while True:
            self.logger.info(f"Listening for messages on {self.host}:{PORT}")

            # When we communicate on UDP we do not stablish any connection, just listen for messages
            message, address = self.server.recvfrom(1024)
            message = message.decode()
            self.logger.info(f"Received message: {message}")

            reply = f"Message received my friend on {address}!"
            self.server.sendto(reply.encode(), address)

            self.server.close()
            self.logger.info("Closed connection")

            break
