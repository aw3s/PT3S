"""

---------------------------
DOCTEST
---------------------------
>>> # ---
>>> # Imports
>>> # ---
>>> import logging
>>> logger = logging.getLogger('PT3S.Plt')  
>>> import os
>>> import pandas as pd
>>> path = os.path.dirname(__file__)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> mx1File=os.path.join(path,'testdata\WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1.MX1')
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> mx.setResultsToMxsFile(NewH5Vec=True)
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...   os.remove(mx.h5FileMxsVecs)
"""

import os
import sys
import logging
logger = logging.getLogger('PT3S.Plt')  
import argparse
import unittest
import doctest

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError

import timeit

import xml.etree.ElementTree as ET
import re
import struct
import collections
import zipfile
import pandas as pd
import h5py

import subprocess

import warnings
import tables
import math

# ---
# --- PT3S Imports
# ---
from Xm import Xm
from Mx import Mx

class PltError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Plt():
    """
      
    """
    def __init__(self,xm=None,mx=None): 
        """
          
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if isinstance(xm,Xm):
                self.xm=xm
            else:
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise PltError(logStrFinal)  
            if isinstance(mx,Mx):
                self.mx=mx
            else:
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise PltError(logStrFinal)                                   
        except PltError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise PltError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def pltNetDhUs(self
                   ,timeDelteToRef=pd.to_timedelta('0 seconds')
                   ,timeDelteToT1=None
                   ,timeDelteToT2=None
                   
                   ): 
        """
          
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            firstTime=self.mx.df.index[0]
            if isinstance(timeDelteToRef,pd.Timedelta):
                timeRef=firstTime+timeDelteToRef
            else:
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise PltError(logStrFinal)  
            if isinstance(timeDelteToT1,pd.Timedelta):
                timeT1=firstTime+timeDelteToT1
            else:
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise PltError(logStrFinal)  
            if isinstance(timeDelteToT2,pd.Timedelta):
                timeT2=firstTime+timeDelteToT2
            else:
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise PltError(logStrFinal)  

            plotTimesUsed=[]
            plotTimesUsed.append(Mx.getMicrosecondsFromRefTime(refTime=firstTime,time=timeRef))
            plotTimesUsed.append(Mx.getMicrosecondsFromRefTime(refTime=firstTime,time=timeT1))
            plotTimesUsed.append(Mx.getMicrosecondsFromRefTime(refTime=firstTime,time=timeT2))

            plotTimesUsedH5Keys=['/'+str(key) for key in plotTimesUsed]

            plotTimeDfs=[]
            with pd.HDFStore(self.mx.h5FileMxsVecs) as h5Store:  
                for h5Key in plotTimesUsedH5Keys:
                    plotTimeDfs.append(h5Store[h5Key])
            
            
                                           
        except PltError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise PltError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

if __name__ == "__main__":
    """
    Run the Stuff or/and perform Unittests.
    """

    try:              
        # Logfile
        logFileName = 'PT3S.log' 
        
        loglevel = logging.INFO
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
                                      
        # Arguments      
        parser = argparse.ArgumentParser(description='Run the Stuff or/and perform Unittests.'
        ,epilog='''
        UsageExample: -v       
        '''                                 
        )

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")                  
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        suite=doctest.DocTestSuite()   
        unittest.TextTestRunner().run(suite)         

    except SystemExit:
        pass                                              
    except:
        logger.error("{0:s}{1:s}".format(logStr,'logging.exception!')) 
        logging.exception('')  
    else:
        logger.debug("{0:s}{1:s}".format(logStr,'No Exception.')) 
        sys.exit(0)
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.')) 
        sys.exit(0)
