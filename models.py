from peewee import *

db = SqliteDatabase("openToW.sqlite")


class BaseModel(Model):

    class Meta:
        database = db


class Faction(BaseModel):
    name = CharField(primary_key=True)


class Sector(BaseModel):
    id = IntegerField(primary_key=True)
    owner_faction = ForeignKeyField(Faction, backref="owned")
    owner_faction_default = ForeignKeyField(Faction)
    active = BooleanField()


class Border(BaseModel):
    sector_1 = ForeignKeyField(Sector)
    sector_2 = ForeignKeyField(Sector)


class Score(BaseModel):
    sector = ForeignKeyField(Sector)
    faction = ForeignKeyField(Faction)
    score = IntegerField()
