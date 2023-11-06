import threading
import secrets
import websockets.sync.server
import xml.etree.ElementTree as Et

from cheroot.wsgi import PathInfoDispatcher, WSGIServer
from flask_cors import CORS
from lib.api.app import app


class ApiController:

    def __init__(self, server_ip: str, server_port: int):

        CORS(app)
        dispatcher = PathInfoDispatcher({'/': app})
        self.rest_server = WSGIServer(
            (
                server_ip,
                int(server_port)
            ),
            dispatcher
        )

        self.sock_server = websockets.sync.server.serve(
            self.register_connection,
            server_ip,
            int(server_port) + 1
        )
        self.SOCKET_CONNECTIONS = set()

    def register_connection(self, connection: websockets.sync.server.ServerConnection) -> None:
        self.SOCKET_CONNECTIONS.add(connection)
        try:
            for _ in connection:
                pass
        finally:
            self.SOCKET_CONNECTIONS.remove(connection)

    def notify(self) -> None:
        for connection in self.SOCKET_CONNECTIONS:
            connection.send("MAP UPDATE")

    def start(self) -> None:
        self.rest_server.prepare()
        threading.Thread(target=self.rest_server.serve).start()
        threading.Thread(target=self.sock_server.serve_forever).start()

    def stop(self) -> None:
        try:
            self.rest_server.stop()
            self.sock_server.shutdown()
        except NameError:
            print("Server has not been initialized, nothing to stop.")


def generate_tokens(conf_root) -> bool:
    conf_changed = False
    sectors = conf_root.find('sectors')
    for sector in sectors.iter('sector'):
        if sector.find('token') is None:
            new_token_element = Et.Element('token')
            new_token_element.text = secrets.token_urlsafe(10)
            sector.append(new_token_element)
            conf_changed = True

    return conf_changed
