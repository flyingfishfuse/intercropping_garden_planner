import pandas

from database_stuff import Plants,add_to_db
import os
import pandas
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
    
##########################
# Colorization Functions #
##########################
# yeah, about the slashes... do you want invisible \n? 
# Because thats how you avoid invisible \n and concatenation errors
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
# lambing while you lamb?
makered    = lambda text: Fore.RED + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen  = lambda text: Fore.GREEN + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue  = lambda text: Fore.BLUE + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow = lambda text: Fore.YELLOW + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print     = lambda text: print(Fore.YELLOW + Style.BRIGHT + \
    ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

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

                for row in dataframe.iloc[0,len(dataframe.index)]:
                    self.attributes_dict.update(\
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

plant_data_lookup = ScrapeWikipediaTableForData(thing_to_get,attributes_dict, sections_to_grab)
print(plant_data_lookup.attributes_dict)