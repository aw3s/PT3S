"""
Configures PT3S Logging
"""

import os
import sys
import logging
logger = logging.getLogger('PT3S')     
import pandas as pd
import warnings
import tables

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

    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    #H5
    warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
    warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)
                                      
except SystemExit:
    pass                                              
except:
    logger.error("{0:s}{1:s}".format(logStr,'logging.exception!')) 
    logging.exception('')  
finally:
    logger.debug("{0:s}{1:s}".format(logStr,'_Done.')) 
    pass

