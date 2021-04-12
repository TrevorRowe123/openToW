import cherrypy
import secrets
import xml.etree.ElementTree as Et

import lib.api.border as borders
import lib.api.faction as factions
import lib.api.sector as sectors


def start(server_ip, server_port):
    conf = {
        '/': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [
                ('Content-Type', 'application/json'),
                ("Access-Control-Allow-Origin", "*")
            ],
        }
    }
    cherrypy.server.socket_host = server_ip
    cherrypy.server.socket_port = int(server_port)

    cherrypy.tree.mount(sectors.Sector(), "/sector", conf)
    cherrypy.tree.mount(factions.Faction(), "/faction", conf)
    cherrypy.tree.mount(borders.Border(), "/border", conf)

    cherrypy.engine.start()


def stop():
    cherrypy.engine.exit()


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
