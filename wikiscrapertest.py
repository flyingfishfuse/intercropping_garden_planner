from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config

# TESTING =True
# set in the std_imports for a global TESTING at top level scope
from std_imports import *
import pandas

TEST_DB            = 'sqlite://'
DATABASE_HOST      = "localhost"
DATABASE           = "plants_info"
DATABASE_USER      = "admin"
SERVER_NAME        = "wat"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + DATABASE_HOST + DATABASE_USER + ".db"

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
    def __init__(self):
        self.sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
        self.thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'
        self.dataframes    = pandas.read_html(self.thing_to_get)
        self.proto_dict = {'plant_type' : '',
                            'name':'',
                            'scientific_name': '',
                            'helps':'',
                            'helped_by':'',
                            'bad_for':'',
                            'attracts_insects':'',
                            'repels_insects':'',
                            'notes':''
                        }

        self.Veggies_table = self.dataframes[0]
        self.Fruit_table   = self.dataframes[1]
        self.Herbs_table   = self.dataframes[2]
        self.Flowers_table = self.dataframes[3]
        self.Other_table   = self.dataframes[4]

        self.box_of_veggies = self.Veggies_table.iloc[range(0,len(self.Veggies_table.index))]
        self.box_of_fruit   = self.Fruit_table.iloc[range(0,len(self.Fruit_table.index))]
        self.box_of_herbs   = self.Herbs_table.iloc[range(0,len(self.Herbs_table.index))]
        self.box_of_flowers = self.Flowers_table.iloc[range(0,len(self.Flowers_table.index))]
        self.box_of_other   = self.Other_table.iloc[range(0,len(self.Other_table.index))]

        self.dothethingjulie()

    def dothethingjulie(self):
        for dataframe in self.dataframes:
            #if the dataframe is in the approved list
            if dataframe.columns[0][0] in self.sections_to_grab:
                #renaming columns for easier use
                dataframe.columns = ['name','scientific_name','helps','helped_by',
                                'attracts_insects','repels_insects','bad_for','notes']
                #loop over rows in dataset
                for row in range(0, len(dataframe.index)):
                    self.proto_dict.update({
                            'plant_type'      : dataframe.columns[0][0],
                            'name'            : self.box_of_veggies.iloc[row][0],
                            'scientific_name' : self.box_of_veggies.iloc[row][1],
                            'helps'           : self.box_of_veggies.iloc[row][2],
                            'helped_by'       : self.box_of_veggies.iloc[row][3],
                            'attracts_insects': self.box_of_veggies.iloc[row][4],
                            'repels_insects'  : self.box_of_veggies.iloc[row][5],
                            'bad_for'         : self.box_of_veggies.iloc[row][6],
                            'notes'           : self.box_of_veggies.iloc[row][7],
                        }
                    )
                    self.juliedothething(self.proto_dict)
    def juliedothething(self, dict_to_db: dict):
        NewPlant = Plants(
            plant_type      = dict_to_db.get('plant_type'),
            name            = dict_to_db.get('name'),
            scientific_name = dict_to_db.get('scientific_name'),
            helps           = dict_to_db.get('helps'),
            helped_by       = dict_to_db.get('helped_by'),
            attracts_insects= dict_to_db.get('attracts_insects'),
            repels_insects  = dict_to_db.get('repels_insects'),
            bad_for         = dict_to_db.get('bad_for'),
            notes           = dict_to_db.get('notes')
            )
        add_to_db(NewPlant)


# this action is done in the database_stuff file once the models and 
# functions have been declared 
# this file is also a standalone application 
#plant_data_lookup = ScrapeWikipediaTableForData()

        #self.juliedothething()
        #for dataframe in self.dataframes:
            # isolate each attribute from dataframe
            #if dataframe.columns[0][0] in self.sections_to_grab:
                #iloc[x] is an entire row entry
                # access each column by using :
                # iloc[x][y] where y = individual column in that row

                #for row in dataframe.iloc[0:len(dataframe.index)]:
                