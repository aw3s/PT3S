"""
SIR 3S Logfile Utilities (short: Lx)
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
import h5py

import subprocess

import csv

class LxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LxSirOPC():
    """
    SirOPC Logfile Set
    """
    def __init__(self,logFile=None):
        """
        (re-)initialize the set with logFile. 
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
             with open(logFile,'r') as f: 
                pass
             self.logFile=logFile 
             restkey='+'
             delimiter='\t'

             with open(logFile,"r") as csvFile: # 1. Zeile enthaelt die Ueberschrift 
                reader = csv.DictReader(csvFile,delimiter=delimiter,restkey=restkey) # erf. wenn eine Spalte selbst delimiter enthalten kann
                colNames=reader.fieldnames
                dcts = [dct for dct in reader] # alle Zeilen lesen
             
             rows = [[dct[colName] for colName in colNames] for dct in dcts]

             for i, dct in enumerate(dcts):
                if restkey in dct:
                    restValue=dct[restkey]
                    restValueStr = delimiter.join(restValue)
                    rows[i][-1]=rows[i][-1]+delimiter+restValueStr

             index=range(len(rows))
             self.pdf = pd.DataFrame(rows,columns=colNames,index=index)

             logger.debug("{0:s}{1:s}: head(10): {2!s}.".format(logStr,logFile,self.pdf.head(10)))   
             logger.debug("{0:s}{1:s}: describe(): {2!s}.".format(logStr,logFile,self.pdf.describe()))         

             self.__convertColumnData()
                          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __convertColumnData(self):
        """
        converts:
        #LogTime to datetime
        ProcessTime to datetime
        Value to float64
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
             #LogTime
             self.pdf['#LogTime']=pd.to_datetime(self.pdf['#LogTime'],unit='ms',errors='coerce') # NaT
             self.pdf=self.pdf.dropna()
             #ProcessTime
             self.pdf['ProcessTime']=pd.to_datetime(self.pdf['ProcessTime'],errors='coerce') # NaT
             #Value
             self.pdf.Value=self.pdf.Value.str.replace(',', '.')
             self.pdf.Value=pd.to_numeric(self.pdf.Value,errors='coerce') # NaN 
                          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def getProcessDataToSirCalc(self):
        """
        returns df containing only the ProcessData To SirCalc-Cmds and the following additional Columns:
        TableName;ProcessDay;ProcessTime;Value
        LogDay;LogTime
        ProcessTime is not additional but different from the original ProcessTime (which is stored in Column ProcessTimeOrig)
        the df is sorted by TableName,ProcessDay,ProcessTime
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        df=None
        try: 
             df=self.pdf[self.pdf['ID'].str.contains('^TABL')]
             df=df.sort_values(by=['ID','ProcessTime','#LogTime'])
             df['TableName']=df['ID'].replace('(TABL~)(\S+)~~~SWVT',r'\2',regex=True)#,inplace=True)
             df['LogDay'], df['LogTime'] = df['#LogTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]).str.split(' ',1).str
             df = df.rename(columns={'ProcessTime':'ProcessTimeOrig'})
             df['ProcessDay'], df['ProcessTime'] = df['ProcessTimeOrig'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]).str.split(' ',1).str        
             df['TimeNr'] = df.groupby('TableName')['ProcessTimeOrig'].rank(ascending=True,method='dense').astype(int)          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
        finally:
            return df

if __name__ == "__main__":
    """
    Run Lx-Stuff or/and perform Lx-Unittests.
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
        parser = argparse.ArgumentParser(description='Run Lx-Stuff or/and perform Lx-Unittests.'
        ,epilog='''
        UsageExample#1: (without parameter): -v --x ./testdata/20171103__000001.log   
        '''                                 
        )
        parser.add_argument('--x','--logFile',type=str, help='.log File (default: ./testdata/20171103__000001.log)',default='./testdata/20171103__000001.log')  

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")                  
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        lx=LxSirOPC(args.x)

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

