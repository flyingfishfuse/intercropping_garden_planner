#!/usr/bin/python3
# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/List_of_companion_plants
# https://en.wikipedia.org/wiki/Companion_planting
import sys,os
import pandas
import traceback
from std_imports import error_message,info_message, TESTING,debug_message
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
    
    PlantsGUIDatabase = Flask(__name__ )
    PlantsGUIDatabase.config.from_object(Config)
    PlantDatabase = SQLAlchemy(PlantsGUIDatabase)
    PlantDatabase.init_app(PlantsGUIDatabase)
    if TESTING == True:
        PlantDatabase.metadata.clear()
except Exception:
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    error_message("[-] Database Initialization FAILED \n" + ''.join(tb.format_exception_only()))

#########################################################
###                    PLANT MODEL
#########################################################
class Plants(PlantDatabase.Model):
    __tablename__       = 'Plants'
    #__table_args__      = {'extend_existing': True}
    id                  = PlantDatabase.Column(PlantDatabase.Integer,
                                          index         = True,
                                          unique        = True,
                                          autoincrement = True)
    plant_type                         = PlantDatabase.Column(PlantDatabase.String(256))                                          
    name                               = PlantDatabase.Column(PlantDatabase.String(256),
                                          primary_key   = True)
    scientific_name                    = PlantDatabase.Column(PlantDatabase.String(256))
    helps                              = PlantDatabase.Column(PlantDatabase.String(256))
    helped_by                          = PlantDatabase.Column(PlantDatabase.String(256))
    bad_for                            = PlantDatabase.Column(PlantDatabase.String(256))
    attracts_insects                   = PlantDatabase.Column(PlantDatabase.String(256))
    repels_insects                     = PlantDatabase.Column(PlantDatabase.String(256))    
    notes                              = PlantDatabase.Column(PlantDatabase.String(256))

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
class Garden(PlantDatabase.Model):
    __tablename__       = 'Garden'
    #__table_args__      = {'extend_existing': True}
    id               = PlantDatabase.Column(PlantDatabase.Integer,
                            index         =True,
                            unique        =True,
                            autoincrement =True)
    name             = PlantDatabase.Column(PlantDatabase.String(256),
                            primary_key   = True)
    hemisphere       = PlantDatabase.Column(PlantDatabase.String(256))
    zone             = PlantDatabase.Column(PlantDatabase.String(256))
    notes            = PlantDatabase.Column(PlantDatabase.String(256))
    grid_data        = PlantDatabase.Column(PlantDatabase.Text)

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
        duplicate_check_query = PlantDatabase.session.query(Plants).filter_by(name=plant_to_add.name).scalar() is not None
        if duplicate_check_query:
            info_message('[+] Duplicate Entry Avoided : ' + plant_to_add.name)
        PlantDatabase.session.add(plant_to_add)
        PlantDatabase.session.commit
        info_message('[+] Plant Added To Database : ' + plant_to_add.name)
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
        debug_message("[-] add_plant_to_db() FAILED \n" + ''.join(tb.format_exception_only()))

#########################################################
###         INITIALIZE DATABASE TABLES
#########################################################
try:
    PlantDatabase.create_all()
    PlantDatabase.session.commit()
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
        PlantDatabase.session.commit()
        info_message("[+] Test Commit SUCESSFUL, Continuing!")
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
        error_message("[-] Test Commit FAILED \n" + ''.join(tb.format_exception_only()))    
