import os
import pandas
from std_imports import greenprint,redprint,blueprint

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
                print(self.plants_attributes_dict)

tables_of_plant_data_as_dict = ScrapeWikipediaTableForData(thing_to_get,plants_attributes_dict) 