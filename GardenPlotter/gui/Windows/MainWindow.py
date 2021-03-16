#from tkinter import *
#from tkinter import filedialog
#import GardenPlotter.database.database_stuff
#from GardenPlotter.database.database_stuff import *
#from GardenPlotter.gui.Windows import *
# Maximum and default grid size
MAX_N, DEFAULT_N = 26, 10
# The "default" plant for an unfilled grid cell
UNFILLED = '#fff'

from tkinter import *
from tkinter import filedialog
#from gui.GardenGridGui import GardenGridGui
from database.database_stuff import Plants
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
        # Padding stuff: xsize, ysize is the cell size in pixels (without pad).
        # cell pixel width with no padding
        self.cell_px_width     = (self.canvas_width_px / self.grid_size_n ) -(self.pad_1px * self.grid_size_n )
        self.cell_px_pad       = self.cell_px_width + self.pad_1px
        # cell pixel height no padding
        self.cell_px_height    = (self.canvas_px_height - self.cell_px_pad) / self.grid_size_n
        self.grid_frame        = Frame(self.master)
        self.grid_frame.pack()

        # The canvas onto which the grid is drawn.
        self.canvasframe = Canvas(self.master, 
                                  width=self.canvas_width_px, 
                                  height=self.canvas_width_px
                                  )
        self.canvasframe.pack()

        # Add the cell rectangles to the grid canvas.
        self.cells = []

        for y_axis_index in range(grid_size_n):
            for x_axis_index in range(grid_size_n):
                xpad  = self.pad_px * (x_axis_index+1)
                ypad  = self.pad_px * (y_axis_index+1) 
                x1    = xpad + x_axis_index * self.cell_px_width
                y1    = ypad + y_axis_index * self.cell_px_height
                x2    = x1 + self.cell_px_width
                y2    = y1 + self.cell_px_height
                garden_cell = self.canvasframe.create_rectangle(x1, y1, x2, y2, fill = UNFILLED)
                self.cells.append(garden_cell)


        # Add a button to clear the grid
        button_clear = Button(self.grid_frame,text='clear',command=self.clear_grid)
        button_clear.pack(side=LEFT,padx=self.pad_px,pady=self.pad_px)
        close_window = Button(self.grid_frame,text='close window',command=self.close_window)
        close_window.pack(side=LEFT,padx=self.pad_px,pady=self.pad_px)

    def close_window(self):
        self.master.destroy()

    def _get_cell_coords(self, i):
        """Get the <letter><number> coordinates of the cell indexed at i."""

        # The horizontal axis is labelled A, B, C, ... left-to-right;
        # the vertical axis is labelled 1, 2, 3, ... bottom-to-top.
        y_axis_index, x_axis_index = divmod(i, self.grid_size_n)
        return '{}{}'.format(chr(x_axis_index+65), self.grid_size_n-y_axis_index)

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
        



