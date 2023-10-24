import threading

from cheroot.wsgi import PathInfoDispatcher, Server
from lib.api.app import app
import secrets
import xml.etree.ElementTree as Et

server: Server


def start(server_ip: str, server_port: str) -> None:
    global server
    dispatcher = PathInfoDispatcher({'/': app})
    server = Server(
        (
            server_ip,
            int(server_port)
        ),
        dispatcher
    )
    server.prepare()
    threading.Thread(target=server.serve).start()


def stop() -> None:
    global server
    try:
        server.stop()
    except:
        pass


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
