from datetime import datetime, timedelta
import threading
import urllib.parse
import webbrowser
# regex
import re

class Command:
    ''' This class specifies the different regex''' 
    
    def __init__(self, regex):
        self._regex = re.compile(regex)
        
    def matches(self, spoken_text):
        return self._regex.search(spoken_text)
    

    def run(self, spoken_text):
        '''
        Raises an exception if the run command doesn't get overridden by the inherited specific command class
        and run only may be called when matches() is true
        '''
        raise Exception('Run must be implemented in subclass')


class TimerCommand(Command):
    def __init__(self):
        Command.__init__(self, r'^timer.* ([0123456789]+)')
        
    def run(self, spoken_text):
        ''' Search through using regex search from the parent object and sets the first parameter to the time to set '''
        # Example command parameters: timer set ten minutes
        print('timer getting params')
        search = self._regex.search(spoken_text)
        time_to_set = search.group(1)
        self.set_timer(timedelta(minutes=int(time_to_set)))
        print('timer successfully set')
            
    def set_timer(self, time_delta):
        ''' Sets a new timer object to run for duration of end_time '''
        def timer_results():
            print('timer expired, launching notification')
            webbrowser.open('data:text/html,' + urllib.parse.quote('<html><body><span style="font-size: 20em; color: red; background: green">Timer Expired'))
        threading.Timer(time_delta.total_seconds(), timer_results).start()
        