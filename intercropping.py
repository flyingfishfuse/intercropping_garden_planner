#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##                    Code to model plants for garden placment                ##
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
"""
This file contains INSERT STUFF HERE
This I think is going to be the main file
"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'

from grid import *

class GardenEntity():
    def __new__(cls) -> Any:
        pass
    def __init__(self) -> None:
        self.hemisphere = 'north'
        pass

class PlantEntity:
	def __init__(self,plant_data : dict):
		self.goodneighbors = list
	
	def __repr__(self):
		print(" I AM A : {}".format(self.__name__))
		#print(self.__name__) 

    
class IntercroppingRelationships:
    def __new__(cls, *args):
        #put the plants here for now
        pass
    def __init__(self):
        pass
    def get_goodneighbors(self, plant_name:str):
        pass
    def get_badneighbors(self, plant_name:str):
        pass