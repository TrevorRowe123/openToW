import queries
import api
import os
import xml.etree.ElementTree as Et

conf_tree = Et.parse('config')
conf_root = conf_tree.getroot()

if not os.path.exists('openToW.sqlite'):
    queries.setup(conf_root)


def main():
    queries.set_active_sectors()
    api.start()


if __name__ == "__main__":
    main()
