#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##      Basic functions for logging/terminal info display/error handling      ##
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

#currently controls color printing functions ONLY
TESTING = True

########################################
# Imports for logging and colorization #
########################################

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
	traceback.print_exc()
	COLORMEQUALIFIED = False
    
##########################
# Colorization Functions #
##########################
# yeah, about the slashes... do you want invisible \n? 
# Because thats how you avoid invisible \n and concatenation errors
blueprint 			= lambda text: print(Fore.BLUE + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint 			= lambda text: print(Fore.GREEN + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint 			= lambda text: print(Fore.RED + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
# lambing while you lamb?
makered				= lambda text: Fore.RED + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen  			= lambda text: Fore.GREEN + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue  			= lambda text: Fore.BLUE + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow 			= lambda text: Fore.YELLOW + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print 	= lambda text: print(Fore.YELLOW + Style.BRIGHT + \
	' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

###########
# LOGGING #
###########
log_file = 'garden_grid_message_log'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger		   		= logging.getLogger()
logger.setLevel(logging.DEBUG)
debug_message		= lambda message: logger.debug(blueprint(message)) 
info_message		= lambda message: logger.info(greenprint(message)) 
warning_message 	= lambda message: logger.warning(yellow_bold_print(message)) 
error_message		= lambda message: logger.error(redprint(message)) 
critical_message 	= lambda message: logger.critical(yellow_bold_print(message))

###############################################
## BeautifulSoup4 
#divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] == divname)
