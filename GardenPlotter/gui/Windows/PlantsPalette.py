#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
#from gui.GardenGridGui import GardenGridGui
from database.database_stuff import Plants
#from gui.Windows.MainWindow import MainWindow

class PlantsPalette:
    def __init__(self, 
                 master, 
                 palette_cells_x   : int ,
                 palette_cells_y   : int ,
                 palette_cell_px_x : int ,
                 palette_cell_px_y : int ,
                 padding_px        : int
                ):
        self.master = master
        self.master.title("Plant selection")
        self.window_size_x  = palette_cells_x * palette_cell_px_x + (padding_px * palette_cells_x)
        self.window_size_y  = palette_cells_y * palette_cell_px_y + (padding_px * palette_cells_y)
        self.master.geometry("{}x{}+20+20".format(str(self.window_size_x),\
                                                  str(self.window_size_y)))
        self.plants_palette = []

        self.frame = Frame(self.master)

        

        for each_plant in Plants.query.all():
            self.plants_palette.append(each_plant)
        for each_plant_button in self.plants_palette:
        #not implmented yet
          #button_image = PhotoImage(file=Plants.plant_button_image)
            # compound options are bottom, center, left, none, right, or top
            plant_button = Button(self.master,
                                  text=each_plant_button.name,
                                  compound="top")
            plant_button.pack()


        self.quit  = Button(self.frame, text="Quit this window" ,command=self.close_window)
        self.quit.pack()
        self.label = Label(self.frame, text="THIS IS THE PALETTE")
        self.label.pack()
        self.frame.pack()

    def plant_button(self):
        pass

    def select_plant(self, plant_clicky_clicky):
        """Select the plant indexed at plant_clicky_clicky in the plants_palette list."""
        pass

    def close_window(self):
        self.master.destroy()