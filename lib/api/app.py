from flask import Flask
import lib.api.border as border
import lib.api.faction as faction
import lib.api.sector as sector

app = Flask(__name__)

# Border Routes
app.add_url_rule('/border/', view_func=border.get_borders, methods=['GET'])

# Faction Routes
app.add_url_rule('/faction/all/', view_func=faction.get_all_factions, methods=['GET'])
app.add_url_rule('/faction/<int:faction_id>', view_func=faction.get_faction)

# Sector Routes
app.add_url_rule('/sector/all/', view_func=sector.get_all_sectors, methods=['GET'])
app.add_url_rule('/sector/<int:sector_id>', view_func=sector.get_sector, methods=['GET'])
app.add_url_rule('/sector/<int:sector_id>', view_func=sector.post_sector, methods=['POST'])
