class CommandSet:
    def __init__(self, commands):
        self._commands = commands
        
    def handle_command(self, spoken_text):
        ''' Finds the right command and runs the appropriate command object associated with that specific command'''
        # loop through all the commands in the commands list
        # also this goes through the list in order so for example 'timer set' should be put before 'timer'
        for command in self._commands:
            # while looking through all the commands in the list, see if the spoken text matches a command in the list
            # uses the matches method from the command class which uses regex to match usually the first part of the spoken string
            if command.matches(spoken_text):
                return command.run(spoken_text)
        
        
        