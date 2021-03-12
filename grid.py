#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##                    Code to create grid for garden simulation               ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
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

import sys

from tkinter import *
from tkinter import filedialog
from config_info import *
from database_stuff import Plants, database

# list of plants to present on the selection palette
plants_list = []
for each_plant in Plants:
    plants_list.append(each_plant.name)

nplants = len(plants_list)


# TKinter code based on https://github.com/scipython/colouring-grid
# A simple colouring grid app, with load/save functionality.
# Christian Hill, August 2018.

class GridApp:
    """The main class representing a grid of planted cells."""

    # The plant palette
    # soon to be the plant pallettettee
    plants_palette = (UNFILLED, 'red', 'green', 'blue', 'cyan', 'orange', 'yellow',
               'magenta', 'brown', 'black')
    num_plants_palette = len(plants_palette)

    def __init__(self, 
                 master,
                 grid_size_n,
                 canvas_width_px=600,
                 canvas_height_px=600,
                 pad=5):
        """Initialize a grid and the Tk Frame on which it is rendered."""

        # Number of cells in each dimension.
            
        # Some dimensions for the App in pixels.
        self.canvas_width_px  = canvas_width_px
        self.canvas_height_px = canvas_height_px
        palette_height        = 40

        # Padding stuff: xsize, ysize is the cell size in pixels (without pad).
        grid_NPAD  = grid_size_n + 1
        self.pad   = pad
        xsize      = (canvas_width_px - grid_NPAD*pad) / grid_size_n
        ysize      = (canvas_height_px - grid_NPAD*pad) / grid_size_n
        p_pad      = 5
        p_width    = p_height = palette_height - 2*p_pad

        # The main frame onto which we draw the App's elements.
        frame = Frame(master)
        frame.pack()

        # The palette for selecting plants_palette.
        self.palette_canvas = Canvas(master, 
                                     width  = self.canvas_width_px,
                                     height = palette_height
                                    )
        self.palette_canvas.pack()

        # Add the plant selection rectangles to the palette canvas.
        self.palette_rects = []
        for i in range(self.num_plants_palette):
            x, y = p_pad * (i+1) + i*p_width, p_pad
            rect = self.palette_canvas.create_rectangle(x, y,
                            x+p_width, y+p_height, fill=self.plants_palette[i])
            self.palette_rects.append(rect)
        # ics is the index of the currently selected plant.
        self.ics = 0
        self.select_plant(self.ics)

        # The canvas onto which the grid is drawn.
        self.w = Canvas(master, width=self.canvas_width_px, height=self.canvas_width_px)
        self.w.pack()

        # Add the cell rectangles to the grid canvas.
        self.cells = []
        for y_axis_index in range(grid_size_n):
            for x_axis_index in range(grid_size_n):
                xpad, ypad = pad * (x_axis_index+1), pad * (y_axis_index+1) 
                x, y = xpad + x_axis_index*xsize, ypad + y_axis_index*ysize
                rect = self.w.create_rectangle(x, y, x+xsize,
                                           y+ysize, fill=UNFILLED)
                self.cells.append(rect)

        # Load and save image buttons
        b_load = Button(frame, text='open', command=self.load_image)
        b_load.pack(side=RIGHT, padx=pad, pady=pad)
        b_save = Button(frame, text='save', command=self.save_by_plant)
        b_save.pack(side=RIGHT, padx=pad, pady=pad)
        # Add a button to clear the grid
        b_clear = Button(frame, text='clear', command=self.clear_grid)
        b_clear.pack(side=LEFT, padx=pad, pady=pad)

        def palette_click_callback(event):
            """Function called when someone clicks on the palette canvas."""
            x, y = event.x, event.y

            # Did the user click a plant from the palette?
            if p_pad < y < p_height + p_pad:
                # Index of the selected palette rectangle (plus padding)
                ic = x // (p_width + p_pad)
                # x-position with respect to the palette rectangle left edge
                xp = x - ic*(p_width + p_pad) - p_pad
                # Is the index valid and the click within the rectangle?
                if ic < self.num_plants_palette and 0 < xp < p_width:
                    self.select_plant(ic)
        # Bind the palette click callback function to the left mouse button
        # press event on the palette canvas.
        self.palette_canvas.bind('<ButtonPress-1>', palette_click_callback)

        def w_click_callback(event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y

            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            x_axis_index = int(x // (xsize + pad))
            y_axis_index = int(y // (ysize + pad))
            xc = x - x_axis_index*(xsize + pad) - pad
            yc = y - y_axis_index*(ysize + pad) - pad
            if x_axis_index < grid_size_n and y_axis_index < grid_size_n and 0 < xc < xsize and 0 < yc < ysize:
                i = y_axis_index*grid_size_n+x_axis_index
                self.w.itemconfig(self.cells[i], fill=self.plants_palette[self.ics])
        # Bind the grid click callback function to the left mouse button
        # press event on the grid canvas.
        self.w.bind('<ButtonPress-1>', w_click_callback)

    def select_plant(self, i):
        """Select the plant indexed at i in the plants_palette list."""

        self.palette_canvas.itemconfig(self.palette_rects[self.ics],
                                       outline='black', width=1)
        self.ics = i
        self.palette_canvas.itemconfig(self.palette_rects[self.ics],
                                       outline='black', width=5)

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
                c = self.w.itemcget(rect, 'fill')
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
            self.w.itemconfig(cell, fill=UNFILLED)
        
    def load_image(self):
        """Load an image from a provided file."""

        def _coords_to_index(coords):
            """
            Translate from the provided coordinate (e.g. 'A1') to an index
            into the grid cells list.
            """

            x_axis_index = ord(coords[0])-65
            y_axis_index = self.grid_size_n - int(coords[1:])
            return y_axis_index*self.grid_size_n + x_axis

        self.filename = filedialog.askopenfilename(filetypes=(
                ('Grid files', '.grid'),
                ('Text files', '.txt'),
                ('All files', '*.*')))
        if not self.filename:
            return
        print('Loading file from', self.filename)
        self.clear_grid()
        # Open the file and read the image, setting the cell plants as we go.
        with open(self.filename) as fi:
            for line in fi.readlines():
                line = line.strip()
                if line in self.plants_palette:
                    this_plant = line
                    continue
                if not line or line.startswith('-'):
                    continue
                coords = line.split(',')
                if not coords:
                    continue
                for coord in coords:
                    i = _coords_to_index(coord.strip())
                    self.w.itemconfig(self.cells[i], fill=this_plant)

# Get the grid size from the command line, if provided
try:
    grid_size_n = int(sys.argv[1])
except IndexError:
    grid_size_n = DEFAULT_N
except ValueError:
    print('Usage: {} <n>\nwhere n is the grid size.'.format(sys.argv[0]))
    sys.exit(1)
if grid_size_n < 1 or grid_size_n > MAX_N:
    print('Minimum grid_size_n is 1, Maximum grid_size_n is {}'.format(MAX_N))
    sys.exit(1)

# Set the whole thing running
root = Tk()
grid = GridApp(root, grid_size_n, 600, 600, 5)
root.mainloop()
