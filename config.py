""" Parse the external config parameters from config.ini """

import configparser

CONFIG_FILE = "config.ini"

def get_config_value(section, name):
    """ Return the specified name if it exists in the section """

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if name in config[section]:
        return config.get(section, name)
    else:
        return 'False'
