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
from database_stuff import Plants,add_to_db
import os
import pandas

class ScrapeWikipediaTableForData:
    def __init__(self,sections_to_grab, thing_to_get):
        self.sections_to_grab = sections_to_grab
        self.thing_to_get = thing_to_get
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
sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'
plant_data_lookup = ScrapeWikipediaTableForData(sections_to_grab,thing_to_get)
