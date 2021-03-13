from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config

# TESTING =True
# set in the std_imports for a global TESTING at top level scope
from std_imports import *
import pandas

sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'
#prototype for matching to this setup
attributes_dict = {
        'name':'',
        'scientific_name': '',
        'helps':'',
        'helped_by':'',
        'bad_for':'',
        'attracts_insects':'',
        'repels_insects':'',
        'notes':''
    }

################################################################################
##############                      CONFIG                     #################
################################################################################
TEST_DB            = 'sqlite://'
DATABASE_HOST      = "localhost"
DATABASE           = "plants_info"
DATABASE_USER      = "admin"
SERVER_NAME        = "wat"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + DATABASE_HOST + DATABASE_USER + ".db"
sections_to_grab   = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get       = 'https://en.wikipedia.org/wiki/List_of_companion_plants'
plants_attributes_dict = {
    'name':'',
    'scientific_name': '',
    'helps':'',
    'helped_by':'',
    'bad_for':'',
    'attracts_insects':'',
    'repels_insects':'',
    'notes':''
}

class Config(object):
# TESTING = True
# set in the std_imports for a global TESTING at top level scope
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
    type                               = database.Column(database.String(256))
    name                               = database.Column(database.String(256))
    scientific_name                    = database.Column(database.String(256))
    helps                              = database.Column(database.String(256))
    helped_by                          = database.Column(database.String(256))
    bad_for                            = database.Column(database.String(256))
    attracts_insects                   = database.Column(database.String(256))
    repels_insects                     = database.Column(database.String(256))    
    notes                              = database.Column(database.String(256))

    def __repr__(self):
        info = '''=========================================
type      : {} 
name      : {} 
scientific name      : {} 
helps     : {} 
helped_by : {}
bad_for   : {}
attracts_insects  : {}
repels_insects    : {}
notes     : {}
'''.format(self.type,
            self.name,
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
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                                          index=True, \
                                          primary_key = True, \
                                          unique=True, \
                                          autoincrement=True)
    name                               = database.Column(database.String(256))
    hemisphere                         = database.Column(database.String(256))
    zone                               = database.Column(database.String(256))
    notes                              = database.Column(database.String(256))
    grid_data                          = database.Column(database.Text)

    def __repr__(self):
        info = '''
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


def add_to_db(thingie):
    database.session.add(thingie)
    database.session.commit

def update_db():
    database.session.commit()

def dump_plants():
        records1 = database.session.query(Plants).all()
        for each in records1:
            print (each)

def dump_gardens():
        records1 = database.session.query(Garden).all()
        for each in records1:
            print (each)

# FUCK IT ALL
# i was trying to be abstract, apparently I have to be...
# IMPLICIT
class ScrapeWikipediaTableForData:
    def __init__(self,url,sqlalchemy_mapping:dict, sections_tograb):
        self.dataframes    = pandas.read_html(url)
        # recursion breaks in a wierd place
        self.veggies_dict  = attributes_dict
        self.fruits_dict   = attributes_dict
        self.herbs_dict    = attributes_dict
        self.flowers_dict  = attributes_dict
        self.other_dict    = attributes_dict

        self.sections_to_grab = sections_tograb
        self.dothethingjulie()

    def dothethingjulie(self):
        # DATAFRAME 1 THROUGH 5 IS WHAT WE WANT
        self.Veggies = self.dataframes[0]
        self.Fruit   = self.dataframes[1]
        self.Herbs   = self.dataframes[2]
        self.Flowers = self.dataframes[3]
        self.Other   = self.dataframes[4]
        
        box_of_veggies = self.Veggies.iloc[range(0,len(plant_data_lookup.Veggies.index))]

        #self.juliedothething()
        #for dataframe in self.dataframes:
            # isolate each attribute from dataframe
            #if dataframe.columns[0][0] in self.sections_to_grab:
                #iloc[x] is an entire row entry
                # access each column by using :
                # iloc[x][y] where y = individual column in that row

                #for row in dataframe.iloc[0:len(dataframe.index)]:
                
    def juliedothething(self):
        NewPlant = Plants(
            name            = self.attributes_dict.get('name'),
            scientific_name = self.attributes_dict.get('scientific_name'),
            helps           = self.attributes_dict.get('helps'),
            helped_by       = self.attributes_dict.get('helped_by'),
            attracts_insects= self.attributes_dict.get('attracts_insects'),
            repels_insects  = self.attributes_dict.get('repels_insects'),
            bad_for         = self.attributes_dict.get('bad_for'),
            notes           = self.attributes_dict.get('notes')
            )
        add_to_db(NewPlant)

# this action is done in the database_stuff file once the models and 
# functions have been declared 
# this file is also a standalone application 
plant_data_lookup = ScrapeWikipediaTableForData(thing_to_get,attributes_dict, sections_to_grab)
print(plant_data_lookup.attributes_dict)