import cherrypy
from lib import queries
import secrets
import xml.etree.ElementTree as Et


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Sector(object):

    def GET(self, **params):
        if 'id' in params:
            return {
                'owner': queries.get_sector_owner(params['id']),
                'scores': queries.get_sector_scores(params['id']),
                'active': queries.sector_is_active(params['id'])
            }
        else:
            return queries.get_sectors()

    @cherrypy.tools.accept(media="application/json")
    def POST(self):
        j_request = cherrypy.request.json
        if not queries.sector_is_active(j_request['sector']):
            raise cherrypy.HTTPError(403, "Forbidden: Specified Sector is not active")
        
        if not queries.token_match(j_request['sector'], j_request['token']):
            raise cherrypy.HTTPError(401)
        queries.update_score(
            j_request['sector'],
            j_request['faction'],
            j_request['score']
        )


@cherrypy.expose
@cherrypy.tools.json_out()
class Border(object):
    def GET(self):
        return queries.get_borders()


@cherrypy.expose
@cherrypy.tools.json_out()
class Faction(object):
    def GET(self, **params):
        if 'id' in params:
            return queries.get_factions(params['id'])[params['id']]
        else:
            return queries.get_factions()


@cherrypy.expose
@cherrypy.tools.json_out()
class Player(object):
    def GET(self, **params):
        if 'id' in params:
            return queries.get_player_by_id()
        elif 'username' in params:
            return queries.get_player_by_username()
        else:
            return queries.get_players()


@cherrypy.expose
@cherrypy.tools.json_out()
class PlayerAccount(object):
    pass


def start(server_ip, server_port):
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [
                ('Content-Type', 'application/json'),
                ("Access-Control-Allow-Origin", "*")
            ]
        }
    }
    cherrypy.server.socket_host = server_ip
    cherrypy.server.socket_port = int(server_port)
    cherrypy.tree.mount(Sector(), "/sector", conf)
    cherrypy.tree.mount(Faction(), "/faction", conf)
    cherrypy.tree.mount(Border(), "/border", conf)
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
