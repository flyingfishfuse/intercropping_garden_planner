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


def error_printer(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    error_message( message + ''.join(tb.format_exception_only()))
    debug_message(str(exc_tb.tb_lineno))
    debug_message(str(exc_tb.tb_frame))
    debug_message(str(exc_tb.tb_lasti))
    #debug_message(str(tb.msg))

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
log_file = 'garden_grid_message_log'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger                   = logging.getLogger()
logger.setLevel(logging.DEBUG)
debug_message        = lambda message: logger.debug(blueprint(message)) 
info_message        = lambda message: logger.info(greenprint(message)) 
warning_message     = lambda message: logger.warning(yellow_bold_print(message)) 
error_message        = lambda message: logger.error(redprint(message)) 
critical_message     = lambda message: logger.critical(yellow_bold_print(message))

###############################################
## BeautifulSoup4 
#divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] == divname)
