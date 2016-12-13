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
        ''' checks if the spoken text matches a regex expression of spoken text '''
        return self._regex.search(spoken_text)
    

    def run(self, spoken_text):
        '''
        Raises an exception if the run command doesn't get overridden by the inherited specific command class
        and run only may be called when matches() is true
        '''
        raise Exception('Run must be implemented in subclass')


class TimerCommand(Command):
    def __init__(self):
        # Inherits the command class and passes in the regex expression for when the user says timer and a number after
        Command.__init__(self, r'^timer.* ([0123456789]+)')
        
    def run(self, spoken_text):
        ''' Search through using regex search from the parent object and sets the first parameter to the time to set '''
        # Example command parameters: timer set ten minutes
        print('timer getting params')
        search = self._regex.search(spoken_text)
        time_to_set = search.group(1)
        self.set_timer(timedelta(minutes=int(time_to_set)))
        print('timer successfully set')
        return 'A timer has been set for {0} minute(s)'.format(time_to_set)
        
            
    def set_timer(self, time_delta):
        ''' Sets a new timer object to run for duration of end_time '''
        def timer_results():
            print('timer expired, launching notification')
            # https://docs.python.org/3/library/urllib.parse.html
            webbrowser.open('data:text/html,' + urllib.parse.quote('<html><body><span style="font-size: 20em; color: red; background: green">Timer Expired'))
        # runs a timer on another thread so that you can continue talking
        threading.Timer(time_delta.total_seconds(), timer_results).start()
        
class GoogleCommand(Command):
    def __init__(self):
        Command.__init__(self, r'^google (.*)')
    def run(self, spoken_text):
        ''' Uses the words after google in a google search '''
        search_words = self._regex.search(spoken_text).group(1)
        webbrowser.open('http://google.com/search?q={0}'.format(search_words))
        return 'Googling for you!'
        