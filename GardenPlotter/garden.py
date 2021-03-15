#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""

"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'

class GardenEntity():
    def __new__(cls) -> Any:
        pass
    def __init__(self) -> None:
        self.hemisphere = 'north'
        pass

class PlantEntity:
    def __init__(self,plant_data : dict):
        self.goodneighbors = list
    def __name__(self):
        return plant_data.get('name')
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