from lib import queries
from flask import abort


def get_all_sectors():
    return queries.get_sectors()


def get_sector(sector_id):
    return {
        'owner': queries.get_sector_owner(sector_id),
        'scores': queries.get_sector_scores(sector_id),
        'active': queries.sector_is_active(sector_id)
    }


def post_sector(j_request, sector_id):
    if not queries.sector_is_active(sector_id):
        abort(403, "Forbidden: Specified Sector is not active")

    if not queries.token_match(sector_id, j_request['token']):
        abort(401)
    queries.update_score(
        int(sector_id),
        j_request['faction'],
        j_request['score']
    )
