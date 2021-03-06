import logging
import os
import sys

from APIHandler import APIHandler
from ConfigHandler import getPath
from DataHandler import DataHandler
from LogCreator import setupLogger
from SleepChecker import SleepChecker
from TimeHandler import today, now, startCheckTime, endCheckTime, stallAction
from TokenGetter import TokenGetter
from WakeUpCaller import WakeUpCaller


#Set the proper path
os.chdir(getPath())

today_as_dt = today()
#This is the Fitbit URL to use for the API call
FitbitURL = "https://api.fitbit.com/1/user/-/sleep/date/" + today_as_dt + ".json"

#Get and write the tokens from here
s = [getPath(), 'Data', 'MyData_' + today_as_dt + '.txt']

# Moderately tricky, and I'm not sure what it does when I revisited this.
OutFile = os.path.join(*s)


def main(): 
    
    LOG = setupLogger()
    LOG.info('STARTING')
    
    # wait until we should start. Make this into a class or method?
    # while now()>endCheckTime() or now()<startCheckTime():
    #    LOG.info('Pinging every 120 seconds to check if the person should be asleep.')
    #    stallAction(120)
    
    key_getter = TokenGetter(os.path.join(getPath(),'tokens.txt'))
    api_handler = APIHandler(FitbitURL, OutFile, key_getter)
    data_handler = DataHandler()
    
    #Make the API call
    APIResponse = api_handler.cancelIfAPICallBad()
    sleep_checker = SleepChecker(OutFile)
    LOG.info('Polling until the user is asleep.');
    while sleep_checker.isAwake():
        stallAction(600)  #Check every 10 minutes if the user is asleep.
        APIResponse = api_handler.cancelIfAPICallBad()
        sleeping, start_time = data_handler.getSleepStartTime(APIResponse)
        
    #The user is now asleep.
    
    user = '-' # Temporary username being used.
    
    LOG.info('User ' + user + ' started sleeping at ' + str(start_time) + ' today.')
    wake_up = WakeUpCaller()
    wake_up.callWake(start_time)



if __name__ == '__main__':
    main()