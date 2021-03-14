#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##                    Code to create grid for garden simulation               ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
# TKinter code based on https://github.com/scipython/colouring-grid
# A simple colouring grid app, with load/save functionality.
# Christian Hill, August 2018.
#  (modified extensively to be much more readable)                            ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

# no, no python 2 compatibility focus on this...
# I am mr python but 2.x is dead now
# a gardening app on the fringe of the code map
# doesnt need to have a legacy system consideration
import sys

from tkinter import *
from tkinter import filedialog
from std_imports import *
from Windows import MainWindow,ConfigurationWindow,PlantListWindow
# Maximum and default grid size
MAX_N, DEFAULT_N = 26, 10
# The "default" plant for an unfilled grid cell
UNFILLED = '#fff'

class GridApp:
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
            main_window             = MainWindow(self.canvas_width_px,
                                             self.canvas_height_px,
                                             self.grid_size_n)
            configuration_window    = ConfigurationWindow(self.master,self.config_win_size)
            plants_list_window      = PlantListWindow(self.master , self.plants_list_window_size)
        except Exception as derp:
            error_message(traceback.print_exc())

        try:
            # Set the whole thing running
            root = Tk()
            #defaults are 30 cells on a 1024x1024px SVG grid of cells with 5px padding
            #TODO: add a number entry/slider + "apply" button to change padding px and re-render
            grid = GridApp(root)
            root.mainloop()
        except Exception as derp:
            error_message(traceback.print_exc())