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

import GardenPlotter.gui.grid
from GardenPlotter.garden import *
from GardenPlotter.gui.grid import *
from GardenPlotter.gui.Windows import *
from GardenPlotter.database.database_stuff import *

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

    