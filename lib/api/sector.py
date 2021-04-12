import cherrypy
from lib import queries


class Sector(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=["GET"])
    def all(self):
        return queries.get_sectors()

    def get_sector(self, sector_id):
        return {
            'owner': queries.get_sector_owner(sector_id),
            'scores': queries.get_sector_scores(sector_id),
            'active': queries.sector_is_active(sector_id)
        }

    def post_sector(self, j_request, sector_id):
        if not queries.sector_is_active(sector_id):
            raise cherrypy.HTTPError(403, "Forbidden: Specified Sector is not active")

        if not queries.token_match(sector_id, j_request['token']):
            raise cherrypy.HTTPError(401)
        queries.update_score(
            int(sector_id),
            j_request['faction'],
            j_request['score']
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media="application/json")
    @cherrypy.tools.allow(methods=["GET", "POST"])
    def default(self, sector_id):
        if cherrypy.request.method == "GET":
            return self.get_sector(sector_id)

        if cherrypy.request.method == "POST":
            return self.post_sector(cherrypy.request.json, sector_id)


