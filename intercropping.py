from plants import *
from uni_vars import *

import numpy as np
from Tkinter import *
import matplotlib.pyplot as plt

from grid import *

class Plant:
	def __init__(self, cls, plant_data : dict):
		cls.plant_data     = plant_data
		self.goodneighbors = list
		for key, value in cls.plant_data.items():
			self.goodneighbors.append(value)
		#for key,value in cls.plant_data.items():
		#	setattr(self, key, value)
		#	self.__name__ = key
	
	def __repr__(self):
		print(" I AM A : {}".format(self.__name__))
		#print(self.__name__) 
