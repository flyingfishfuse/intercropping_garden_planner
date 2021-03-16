#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains INSERT STUFF HERE
This I think is going to be the main file
"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'

import garden
import pandas
from tkinter import *
from gui.GardenGridGui import GardenGridGui
from database.database_stuff import *
from std_imports import error_printer,warning_message

    #TODO: 
            # FALLBACK 
        # TO
    # TERMINAL
# ASK IF USER WANTS POP

#########################################################
###           VERIFY / POPULATE DATABASE
#########################################################
class ScrapeWikipediaTableForData:
    def __init__(self,sections_to_grab, thing_to_get):
        self.sections_to_grab = sections_to_grab
        self.thing_to_get     = thing_to_get
        self.dataframes       = pandas.read_html(self.thing_to_get)
        for dataframe in self.dataframes:
            if dataframe.columns[0][0] in self.sections_to_grab:
                dataframe.columns = ['name','scientific_name','helps','helped_by',
                                'attracts_insects','repels_insects','bad_for','notes']
                for row in range(0, len(dataframe.index)):
                    if dataframe.iloc[row]['name'] == 'Common name':
                        warning_message("[-] PANDAS - Table Header discarded from rows")
                    else :
                        plant_entry = Plants(plant_type  = dataframe.columns[0][0],
                                        name            = dataframe.iloc[row]['name'],
                                        scientific_name = dataframe.iloc[row]['scientific_name'],
                                        helps           = dataframe.iloc[row]['helps'],
                                        helped_by       = dataframe.iloc[row]['helped_by'],
                                        attracts_insects= dataframe.iloc[row]['attracts_insects'],
                                        repels_insects  = dataframe.iloc[row]['repels_insects'],
                                        bad_for         = dataframe.iloc[row]['bad_for'],
                                        notes           = dataframe.iloc[row]['notes'],
                                        )
                    #PlantDatabase.session.add(plant_entry)
                    add_plant_to_db(plant_entry)
                #PlantDatabase.session.commit()

if DATABASE_EXISTS:
    plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
else:
    warning_message('[+] Database already exists, skipping creation')


try:
    # Set the whole thing running
    root = Tk()
    #defaults are 30 cells on a 1024x1024px SVG grid of cells with 5px padding
    #TODO: add a number entry/slider + "apply" button to change padding px and re-render
    Garden = GardenGridGui(root, grid_size_n=40)
    root.mainloop()
except Exception:
    error_printer("[-] Application Initialization FAILED")

    