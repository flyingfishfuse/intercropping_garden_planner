#!/usr/bin/python3
# -*- coding: utf-8 -*-
#currently controls color printing functions ONLY
TESTING = True

########################################
# Imports for logging and colorization #
########################################
import sys
import logging
import traceback

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
LOGLEVELS = [1,2,3,'DEV_IS_DUMB']

log_file  = 'garden_grid_message_log'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger    = logging.getLogger()

def set_logger_level(matrice_of_pain):
    if LOGLEVEL in LOGLEVELS:
        if LOGLEVEL == 'DEV_IS_DUMB'
            logger.setLevel(logging.DEBUG)
            debug_message        = lambda message: logger.debug(blueprint(message)) 
            info_message         = lambda message: logger.info(greenprint(message))   

warning_message      = lambda message: logger.warning(yellow_bold_print(message)) 
error_message        = lambda message: logger.error(redprint(message)) 
critical_message     = lambda message: logger.critical(yellow_bold_print(message))

def error_printer(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    error_message( message + ''.join(tb.format_exception_only()))
    traceback.format_list(traceback.extract_tb(tb)[-1:])[-1]
    debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    #debug_message(str(exc_tb.tb_frame))
    #debug_message(str(exc_tb.tb_lasti))
    #debug_message(str(tb.msg))

###############################################
## BeautifulSoup4 
#divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] == divname)

################################################]
## SQLALCHEMY
#################################################

def check_if_plants_exist_bool(plant_name):
    exists = database.session.query(Plants.id).filter_by(name=plant_name).first() is not None
    if exists:
        info_message()
        return True
    else:
        return False
        #hwhat the he-hockey stick hockey stick am I doing!?!?!?


def table_exists(engine,name):
    try:
        from sqlalchemy import inspect
        blarf = inspect(engine).dialect.has_table(engine.connect(),name)
        print('[+] Database Table {} EXISTS'.format(name, blarf))
        #return blarf
    except Exception:
        error_printer("[-] TABLE {} does NOT EXIST!".format(name))

