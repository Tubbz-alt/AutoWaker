import logging
import os

LOG = logging.getLogger(name="autoWaker")

#Returns the path contained in the config file.
def getPath():
    config_file = open(getRelativeLocation())
    relative_path = config_file.readline().strip()
    config_file.close()
    LOG.info('Relative path read from file: ' + relative_path)
    return relative_path

#Moves back a directory and grabs the config file.
def getRelativeLocation():
    try:
        cwd = os.getcwd()
        supposed_config_path = cwd.split('/')
        supposed_config_string_unjoined = supposed_config_path[0:len(supposed_config_path)-1]+['Config.txt']
        return '/'.join(supposed_config_string_unjoined)
    except:
        LOG.error('Tossed when trying to get the relative location of Config.txt.')