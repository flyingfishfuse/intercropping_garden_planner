#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
from GardenPlotter.database.database_stuff import Plants
from GardenPlotter.gui.Windows.MainWindow import MainWindow

class PlantsPalette(MainWindow):
    def __init__(self, 
                 master, 
                 palette_cells_column  : int,
                 palette_cells_y    : int,
                 palette_cells_px_w : int,
                 palette_cells_px_h : int
                ):
        self.master = master
        self.master.title("Plant selection")
        self.window_size_x = palette_cells_column * palette_cells_px_w
        self.window_size_y = palette_cells_px_h * palette_cells_y
        self.master.geometry() 
        self.palette_canvas = Canvas(self.master, 
                                     width  = self.canvas_width_px,
                                     height = self.palette_height_px
                                    )
        self.palette_canvas.pack()
        self.selected_plant_index = 0
        self.select_plant(self.selected_plant_index)

        # Add the plant selection rectangles to the palette canvas.
        self.palette_plant_boxes = []
        for each_plant in Plants.query.all():
            self.plants_palette.append(each_plant.name)

        self.num_plants_palette = len(self.plants_palette)

        for plant_num in range(self.num_plants_palette):
            palette_square_x = self.pad_px * (plant_num + 1) + (plant_num * self.palette_width_px)
            palette_square_y = self.pad_px
            rectangle = self.palette_canvas.create_rectangle(palette_square_x, 
                                            palette_square_y,
                                            palette_square_x + self.palette_width_px,
                                            palette_square_y + self.palette_height_px,
                                            # change to image and link to action for plant selection 
                                            # maybe as a stateful thing
                                            fill = self.plants_palette[plant_num]
                                        )
            self.palette_rects.append(rectangle)
        # selected_plant_index is the index of the currently selected plant.
        self.selected_plant_index = 0
        self.select_plant(self.selected_plant_index)
        self.show_widgets()

        #self.button_image = PhotoImage(file=plant_button_image)
        # compound options are bottom, center, left, none, right, or top
        #button_qwer = tk.Button(root, image=imagetest, text="asdfasdf", compound="top", command=print_hello)


    def show_widgets(self):
        self.frame = Frame(self.master)
        self.quit  = Button(self.frame, text=f"Quit this window" ,command=self.close_window)
        self.quit.pack()
        self.label = Label(self.frame, text="THIS IS THE PALETTE")
        self.label.pack()
        self.frame.pack()

    #def palette_click_callback(event):
    #    """Function called when someone clicks on the palette canvas."""
        # Bind the palette click callback function to the left mouse button
        # press event on the palette canvas.
    #self.palette_canvas.bind('<ButtonPress-1>', palette_click_callback)

    def select_plant(self, plant_clicky_clicky):
        """Select the plant indexed at i in the plants_palette list."""
        pass
    def close_window(self):
        self.master.destroy()