import warnings

import os
import sys
import logging
import pandas as pd

import tables
import re

try:              
    # Logfile
    logFileName = os.path.join(os.path.dirname(__file__),'PT3S.log')
        
    loglevel = logging.DEBUG
    logging.basicConfig(filename=logFileName
                        ,filemode='w'
                        ,level=loglevel
                        ,format="%(asctime)s ; %(name)-60s ; %(levelname)-7s ; %(message)s")    

    fileHandler = logging.FileHandler(logFileName)     
    
    # -------------------------------------- 
    logger = logging.getLogger('PT3S')      
    # -------------------------------------- 
    
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter("%(levelname)-7s ; %(message)s"))
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)

    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
    logger.debug("{:s}Logfile: {:s}".format(logStr,logFileName)) 

    #H5
    warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
    warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)
                                                                                 
except Exception as e:
    logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
    logger.error(logStrFinal)
    logger.error("{0:s}{1:s}".format(logStr,"logging.exception('') ...")) 
    logging.exception('')  

finally:
    logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))

