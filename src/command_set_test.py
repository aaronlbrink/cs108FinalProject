import command
import command_set
import unittest

class MockCommand(command.Command):
    ''' Creating a fake command which inherits from the base class Command '''
    def __init__(self, regex):
        command.Command.__init__(self, regex)
        self.run_called = False

        
    def run(self, spoken_text):
        self.run_called = True

class CommandSetTests(unittest.TestCase):
    def test_not_match(self):
        ''' Tests that the regex matching functionality works (by testing things that don't match) '''
        mock_command_a = MockCommand(r'^hey')
        mock_command_b = MockCommand(r'^there')
        my_command_set = command_set.CommandSet([
            mock_command_a,
            mock_command_b,
            ])
        my_command_set.handle_command('blah')
        assert not mock_command_a.run_called, 'non-matching command A was run when it should\'nt\'ve been'
        assert not mock_command_b.run_called, 'non-matching command B was run incorrectly'

    def test_match(self):
        ''' Tests that the regex matching functionality works '''
        mock_command_a = MockCommand(r'^hey')
        mock_command_b = MockCommand(r'^there')
        my_command_set = command_set.CommandSet([
            mock_command_a,
            mock_command_b,
            ])
        my_command_set.handle_command('hey')
        assert mock_command_a.run_called, 'non-matching command A was run and it should have'
        assert not mock_command_b.run_called, 'non-matching command B was run incorrectly'

    def test_first_match(self):
        ''' Tests that the regex matching functionality chooses the first option in the list'''
        mock_command_a = MockCommand(r'^hey')
        mock_command_b = MockCommand(r'^hey')
        mock_command_c = MockCommand(r'^hey')
        my_command_set = command_set.CommandSet([
            mock_command_a,
            mock_command_b,
            mock_command_c,
            ])
        my_command_set.handle_command('hey')
        assert mock_command_a.run_called, 'make sure command_a runs (because it\'s the first in the list'
        assert not mock_command_b.run_called, 'make sure command B doesn\'t run'
        assert not mock_command_c.run_called, 'make sure that command C does not run'

