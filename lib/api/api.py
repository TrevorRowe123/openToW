import threading
import secrets
import websockets.sync.server
import xml.etree.ElementTree as Et

from cheroot.wsgi import PathInfoDispatcher, WSGIServer
from flask_cors import CORS
from lib.api.app import app

rest_server: WSGIServer
sock_server: websockets.sync.server.WebSocketServer
SOCKET_CONNECTIONS = set()


def register_connection(connection: websockets.sync.server.ServerConnection) -> None:
    SOCKET_CONNECTIONS.add(connection)
    try:
        for msg in connection:
            pass
    finally:
        SOCKET_CONNECTIONS.remove(connection)


def notify() -> None:
    for connection in SOCKET_CONNECTIONS:
        connection.send("MAP UPDATE")


def start(server_ip: str, server_port: str) -> None:
    global rest_server
    global sock_server
    CORS(app)
    dispatcher = PathInfoDispatcher({'/': app})

    rest_server = WSGIServer(
        (
            server_ip,
            int(server_port)
        ),
        dispatcher
    )
    rest_server.prepare()
    threading.Thread(target=rest_server.serve).start()

    sock_server = websockets.sync.server.serve(
        register_connection,
        server_ip,
        int(server_port) + 1
    )
    threading.Thread(target=sock_server.serve_forever).start()


def stop() -> None:
    global rest_server
    global sock_server
    try:
        rest_server.stop()
        sock_server.shutdown()
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
