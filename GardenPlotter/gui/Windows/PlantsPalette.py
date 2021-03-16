#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
from GardenPlotter.database.database_stuff import Plants
from GardenPlotter.gui.Windows.MainWindow import MainWindow

class PlantsPalette(MainWindow):
    def __init__(self, 
                 master, 
                 palette_cells_x  ,
                 palette_cells_y  ,
                 palette_cell_px_x,
                 palette_cell_px_y,
                 padding_px      
                ):
        self.master = master
        self.master.title("Plant selection")
        self.window_size_x = 1024
        self.window_size_y = palette_cells_y * palette_cell_px_y + (padding_px * palette_cells_y)
        self.master.geometry(self.window_size_x,self.window_size_y) 
        self.plants_palette   = []

        # add plants from database to list
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

        self.frame = Frame(self.master)
        self.quit  = Button(self.frame, text=f"Quit this window" ,command=self.close_window)
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