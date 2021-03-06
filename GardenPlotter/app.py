#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains INSERT STUFF HERE
This I think is going to be the main file
"""
__author__  = 'Adam Galindo'
__email__   = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'

import sys,os
import garden
import pandas
from tkinter import *
import std_imports
from database.database_stuff import *
from gui.GardenGridGui import GardenGridGui
from std_imports import error_printer,warning_message,info_message
    #TODO: 
            # FALLBACK 
        # TO
    # TERMINAL
# ASK IF USER WANTS POP
# !was I high when I wrote this? ^

#########################################################
###           VERIFY / POPULATE DATABASE
#########################################################
################################################]
## SQLALCHEMY
#################################################

def check_if_plants_exist_bool(plant_name):
    try:
        exists = PlantDatabase.session.query(Plants.id).filter_by(name=plant_name).first() is not None
    except Exception:
        error_printer('[-] Database VERIFICATION FAILED!')
    if exists:
        info_message()
        return True
    else:
        return False
        #hwhat the he-hockey stick hockey stick am I doing!?!?!?


def table_exists(name):
    try:
        from sqlalchemy import inspect
        blarf = inspect(engine).dialect.has_table(engine.connect(),name)

        info_message('[+] Database Table {} EXISTS'.format(name))
        return True
    except Exception:
        error_printer("[-] TABLE {} does NOT EXIST!".format(name))


class ScrapeWikipediaTableForData:
    def __init__(self,sections_to_grab, thing_to_get):
        self.sections_to_grab = sections_to_grab
        self.thing_to_get     = thing_to_get
    
    def dothethingjulie(self):
        try:
            self.dataframes = pandas.read_html(self.thing_to_get)
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
                        add_plant_to_db(plant_entry)
        except Exception:
            error_printer("[-] WikiScraper FAILEDFAILED")

try:
    if os.path.exists('./database/plants_info.db') == False:
        try:
            PlantDatabase.create_all()
            PlantDatabase.session.commit()
            info_message("[+] Database Tables Created")
        except Exception:
            error_printer("[-] Database Table Creation FAILED \n")
        try:            
            add_plant_to_db(test_plant)
            add_plant_to_db(test_garden)
            info_message("[+] Test Commit SUCESSFUL, Continuing!\n")
        except Exception:
            error_printer("[-] Test Commit FAILED \n") 

        try:
            plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
            plant_data_lookup.dothethingjulie()
        except Exception:
            error_printer("[-] Database Table Creation FAILED \n")
    else:
        warning_message('[+] Database already exists, skipping creation')
except Exception:
    error_printer("[-] Database existence Check FAILED")



try:
    # Set the whole thing running
    GardenWindow = Tk()
    GardenWindow.title = "A garden planning application"
    #defaults are 30 cells on a 1024x1024px SVG grid of cells with 5px padding
    #TODO: add a number entry/slider + "apply" button to change padding px and re-render
    Garden = GardenGridGui(GardenWindow, grid_size_n=40)
    GardenWindow.mainloop()
except Exception:
    error_printer("[-] Application Initialization FAILED")

    