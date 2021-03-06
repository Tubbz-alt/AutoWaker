import logging
import os

from ConfigHandler import getPath
from TimeHandler import today


#  Puts log into a relative location, and adds a day stamp.
def setupLogger():
    today_as_dt = today()
    logging.basicConfig(filename='sleepDataLogs.log',level=logging.INFO, filemode ='w')
    
    # ~/Logs/sleepLogs*date*.log
    relative_log_location = [getPath(), 'Logs', 'sleepLogs' + today_as_dt + '.log']
    hdlr = logging.FileHandler(os.path.join(*relative_log_location))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    
    hdlr.setFormatter(formatter)
    hdlr.setLevel(logging.INFO)
    LOG = logging.getLogger(name = "autoWaker")
    LOG.addHandler(hdlr)
    LOG.setLevel(logging.INFO)
    return LOG