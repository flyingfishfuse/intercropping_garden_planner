#!/usr/bin/python3
# -*- coding: utf-8 -*-
#from tkinter import *
from tkinter import *
from tkinter import filedialog
import database.database_stuff
from database.database_stuff import *
from std_imports import error_printer
from gui.Windows.PlantsInformation import PlantInformationWindow
from gui.Windows.MainWindow import MainWindow
from gui.Windows.ConfigurationWindow import ConfigurationWindow
from gui.Windows.PlantsListWindow import PlantListWindow
from gui.Windows.PlantsPalette import PlantsPalette

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
        self.plant_info_size    = "800x600+200+200"
        plants_list_window_size = '1024x1024+20+20'
        try:       
            main_window = MainWindow(master= self.master,
                            canvas_width_px = self.canvas_width_px,
                            canvas_height_px = self.canvas_height_px,
                            # interpreter was acting like this wasnt set with
                            # positional argument, testing implicit argument
                            grid_size_n=self.grid_size_n
                        )
        except Exception:
            error_printer("[-] MAIN Window Initialization FAILED")
        try:
            plants_palette = PlantsPalette(self.master,
                                palette_cells_x   = 10,
                                palette_cells_y   = 4,
                                palette_cell_px_x = 80,
                                palette_cell_px_y = 60,
                                padding_px        = 5
                            )
            #plants_info    = PlantInformationWindow(self.master,
            #                    self.plant_info_size
            #                )
            #configuration_window    = ConfigurationWindow.ConfigurationWindow(self.master,self.config_win_size)
            #aplants_list_window      = PlantListWindow(self.master,self.plants_list_window_size)
        except Exception:
            error_printer("[-] PALETTE Window Initialization FAILED")
