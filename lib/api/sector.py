import cherrypy
from lib import queries


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