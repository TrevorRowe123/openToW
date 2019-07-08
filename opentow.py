import queries
import api
import os
import xml.etree.ElementTree as Et
from timer import *


def main():
    conf_tree = Et.parse('config')
    conf_root = conf_tree.getroot()
    conf_settings = conf_root.find('settings')
    conf_timer = int(conf_settings.find('timer').text)

    if not os.path.exists('openToW.sqlite'):
        queries.setup(conf_root)

    reset()
    game_timer = RepeatedTimer(conf_timer, reset)


def reset():
    api.stop()
    queries.update_sectors()
    api.start()
    

if __name__ == "__main__":
    main()
