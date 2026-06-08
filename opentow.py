import argparse
import os
import shutil
import time
import xml.etree.ElementTree as Et

from lib import queries
from lib.api import api
from lib.timer import RepeatedTimer

game_timer = None


def init():
    if not os.path.exists('config'):
        shutil.copyfile('config.default.xml', 'config')

    conf_tree = Et.parse('config')
    conf_root = conf_tree.getroot()

    if api.generate_tokens(conf_root):
        conf_tree.write('config')
        
    # Wait for the database to be fully stable before running schema migrations
    from lib.models import db
    for i in range(10):
        try:
            db.connect(reuse_if_open=True)
            break
        except Exception as e:
            print(f"Database not ready. Retrying in 3 seconds... ({i+1}/10)")
            time.sleep(3)
    else:
        print("Failed to connect to the database after multiple attempts. Exiting.")
        raise SystemExit(1)

    queries.setup(conf_root)
    print("Database setup complete.")
    return conf_root


def tick():
    queries.update_sectors()
    winner = queries.winner()
    if winner:
        queries.add_win(winner)
        queries.new_game()
        tick()
    print("Tick complete.")
    

def reset():
    tick()


def shutdown():
    global game_timer
    if game_timer:
        game_timer.stop()
    api.stop()
    raise SystemExit


def menu_loop():
    while True:
        print_menu()
        response = input()
        menu_handler(response)


def menu_handler(response):
    menu_options = {'0': shutdown}
    try:
        menu_options[response]()
    except KeyError:
        pass


def print_menu():
    print("MAIN MENU:")
    print('0: Quit openTow')


def standalone():
    global game_timer
    conf_root = init()
    conf_settings = conf_root.find('settings')
    conf_timer = int(conf_settings.find('timer').text)
    
    api.start(conf_settings.find('ip').text, conf_settings.find('port').text)
    game_timer = RepeatedTimer(conf_timer, reset)
    menu_loop()


def main():
    parser = argparse.ArgumentParser(description="openToW management CLI")
    parser.add_argument('command', choices=['init', 'tick', 'standalone'], help='Command to run')
    args = parser.parse_args()

    if args.command == 'init':
        init()
    elif args.command == 'tick':
        tick()
    elif args.command == 'standalone':
        standalone()


if __name__ == "__main__":
    main()
