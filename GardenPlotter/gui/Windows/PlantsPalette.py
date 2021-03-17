#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
#from gui.GardenGridGui import GardenGridGui
from database.database_stuff import Plants
#from gui.Windows.MainWindow import MainWindow

class PlantsPalette:
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
        self.master.geometry("{}x{}+20+20".format(self.window_size_x,self.window_size_y))
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

#    def click_callback(self, event):
#        """Function called when someone clicks on the palette canvas."""
#        x, y = event.x, event.y
#        # Did the user click a colour from the palette?
#        if p_pad < y < p_height + p_pad:
#            # Index of the selected palette rectangle (plus padding)
#            ic = x // (p_width + p_pad)
#            # x-position with respect to the palette rectangle left edge
#            xp = x - ic*(p_width + p_pad) - p_pad
#            # Is the index valid and the click within the rectangle?
#            if ic < self.ncolours and 0 < xp < p_width:
#                self.select_colour(ic)
#    # Bind the palette click callback function to the left mouse button
#    # press event on the palette canvas.
#    self.canvasframe.bind('<ButtonPress-1>', palette_click_callback)

    def plant_button(self):
        pass

    def select_plant(self, plant_clicky_clicky):
        """Select the plant indexed at plant_clicky_clicky in the plants_palette list."""
        pass

    def close_window(self):
        self.master.destroy()