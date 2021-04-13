import cherrypy
from lib import queries


class Faction(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=["GET"])
    def all(self):
        return queries.get_factions()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=["GET"])
    def default(self, faction_id):
        return queries.get_factions(faction_id)[faction_id]

