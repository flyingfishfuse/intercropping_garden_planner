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

# TKinter code based on https://github.com/scipython/colouring-grid
# A simple colouring grid app, with load/save functionality.
# Christian Hill, August 2018.

class CreateGardenGrid():
    def __new__(cls, *args):
        pass

    def __init__(self,
                grid_cell_n      = 30, 
                filename         = 'blank_grid', 
                canvas_height_px = 800,
                canvas_width_px  = 800,
                SIZE             = 800,
                PAD              = 40
                ):
        self.grid_cell_n         = grid_cell_n
        self.canvas_height_px    = canvas_height_px
        self.canvas_width_px     = canvas_width_px

        # SIZE is the grid image size, including 
        # padding around all sides of PAD.
        self.SIZE = SIZE
        self.PAD = PAD
        # output SVG image filename, size of the grid
        # within the image.
        self.filename = '{name}-{size}x{size}.svg'.format(name = filename, size = grid_cell_n)
        self.c_size = (self.SIZE - 2 * self.PAD) / grid_cell_n
        

    def svg_preamble(self, height, width):
        line1 = '<?xml version="1.0" encoding="utf-8"?>\n'
        line2 = '<svg xmlns="http://www.w3.org/2000/svg"\n      '
        line3 = 'xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >'.format(height, width)
        block1 = """<defs>
<style type="text/css"><![CDATA[
line {
        stroke-width: 1px;
        stroke: #888;
     }
    ]]></style>
</defs>
"""         
        data_required = ''' {}{}{}{}'''.format(line1,line2,line3,block1)
        return data_required

    def get_letter_coord(self, i):
        """Return the letter A, B, C, ... corresponding to i = 1, 2, 3, ..."""
        return chr(i+64)

    def createimagefile(self, filename, stuff):
        #open a file and start the preamble to create the SVG
        SVGtext = [self.svg_preamble()]
        new_image_file = open(filename, 'w+')
        #new_image_file.write(self.svg_preamble(stuff))
        
        # We need n+1 lines to mark out n cells and two nested loops; write both
        # coordinate labels in the outer loop.
        some_number_v = self.PAD // 2
        for cell in range(self.grid_cell_n + 1):

            if cell:
                some_number_u = self.PAD + self.c_size*(cell-0.5)
                SVGtext.append('<text x="{}" y="{}" text-anchor="middle" dominant-baseline="central">\
                    {}</text>'.format(some_number_u, self.SIZE-some_number_v,self.get_letter_coord(cell)))
                SVGtext.append('<text x="{}" y="{}" text-anchor="middle" dominant-baseline="central">\
                    {}</text>'.format(some_number_v, self.SIZE-some_number_u,str(cell)))
    
            for j in range(self.grid_cell_n + 1 ):
                x1, x2 = self.PAD + cell * self.c_size
                y1, y2 = self.PAD, self.SIZE-self.PAD
                SVGtext.append('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2))
                SVGtext.append('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(y1, x1, y2, x2))

        SVGtext.append('</svg>')
        finalSVG = ''.join(SVGtext)
        new_image_file.write(finalSVG)