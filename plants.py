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

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config

from std_imports import *


################################################################################
##############                      CONFIG                     #################
################################################################################
TESTING = True
TEST_DB            = 'sqlite://'
DATABASE_HOST      = "localhost"
DATABASE           = "plants_info"
DATABASE_USER      = "admin"
SERVER_NAME        = "wat"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + DATABASE_HOST + DATABASE_USER + ".db"

class Config(object):
    if TESTING == True:
        #SQLALCHEMY_DATABASE_URI = TEST_DB
        SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        #engine = create_engine(TEST_DB ,\
        #    connect_args={"check_same_thread": False},poolclass=StaticPool)
    elif TESTING == False:
        SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
        SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    PlantsDatabase = Flask(__name__ )
    PlantsDatabase.config.from_object(Config)
    database = SQLAlchemy(PlantsDatabase)
    database.init_app(PlantsDatabase)

    if TESTING == True:
        database.metadata.clear()

except Exception:
    redprint(Exception.with_traceback)

# from stack overflow
#In the second case when you're just restarting the app I would write a 
#test to see if the table already exists using the reflect method:

#db.metadata.reflect(engine=engine)

#Where engine is your db connection created using create_engine(), and see 
#if your tables already exist and only define the class if the table is undefined.
    
class Plants(database.Model):
    __tablename__       = 'Plants_Data'
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                                          index=True, \
                                          primary_key = True, \
                                          unique=True, \
                                          autoincrement=True)
    helps                              = database.Column(database.String(256))
    helped_by                          = database.Column(database.String(256))
    bad_for                            = database.Column(database.String(256))
    attracts_insects                   = database.Column(database.String(256))
    repels_insects                     = database.Column(database.String(256))    
    notes                              = database.Column(database.String(256))

    def __repr__(self):
        info = '''=========================================
name      : {} 
helps     : {} 
helped_by : {}
bad_for   : {}
attracts_insects  : {}
repels_insects    : {}
notes     : {}
'''.format(self.helps,
                        self.helped_by,
                        self.bad_for,
                        self.attracts_insects,
                        self.repels_insects,
                        self.notes
                    )

##########################
#  Test/Init DB Commits  #
##########################
#
#
# blah blah blah
#
#
#
###########################

def add_to_db(thingie):
    """
    Takes SQLAchemy model Objects 
    For updating changes to Class_model.Attribute using the form:
        Class_model.Attribute = some_var 
        add_to_db(some_var)
    """
    try:
        database.session.add(thingie)
        database.session.commit
        redprint("=========Database Commit=======")
        greenprint(thingie)
        redprint("=========Database Commit=======")
    except Exception as derp:
        print(derp)
        print(makered("[-] add_to_db() FAILED"))

def update_db():
    try:
        database.session.commit()
    except Exception as derp:
        print(derp.with_traceback)
        print(makered("[-] Update_db FAILED"))

def dump_db():
        """
    Prints database to screen
        """
        print(makered("-------------DUMPING DATABASE------------"))
        records1 = database.session.query(Plants).all()
        for each in records1:
            print (each)
        print(makered("------------END DATABASE DUMP------------"))
##########################################
#Relationships from online tables, currently, requires internet connection
# on first run. Will distribute with primed DB on release.
##########################################
class ScrapeWikipediaTableForData:
    '''
Yeah I know it's bad form to import in the middle but this is 
ANOTHER modular prototype I am making here
    '''
    def __init__(self) -> None:
        from bs4 import BeautifulSoup
        #import lxml
        import requests
        fulltable = {}
        self.sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
        self.thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'
        
        # Either one works I guess, gotta look into whats more efficient/fastest/?best?
        wikipage1 = requests.get(self.thing_to_get).response.read().decode('utf-8')
        wikipage2 = requests.request(method='GET', url=self.thing_to_get).content.decode('utf-8')
        self.soupyresults = BeautifulSoup(wikipage1, 'html.parser')
        #section_header = self.soupyresults.find(lambda tag:  tag.name=='span' and tag.has_key('id') and tag['id'] in self.sections_to_grab)
        #for section_header in soup.find_all('h2'):
        #    if section_header in self.sections_to_grab:
        tables_data = self.soupyresults.find(lambda tag:  tag.name=='table')
    
class IntercroppingRelationships:
    """
    Contains the data from the wikipedia page on intercropping
    in the variable "plant_info"
    """
    def __new__(cls, *args):
        #put the plants here for now
        pass
    def __init__(self):
        self.plant_info = [{"Asparagus"     : ["Tomato", "Parsley", "Basil"]},
                {"BushBeans"     : ["Potato", "Cucumber", "Corn", "Strawberry", "Celery", "SummerSavory"]},
                {"PoleBeans"     : ["Corn", "SummerSavory", "Radish"]},
                {"CabbageFamily" : ["AromaticHerbs", "Celery", "Beets", "OnionFamily", "Chamomile", "Spinach", "Chard"]},
                {"Carrots"       : ["Radish", "Lettuce", "Rosemary", "OnionFamily", "Sage", "Tomato"]},
                {"Celery"        : ["Onion", "CabbageFamily", "Tomato", "BushBeans", "Nasturtium"]},
                {"Corn"          : ["Potato", "Beans", "Pumpkins", "Cucumber", "Squash"]},
                {"Eggplant"      : ["Beans", "Marigold"]},
                {"Lettuce"       : ["Carrots", "Radish", "Strawberry", "Cucumber"]},
                {"OnionFamily"   : ["Beets", "Carrots", "Lettuce", "CabbageFamily", "SummerSavory"]},
                {"Parsley"       : ["Tomato", "Asparagus"]},
                {"Potato"        : ["Beans", "Corn", "CabbageFamily", "Marigolds", "HorseRadish"]},
                {"Pumpkins"      : ["Beans", "Corn", "Marigold"]},
                {"Radish"        : ["Carrots", "Nasturtium", "Lettuce", "Cucumber"]},
                {"Spinach" : ["Strawberry", "Beans"]},
                {"Squash" : ["Nasturtium", "Corn", "Marigold"]},
                {"Tomato" : ["OnionFamily", "Nasturtium", "Marigold", "Asparagus", "Carrots", "Parsley", "Cucumber"]},
                {"Turnip" : ["AromaticHerbs", "Celery", "Beets", "OnionFamily", "Chamomile", "Spinach", "Chard"]}]

##################################################
## Class prototypes for each plant
#class Asparagus:
#    def __init__(self):
#        pass
#    def information(self):
#        pass
 
