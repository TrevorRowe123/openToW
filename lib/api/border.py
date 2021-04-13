import cherrypy
from lib import queries


class Border(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=["GET"])
    def default(self):
        return queries.get_borders()
