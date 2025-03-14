import argparse
import logging
import threading

from enum import Enum
from src.server import Server
from src.client import Client


class PROTOCOLS(Enum):
    TCP = "TCP"
    UDP = "UDP"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--protocol",
        choices=[protocol.value for protocol in PROTOCOLS],
        help="Socket protocol",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    protocol = args.protocol

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("main")

    server = Server(protocol)
    client = Client(protocol)

    logger.info("Initializing server")
    threading.Thread(target=server.init_server).start()
    logger.info("Initializing client")
    threading.Thread(target=client.init_client).start()
