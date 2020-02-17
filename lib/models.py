from peewee import *

db = SqliteDatabase("openToW.sqlite")


class BaseModel(Model):

    class Meta:
        database = db


class Faction(BaseModel):
    name = CharField(primary_key=True)
    total_wins = IntegerField(default=0)


class Sector(BaseModel):
    id = IntegerField(primary_key=True)
    owner_faction = ForeignKeyField(Faction, backref="owned")
    owner_faction_default = ForeignKeyField(Faction)
    active = BooleanField()
    token = CharField()


class Border(BaseModel):
    sector_1 = ForeignKeyField(Sector)
    sector_2 = ForeignKeyField(Sector)


class Score(BaseModel):
    sector = ForeignKeyField(Sector, backref="scores")
    faction = ForeignKeyField(Faction, backref="scores")
    score = IntegerField()


class Player(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField()
    faction = ForeignKeyField(Faction, backref="players")
