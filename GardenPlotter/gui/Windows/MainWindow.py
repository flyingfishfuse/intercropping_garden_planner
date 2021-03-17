#from tkinter import *
#from tkinter import filedialog
#import GardenPlotter.database.database_stuff
#from GardenPlotter.database.database_stuff import *
#from GardenPlotter.gui.Windows import *
# Maximum and default grid size
MAX_N, DEFAULT_N = 26, 10
# The "default" plant for an unfilled grid cell
UNFILLED = '#fff'

import pandas
import itertools
from tkinter import *
from tkinter import filedialog
#from gui.GardenGridGui import GardenGridGui
from database.database_stuff import Plants
from std_imports import debug_message
import std_imports
#lets try to clean up the grid and use numpy?
import numpy

class MainWindow:
    def __init__(self, 
                 master, 
                 canvas_width_px : int, 
                 canvas_height_px: int, 
                 grid_size_n     : int
                ):
        """
        Initialize a grid and the Tk Frame on which it is rendered.
        Modified to be non-monolithic
        """
        self.master            = master
        # Number of cells in each dimension.
        self.grid_size_n       = grid_size_n 
        self.pad_px            = 5
        self.pad_1px           = 1
        self.canvas_width_px   = canvas_width_px
        self.canvas_px_height  = canvas_height_px
        self.cell_px_width     = self.canvas_width_px / self.grid_size_n - self.grid_size_n 
        self.cell_px_height    = self.canvas_px_height / self.grid_size_n
        
        self.grid_frame        = Frame(self.master)
        self.grid_frame.pack()
        
        self.canvasframe = Canvas(self.master, width=self.canvas_width_px,height=self.canvas_width_px)
        self.canvasframe.bind('<ButtonPress-1>', self.get_cell_from_clickyclicky)
        self.canvasframe.pack()

        self.cells = []

        # Welcome to the grid
        self.grid_points = []
        self.list_of_all_cells = []
        grid_x = range(grid_size_n)
        grid_y = range(grid_size_n)
        x_coordinates, y_coordinates = numpy.meshgrid(grid_x,grid_y,indexing='xy')
        coordinate_array = list(itertools.zip_longest(x_coordinates,y_coordinates))
        for field in coordinate_array:
            x_field       = field[0]
            y_field       = field[1]
            grid_location = list(itertools.zip_longest(x_field,y_field))
            self.grid_points.append(grid_location)
            for thing in self.grid_points:
                for each in thing:
                    self.list_of_all_cells.append(each)
        #>>> for each in grid_points:
        #...     print(each)
        #  -------------------X-------------------- 
        #   [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        #   [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
        # Y [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
        #   [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]
        #   [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
        # 
        #>>> y axis index is grid_points[y_index]
        # >>> grid_points[0]
        # [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]

        def grab_xy(self, x , y):
            return self.grid_points[y][x]

        for (x_coord, y_coord) in self.list_of_all_cells:
            #drawing from
            x1 = x_coord * self.cell_px_width
            y1 = y_coord * self.cell_px_height
            #drawing to
            x2 = x1 + self.cell_px_width
            y2 = y1 + self.cell_px_height
            # zort!
            #garden_cell = self.canvasframe.create_rectangle(x1, y1, x2, y2, fill = UNFILLED)
            #self.cells.append(garden_cell)
            new_cell = self.canvasframe.create_rectangle(x1, y1, x2, y2, fill = UNFILLED)
            new_cell
            self.canvasframe.pack()

        # Add a button to clear the grid
        button_clear = Button(self.grid_frame,text='clear',command=self.clear_grid)
        button_clear.pack(side=LEFT,padx=self.pad_px,pady=self.pad_px)
        close_window = Button(self.grid_frame,text='close window',command=self.close_window)
        close_window.pack(side=LEFT,padx=self.pad_px,pady=self.pad_px)

    def get_cell_from_clickyclicky(self, event):
        """Function called when someone clicks on the grid canvas."""
        click_x_px, click_y_px = event.x, event.y
        cell_x_location  = click_x_px // self.cell_px_width
        cell_y_location  = click_y_px // self.cell_px_height
        cell_boundry_x   = click_x_px - cell_x_location * self.cell_px_width 
        cell_boundry_y   = click_y_px - cell_y_location * self.cell_px_height
        self.user_just_clicked_on = (cell_x_location,cell_y_location)
        #checking pixel boundries
        if (cell_x_location < self.grid_size_n)\
            and (cell_y_location < self.grid_size_n )\
            and (0 < cell_boundry_x < self.cell_px_width)\
            and (0 < cell_boundry_y < self.cell_px_height):
            index = cell_y_location*self.grid_size_n + cell_x_location
            self.canvasframe.itemconfig(self.cells[index], fill=UNFILLED)
            debug_message("USER CLICKED AT : {click_x_px},{click_y_px}".format())
            debug_message("cell coordinate : {cell_x_location},{cell_y_location}".format())

    
    def close_window(self):
        self.master.destroy()

    def _get_cell_coords(self, i):
        """Get the <letter><number> coordinates of the cell indexed at i."""

        # The horizontal axis is labelled A, B, C, ... left-to-right;
        # the vertical axis is labelled 1, 2, 3, ... bottom-to-top.
        y_coord, x_coord = divmod(i, self.grid_size_n)
        return '{}{}'.format(chr(x_coord+65), self.grid_size_n-y_coord)

    def save_by_plant(self):
        """Output a list of cell coordinates, sorted by cell plant."""

        # When we save the list of coordinates with each plant it looks
        # better if we limit the number of coordinates on each line of output.
        MAX_COORDS_PER_ROW = 12

        def _get_planted_cells_dict():
            """Return a dictionary of cell coordinates and their plants_palette."""

            planted_cell_cmds = {}
            for i, rect in enumerate(self.cells):
                c = self.canvasframe.itemcget(rect, 'fill')
                if c == UNFILLED:
                    continue
                planted_cell_cmds[self._get_cell_coords(i)] = c
            return planted_cell_cmds

        def _output_coords(coords):
            """Sort the coords into column (by letter) and row (by int)."""

            coords.sort(key=lambda e: (e[0], int(e[1:])))
            nrows = len(coords) // MAX_COORDS_PER_ROW + 1
            for i in range(nrows):
                print(', '.join(
                      coords[i*MAX_COORDS_PER_ROW:(i+1)*MAX_COORDS_PER_ROW]),
                      file=fo)

        # Create a dictionary of plants (the keys) and a list of cell
        # coordinates with that plant (the value).
        planted_cell_cmds = _get_planted_cells_dict()
        cell_plant = {}
        for k, v in planted_cell_cmds.items():
            cell_plant.setdefault(v, []).append(k)

        # Get a filename from the user and open a file with that name.
        with filedialog.asksaveasfile(mode='w',defaultextension=".grid") as fo:
            if not fo:
                return

            self.filename = fo.name
            print('Writing file to', fo.name)
            for plant, coords in cell_plant.items():
                print('{}\n{}'.format(plant,'-'*len(plant)), file=fo)
                _output_coords(coords)
                print('\n', file=fo)

    def clear_grid(self):
        """Reset the grid to the background "UNFILLED" plant."""

        for cell in self.cells:
            self.canvasframe.itemconfig(cell, fill=UNFILLED)
        



