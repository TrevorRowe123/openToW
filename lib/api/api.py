from cheroot.wsgi import PathInfoDispatcher, Server
from app import app
import secrets
import xml.etree.ElementTree as Et

server: Server


def start(server_ip, server_port):
    global server
    dispatcher = PathInfoDispatcher({'/': app})
    server = Server(
        (server_ip, server_port),
        dispatcher
    )
    server.start()


def stop():
    global server
    try:
        server.stop()
    except:
        pass


def generate_tokens(conf_root):
    conf_changed = False
    sectors = conf_root.find('sectors')
    for sector in sectors.iter('sector'):
        if sector.find('token') is None:
            new_token_element = Et.Element('token')
            new_token_element.text = secrets.token_urlsafe(10)
            sector.append(new_token_element)
            conf_changed = True

    return conf_changed
