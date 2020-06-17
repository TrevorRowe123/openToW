import cherrypy
from lib import queries


@cherrypy.expose
@cherrypy.tools.json_out()
class Faction(object):
    def GET(self, **params):
        if 'id' in params:
            return queries.get_factions(params['id'])[params['id']]
        else:
            return queries.get_factions()