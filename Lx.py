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

    Maintains a H5-File with dfs.   
    1 df per Logfile.
    1 Key per Logfile.

    H5-File: 
    "Log ab ... .h5".
    Path: Path of Initialization-File.
    Existing H5-File will be deleted.

    H5-Keys are the Logfilenames praefixed by Log without extension.
    
    1 Key named "init" for Initialization-Logfile. 
    The 'init'-Key Logfile is intended to represent the 1st Logfile after App Start. 

    The 'Logfile'-Keys are intended represent all Logdata.
    Therefore the 'init'-Key Logfile can and should be also available as 'Logfile'-Key Logfile.

    Usage:
    # init with 1st Log in Zip:
    lx=Lx.AppLog(zip7File=zip7File)
    # add whole Zip:
    lx.addZip7File(zip7File)

    Attributes:    
    * delimiter
    * parseRestvalues
    * lookUpDf
        * Logfile
        * Timestart
        * Timeend
    * h5File
        * init
        * lookUpDf
        * Log...
    """
    def __init__(self,logFile=None,zip7File=None,h5File=None,delimiter='\t',parseRestvalues=False):
        """
        (re-)initialize with logFile XOR zip7File XOR h5File

        logFile: 'init'-Key Logfile
        zip7File: 1st File is considered as 'init'-Key Logfile; the whole zip7File is _not processed to H5
        h5File: 

        delimiter: CSV-Log Col-Seperator
        parseRestvalues: 
            * if False (default), read_csv(...,...,error_bad_lines=False,warn_bad_lines=True) is used
            * if True csv.DictReader with postprocessing is used and restValues are added with delimiter as seperator to last col
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        self.delimiter=delimiter
        self.parseRestvalues=parseRestvalues

        self.lookUpDf=pd.DataFrame() 

        try:     
             if logFile != None and zip7File != None and h5File != None:
                logger.debug("{0:s}{1:s}".format(logStr,'3 Files (logFile and zip7File and h5File) specified.'))             
             elif logFile != None and zip7File != None:
                logger.debug("{0:s}{1:s}".format(logStr,'2 Files (logFile and zip7File) specified.')) 
             elif logFile != None and h5File != None:
                logger.debug("{0:s}{1:s}".format(logStr,'2 Files (logFile and h5File) specified.')) 
             elif h5File != None and zip7File != None:
                logger.debug("{0:s}{1:s}".format(logStr,'2 Files (h5File and zip7File) specified.')) 
             elif  logFile != None:                 
                 self.__initlogFile(logFile)
             elif zip7File != None:
                 self.__initzip7File(zip7File)
             elif h5File != None:
                 self.__initWithH5File(h5File)
             else:                 
                 logger.debug("{0:s}{1:s}".format(logStr,'No File (logFile XOR zip7File XOR h5File) specified.')) 

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
             
    def __initlogFile(self,logFile):
        """
        (re-)initialize with logFile
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                 
             # wenn logFile nicht existiert ...
             if not os.path.exists(logFile):                                      
                logger.debug("{0:s}logFile {1:s} not existing.".format(logStr,logFile))    
             else:
                df = self.__processALogFile(logFile=logFile)    
                self.__initH5File(logFile,df)
         
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   


    def __initH5File(self,h5File,df):
        """
        creates self.h5File and writes 'init'-Key Logfile df to it
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                                              
             (h5FileHead,h5FileTail)=os.path.split(h5File)
             
             # H5-File
             h5FileTail="Log ab {0:s}.h5".format(str(df['#LogTime'].min())).replace(':',' ').replace('-',' ')           
             self.h5File=os.path.join(h5FileHead,h5FileTail)

             # wenn H5 existiert wird es geloescht
             if os.path.exists(self.h5File):                                         
                os.remove(self.h5File)
                logger.debug("{0:s}Existing H5-File {1:s} deleted.".format(logStr,h5FileTail))    

             # init-Logfile schreiben
             self.__toH5('init',df) 
             logger.debug("{0:s}'init'-Key Logfile done.".format(logStr))    

         
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def __initWithH5File(self,h5File,useRawHdfAPI=False):
        """
        self.h5File=h5File
        self.lookUpDf from H5-File
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:  
             # H5 existiert 
             if os.path.exists(h5File):
                self.h5File=h5File
                if useRawHdfAPI:
                    with pd.HDFStore(self.h5File) as h5Store:
                        self.lookUpDf=h5Store['lookUpDf']
                else:
                    self.lookUpDf=pd.read_hdf(self.h5File, key='lookUpDf')                    
             else:                                
                logger.error("{0:s}H5-File {1:s} existiert nicht.".format(logStr,h5File))                
                    
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def __initzip7File(self,zip7File):
        """
        (re-)initialize with zip7File
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                                             
                # wenn zip7File nicht existiert ...
                if not os.path.exists(zip7File):                     
                   logStrFinal="{0:s}zip7File {1:s} not existing.".format(logStr,zip7File) 
                   logger.debug(logStrFinal)    
                   raise LxError(logStrFinal)    
                else:
                   (zip7FileHead, zip7FileTail)=os.path.split(zip7File)
                
                tmpDir=os.path.dirname(zip7File)

                aDfRead=False
                with py7zr.SevenZipFile(zip7File, 'r') as zip7FileObj:                
                    allLogFiles = zip7FileObj.getnames()

                    logger.debug("{0:s}{1:s}: len(getnames()): {2:d}.".format(logStr,zip7FileTail,len(allLogFiles)))  

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
                            df = self.__processALogFile(logFile=logFile) 
                            if df is None:      
                                logger.warning("{0:s}idx: {1:d} Log: {2:s} NOT processed?! Continue with next Name in 7Zip.".format(logStr,idx,logFileTail))  
                                # nichts zu prozessieren ...
                                continue
                            else:
                                aDfRead=True
                        # ...

                        # gleich wieder loeschen
                        if os.path.exists(logFile) and logFileTBDeleted:
                            if os.path.isfile(logFile):
                                os.remove(logFile)
                                logger.debug("{0:s}idx: {1:d} Log: {2:s} wieder geloescht.".format(logStr,idx,logFileTail))         
                                
                        # wir wollen nur das 1. File lesen ...
                        if aDfRead:                           
                           break;

                for dirName in extDirLstTBDeleted:
                    if os.path.exists(dirName):
                        if os.path.isdir(dirName):
                            if not os.path.getsize(dirName):
                                os.rmdir(dirName)    
                                (dirNameHead, dirNameTail)=os.path.split(dirName)
                                logger.debug("{0:s}dirName: {1:s} existierte nicht und wurde wieder geloescht.".format(logStr,dirNameTail))     
                            
                
                self.__initH5File(zip7File,df)
         
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def addZip7File(self,zip7File):
        """
        add zip7File
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                                             
                # wenn zip7File nicht existiert ...
                if not os.path.exists(zip7File):                     
                   logStrFinal="{0:s}zip7File {1:s} not existing.".format(logStr,zip7File) 
                   logger.debug(logStrFinal)    
                   raise LxError(logStrFinal)    
                else:
                   (zip7FileHead, zip7FileTail)=os.path.split(zip7File)
                
                tmpDir=os.path.dirname(zip7File)
              
                with py7zr.SevenZipFile(zip7File, 'r') as zip7FileObj:                
                    allLogFiles = zip7FileObj.getnames()

                    logger.debug("{0:s}{1:s}: len(getnames()): {2:d}.".format(logStr,zip7FileTail,len(allLogFiles)))  

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
                            df = self.__processALogFile(logFile=logFile) 
                            if df is None:      
                                logger.warning("{0:s}idx: {1:d} Log: {2:s} NOT processed?! Continue with next Name in 7Zip.".format(logStr,idx,logFileTail))  
                                # nichts zu prozessieren ...
                                continue                        
                        # ...

                        # gleich wieder loeschen
                        if os.path.exists(logFile) and logFileTBDeleted:
                            if os.path.isfile(logFile):
                                os.remove(logFile)
                                logger.debug("{0:s}idx: {1:d} Log: {2:s} wieder geloescht.".format(logStr,idx,logFileTail))         

                        #  ...
                        (name, ext)=os.path.splitext(logFileTail)
                        key='Log'+name
                        self.__toH5(key,df,updLookUpDf=True,logFile=logFileTail)
                        # danach gleich schreiben ...
                        self.__toH5('lookUpDf',self.lookUpDf)
                                
                for dirName in extDirLstTBDeleted:
                    if os.path.exists(dirName):
                        if os.path.isdir(dirName):
                            if not os.path.getsize(dirName):
                                os.rmdir(dirName)    
                                (dirNameHead, dirNameTail)=os.path.split(dirName)
                                logger.debug("{0:s}dirName: {1:s} existierte nicht und wurde wieder geloescht.".format(logStr,dirNameTail))                                                                 
         
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def __toH5(self,key,df,useRawHdfAPI=False,updLookUpDf=False,logFile=''):
        """
        write df with key to H5-File
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:   
            
             (h5FileHead,h5FileTail)=os.path.split(self.h5File)

             if useRawHdfAPI:
                 with pd.HDFStore(self.h5File) as h5Store:                 
                    try:
                        h5Store.put(key,df)
                    except Exception as e:
                        logger.error("{0:s}Writing df with h5Key={1:s} to {2:s} FAILED!".format(logStr,key,h5FileTail))    
                        raise e
             else:
                 df.to_hdf(self.h5File, key=key)
             logger.debug("{0:s}Writing df with h5Key={1:s} to {2:s} done.".format(logStr,key,h5FileTail))    

             if updLookUpDf:
                 s=df.iloc[[0,-1]]['#LogTime']
                 FirstTime=s.iloc[0]
                 LastTime=s.iloc[-1]
                 data={ 'LogFile': [logFile]
                       ,'FirstTime' : [FirstTime]
                       ,'LastTime' : [LastTime]
                      }

                 if self.lookUpDf.empty:
                     data={ 'LogFile': [logFile]
                           ,'FirstTime' : [FirstTime]
                           ,'LastTime' : [LastTime]
                          }
                     self.lookUpDf = pd.DataFrame (data, columns = ['LogFile','FirstTime','LastTime'])
                 else:
                     data={ 'LogFile': logFile
                           ,'FirstTime' : FirstTime
                           ,'LastTime' : LastTime
                          }
                     self.lookUpDf=self.lookUpDf.append(data,ignore_index=True)                                       
                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
          
    def __processALogFile(self,logFile=None,restkey='+'):
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
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        df=None
        try: 
             with open(logFile,'r') as f: 
                pass

             (logFileHead,logFileTail)=os.path.split(logFile)

             if self.parseRestvalues:
                 
                with open(logFile,"r") as csvFile: # 1. Zeile enthaelt die Ueberschrift 
                     reader = csv.DictReader(csvFile,delimiter=self.delimiter,restkey=restkey) 
                     # If a row has more fields than fieldnames, the remaining data is put in a list and stored with the fieldname specified by restkey (which defaults to None). 
                     colNames=reader.fieldnames
                     dcts = [dct for dct in reader] # alle Zeilen lesen
                logger.debug("{0:s}{1:s} csv.DictReader processed.".format(logStr,logFileTail)) 
             
                # nur die Spaltennamen werden als row-Spalten erzeugt
                rows = [[dct[colName] for colName in colNames] for dct in dcts]
                logger.debug("{0:s}{1:s} rows processed.".format(logStr,logFileTail)) 

                # die "ueberfluessigen" Spalten an die letzte Spalte dranhaengen             
                for i, dct in enumerate(dcts):
                    pass
                    if restkey in dct:
                        restValue=dct[restkey]
                        restValueStr = self.delimiter.join(restValue)
                        newValue=rows[i][-1]+self.delimiter+restValueStr
                        logger.debug("{0:s}{1:s} restValueStr: {2:s} - Zeile {3:10d}: {4:s} - neuer Wert letzte Spalte: {5:s}.".format(logStr,logFileTail,restValueStr,i,str(rows[i]),newValue)) 
                        rows[i][-1]=rows[i][-1]+newValue
                logger.debug("{0:s}{1:s} restkey processed.".format(logStr,logFileTail)) 

                index=range(len(rows))
                df = pd.DataFrame(rows,columns=colNames,index=index)
             else:
                pass
                df=pd.read_csv(logFile,delimiter=self.delimiter,error_bad_lines=False,warn_bad_lines=False)
                
             logger.debug("{0:s}{1:s} pd.DataFrame processed.".format(logStr,logFileTail)) 

             #LogTime
             df['#LogTime']=pd.to_datetime(df['#LogTime'],unit='ms',errors='coerce') # NaT     
             
             #ProcessTime
             df['ProcessTime']=pd.to_datetime(df['ProcessTime'],unit='ms',errors='coerce') # NaT
             
             #Value
             df.Value=df.Value.str.replace(',', '.')
             df.Value=pd.to_numeric(df.Value,errors='coerce') # NaN 

             #Strings
             #df['LogLevel'] = df.LogLevel.astype('category')
             #df['SubSystem'] = df.SubSystem.astype('category')
             #df['Direction'] = df.Direction.astype('category')
             #df['ID'] = df.ID.astype('category')
             for col in ['ID','Direction','SubSystem','LogLevel','State','Remark']: #['State','Remark']:
                df[col]=df[col].astype(str)

             ##ScenTime             
             p=re.compile('(^Starting cycle for )(?P<Time>[0-9,\-,\ ,\:,\.]+)') # Starting cycle for 2020-11-13 15:20:52.000        
             f1=lambda row: p.search(row['Remark'])
             df['ScenTimeTmp']=df.apply(f1,axis=1)
             f2=lambda row: pd.to_datetime(row['ScenTimeTmp'].group('Time'),format='%Y-%m-%d %H:%M:%S.%f') if row['ScenTimeTmp'] != None else None             
             df['ScenTime']=df.apply(f2,axis=1)
             firstScenTimeLoggedWithLdsMcl=df['ScenTime'].loc[df['ScenTime'].notnull()].iloc[0]
             #lastScenTimeLoggedWithLdsMcl=df['ScenTime'].loc[df['ScenTime'].notnull()].iloc[-1]            
             df['ScenTime']=df['ScenTime'].fillna(method='ffill')
             df['ScenTime']=df['ScenTime'].fillna(value=firstScenTimeLoggedWithLdsMcl-pd.Timedelta('1000 ms'))

             df=df[['#LogTime','LogLevel','SubSystem','Direction','ProcessTime','ID','Value','ScenTime','State','Remark']]
                        
             logger.debug("{0:s}{1:s} processed.".format(logStr,logFileTail))     
                          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                    
            return df

    #def genExtDfs(self):
    #    """
    #    calculates slices and stores the result in H5

    #    slices:
    #    SubSystem:
    #    * extDfMCL
    #    * extDfOPC
    #    * extDfLDS
    #    """ 
 
    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
                
    #    try:               
    #        extDfMCL=self.getDfByFilterFct(filter_fct=lambda row: True if re.search('MCL$',row['SubSystem']) != None else False)
    #        extDfOPC=self.getDfByFilterFct(filter_fct=lambda row: True if re.search('^OPC',row['SubSystem']) != None else False)
    #        extDfLDS=self.getDfByFilterFct(filter_fct=lambda row: True if row['SubSystem']=='LDS' else False)

    #        self.__toH5('extDfMCL',extDfMCL)
    #        self.__toH5('extDfOPC',extDfOPC)
    #        self.__toH5('extDfLDS',extDfLDS)
            
    #    except Exception as e:
    #        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
    #        logger.error(logStrFinal) 
    #        raise LxError(logStrFinal)                       
    #    finally:           
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))         
            
    #def getExtDfs(self,extDf):
    #    """
    #    returns a slice previously stored by genExtDfs in H5

    #    slices:
    #    see genExtDfs
    #    """ 
 
    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
                
    #    try:                           
    #        with pd.HDFStore(self.h5File) as h5Store:                             
    #            logger.debug("{0:s}Get h5Key: {1:s} ...".format(logStr,'/'+extDf)) 
    #            df=h5Store['/'+extDf]
            
    #    except Exception as e:
    #        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
    #        logger.error(logStrFinal) 
    #        raise LxError(logStrFinal)                       
    #    finally:           
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
    #        return df

    def get(self,filter_fct=None,filterAfter=True,useRawHdfAPI=False):
        """
        returns df with filter_fct applied; filter_fct Example: lambda row: True if row['SubSystem']=='LDS MCL' else False        
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        h5KeySep='/'
        
        dfRet=None
        try:   
            dfLst=[]
            with pd.HDFStore(self.h5File) as h5Store:
                    h5Keys=sorted(h5Store.keys())                
                    h5Keys=[item for item in h5Keys if re.search('^Log', item.replace(h5KeySep,'')) != None]
                    logger.debug("{0:s}h5Keys used: {1:s}".format(logStr,str(h5Keys))) 
            if useRawHdfAPI:
                with pd.HDFStore(self.h5File) as h5Store:
                    h5Keys=sorted(h5Store.keys())                
                    h5Keys=[item for item in h5Keys if re.search('^Log', item.replace(h5KeySep,'')) != None]
                    logger.debug("{0:s}h5Keys used: {1:s}".format(logStr,str(h5Keys))) 
                    for h5Key in h5Keys:
                        logger.debug("{0:s}Get df with h5Key: {1:s} ...".format(logStr,h5Key)) 
                        df=h5Store[h5Key]
                        if not filterAfter and filter_fct != None:
                            logger.debug("{0:s}Apply Filter ...".format(logStr)) 
                            df=pd.DataFrame(df[df.apply(filter_fct,axis=1)].values,columns=df.columns)                              
                        #df['Logfile']=h5Key.replace('/','')
                        #df['Logfile']=df['Logfile'].astype(str)
                        #logger.debug("{0:s}Append h5Key: {1:s} ...".format(logStr,h5Key)) 
                        dfLst.append(df)
            else:
                    for h5Key in h5Keys:
                        logger.debug("{0:s}Get df with h5Key: {1:s} ...".format(logStr,h5Key)) 
                        df=pd.read_hdf(self.h5File, key=h5Key)
                        if not filterAfter and filter_fct != None:
                            logger.debug("{0:s}Apply Filter ...".format(logStr)) 
                            df=pd.DataFrame(df[df.apply(filter_fct,axis=1)].values,columns=df.columns)    
                        dfLst.append(df)                    
            logger.debug("{0:s}{1:s}".format(logStr,'Extraction finished. Concat ...')) 
            dfRet=pd.concat(dfLst)
            if filterAfter and filter_fct != None:
                logger.debug("{0:s}Apply Filter ...".format(logStr)) 
                dfRet=pd.DataFrame(dfRet[dfRet.apply(filter_fct,axis=1)].values,columns=dfRet.columns)   
                               
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
            return dfRet


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

