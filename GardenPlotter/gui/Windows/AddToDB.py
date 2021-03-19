#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains :
    - This is a monolithic test file for exploration in bpython

    - I think this is going to be the final monolith we feed
        to a compiler/packager for cross platform releases.
        The main assembly of code in multiple files is for development/openness
    
"""
__author__  = 'Adam Galindo'
__email__   = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'
from tkinter import *

class AddPlantToDatabase:
    def __init__(self, master, size, plant_to_display):
        self.master = master
        self.master.title("Plant Information")
        self.master.geometry(size)
        self.show_widgets()

    def show_widgets(self):
        self.frame = Frame(self.master)
        self.quit  = Button(self.frame, text=f"Quit this window" ,command=self.close_window)
        self.quit.pack()
        self.label = Label(self.frame, text="THIS IS ONLY IN THE INFORMATION WINDOW")
        self.label.pack()
        self.frame.pack()
        
    def close_window(self):
        self.master.destroy()