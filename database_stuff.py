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

# https://en.wikipedia.org/wiki/List_of_companion_plants
# https://en.wikipedia.org/wiki/Companion_planting
import pandas
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config

# TESTING =True
# set in the std_imports for a global TESTING at top level scope
from std_imports import *

################################################################################
##############                      CONFIG                     #################
################################################################################

TEST_DB            = 'sqlite://'
DATABASE           = "plants_info"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + ".db"
sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'

class Config(object):
# TESTING = True
# set in the std_imports for a global TESTING at top level scope
    SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
try:
    PlantsDatabase = Flask(__name__ )
    PlantsDatabase.config.from_object(Config)
    database = SQLAlchemy(PlantsDatabase)
    database.init_app(PlantsDatabase)
    engine = create_engine(LOCAL_CACHE_FILE , connect_args={"check_same_thread": False},poolclass=StaticPool)
    if TESTING == True:
        database.metadata.clear()
except Exception:
    error_message("[-] Database Initialization FAILED \n" + str(traceback.print_exc()))
    
class Plants(database.Model):
    __tablename__       = 'Plants'
    #__table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer,
                                          index         = True,
                                          unique        = True,
                                          autoincrement = True)
    plant_type                         = database.Column(database.String(256))                                          
    name                               = database.Column(database.String(256),
                                          primary_key   = True,
                                          unique        = True)
    scientific_name                    = database.Column(database.String(256))
    helps                              = database.Column(database.String(256))
    helped_by                          = database.Column(database.String(256))
    bad_for                            = database.Column(database.String(256))
    attracts_insects                   = database.Column(database.String(256))
    repels_insects                     = database.Column(database.String(256))    
    notes                              = database.Column(database.String(256))

    def __repr__(self):
        return '''=========================================
Type      : {}
name      : {} 
scientific name      : {} 
helps     : {} 
helped_by : {}
bad_for   : {}
attracts_insects  : {}
repels_insects    : {}
notes     : {}
'''.format(self.plant_type,
            self.name,
            self.scientific_name,    
            self.helps,
            self.helped_by,
            self.bad_for,
            self.attracts_insects,
            self.repels_insects,
            self.notes
        )

# representation of a whole garden grid
#stores the data for the GUI representation
class Garden(database.Model):
    __tablename__       = 'Garden'
    #__table_args__      = {'extend_existing': True}
    id               = database.Column(database.Integer,
                            index         =True,
                            unique        =True,
                            autoincrement =True)
    name             = database.Column(database.String(256),
                            primary_key   = True,
                            unique        =True)
    hemisphere       = database.Column(database.String(256))
    zone             = database.Column(database.String(256))
    notes            = database.Column(database.String(256))
    grid_data        = database.Column(database.Text)

    def __repr__(self):
        return '''
=========================================
name       : {} 
hemisphere : {}
zone       : {}
notes      : {}
=========================================
'''.format(self.name,
            self.hemisphere,
            self.zone,
            self.notes
        )
try:
    database.create_all()
    database.session.commit()
except Exception as derp:
    error_message("[-] Update_db FAILED \n" + str(traceback.print_exc()))

test_plant = Plants(plant_type      = 'Tree',
                    name            = 'fuck apple',
                    scientific_name = 'fruitus givafuckus',
                    helps           = 'thineself',
                    helped_by       = 'cannabis indica',
                    attracts_insects= 'ladybugs',
                    repels_insects  = 'mosquitos',
                    bad_for         = 'negative vibes',
                    notes           = 'Grows best in in the sun giving shade'
                    )
test_garden = Garden(name = 'home base',
                     hemisphere = 'south',
                     zone = '7a',
                     notes = 'bada-bing bada-boom, big badaboom'
                    )
try:
    database.session.add(test_plant)
    database.session.add(test_garden)
    database.session.commit()
except Exception as derp:
    error_message("[-] Update_db FAILED \n" + str(traceback.print_exc()))

def add_plant_to_db(plant_to_add):
    """
    """
    try:
        duplicate_check_query = database.session.query(Plants).filter_by(name=plant_to_add.name).scalar() is not None
        if duplicate_check_query:
            info_message('[+] Duplicate Entry Avoided : ' + plant_to_add.name)
        database.session.add(plant_to_add)
        database.session.commit
    except Exception as derp:
        error_message("[-] add_plant_to_db() FAILED \n" + str(traceback.print_exc()))

def update_db():
    try:
        database.session.commit()
    except Exception as derp:
        error_message("[-] Update_db FAILED \n" + str(traceback.print_exc()))

class ScrapeWikipediaTableForData:
    def __init__(self,sections_to_grab, thing_to_get):
        self.sections_to_grab = sections_to_grab
        self.thing_to_get     = thing_to_get
        self.dataframes       = pandas.read_html(self.thing_to_get)
        #self.Veggies_table   = self.dataframes[0]
        #self.box_of_veggies  = self.Veggies_table.iloc[range(0,len(self.Veggies_table.index))]
        for dataframe in self.dataframes:
            #if the dataframe is in the approved list
            if dataframe.columns[0][0] in self.sections_to_grab:
                #renaming columns for easier use
                dataframe.columns = ['name','scientific_name','helps','helped_by',
                                'attracts_insects','repels_insects','bad_for','notes']
                #loop over rows in dataset
                for row in range(0, len(dataframe.index)):
                    plant_entry = Plants(plant_type      = dataframe.columns[0][0],
                                         name            = dataframe.iloc[row]['name'],
                                         scientific_name = dataframe.iloc[row]['scientific_name'],
                                         helps           = dataframe.iloc[row]['helps'],
                                         helped_by       = dataframe.iloc[row]['helped_by'],
                                         attracts_insects= dataframe.iloc[row]['attracts_insects'],
                                         repels_insects  = dataframe.iloc[row]['repels_insects'],
                                         bad_for         = dataframe.iloc[row]['bad_for'],
                                         notes           = dataframe.iloc[row]['notes'],
                                        )
                    database.session.add(plant_entry)
                database.session.commit()

plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
