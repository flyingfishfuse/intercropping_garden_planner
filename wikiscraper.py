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
import pandas

if __name__ == '__main__':
    from database_stuff import Plants,add_to_db
    import os
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

class ScrapeWikipediaTableForData:
    def __init__(self,url,sqlalchemy_mapping:dict, sections_tograb):
        self.dataframes  = pandas.read_html(url)
        self.attributes_dict  = {}
        self.sections_to_grab = sections_tograb
        self.dothethingjulie()

    def dothethingjulie(self):
        for dataframe in self.dataframes:
            # isolate each attribute from dataframe
            if dataframe.columns[0][0] in self.sections_to_grab:
                #iloc[x] is an entire row entry
                # access each column by using :
                # iloc[x][y] where y = individual column in that row

                for row in dataframe.iloc[range(0,len(dataframe.index))]:
                    self.attributes_dict.update(\
                        # HEY LISTEN!
                        plant_type      = row[0], # HEY! 
                        # SET THIS TO THE SECTION ITS IN!
                        # THANK YOU
                        name            = row[0],
                        scientific_name = row[1],
                        helps           = row[2],
                        helped_by       = row[3],
                        attracts_insects= row[4],
                        repels_insects  = row[5],
                        bad_for         = row[6],
                        notes           = row[7]
                    )
        self.juliedothething()
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
if __name__ == '__main__':
    plant_data_lookup = ScrapeWikipediaTableForData(thing_to_get,attributes_dict, sections_to_grab)
    print(plant_data_lookup.attributes_dict)