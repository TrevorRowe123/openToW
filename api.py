import cherrypy
import queries


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
    def GET(self, id):
        return {
            'owned': queries.get_owned_sectors(id),
            'scores': queries.get_faction_scores(id)
        }


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
    cherrypy.tree.mount(Border(), "/border", conf)
    cherrypy.engine.start()


def stop():
    cherrypy.engine.exit()
