"""

"""

import os
import sys
import logging
logger = logging.getLogger('PT3S')     


try:              
    # Logfile
    logFileName = 'PT3S.log' 
        
    loglevel = logging.DEBUG
    logging.basicConfig(filename=logFileName
                        ,filemode='w'
                        ,level=loglevel
                        ,format="%(asctime)s ; %(name)-60s ; %(levelname)-7s ; %(message)s")    

    fileHandler = logging.FileHandler(logFileName)        
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter("%(levelname)-7s ; %(message)s"))
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
                                      
except SystemExit:
    pass                                              
except:
    logger.error("{0:s}{1:s}".format(logStr,'logging.exception!')) 
    logging.exception('')  
else:
    logger.debug("{0:s}{1:s}".format(logStr,'No Exception.')) 
    pass
finally:
    logger.debug("{0:s}{1:s}".format(logStr,'_Done.')) 
    pass

