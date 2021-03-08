# Maximum and default grid size
MAX_N, DEFAULT_N = 26, 10
# The "default" colour for an unfilled grid cell
UNFILLED = '#fff'

# The colour palette
colours = (UNFILLED, 'red', 'green', 'blue', 'cyan', 'orange', 'yellow',
               'magenta', 'brown', 'black')
ncolours = len(colours)

def svg_preamble():
    line1 = '<?xml version="1.0" encoding="utf-8"?>\n'
    line2 = '<svg xmlns="http://www.w3.org/2000/svg"\n      xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >'.format(SIZE, SIZE)
    block1 = """
        <defs>
        <style type="text/css"><![CDATA[

        line {
            stroke-width: 1px;
            stroke: #888;
        }

        ]]></style>
        </defs>
        """         
    data_required = ''' {}{}{}'''.format(line1,line2,block1)
    return data_required

##########################################
#Relationships from online tables
##########################################
class IntercroppingRelationships:
    """
    Contains the data from the wikipedia page on intercropping
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