# openToW
openToW is an automated game server management tool that roughly emulates the "Theater of War" game mode from Tom Clancy's Endwar.

### Table of Contents
1. [How It Works](#how-it-works)

2. [Installation](#installation)

3. [Configuration](#configuration)
   - [Sectors](#sectors)
   - [Factions](#factions)
   - [Settings](#settings)
 
4. [Example Game](#example-game)

# How It Works
openToW keeps a local database of Sectors, which each correspond to a multiplayer game server. The database contains a record of what team controls the sector, what other sectors border it, whether the sector is active or not, and what scores each team has in that sector

Each time the sector owners are updated, openToW will check for any neighboring sectors that do not share the same owner. These sectors make up the border between two teams' territory and are contested. Contested sectors are marked as active, allowing teams to score points there. The API will reject score reports for any sectors that are not marked as active.

After each match on a server in the network, that server will report the winning team via openToW's http API, which will then update the team's score in the sector. After a set amount of time has passed, openToW will award ownership of a sector to the team with the most wins in the sector, and the map will be redrawn with the new sector owners and borders. If a single team owns all sectors on the map, that team will be awarded a win and the map will be reset to its original layout. 

# Installation
note: openToW Requires Python 3.6 or above

1. Clone the openToW repository

        git clone https://github.com/TrevorRowe123/openToW
    
2. Move into the newly created openToW directory

        cd openToW
    
3. Install dependencies

        pip3 install -r requirements.txt
    
4. Run openToW

        python3 opentow.py
        
# Configuration
During first run, openToW will create files needed to configure and run the program:

1. 'config.default.xml' will be copied to 'config'
2. 'openToW.sqlite' will be created and the database populated based on entries in config

The config file contains `<factions>`, `<sectors>`, and `<settings>` XML elements

## Sectors
Each sector element must have an `<id>`, `<startOwner>`, and `<border>`.  `<name>` is currently unused and `<token>` will be automatically generated if left out of the config.

    <sector>
        <id>8</id>
        <name>Blue HQ</name>
        <startOwner>Blue</startOwner>
        <border>6</border>
        <border>7</border>
        <token>_Ygc9NrI1--mHA</token>
    </sector>
    
`<id>`: Defines the ID of each sector, must be unique

`<startOwner>`: The name of the faction that owns the sector at game start, must match the `<name>` element of a faction

`<border>`: IDs of sectors that border the sector, each `<border>` must be the ID of another sector

`<token>`: The API token to be used for reporting scores in this sector. If missing from the config file, `<token>` will be auto generated
    
## Factions
Each `<faction>` element must have a `<name>` element, which must be unique

    <faction>
        <name>Red</name>
    </faction>
    
## Settings
The `<settings>` element contains server settings.

    <settings>
        <timer>60</timer>
        <ip>0.0.0.0</ip>
        <port>8080</port>
    </settings>

`<timer>`: Defines the time between each map refresh (in seconds)

`<ip>`: Defines the interface that the http server will listen on

`<port>`: Defines the TCP port that the http server will listen on

# Example Game

The example game shows a quick game playing out with the map and factions defined in `config.default.xml`

1. Game starts out with Red and Blue controlling equal parts of the map, and sectors on the border between the factions are contested.
![Initial Map](https://imgur.com/UyeDCMt.png)
    
2. Blue captures a sector from Red, shifting the border.
![Blue Takes a Sector](https://imgur.com/E0H8ncq.png)

3. Blue pushes further into Red territory, cornering Red at the edge of the map.
![Blue Pushes Forward](https://imgur.com/TJgcJqe.png)

4. Blue takes the remaining Red sector, causing a reset of the map and a win being added to Blue's tally.
![Blue Wins](https://imgur.com/XPV4MYD.png)
