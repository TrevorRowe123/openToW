import cherrypy
from lib import queries


def get_all_factions():
    return queries.get_factions()


def get_faction(faction_id):
    return queries.get_factions(faction_id)[faction_id]
