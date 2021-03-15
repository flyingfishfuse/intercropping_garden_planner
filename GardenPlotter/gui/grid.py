#!/usr/bin/python3
# -*- coding: utf-8 -*-
# no python 2 compatibility focus on this...
from tkinter import *
from GardenPlotter.std_imports import *
from GardenPlotter.Windows import MainWindow,ConfigurationWindow,PlantListWindow

# Maximum and default grid size
MAX_N, DEFAULT_N = 26, 10
# The "default plant" for an unfilled grid cell
UNFILLED = '#fff'

class GardenGridGui:
    """The main class representing a grid of planted cells."""
    def __init__(self, 
                 master,
                 grid_size_n      = 30,
                 canvas_width_px  = 1024,
                 canvas_height_px = 1024
                ):
        
        self.master             = master
        self.padding_px         = 5
        self.grid_size_n        = grid_size_n
        self.canvas_width_px    = canvas_width_px
        self.canvas_height_px   = canvas_height_px
        self.plants_palette     = [UNFILLED]
        self.palette_width_px   = self.canvas_width_px - (self.padding_px * 2)
        self.palette_height_px  = self.canvas_height_px * (1/5)
        #abstractify this
        self.config_menu_size   = "800x600+200+200"
        plants_list_window_size = '1024x1024+20+20'
        try:       
            main_window = MainWindow(self.canvas_width_px,
                                     self.canvas_height_px,
                                     # interpreter was acting like this wasnt set with
                                     # positional argument, testing implicit argument
                                     grid_size_n=self.grid_size_n)
            #configuration_window    = ConfigurationWindow(self.master,self.config_win_size)
            #plants_list_window      = PlantListWindow(self.master,self.plants_list_window_size)
        except Exception:
            error_printer("[-] Window Initialization FAILED")

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
