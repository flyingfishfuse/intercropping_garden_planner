#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains :
    - This is a monolithic test file for exploration in bpython

    - this file will be stripped/abstracted/compiled/packaged

    - you (me) will ab-so-fucking-lutely document the file that performs the conversion/packaging
        so others can see how the development version turns into a final product

    - I think this is going to be the final monolith we feed
        to a compiler/packager for cross platform releases.
        The main assembly of code in multiple files is for development/openness
    
"""
__author__  = 'Adam Galindo'
__email__   = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'


################################################################################
##############                      imports                    #################
################################################################################
import os
import sys
import numpy
import shutil
import pandas
import logging
import itertools
import traceback
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from flask import Flask, render_template, Response, Request ,Config

TESTING = True
try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    if TESTING == True:
        COLORMEQUALIFIED = True
except ImportError as derp:
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
    COLORMEQUALIFIED = False
################################################################################
##############                      VARS                       #################
################################################################################
list_of_db_tables  = ['Vegetables','Fruits','Herbs','Flowers','Other']
db_is_initialized  = bool
db_is_populated    = bool
test_commit_result = bool

##########################
# Colorization Functions #
##########################
# yeah, about the slashes... do you want invisible \n? 
# Because thats how you avoid invisible \n and concatenation errors
blueprint             = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint             = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint             = lambda text: print(Fore.RED + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
# lambing while you lamb?
makered                = lambda text: Fore.RED + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen              = lambda text: Fore.GREEN + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue              = lambda text: Fore.BLUE + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow             = lambda text: Fore.YELLOW + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print     = lambda text: print(Fore.YELLOW + Style.BRIGHT + \
    ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

###########
# LOGGING #
###########
LOGLEVEL = 'DEV_IS_DUMB'
LOGLEVELS = [1,2,3,'DEV_IS_DUMB'] # critical defcon 1 level shit

log_file  = 'garden_grid_message_log'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger    = logging.getLogger()


debug_message = lambda message: logger.debug(blueprint(message)) 
info_message  = lambda message: logger.info(greenprint(message))   
warning_message  = lambda message: logger.warning(yellow_bold_print(message)) 
error_message    = lambda message: logger.error(redprint(message)) 
critical_message = lambda message: logger.critical(yellow_bold_print(message))

def error_printer(text):
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    if LOGLEVEL == 'DEV_IS_DUMB':
        error_message( text + ''.join(trace.format_exception_only()))
        #bad_LOC = traceback.format_list(trace.extract_tb(trace)[-1:])[-1]
        #warning_message(bad_LOC)
        debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    else:
        error_message(text + ''.join(trace.format_exception_only()))

################################################################################
##############                      CONFIG                     #################
################################################################################
TEST_DB            = 'sqlite://'
DATABASE           = "plants_info"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + ".db"
DATABASE_FILENAME  = DATABASE + '.db'
sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'

if database_exists(LOCAL_CACHE_FILE) or os.path.exists('/database/' + DATABASE_FILENAME):
    DATABASE_EXISTS = True
else:
    DATABASE_EXISTS = False        
  
class Config(object):
# TESTING = True
# set in the std_imports for a global TESTING at top level scope
    SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    engine = create_engine(LOCAL_CACHE_FILE , connect_args={"check_same_thread": False},poolclass=StaticPool)
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
        #info_message('[+] Plant Added To Database : ' + plant_to_add.name)
    except Exception:
        error_printer("[-] add_plant_to_db() FAILED")

#########################################################
###         INITIALIZE DATABASE TABLES
#########################################################
#try:
#    PlantDatabase.create_all()
#    PlantDatabase.session.commit()
#except Exception:
#    exc_type, exc_value, exc_tb = sys.exc_info()
#    tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
#    error_message("[-] Database Table Creation FAILED \n" + ''.join(tb.format_exception_only()))

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
                     zone = '9a',
                     notes = 'bada-bing bada-boom, big badaboom'
                    )  
def does_plant_exists(self,plant_name):
    try:
        if PlantDatabase.session.query(Plants.id).filter_by(name=plant_name).first() is not None:
            info_message('[+] Plant {} Exists'.format(plant_name))
            return True
        else:
            return False        
    except Exception:
        error_printer('[-] Database VERIFICATION FAILED!')


    #veggies = PlantDatabase.session.query(Plants).filter_by(plant_type = 'Vegetables').all()
    #fruits  = PlantDatabase.session.query(Plants).filter_by(plant_type = 'Fruits').all()
    #herbs   = PlantDatabase.session.query(Plants).filter_by(plant_type = 'Herbs').all()
    #flowers = PlantDatabase.session.query(Plants).filter_by(plant_type = 'Flowers').all()
    #Other   = PlantDatabase.session.query(Plants).filter_by(plant_type = 'Other').all()
    


class ScrapeWikipediaTableForData:
    '''
    feed it :
        local_or_remote = 'remote'

    to fetch wikipedia article

        local_or_remote = 'local'
    
    will unpack and read a tar.gz of the wikipedia page
  
    '''
    def __init__(self,sections_to_grab, thing_to_get, local_or_remote = 'local'):
        self.sections_to_grab = sections_to_grab
        self.thing_to_get     = thing_to_get
        archive_list     = [
                            './database/everipedia_cache.tar.gz',
                            './database/wikipedia_cache.tar.gz'
                            ]

    def extract_deep_storage(self, archives, extract_path = './database/workingdir'):
            shutil.unpack_archive(archives, extract_path)
    
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
            error_printer("[-] WIKISCRAPER FAILED!")
################################################################################
##############         GRID CREATION - Warning : Dragons       #################
################################################################################
# so we are pretty much "simulating reality" with the creation of a grid 
# representing a physical space with real items having thier own unique traits

# the easiest way to program in OOP is to train your mind to see these 
# things as physical objects with fiddly bits to tug on

# define reality
#places in the physical space
grid_points = []
#map of the physical space
list_of_all_cells = []
#size of the physical space
grid_size_n = 5

# set the limits of the physical space
grid_x = range(grid_size_n)
grid_y = range(grid_size_n)

# assign meaning to the physical space in the form of a 2-d grid
x_coordinates, y_coordinates = numpy.meshgrid(grid_x,grid_y,indexing='xy')
coordinate_array = list(itertools.zip_longest(x_coordinates,y_coordinates))

# map the physical space to an array in cartesian format
for field in coordinate_array:
    x_field       = field[0]
    y_field       = field[1]
    grid_location = list(itertools.zip_longest(x_field,y_field))
    grid_points.append(grid_location)
    for thing in grid_points:
        for each in thing:
            list_of_all_cells.append(each)

# present a text representation of the physical space
# for your viewing displeasure
if len(grid_points) > 10:
    warning_message('[-] Grid too large to display properly in terminal')
else:
    warning_message("WELCOME TO THE GRID")
    for each in grid_points:
        print(each)

################################################################################
##############          database/ verification functions       #################
################################################################################
def does_table_exist(name):
    try:
        blarf = inspect(engine).dialect.has_table(engine.connect(),name)
        if blarf == True:
            db_is_initialized = True 
            info_message('[+] Database Table {} EXISTS'.format(name))
            return True
        else:
            warning_message("[-] TABLE {} does NOT EXIST!".format(name))
            db_is_initialized = False 
            return False
    except Exception:
        error_printer('[-] Table Verification FAILED!')


def is_db_populated():
    try:
        info_message('[+] Checking the Database Population')
        #checking table entries
        for type_of_plant in list_of_db_tables:
            list_of_type = PlantDatabase.session.query(Plants).filter_by(plant_type = type_of_plant).all()
            if len(list_of_type) > 0:
                info_message('[+] Database has {} entries for {}'.format(len(list_of_type), type_of_plant))
                db_is_initialized = True        
            else:
                db_is_initialized = False
                warning_message('[-] Database has no entries for {}'.format(type_of_plant))
        if db_is_populated:
            warning_message('[+] Database is Populated')
            return True
        else:
            warning_message('[-] Database is NOT Populated')
            return False
    except Exception:
        error_printer('[-] Database Population Check FAILED!')

def init_database():
    try:
        PlantDatabase.create_all()
        PlantDatabase.session.commit()
        info_message("[+] Database Tables Created")
    except Exception:
        error_printer("[-] Database Table Creation FAILED ")

################################################################################
##############                   Control loop                  #################
################################################################################
try:
    #if DB or tables dont exist, create them
    if not database_exists(LOCAL_CACHE_FILE) or does_table_exist("Plants") == False:

    #######################################################################
    #function returns a boolean but also sets a semi-global bool            
    elif is_db_populated() == False:
        try:
            add_plant_to_db(test_plant)
            info_message("[+] Test Commit SUCESSFUL, Continuing!")
        except Exception:
            test_commit_result = False
            error_printer("[-] Test Commit FAILED ")
    #######################################################################
    # populates the DB by unzipping the tarball and reading the html
        info_message('[+] Attempting to Populate the Database')
        try:
            plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
            plant_data_lookup.dothethingjulie()
        except Exception:
            error_printer("[-] Database Table Creation FAILED")
    elif (database_exists(LOCAL_CACHE_FILE)) or  \
        (does_table_exist("Plants") == True) and\
        (is_db_populated() == True): 
        warning_message('[+] Database already exists, skipping creation')
except Exception:
    error_printer("[-] Database existance Check FAILED")

plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
plant_data_lookup.dothethingjulie()
#>>> for each in grid_points:
#...     print(each)
#  -------------------X-------------------- 
#   [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
#   [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
# Y [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
#   [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]
#   [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
# 
#>>> y axis index is grid_points[y_index]
# [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]

#for (x_coord, y_coord) in coordinate_array:

#>>> x_coordinates
#array([[0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4],
#       [0, 1, 2, 3, 4]])
#>>> x_coordinates[0]

#array([0, 1, 2, 3, 4])
#>>> asdf = itertools.zip_longest(x_coordinates,y_coordinates)

#>>> for each in asdf:
#...     print(each)
#... 
#>>> asdf = itertools.zip_longest(x_coordinates,y_coordinates)
#>>> for each in asdf:
#...     print(each[1]) # this is y field
#...                     
#[0 0 0 0 0]
#[1 1 1 1 1]
#[2 2 2 2 2]
#[3 3 3 3 3]
#[4 4 4 4 4]
#       field[0]                 field[1]
#       x axis                   y axis
#(array([0, 1, 2, 3, 4]), array([0, 0, 0, 0, 0]))
#(array([0, 1, 2, 3, 4]), array([1, 1, 1, 1, 1]))
#(array([0, 1, 2, 3, 4]), array([2, 2, 2, 2, 2]))
#(array([0, 1, 2, 3, 4]), array([3, 3, 3, 3, 3]))
#(array([0, 1, 2, 3, 4]), array([4, 4, 4, 4, 4]))