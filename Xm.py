"""

"""

import os
import sys
import logging
logger = logging.getLogger(__name__)     
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
import numpy as np

class XmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Xm():
    """
   
    """
    def __init__(self,XmlFile=None ):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if type(XmlFile) == str:
                self.xmlFile=XmlFile  
                with open(self.xmlFile,'r') as f: 
                    pass
                
                logger.debug("{0:s}xmlFile: {1:s}.".format(logStr,self.xmlFile))     
                tree = ET.parse(self.xmlFile) # ElementTree
                root = tree.getroot()  # Element
                pm = {c:p for p in root.iter() for c in p}   # parentMap
                tableNames=[]
                oldTableName=None
                for element in root.iter():
                    p = None
                    if element in pm:
                        p = pm[element]
                    if p != root:
                        continue
                    actTableName=element.tag
                    if actTableName != oldTableName:
                        tableNames.append(actTableName)
                        oldTableName=actTableName                
                self.dataFrames={}
                for tableName in tableNames:
                    all_records = []
                    for elementRow in root.iter(tag=tableName):
                        record = {}
                        for elementCol in elementRow:
                            record[elementCol.tag] = elementCol.text
                        all_records.append(record)
                    self.dataFrames[tableName]=pd.DataFrame(all_records) 
                self.__convertAndFix()
                
        except FileNotFoundError as e:
            logStrFinal="{0:s}xmlFile: {1!s}: FileNotFoundError.".format(logStr,self.xmlFile)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)
        except OSError as e:
            logStrFinal="{0:s}xmlFile: {1!s}: OSError.".format(logStr,self.xmlFile)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}xmlFile: {1!s}: TypeError.".format(logStr,self.xmlFile)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                            
        except:
            logStrFinal="{0:s}mx1File: {1!s}: Error.".format(logStr,self.xmlFile)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     


    def __convertAndFix(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            self.dataFrames['SWVT_ROWT'].ZEIT=self.dataFrames['SWVT_ROWT'].ZEIT.str.replace(',', '.')
            self.dataFrames['SWVT_ROWT'].W=self.dataFrames['SWVT_ROWT'].W.str.replace(',', '.')

            self.dataFrames['LFKT_ROWT'].ZEIT=self.dataFrames['LFKT_ROWT'].ZEIT.str.replace(',', '.')
            self.dataFrames['LFKT_ROWT'].LF=self.dataFrames['LFKT_ROWT'].LF.str.replace(',', '.')

            self.dataFrames['SWVT_ROWT']=self.dataFrames['SWVT_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
            self.dataFrames['LFKT_ROWT']=self.dataFrames['LFKT_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
                      
        except:
            logStrFinal="{0:s}mx1File: {1!s}: Error.".format(logStr,self.xmlFile)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

if __name__ == "__main__":
    """
    Run Xm-Stuff or/and perform Xm-Unittests.
    """

    try:              
        # Logfile
        head,tail = os.path.split(__file__)
        file,ext = os.path.splitext(tail)
        logFileName = os.path.normpath(os.path.join(head,os.path.normpath('./testresults'))) 
        logFileName = os.path.join(logFileName,file + '.log') 
        
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
        parser = argparse.ArgumentParser(description='Run Xm-Stuff or/and perform Xm-Unittests.'
        ,epilog='''
        UsageExample#1: -v --x ./testdata/FW.XML       
        '''                                 
        )
        parser.add_argument('--x','--XmlFile',type=str, help='.xml File (default: ./testdata/FW.XML)',default='./testdata/FW.XML')  

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")                  
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        xm = Xm(XmlFile=args.x)
        pass

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

