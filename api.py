import cherrypy
import queries


@cherrypy.expose
class Sector(object):
    @cherrypy.tools.accept(media="application/json")
    def GET(self):
        return "Get method".encode("UTF-8")

    def POST(self):
        queries.update_score(1, 'Red', 2)


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
