#!/usr/bin/env python3

import speech_recognition as sr
from tkinter import *
from speech_recognition import recognize_api
from command_set import CommandSet
import command
import sys

''' This application makes use of the speech recognition library located here
https://pypi.python.org/pypi/SpeechRecognition/
it also uses a few lines of code from the example provided on creating the Recognizer object
and listening for speech with the microphone object (which is using pyaudio)
'''
        
# App name variable
app_name = 'Anke'    
# initialized the recognizer from the speech recognition library
r = sr.Recognizer()
class GuiWindow:
    '''
    GuiWindow is the main window of the application by which speech recognition can start/cancel and text results are outputted
    '''
    def __init__(self, window):
        # Initialize the stop_listen variable to None if it doesn't get set later
        self.stop_listen = None
        # Initialize text line count
        self.line_count = 1.0
        self.window = window
        self.window.minsize(width=400, height=200)
        # Create a toolbar help menu
        self.menu = Menu(window)
        # tells the window configuration that the self.menu variable is the menu for this window
        self.window.config(menu=self.menu)
        
        # Making a sub menu (help)
        # http://effbot.org/tkinterbook/tkinter-application-windows.htm
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label='About', command=self.about_info)

        # Creating the GUI buttons
        self.listen_button = Button(window, text='Start Listening', command=self.listen)
        self.stop_listen_button = Button(window, text='Cancel', command=self.stop_listen_button, state='disabled')
        # Create Welcoming Text
        self.introduction = Label(window, text=app_name, font=("Helvetica", 24))
        self.message = Entry(width=70, justify='center')

        # Insert a message on a new line using the line_count_increase function
        self.handle_output("Hello! To begin click Start     ")
        # Pack the GUI components
        self.introduction.pack()
        self.listen_button.pack()
        self.stop_listen_button.pack()
        self.message.pack()
        
        # Creates the command set object to list out the possible command objects from the command module
        self.command_set = CommandSet([
            command.TimerCommand(),
            command.GoogleCommand(),
            ])
        
    def listen(self):
        ''' Starts listening to the microphone as the source.'''
        # listen button disabled because it's listening right now
        self.listen_button.config(state='disabled')
        self.stop_listen_button.config(state='normal')
        source = sr.Microphone()
        print("Say something, I'm giving up on you now!")
        # updates the entry text to ask for speech (just like the print statement above in the console
        self.handle_output('Okay, say something...')

        
        def handler(recognizer, audio):
            self.handle_results(audio)
        # listen in background command must be used instead of just the listen command to avoid having the main TKinter loop stopping causing the application to freeze which prevents the GUI from being updated
        self.stop_listen = r.listen_in_background(source, handler)

    def handle_results(self, audio):
        ''' Handles the audio results'''
        # recognize speech using Google Speech Recognition
        self.handle_output('°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°Working`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸')
        print('handling results...')
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            recognized_audio = r.recognize_google(audio).lower()
            print("Google Speech Recognition thinks you said " + recognized_audio)
            # Outputs the audio to the GUI
            self.handle_output(recognized_audio)
            # Searches through the command set for a command associated with the recognized audio by using the command_set's handle command method
            if self.command_set.handle_command(recognized_audio) is not None:
                output = self.command_set.handle_command(recognized_audio)
                self.handle_output(output)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.handle_output("Audio not understood.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.handle_output("Could not fetch results from Google Speech Recognition (maybe offline?)")
        except Exception as e:
            print("Something went wrong.", e)
        except:
            print('something went even more wrong.', sys.exc_info())
            self.handle_output("See console for error messages")
    
    def stop_listen_button(self):
        f = self.stop_listen
        f()
        # Disables the stop listening button after it has been pressed for a better UX
        self.listen_button.config(state='normal')
        self.stop_listen_button.config(state='disabled')
        self.handle_output(app_name + ' has stopped listening to your speech.')
        
    def about_info(self):
        ''' Popup for the about information '''
        self.new_window = Toplevel()
        self.new_window.title("About")
        # http://stackoverflow.com/questions/16631729/tkinter-toplevel-width-and-height-not-working
        self.new_window.geometry("%dx%d%+d%+d" % (300, 200, 250, 125))
        self.about_popup = Message(self.new_window, text='About', font=("Helvetica", 28), width=90)
        self.about_popup_body = Message(self.new_window, text='Made by Aaron Brink.\n The goal of this application is to provide a speech interface (GUI asisted) by which the user can speak keyword phrases to run functions such as setting timers.')
        self.about_exit = Button(self.new_window, text='Hide', command=self.new_window.destroy)
        self.about_popup.pack()
        self.about_popup_body.pack()
        self.about_exit.pack()
    
    def handle_output(self, message):
        ''' handles the outputting text by clearing the text box and returning the newly given message '''
        self.message.delete(0, END)
        self.message.insert(0, message)
        
if __name__ == '__main__':
    root = Tk()
    root.title('Voice Recognition')    
    app = GuiWindow(root)
    root.mainloop()
    
    # Testing
    try: 
        # Test the command
        pass
    except:
        pass
    

'''
# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
'''

'''
# recognize speech using Wit.ai
WIT_AI_KEY = "INSERT WIT.AI API KEY HERE" # Wit.ai keys are 32-character uppercase alphanumeric strings
try:
    print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "INSERT BING API KEY HERE" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
try:
    print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
except sr.UnknownValueError:
    print("Microsoft Bing Voice Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

# recognize speech using Houndify
HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE" # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE" # Houndify client keys are Base64-encoded strings
try:
    print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
except sr.UnknownValueError:
    print("Houndify could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Houndify service; {0}".format(e))

# recognize speech using IBM Speech to Text
IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE" # IBM Speech to Text passwords are mixed-case alphanumeric strings
try:
    print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
except sr.UnknownValueError:
    print("IBM Speech to Text could not understand audio")
except sr.RequestError as e:
    print("Could not request results from IBM Speech to Text service; {0}".format(e))
'''