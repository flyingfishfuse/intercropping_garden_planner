import os
from plants import Plant
import pandas
from std_imports import greenprint,redprint,blueprint
from database_stuff import *
fulltable = {}
sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'

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

class ScrapeWikipediaTableForData:
    def __init__(self,url,sqlalchemy_mapping:dict):
        self.dataframes  = pandas.read_html(url)
        self.plants_attributes_dict  = {}
        self.dothethingjulie()

    def dothethingjulie(self):
        for dataframe in self.dataframes:
            # isolate each attribute from dataframe
            if dataframe.columns[0][0] in sections_to_grab:
                self.plants_attributes_dict.update(\
                    name            = dataframe.iloc[0],
                    scientific_name = dataframe.iloc[1],
                    helps           = dataframe.iloc[2],
                    helped_by       = dataframe.iloc[3],
                    attracts_insects= dataframe.iloc[4],
                    repels_insects  = dataframe.iloc[5],
                    bad_for         = dataframe.iloc[6],
                    notes           = dataframe.iloc[7]
                )
        self.juliedothething()
    def juliedothething(self):
        NewPlant = Plant(
            name            = self.plants_attributes_dict.get('name'),
            scientific_name = self.plants_attributes_dict.get('scientific_name'),
            helps           = self.plants_attributes_dict.get('helps'),
            helped_by       = self.plants_attributes_dict.get('helped_by'),
            attracts_insects= self.plants_attributes_dict.get('attracts_insects'),
            repels_insects  = self.plants_attributes_dict.get('repels_insects'),
            bad_for         = self.plants_attributes_dict.get('bad_for'),
            notes           = self.plants_attributes_dict.get('notes')
            )
        add_to_db(NewPlant)
        

plant_data_lookup = ScrapeWikipediaTableForData(thing_to_get,plants_attributes_dict)
