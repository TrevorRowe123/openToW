import cherrypy
import queries


@cherrypy.expose
@cherrypy.tools.json_in()
class Sector(object):
    @cherrypy.tools.accept(media="application/json")
    def GET(self):
        return "Get method".encode("UTF-8")

    def POST(self):
        j_request = cherrypy.request.json
        if not queries.sector_is_active(j_request['sector']):
            raise cherrypy.HTTPError(403, "Forbidden: Specified Sector is not active")
        queries.update_score(
            j_request['sector'],
            j_request['faction'],
            j_request['score']
        )


@cherrypy.expose
class Faction(object):
    @cherrypy.tools.accept(media="application/json")
    def GET(self):
        return "Get method".encode("UTF-8")


def start():
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }
    }
    cherrypy.tree.mount(Sector(), "/sector", conf)
    cherrypy.tree.mount(Faction(), "/faction", conf)
    cherrypy.engine.start()
