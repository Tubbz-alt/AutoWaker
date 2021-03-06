import datetime
import logging
import os
import pyaudio
import time
import wave

from ConfigHandler import getPath
from SleepChecker import SleepChecker
from TimeHandler import stallAction, now, addHours

LOG = logging.getLogger(name="autoWaker")

"""
  Used to wake the target up, with a specific noise if requested.
  
  To be implemented:
    makeCoffee() Use a blutooth connection to a coffee maker nearby and make coffee
    sleepSync() sync two sleepers so they wake at the same time at optimal
        sleep cycle points.
    Logging
    
  Author: Alex Hoff
  License: ---
"""
class WakeUpCaller():
    def __init__(self, fileLocation=None, sleep_start_time = None):
        if fileLocation!=None:
            self.wake_up_noise_ = fileLocation
    
    """
    #  One call to handle waking so data doesn't need to be passed around.
    def callWake(self, sleep_start_time = None):
        wake_up_time = self.calculateWakeTime(sleep_start_time = sleep_start_time)
        self.setWakeTime(wake_up_time = wake_up_time)
        should_be_awake = self.wakeAtTime(wake_up_time = wake_up_time)
        if (should_be_awake) and self.isAsleep():
            LOG.debug('FAILED TO WAKE TARGET.')
    """
        
    """
    #  Plays my favorite wakeup noise :D!
    def wakeUp(self):
        head, tail = os.path.split(self.wake_up_noise_)
        wf = wave.open(self.wake_up_noise_,'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)    #END wakeUp()
        data = wf.readframes(1024)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()
    """
    
    def isAsleep(self):
        sleep_checker = SleepChecker()
        return sleep_checker.isAsleep()
    #END isAsleep()
    
    
    def setWakeTime(self, wake_up_time = None):
        LOG.INFO('Wake up time is now: ' + str(wake_up_time))
        self.wake_up_time_ = wake_up_time
    #END setWakeTime()
    
    
    def getWakeTime(self):
        return self.wake_up_time_
    #END getWakeTime()
    
    """
    #  Wakes the target up with 30 second precision.
    def wakeAtTime(self, wake_up_time = None):
        self.setWakeTime(wake_up_time = wake_up_time)
        if wake_up_time == None:
            LOG.debug('No time provided to wake up at.')
            raise IOError, 'Need a time to wakeup.'
        
        else:
            while self.shouldSleep():
                stallAction(30)
            LOG.info('Time to wake up!')
            self.wakeUp()
        return True
    #END wakeAtTime()
    """
    
    #  Returns whether or not the person should still be asleep.
    def shouldSleep(self):
        #NOTE: The important thing about this implementation is that threading
        #Could potentially change the wake time, or it could be dynamically 
        #changed here.
        return self.getWakeTime()>now()
    #END shouldSleep
    

    
    
    #  Currently adds 6 hours to when the person fell asleep, exactly.
    #   Future implementations will calculate this based on heart rate,
    #   sleep stages, and other various factors for more efficient times.
    def calculateWakeTime(self, sleep_start_time):
        wake_up_time = addHours(sleep_start_time, 6)
        self.setWakeTime(wake_up_time)
        return wake_up_time 
    #END calculateWakeTime()

 
    ############CLASS VARIABLES##############
    wake_up_time_ = None
    wake_up_noise_ = reduce(os.path.join,[getPath(),"Assets","Music","mortalkombat.wave"])
    ############CLASS VARIABLES##############

#END wakeUpCaller()