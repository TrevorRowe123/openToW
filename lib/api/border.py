import cherrypy
from lib import queries


@cherrypy.expose
@cherrypy.tools.json_out()
class Border(object):
    def GET(self):
        return queries.get_borders()