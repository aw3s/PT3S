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
import py7zr
import pandas as pd
import h5py

import subprocess

import csv

class LxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class AppLog():
    """
    SIR 3S App Log (SQC Log)
    """
    def __init__(self,logFile=None):
        """
        (re-)initialize with logFile 
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:            
             self.df = self.__processALogFile(logFile=logFile)     
             logger.debug("{0:s}{1:s} initialized.".format(logStr,logFile))     
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
         
    def addALogFile(self,logFile=None):
        """
        add logFile

        Args:
            logFile: logFile to be added
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:            
             df = self.__processALogFile(logFile=logFile) 
             if df is None:      
                 logger.info("{0:s}LogFile {1:s} not added.".format(logStr,logFile))       
             else:
                 self.df=pd.concat([self.df,df])      
                 logger.debug("{0:s}LogFile {1:s} added.".format(logStr,logFile)) 
                   
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   


    def addAZip7File(self,zip7File=None,tmpDir=None):
        """
        add zip7File (add all logFiles from zip7File)

        Args:
            zip7File: zip7File which logFiles to be added
            tmpDir: 
                dir in which the logFiles are temporarily extracted
                default: os.path.dirname(zipFile)
                Verz. und Dateien die nicht existierten werden wieder geloescht
                Verz. die existierten werden benutzt und am Ende nicht geloescht
                Dateien die existierten werden ueberschrieben und am Ende nicht geloescht
        """ 

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
          
            # Zip7 existence ...                                     
            with py7zr.SevenZipFile(zip7File, 'r') as zip7FileObj:
                pass
                
            if tmpDir == None:                
                tmpDir=os.path.dirname(zip7File)

            with py7zr.SevenZipFile(zip7File, 'r') as zip7FileObj:                
                allLogFiles = zip7FileObj.getnames()

                logger.debug("{0:s}Zip: {1:s} NumOf7Zip's getnames(): {2:d} ...".format(logStr,zip7File,len(allLogFiles)))  

                extDirLstTBDeleted=[]
                extDirLstExistingLogged=[]

                for idx,logFileNameInZip in enumerate(allLogFiles):

                    logger.debug("{0:s}idx: {1:d} item: {2:s} ...".format(logStr,idx,logFileNameInZip))   

                    # die Datei die 7Zip bei extract erzeugen wird
                    logFile=os.path.join(tmpDir,logFileNameInZip)
                    (logFileHead, logFileTail)=os.path.split(logFile)

                    # evtl. bezeichnet logFileNameInZip keine Datei sondern ein Verzeichnis
                    (name, ext)=os.path.splitext(logFileNameInZip)
                    if ext == '':
                        # Verzeichnis!                        
                        extDir=os.path.join(tmpDir,logFileNameInZip)                       
                        (extDirHead, extDirTail)=os.path.split(extDir)
                        if os.path.exists(extDir) and extDir not in extDirLstExistingLogged:
                            logger.debug("{0:s}idx: {1:d} extDir: {2:s} existiert bereits.".format(logStr,idx,extDirTail))  
                            extDirLstExistingLogged.append(extDir)
                        elif not os.path.exists(extDir):
                            logger.debug("{0:s}idx: {1:d} extDir: {2:s} existiert noch nicht.".format(logStr,idx,extDirTail))                      
                            extDirLstTBDeleted.append(extDir)
                        # kein Logfile zu prozessieren ...
                        continue

                    # logFileNameInZip bezeichnet eine Datei       
                    if os.path.exists(logFile):
                        isFile = os.path.isfile(logFile)
                        if isFile:
                            logger.debug("{0:s}idx: {1:d} Log: {2:s} existiert bereits. Wird durch Extrakt ueberschrieben werden.".format(logStr,idx,logFileTail))  
                            logFileTBDeleted=False
                        else:
                            logFileTBDeleted=False
                    else:
                        logger.debug("{0:s}idx: {1:d} Log: {2:s} existiert nicht. Wird extrahiert, dann prozessiert und dann wieder geloescht.".format(logStr,idx,logFileTail))                      
                        logFileTBDeleted=True
                  
                    # extrahieren 
                    zip7FileObj.extract(path=tmpDir,targets=logFileNameInZip)
                    
                    if os.path.exists(logFile):
                        pass                       
                    else:
                        logger.warning("{0:s}idx: {1:d} Log: {2:s} NOT extracted?! Continue with next Name in 7Zip.".format(logStr,idx,logFileTail))  
                        # nichts zu prozessieren ...
                        continue

                    # ...
                    if os.path.isfile(logFile):                        
                        self.addALogFile(logFile=logFile)
                    # ...

                    # gleich wieder loeschen
                    if os.path.exists(logFile) and logFileTBDeleted:
                        if os.path.isfile(logFile):
                            os.remove(logFile)
                            logger.debug("{0:s}idx: {1:d} Log: {2:s} wieder geloescht.".format(logStr,idx,logFileTail))                                

            for dirName in extDirLstTBDeleted:
                if os.path.exists(dirName):
                    if os.path.isdir(dirName):
                        if not os.path.getsize(dirName):
                            os.rmdir(dirName)    
                            (dirNameHead, dirNameTail)=os.path.split(dirName)
                            logger.debug("{0:s}dirName: {1:s} existierte nicht und wurde wieder geloescht.".format(logStr,dirNameTail))      
                                                                                                
        except LxError:
            raise
        except Exception as e:
            logStrFinal="{:s}zip7File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,zip7File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                                  
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                  


    def __processALogFile(self,logFile=None,delimiter='\t',restkey='+'):
        """
        process logFile

        Args:
            logFile: logFile to be processed
        Returns:
            df: logFile processed to df

                *  converted:
                    * #LogTime      to datetime
                    * ProcessTime   to datetime
                    * Value         to float64

                *  new:
                    * ScenTime      ProcessTime der jeweils vorangegangenen LogZeile mit SubSystem=='LDS MCL'; Anfang: 1. LogZeile mit SubSystem=='LDS MCL' - 1000 ms
                    * Logfile
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        df=None
        try: 
             with open(logFile,'r') as f: 
                pass

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
             df = pd.DataFrame(rows,columns=colNames,index=index)

             #LogTime
             df['#LogTime']=pd.to_datetime(df['#LogTime'],unit='ms',errors='coerce') # NaT     
             
             #ProcessTime
             df['ProcessTime']=pd.to_datetime(df['ProcessTime'],unit='ms',errors='coerce') # NaT
             
             #Value
             df.Value=df.Value.str.replace(',', '.')
             df.Value=pd.to_numeric(df.Value,errors='coerce') # NaN 

             #ScenTime
             df['ScenTime']=df.apply(lambda row: row['ProcessTime'] if row['SubSystem']=='LDS MCL' else None,axis=1)
             df['ScenTime']=df['ScenTime'].fillna(method='ffill')
             firstScenTimeLoggedWithLdsMcl=df['ScenTime'].loc[~df['ScenTime'].isnull()].iloc[0]
             df['ScenTime']=df['ScenTime'].fillna(value=firstScenTimeLoggedWithLdsMcl-pd.Timedelta('1000 ms'))

             #Logfile
             df['Logfile']=logFile

             logger.debug("{0:s}{1:s} processed.".format(logStr,logFile))     
                          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        finally:            
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
            return df


    def ToH5(self,h5File=None):
        """
        write h5File

        Args:
            h5File: h5File to be written; existing h5File will be deleted
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                         
             if h5File==None:
                 h5File="Log von {0:s} bis {1:s}.h5".format(str(self.df['ScenTime'].min())
                            ,str(self.df['ScenTime'].max())
                            ).replace(':',' ').replace('-',' ')

             if os.path.exists(h5File):                        
                logger.debug("{0:s}Delete {1:s} ...".format(logStr,h5File))     
                os.remove(h5File)

             with pd.HDFStore(h5File) as h5Store:                 
                try:
                    h5Store.put('df',self.df)
                except Exception as e:
                    logger.error("{0:s}: Writing DataFrame df with h5Key=df to {1:s} FAILED!".format(logStr,h5File))    
                    raise e
             logger.debug("{0:s}: Writing DataFrame df with h5Key=df to {1:s} done.".format(logStr,h5File))    
                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def FromH5(self,h5File=None):
        """
        read h5File

        Args:
            h5File: h5File to be read; existing df will be replaced 
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                         
             if h5File==None:
                 h5File="Log von {0:s} bis {1:s}.h5".format(str(self.df['ScenTime'].min())
                            ,str(self.df['ScenTime'].max())
                            ).replace(':',' ').replace('-',' ')

             if not os.path.exists(h5File):                        
                logger.warning("{0:s}File {1:s} not existing.".format(logStr,h5File))     
             else:
                 with pd.HDFStore(h5File) as h5Store:   
                    try:                                        
                        df=h5Store['df']                                                    
                        self.df=df
                    except Exception as e:
                        logger.error("{0:s}: Reading DataFrame df with h5Key=df from {1:s} FAILED!".format(logStr,h5File))    
                        raise e
                 logger.debug("{0:s}: Reading DataFrame df with h5Key=df from {1:s} done.".format(logStr,h5File))    
                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    
    #def __convertColumnData(self):
    #    """
    #    converts:
    #    #LogTime to datetime
    #    ProcessTime to datetime
    #    Value to float64
    #    """ 
 
    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    #    try: 
    #         #LogTime
    #         self.df['#LogTime']=pd.to_datetime(self.df['#LogTime'],unit='ms',errors='coerce') # NaT
    #         #self.pdf=self.pdf.dropna()
    #         #ProcessTime
    #         self.df['ProcessTime']=pd.to_datetime(self.df['ProcessTime'],unit='ms',errors='coerce') # NaT
    #         #Value
    #         self.df.Value=self.df.Value.str.replace(',', '.')
    #         self.df.Value=pd.to_numeric(self.df.Value,errors='coerce') # NaN 
                          
    #    except LxError:
    #        raise            
    #    except:
    #        logStrFinal="{0:s}Error.".format(logStr)
    #        logger.error(logStrFinal) 
    #        raise LxError(logStrFinal)               
    #    else:
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    #def getProcessDataToSirCalc(self):
    #    """
    #    returns df containing only the ProcessData To SirCalc-Cmds and the following additional Columns:
    #    TableName;ProcessDay;ProcessTime;Value
    #    LogDay;LogTime
    #    ProcessTime is not additional but different from the original ProcessTime (which is stored in Column ProcessTimeOrig)
    #    the df is sorted by TableName,ProcessDay,ProcessTime
    #    """ 
 
    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    #    df=None
    #    try: 
    #         df=self.df[self.df['ID'].str.contains('^TABL')]
    #         df=df.sort_values(by=['ID','ProcessTime','#LogTime'])
    #         df['TableName']=df['ID'].replace('(TABL~)(\S+)~~~SWVT',r'\2',regex=True)#,inplace=True)
    #         df['LogDay'], df['LogTime'] = df['#LogTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]).str.split(' ',1).str
    #         df = df.rename(columns={'ProcessTime':'ProcessTimeOrig'})
    #         df['ProcessDay'], df['ProcessTime'] = df['ProcessTimeOrig'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]).str.split(' ',1).str        
    #         df['TimeNr'] = df.groupby('TableName')['ProcessTimeOrig'].rank(ascending=True,method='dense').astype(int)          
    #    except LxError:
    #        raise            
    #    except:
    #        logStrFinal="{0:s}Error.".format(logStr)
    #        logger.error(logStrFinal) 
    #        raise LxError(logStrFinal)               
    #    else:
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
    #    finally:
    #        return df

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

        lx=AppLog(args.x)

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

