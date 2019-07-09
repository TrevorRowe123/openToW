from models import *


def get_sectors():
    sector_list = []
    sectors = Sector.select()
    for sector in sectors:
        sector_list.append({
            'id': sector.id,
            'owner': sector.owner_faction.name,
            'active': sector.active
        })
    return sector_list


def get_owned_sectors(faction_id):
    sector_list = []
    owned_sectors = Faction.get(Faction.name == faction_id).owned
    for sector in owned_sectors:
        sector_list.append(sector.id)
    return sector_list


def get_borders():
    list_borders = []
    borders = Border.select()
    for border in borders:
        list_borders.append({
            'from': border.sector_1.id,
            'to': border.sector_2.id
        })
    return list_borders


def get_faction_scores(faction_id):
    dict_scores = {}
    scores = Score.select().where(Score.faction == faction_id)
    for score in scores:
        dict_scores[score.sector.id] = score.score
    return dict_scores


def sector_is_active(sector_id):
    return Sector.get(Sector.id == sector_id).active


def get_sector_scores(sector_id):
    dict_scores = {}
    scores = Score.select().where(Score.sector == sector_id)
    for score in scores:
        dict_scores[score.faction.name] = score.score
    return dict_scores


def get_sector_owner(sector_id):
    return Sector.get(Sector.id == sector_id).owner_faction.name


def update_score(sector_id, faction_id, points):
    Score.update(score=Score.score + points).where(
            Score.sector == Sector.get_by_id(sector_id),
            Score.faction == Faction.get_by_id(faction_id)
    ).execute()


def set_active_sectors():
    Sector.update(active=False).execute()
    with db.atomic():
        for border in Border.select():
            if border.sector_1.owner_faction != border.sector_2.owner_faction:
                border.sector_1.active = True
                border.sector_2.active = True
                border.sector_1.save()
                border.sector_2.save()


def update_sector_owners():
    active_sectors = Sector.select().where(Sector.active)
    with db.atomic():
        for sector_id in active_sectors:
            defender = Score.get(Score.sector == sector_id, Score.faction == sector_id.owner_faction)
            attackers = Score.select().where(
                Score.score > defender.score,
                Score.faction != sector_id.owner_faction,
                Score.sector == sector_id
            )
            for attacker in attackers:
                if attacker.score > defender.score:
                    defender = attacker

            sector_id.owner_faction = Faction.get_by_id(defender.faction)
            sector_id.save()
        
        Score.update(score=0).execute()


def setup(conf_root):
    sectors = conf_root.find('sectors').findall('sector')
    factions = conf_root.find('factions').findall('faction')
    create_tables()
    create_factions(factions)
    create_sectors(sectors)
    create_borders(sectors)
    create_scores()


def create_tables():
    # create tables
    with db:
        db.create_tables([Faction, Sector, Border, Score])


def create_factions(factions):
    # create faction records
    with db.atomic():
        for faction in factions:
            Faction.create(
                name=faction.find('name').text
            )


def create_sectors(sectors):
    # create sector records
    with db.atomic():
        for sector in sectors:
            Sector.create(
                id=sector.find('id').text,
                owner_faction=Faction.get_by_id(sector.find('startOwner').text),
                owner_faction_default=Faction.get_by_id(sector.find('startOwner').text),
                active=False
            )


def create_borders(sectors):
    # create border records
    with db.atomic():
        for sector in sectors:
            for border in sector.findall('border'):
                if not Border.select().where(
                        Border.sector_1 == border.text,
                        Border.sector_2 == sector.find('id').text
                ):
                    Border.create(
                        sector_1=sector.find('id').text,
                        sector_2=border.text
                    )


def create_scores():
    # create score records
    with db.atomic():
        for faction_key in Faction.select():
            for sector_key in Sector.select():
                Score.create(
                    sector=sector_key,
                    faction=faction_key,
                    score=0
                )


def update_sectors():
    update_sector_owners()
    set_active_sectors()
