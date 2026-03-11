# ToothTyper
# Voice-to-text for Patterson Eaglesoft perio charting
#
# Copyright (c) 2026 Hunt Burke (Hexadecimal Development)
# Licensed under the GPL 3.0


# TO-DO: Add try-except block around whole script

import sys
import os
import subprocess
import threading
import platform
import speech_recognition as sr
from word2number import w2n
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow

# Hide support prompt, import pygame, and init mixer
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.mixer.init()

# Uncomment these to hide microphone errors:
#os.close(sys.stderr.fileno())
#os.open(os.devnull, os.O_RDWR)

class GUI(QMainWindow):

    def __init__(self):

        # Init class and launch GUI

        # Variables for listener thread
        self.listening = False
        self.listener = threading.Thread(target=self.listen)
        self.stop = threading.Event()

        # Variables for status sound
        self.ding = pygame.mixer.Sound(os.path.abspath('audio/ding.mp3'))

        # TO-DO: Update icon and window header
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load(os.path.abspath('Qt/mainwindow.ui'), None)
        self.setCentralWidget(self.ui)
        self.ui.button.clicked.connect(self.switch)

    def switch(self):

        if not self.listening:
            self.ui.button.setText('Stop Listening')
            self.listening = True

            self.showMinimized()

            if self.stop.is_set: self.stop.clear()

            # Recreate the thread if it's been destroyed, start it if not
            if self.listener:
                self.listener.start()
            else:
                self.listener = threading.Thread(target=self.listen)
                self.listener.start()
            
        else:
            
            # Stop listening and destroy the thread object
            self.stop.set()
            self.listener.join()
            self.ui.button.setText('Start Listening')
            self.listening = False
            self.listener = None

    def listen(self):

        r = sr.Recognizer()

        print("Adjusting...")
        with sr.Microphone() as source: r.adjust_for_ambient_noise(source, duration=1)
        self.ding.play()  # Notify the user they can start reciting

        while not self.stop.is_set():

            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    print("Analyzing...")
                    text = r.recognize_google(audio)
                    text = text.lower()
                    text = text.split()  # Split text into list

                    # Uncomment this to print text list for debugging
                    print(text)

                    if not self.stop.is_set():

                        for word in text:  # Every word

                            currentword = None  # Unset currentword

                            if word.isdigit():
                                print(word)
                                self.sendkeys(word)  # Type word

                            else:

                                try:
                                    currentword = str(w2n.word_to_num(word))  # Convert words to numbers

                                except ValueError: pass  # Skip if word is not a number

                                else:
                                    print(currentword)
                                    self.sendkeys(currentword)  # Type word

            # TO-DO: Add message boxes instead of passing

            except sr.RequestError as e:
                pass

            except sr.UnknownValueError:
                pass

            except sr.WaitTimeoutError:
                pass

        print('Stopped listening.')

    def sendkeys(self, text: str):

        if platform.system() == "Linux":
            subprocess.run(("xdotool", "type", text))  # If on Linux
        elif platform.system() == "Windows":
            subprocess.run((f"powershell", "-Command", f"(New-Object -ComObject WScript.Shell).SendKeys('{text}')"), check=True)  # If on Windows


    def closeEvent(self, event):
        self.stop.set()  # Send stop to listener
        self.listener.join(timeout=0.1)  # Don't wait for it to close
        event.accept()  # Close the window


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    app.exec()