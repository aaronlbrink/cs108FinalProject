import unittest
import command
import re
from datetime import timedelta

class CommandTest(unittest.TestCase):
    def test_command(self):
        ''' Test the base class throws errors correctly
        
        This test case was written by binki to show me how to write test cases
        '''
        failed_to_throw = False
        try:
            command.Command(re.compile('')).run('spoken text')
            failed_to_throw = True
        except Exception as e:
            # The following assert was written by someone else.
            assert 'Run must be implemented in subclass' in e.args[0], 'Wrong exception thrown: %s' % e
        assert not failed_to_throw, 'Should have thrown exception when trying to run unimpelmented run()'

class TimerTest(unittest.TestCase):
    def test_timer_matches(self):
        ''' '''
        things_that_should_match = [
            'timer set 2',
            'timer set 35 minutes',
            'timer set 0',
            # shouldn't matter what the user says between the numerical value for the timer
            'timer eat 2',
            ]
        for spoken_text in things_that_should_match:
            assert command.TimerCommand().matches(spoken_text), 'A phrase was not matched that should be match' + str(spoken_text)
        
    def test_timer_matches_unmatched(self):
        things_that_should_not_match = [
            'timer thirty',
            'timer hello',
            'blah',
            'time this',
            ]
        for spoken_text in things_that_should_not_match:
            assert not command.TimerCommand().matches(spoken_text), 'A phrase was matched that shouldn\'t\'ve: ' + str(spoken_text)
            
    def test_timer_run_parses(self):
        '''Also made by binki because he can't stand things'''
        class TestableTimerCommand(command.TimerCommand):
            
            def __init__(self):
                command.TimerCommand.__init__(self)
                self.set_timer_called_with = None
                
            def set_timer(self, time_delta):
                self.set_timer_called_with = time_delta

        timer_command = TestableTimerCommand()
        timer_command.run('timer 4')
        assert isinstance(timer_command.set_timer_called_with, timedelta), 'called with something other than timedelta: {}'.format(type(timer_command.set_timer_called_with).__name__)
        assert timer_command.set_timer_called_with == timedelta(minutes=4), 'not called with proper timedelta. Instead called with {}'.format(timer_command.set_timer_called_with)
