import logging
import socket

# Binded port on the server
PORT = 8000
# Close message
CLOSE_MSG = "CLOSE"


class Client:
    """Class client to interact with server"""

    def __init__(self, protocol: str):
        self.logger = logging.getLogger("client")
        self.protocol = protocol
        self.client = None
        self.host = None

        match self.protocol:
            # type: TCP - Stream
            case "TCP":
                # Get host by hostname in the case we are on the same device as server
                self.host = socket.gethostbyname(socket.gethostname())
                self.socket_type = socket.SOCK_STREAM

            # UDP - Diagram
            case "UDP":
                self.host = "127.0.0.1"
                self.socket_type = socket.SOCK_DGRAM
            case other:
                raise Exception(f"Unknown protocol {other}")

        # Tuple to connect to the server
        self.address = (self.host, PORT)

    def init_client(self) -> None:
        # Family: Internet
        self.client = socket.socket(socket.AF_INET, self.socket_type)

        if self.protocol == "TCP":
            self.tcp_setup()
        elif self.protocol == "UDP":
            self.udp_setup()

    def tcp_setup(self):
        # Bind the client to the server address
        self.logger.info(f"Connecting to {self.address}")
        self.client.connect(self.address)

        message = f"Hello from {socket.gethostbyname(socket.gethostname())}"
        self.logger.info("Sending message to the server")
        self.client.send(message.encode("utf-8"))

        reply = self.client.recv(1024).decode("utf-8")
        self.logger.info(f"Server replied: {reply}")

        self.client.close()
        self.logger.info(f"Closed connection on {self.address}")

    def udp_setup(self):
        # UDP does not require a connection so we can send the message directly to the server
        message = f"Hello from {socket.gethostbyname(socket.gethostname())}"
        self.logger.info(f"Sending message to the server on {self.address}")
        self.client.sendto(message.encode("utf-8"), self.address)

        reply, address = self.client.recvfrom(1024)
        reply = reply.decode()
        self.logger.info(f"{address} replied: {reply}")

        self.client.close()
        self.logger.info("Closed connection")
