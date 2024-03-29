from lib import queries
from lib.api import api
from lib.timer import *
import os
import shutil
import xml.etree.ElementTree as Et


def main():
    global game_timer

    if not os.path.exists('config'):
        shutil.copyfile('config.default.xml', 'config')

    conf_tree = Et.parse('config')
    conf_root = conf_tree.getroot()
    conf_settings = conf_root.find('settings')
    conf_timer = int(conf_settings.find('timer').text)

    if api.generate_tokens(conf_root):
        conf_tree.write('config')

    if not os.path.exists('openToW.sqlite'):
        queries.setup(conf_root)

    reset()
    api.start(
        conf_settings.find('ip').text,
        conf_settings.find('port').text
    )
    game_timer = RepeatedTimer(conf_timer, reset)
    menu_loop()


def reset():
    # api.stop()
    queries.update_sectors()
    winner = queries.winner()
    if not winner:
        pass
    else:
        queries.add_win(winner)
        queries.new_game()
        reset()
    # api.start()
    
    
def shutdown():
    game_timer.stop()
    api.stop()
    raise SystemExit
    

def menu_loop():
    while True:
        print_menu()
        response = input()
        menu_handler(response)


def menu_handler(response):
    try:
        menu_options[response]()
    except KeyError:
        pass


def print_menu():
    print("MAIN MENU:")
    print('0: Quit openTow')
        
        
menu_options = {
    '0': shutdown
}
    

if __name__ == "__main__":
    main()
