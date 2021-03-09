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
    helps                              = database.Column(database.String(32))
    helped_by                          = database.Column(database.String(32))
    bad_for                            = database.Column(database.String(64))
    attracts_insects                   = database.Column(database.String(32))
    repels_insects                     = database.Column(database.String(32))    
    notes                              = database.Column(database.String(32))

    def __repr__(self):
        return 'name         : {} \n \
helps : {}  \n\
helped_by : {}  \n\
bad_for  : {}  \n\
attracts_insects  : {}  \n\
repels_insects  : {} \n\
notes : {} \n '.format(self.helps,self.helped_by,self.bad_for,self.attracts_insects,self.repels_insects, self.notes)

class ConnectedHosts(LoginInformation):
    __tablename__       = 'Connected_hosts'
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                                          index=True, \
                                          primary_key = True, \
                                          unique=True, \
                                          autoincrement=True)
    username                  = database.Column(database.String(32))

##########################
#  Test/Init DB Commits  #
##########################

credentials =  [['user1'  , 'password' ],
                ['user2'  , 'password2']]
for user_pass in credentials:
    pass


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
        records1 = database.session.query(Compound).all()
        for each in records1:
            print (each)
        print(makered("------------END DATABASE DUMP------------"))
##########################################
#Relationships from online tables
##########################################
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
 
