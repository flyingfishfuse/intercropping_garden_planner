#!/usr/bin/python3
# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/List_of_companion_plants
# https://en.wikipedia.org/wiki/Companion_planting
import sys,os
import pandas
import traceback
from std_imports import *
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config
from sqlalchemy_utils import database_exists,create_database

################################################################################
##############                      CONFIG                     #################
################################################################################

TEST_DB            = 'sqlite://'
DATABASE           = "plants_info"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + ".db"
DATABASE_FILENAME  = DATABASE + '.db'
sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'

class Config(object):
# TESTING = True
# set in the std_imports for a global TESTING at top level scope
    SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    engine = create_engine(LOCAL_CACHE_FILE , connect_args={"check_same_thread": False},poolclass=StaticPool)
    #check if exists
    if not database_exists(LOCAL_CACHE_FILE) or os.path.exists(DATABASE_FILENAME):
        DATABASE_EXISTS = True
    else:
        DATABASE_EXISTS = False        
    
    PlantsDatabase = Flask(__name__ )
    PlantsDatabase.config.from_object(Config)
    database = SQLAlchemy(PlantsDatabase)
    database.init_app(PlantsDatabase)
    if TESTING == True:
        database.metadata.clear()
except Exception:
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    error_message("[-] Database Initialization FAILED \n" + ''.join(tb.format_exception_only()))

#########################################################
###                    PLANT MODEL
#########################################################
class Plants(database.Model):
    __tablename__       = 'Plants'
    #__table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer,
                                          index         = True,
                                          unique        = True,
                                          autoincrement = True)
    plant_type                         = database.Column(database.String(256))                                          
    name                               = database.Column(database.String(256),
                                          primary_key   = True)
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

#########################################################
###                    GARDEN MODEL
#########################################################
class Garden(database.Model):
    __tablename__       = 'Garden'
    #__table_args__      = {'extend_existing': True}
    id               = database.Column(database.Integer,
                            index         =True,
                            unique        =True,
                            autoincrement =True)
    name             = database.Column(database.String(256),
                            primary_key   = True)
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

#########################################################
###             DATABASE FUNCTIONS
#########################################################
def add_plant_to_db(plant_to_add):
    """
    """
    try:
        duplicate_check_query = database.session.query(Plants).filter_by(name=plant_to_add.name).scalar() is not None
        if duplicate_check_query:
            info_message('[+] Duplicate Entry Avoided : ' + plant_to_add.name)
        database.session.add(plant_to_add)
        database.session.commit
        info_message('[+] Plant Added To Database : ' + plant_to_add.name)
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
        debug_message("[-] add_plant_to_db() FAILED \n" + ''.join(tb.format_exception_only()))

#########################################################
###         INITIALIZE DATABASE TABLES
#########################################################
try:
    database.create_all()
    database.session.commit()
except Exception:
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    error_message("[-] Database Table Creation FAILED \n" + ''.join(tb.format_exception_only()))

#########################################################
###                  TEST ENTRIES 
#########################################################
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

if not DATABASE_EXISTS:
    try:
        add_plant_to_db(test_plant)
        add_plant_to_db(test_garden)
        database.session.commit()
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
        error_message("[-] Test Commit FAILED \n" + ''.join(tb.format_exception_only()))    

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
                    #database.session.add(plant_entry)
                    add_plant_to_db(plant_entry)
                #database.session.commit()

if DATABASE_EXISTS:
    plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
else:
    warning_message('[+] Database already exists, skipping creation')

