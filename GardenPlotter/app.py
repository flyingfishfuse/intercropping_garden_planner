#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains INSERT STUFF HERE
This I think is going to be the main file
"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'

from tkinter import *
from GardenPlotter.std_imports import error_printer
import GardenPlotter.gui.grid
import GardenPlotter.garden
from GardenPlotter.gui.grid import GardenGridGui
import GardenPlotter.database.database_stuff

    #TODO: 
            # FALLBACK 
        # TO
    # TERMINAL
# ASK IF USER WANTS POP

try:
    # Set the whole thing running
    root = Tk()
    #defaults are 30 cells on a 1024x1024px SVG grid of cells with 5px padding
    #TODO: add a number entry/slider + "apply" button to change padding px and re-render
    Garden = GardenGridGui(root, grid_size_n=40)
    root.mainloop()
except Exception:
    error_printer("[-] Application Initialization FAILED")

    