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



# folgende IDs werden von folgender RE _nicht erfasst:
#'IMDI.App.CALC'
# 'Objects.3S_STEUERUNG.3S_APP_LDS.In.LIFE'
# 'IMDI. ... .Linepackrate'

pID=re.compile('(?P<Prae>IMDI\.)?(?P<A>[a-z,A-Z,0-9,_]+)\.(?P<B>[a-z,A-Z,0-9,_]+)\.(?P<C1>[a-z,A-Z,0-9]+)_(?P<C2>[a-z,A-Z,0-9]+)_(?P<C3>[a-z,A-Z,0-9]+)_(?P<C4>[a-z,A-Z,0-9]+)_(?P<C5>[a-z,A-Z,0-9]+)(?P<C6>_[a-z,A-Z,0-9]+)?(?P<C7>_[a-z,A-Z,0-9]+)?\.(?P<D>[a-z,A-Z,0-9,_]+)\.(?P<E>[a-z,A-Z,0-9,_]+)(?P<F>\.[a-z,A-Z,0-9,_]+)?') # 

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
    * #delimiter
    * #readWithDictReader
    * #nRows
    * lookUpDf
        * zipName
            i.e. 20201113_151238a.7z
        * Name
            i.e. 20201113_0000004.log 
        * Timestart
        * Timeend
    * h5File
        * init
        * lookUpDf
        * Log...
    """
    def __init__(self,logFile=None,zip7File=None,zip7Files=None,h5File=None,readWithDictReader=False,nRows=None):
        """
        (re-)initialize with logFile XOR zip7File XOR h5File

        Args:
            * logFile: 'init'-Key Logfile
            * zip7File: 1st Logfile is considered as 'init'-Key Logfile; - nothing außer 'init'-Key Logfile is processed to H5
            * zip7Files: 1st Logfile in 1st zip7File is considered as 'init'-Key Logfile; the whole zip7Files are processed only to build lookUpDfZips - nothing außer 'init'-Key Logfile is processed to H5
            * h5File: H5-File to initialize from 

            * delimiter: CSV-Log Col-Seperator
            * readWithDictReader: 
                * if False (default), read_csv(...,...,error_bad_lines=False,warn_bad_lines=True) is used
                * if True csv.DictReader with postprocessing is used and restValues are added with delimiter as seperator to last col
            * nRows: read only nRows (if readWithDictReader is True, the last row is also read)
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        #self.delimiter=delimiter
        #self.readWithDictReader=readWithDictReader
        #self.nRows=nRows

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
             elif zip7Files != None:
                 self.__initzip7Files(zip7Files)
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

        Args:
        * h5File: name of logFile or zip7File; from the name the H5-Filename is derived 
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

    def __initzip7File(self,zip7File,nRows=None,readWithDictReader=False):
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
                            df = self.__processALogFile(logFile=logFile,nRows=nRows,readWithDictReader=readWithDictReader) 
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

    def addZip7File(self,zip7File,firstsAndLastsLogsOnly=False,nRows=None,readWithDictReader=False):
        """
        add zip7File

        Args:
        * zipFile: zipFile which LogFiles shall be added

        * internal Usage: 
            * firstsAndLastsLogsOnly (True dann)
            * nRows (1 dann)
            * readWithDictReader (True dann)
            d.h. es werden nur die ersten und letzten Logs pro Zip angelesen und dort auch nur die 1. und letzte Zeile und das mit DictReader
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
                    allLogFilesLen=len(allLogFiles)
                    logger.debug("{0:s}{1:s}: len(getnames()): {2:d}.".format(logStr,zip7FileTail,allLogFilesLen))  

                    extDirLstTBDeleted=[]
                    extDirLstExistingLogged=[]                    

                    for idx,logFileNameInZip in enumerate(allLogFiles):

                        if firstsAndLastsLogsOnly:
                            if idx not in [0,1,allLogFilesLen-2,allLogFilesLen-1]:
                                #logger.debug("{0:s}idx: {1:d} item: {2:s} NOT processed ...".format(logStr,idx,logFileNameInZip))   
                                continue

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
                            df = self.__processALogFile(logFile=logFile,nRows=nRows,readWithDictReader=readWithDictReader) 
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
                        self.__toH5(key,df,updLookUpDf=True,logName=logFileTail,zipName=os.path.join(os.path.relpath(zip7FileHead),zip7FileTail))
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


    def __initzip7Files(self,zip7Files):
        """
        build self.lookUpDfZips

        Attributes:
            * self.lookUpDfZips

        Args:
            * zip7Files: zip7Files which LogFiles shall be processed 
        
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                                                             
                self.__initzip7File(zip7File=zip7Files[0],nRows=1,readWithDictReader=True)
            
                for zip7File in zip7Files:
                    self.addZip7File(zip7File,firstsAndLastsLogsOnly=True,nRows=1,readWithDictReader=True)

                df=self.lookUpDf.groupby(by='zipName').agg(['min', 'max'])
                minTime=df.loc[:,('FirstTime','min')]
                maxTime=df.loc[:,('LastTime','max')]

                minFileNr=df.loc[:,('logName','min')].apply(lambda x: int(re.search('([0-9]+)_([0-9]+)(\.log)',x).group(2)))
                maxFileNr=df.loc[:,('logName','max')].apply(lambda x: int(re.search('([0-9]+)_([0-9]+)(\.log)',x).group(2)))


                s=(maxTime-minTime)/(maxFileNr-minFileNr)
                lookUpDfZips=s.to_frame().rename(columns={0:'TimespanPerLog'})
                lookUpDfZips['NumOfFiles']=maxFileNr-minFileNr
                lookUpDfZips['FirstTime']=minTime
                lookUpDfZips['LastTime']=maxTime
                lookUpDfZips['minFileNr']=minFileNr
                lookUpDfZips['maxFileNr']=maxFileNr

                lookUpDfZips=lookUpDfZips[['FirstTime','LastTime','TimespanPerLog','NumOfFiles','minFileNr','maxFileNr']]

                self.lookUpDfZips=lookUpDfZips

                
                                                             
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def __toH5(self,key,df,useRawHdfAPI=False,updLookUpDf=False,logName='',zipName=''):
        """
        write df with key to H5-File

        Args:
        * updLookUpDf: if True, self.lookUpDf is updated with 
            * zipName (the Zip of logFile)
            * logName (the name of the logFile i.e. 20201113_0000004.log)
            * FirstTime (the first logTime in df)
            * LastTime (the last logTime in df)
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
                 if self.lookUpDf.empty:
                     data={ 'zipName': [zipName]
                           ,'logName': [logName]
                           ,'FirstTime' : [FirstTime]
                           ,'LastTime' : [LastTime]
                          }
                     self.lookUpDf = pd.DataFrame (data, columns = ['zipName','logName','FirstTime','LastTime'])
                     self.lookUpDf['zipName']=self.lookUpDf['zipName'].astype(str)
                     self.lookUpDf['logName']=self.lookUpDf['logName'].astype(str)
                 else:
                     data={ 'zipName': zipName
                           ,'logName': logName
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
          
    def __processALogFile(self,logFile=None,delimiter='\t',nRows=None,readWithDictReader=False):
        """
        process logFile

        Args:
            * logFile: logFile to be processed        
            * nRows: number of logFile rows to be processed; default: None (:= all rows are processed); if readWithDictReader: last row is also processed
            * readWithDictReader: if True, csv.DictReader is used; default: None (:= pd.read_csv is used)                

        Returns:
            * df: logFile processed to df

                *  converted:
                    * #LogTime:                                      to datetime
                    * ProcessTime:                                   to datetime
                    * Value:                                         to float64        
                    * ID,Direction,SubSystem,LogLevel,State,Remark:  to str
                *  new:
                    * ScenTime                                          datetime
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        df=None
        try: 
             with open(logFile,'r') as f: 
                pass

             (logFileHead,logFileTail)=os.path.split(logFile)

             if readWithDictReader:
                restkey='+' 
                with open(logFile,"r") as csvFile: # 1. Zeile enthaelt die Ueberschrift 
                     reader = csv.DictReader(csvFile,delimiter=delimiter,restkey=restkey) 
                     logger.debug("{0:s}{1:s} csv.DictReader reader processed.".format(logStr,logFileTail)) 
             
                     # If a row has more fields than fieldnames, the remaining data is put in a list and stored with the fieldname specified by restkey. 
                     colNames=reader.fieldnames
                     
                     dcts = [dct for dct in reader] # alle Zeilen lesen  

                logger.debug("{0:s}{1:s} csv.DictReader processed.".format(logStr,logFileTail)) 
                if nRows!=None:
                    dcts=dcts[0:nRows]+[dcts[-1]]
             
                # nur die Spaltennamen werden als row-Spalten erzeugt
                rows = [[dct[colName] for colName in colNames] for dct in dcts]
                logger.debug("{0:s}{1:s} rows processed.".format(logStr,logFileTail)) 

                # die "ueberfluessigen" Spalten an die letzte Spalte dranhaengen             
                for i, dct in enumerate(dcts):                    
                    if restkey in dct:
                        restValue=dct[restkey]
                        restValueStr = delimiter.join(restValue)
                        newValue=rows[i][-1]+delimiter+restValueStr
                        logger.debug("{0:s}{1:s} restValueStr: {2:s} - Zeile {3:10d}: {4:s} - neuer Wert letzte Spalte: {5:s}.".format(logStr,logFileTail,restValueStr,i,str(rows[i]),newValue)) 
                        rows[i][-1]=rows[i][-1]+newValue
                logger.debug("{0:s}{1:s} restkey processed.".format(logStr,logFileTail)) 

                index=range(len(rows))
                df = pd.DataFrame(rows,columns=colNames,index=index)
             else:
                if nRows==None:
                    df=pd.read_csv(logFile,delimiter=delimiter,error_bad_lines=False,warn_bad_lines=False)
                else:
                    df=pd.read_csv(logFile,delimiter=delimiter,error_bad_lines=False,warn_bad_lines=False,nrows=nRows)                
                
             logger.debug("{0:s}{1:s} pd.DataFrame processed.".format(logStr,logFileTail)) 
             #logger.debug("{0:s}df: {1:s}".format(logStr,str(df))) 

             #LogTime
             df['#LogTime']=pd.to_datetime(df['#LogTime'],unit='ms',errors='coerce') # NaT     
             
             #ProcessTime
             df['ProcessTime']=pd.to_datetime(df['ProcessTime'],unit='ms',errors='coerce') # NaT
             
             #Value
             #df.Value=df.Value.str.replace(',', '.')
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
             #logger.debug("{0:s}df: {1:s}".format(logStr,str(df)))
             #logger.debug("{0:s}df['ScenTimeTmp']: {1:s}".format(logStr,str(df['ScenTimeTmp']))) 
             try:
                 f2=lambda row: pd.to_datetime(row['ScenTimeTmp'].group('Time'),format='%Y-%m-%d %H:%M:%S.%f') if row['ScenTimeTmp'] != None else None             
                 df['ScenTime']=df.apply(f2,axis=1)
                 firstScenTimeLoggedWithLdsMcl=df['ScenTime'].loc[df['ScenTime'].notnull()].iloc[0]
                 #lastScenTimeLoggedWithLdsMcl=df['ScenTime'].loc[df['ScenTime'].notnull()].iloc[-1]            
                 df['ScenTime']=df['ScenTime'].fillna(method='ffill')
                 df['ScenTime']=df['ScenTime'].fillna(value=firstScenTimeLoggedWithLdsMcl-pd.Timedelta('1000 ms'))
             except:
                 logger.debug("{0:s}{1:s}: ScenTime set to #LogTime.".format(logStr,logFileTail))
                 df['ScenTime']=df['#LogTime']         

             df=df[['#LogTime','LogLevel','SubSystem','Direction','ProcessTime','ID','Value','ScenTime','State','Remark']]
                        
             logger.debug("{0:s}{1:s} processed with nRows (None if all): {2:s}.".format(logStr,logFileTail,str(nRows)))     
                          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                    
            return df

    def get(self,timeStart=None,timeEnd=None,filter_fct=None,filterAfter=True,useRawHdfAPI=False):
        """
        returns df with filter_fct applied
        
        Args:
        timeStart: time to start (default: Logs from the Beginning)
        timeEnd: time to end (default: Logs to the End)

        filter_fct: filter to apply (default: None); Example: lambda row: True if row['SubSystem']=='LDS MCL' else False    
        filterAfter: when to filter (default: True); True: Filtering is done after concattening all Logs - faster than filter every single Log before concattening
        useRawHdfAPI: default: False; False: pd.read_hdf is used; True: h5Store[...] is used

        Returns:
        df with filter_fct applied
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        h5KeySep='/'
        
        dfRet=None
        try:   
            dfLst=[]

            dfLookUpTimes=self.lookUpDf
            if timeStart!=None:
                dfLookUpTimes=dfLookUpTimes[dfLookUpTimes['LastTime']>=timeStart] # endet nach dem Anfang oder EndeFile ist Anfang
            if timeEnd!=None:
                dfLookUpTimes=dfLookUpTimes[dfLookUpTimes['FirstTime']<=timeEnd] # beginnt vor dem Ende oder AnfangFile ist Ende
            dfLookUpTimesIdx=dfLookUpTimes.set_index('Name')
            dfLookUpTimesIdx.filter(regex='\.log$',axis=0)
            h5Keys=['Log'+re.search('([0-9,_]+)(\.log)',logFile).group(1) for logFile in dfLookUpTimesIdx.index]
            logger.debug("{0:s}h5Keys used: {1:s}".format(logStr,str(h5Keys))) 
                         
            #with pd.HDFStore(self.h5File) as h5Store:
            #        h5Keys=sorted(h5Store.keys())                
            #        h5Keys=[item for item in h5Keys if re.search('^Log', item.replace(h5KeySep,'')) != None]
            #        logger.debug("{0:s}h5Keys used: {1:s}".format(logStr,str(h5Keys))) 

            if useRawHdfAPI:
                with pd.HDFStore(self.h5File) as h5Store:                   
                    for h5Key in h5Keys:
                        logger.debug("{0:s}Get df with h5Key: {1:s} ...".format(logStr,h5Key)) 
                        df=h5Store[h5Key]
                        if not filterAfter and filter_fct != None:
                            logger.debug("{0:s}Apply Filter ...".format(logStr)) 
                            df=pd.DataFrame(df[df.apply(filter_fct,axis=1)].values,columns=df.columns)                                                     
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


    def getFromZips(self,timeStart=None,timeEnd=None,filter_fct=None,filterAfter=True):
        """
        returns df with filter_fct applied

        Description:
            * source are the zips in self.lookUpDfZips
            * self.lookUpDfZips is generated by a _previous call to self.addZip7Files
            * LogFiles are extracted from the 7Zips as needed and deleted after parsing
            * _no H5-Storage
                   
        Args:
            * timeStart: time to start (default: None: no 7Zip-Filtering by timeStart)
            * timeEnd: time to end (default: None: no 7Zip-Filtering by timeEnd)

            * filter_fct: filter to apply (default: None); Example: lambda row: True if row['SubSystem']=='LDS MCL' else False    
            * filterAfter: when to filter (default: True); True: Filtering is done after concattening all Logs - faster (but more memory is needed) than filter every single Log before concattening       

        Returns:
            * df 
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        #h5KeySep='/'
        
        dfRet=None
        try:   
            dfLst=[]


            timeStart=pd.Timestamp(timeStart)
            timeEnd=pd.Timestamp(timeEnd)

            # zips die prozessiert werden muessen 
            dfLookUpZips=self.lookUpDfZips
            if timeStart!=None:
                dfLookUpZips=dfLookUpZips[dfLookUpZips['LastTime']>=timeStart] # endet nach dem Anfang oder EndeFile ist Anfang
            if timeEnd!=None:
                dfLookUpZips=dfLookUpZips[dfLookUpZips['FirstTime']<=timeEnd] # beginnt vor dem Ende oder AnfangFile ist Ende

            for index, row in dfLookUpZips.iterrows():
                
                zip7File=index
                (zip7FileHead, zip7FileTail)=os.path.split(zip7File)
                
               
                dTime=timeStart-row['FirstTime']
                nStart = int(dTime.total_seconds()/row['TimespanPerLog'].total_seconds())
                dTime=timeEnd-timeStart
                nDelta = int(dTime.total_seconds()/row['TimespanPerLog'].total_seconds())+1
                nEnd=nStart+nDelta

                logger.debug("{0:s}zip7File: {1:s}: Start: {2:d}/{3:07d} End: {4:d}/{5:07d}".format(logStr,zip7FileTail
                                                                                                   ,nStart,nStart+row['minFileNr']
                                                                                                   ,nStart+nDelta,nStart+row['minFileNr']+nDelta)) 
            
                try:                                             
                        # wenn zip7File nicht existiert ...
                        if not os.path.exists(zip7File):                     
                           logStrFinal="{0:s}zip7File {1:s} not existing.".format(logStr,zip7File) 
                           logger.debug(logStrFinal)    
                           raise LxError(logStrFinal)    
                
                        tmpDir=os.path.dirname(zip7File)
              
                        with py7zr.SevenZipFile(zip7File, 'r') as zip7FileObj:                
                            allLogFiles = zip7FileObj.getnames()
                            allLogFilesLen=len(allLogFiles)
                            logger.debug("{0:s}{1:s}: len(getnames()): {2:d}.".format(logStr,zip7FileTail,allLogFilesLen))  

                            extDirLstTBDeleted=[]
                            extDirLstExistingLogged=[]                    

                            idxEff=0
                            for idx,logFileNameInZip in enumerate(allLogFiles):
                             
                                if idx < nStart-idxEff or idx > nEnd+idxEff: 
                                        continue

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
                                    idxEff+=1
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
                                        if not filterAfter and filter_fct != None:
                                            logger.debug("{0:s}Apply Filter ...".format(logStr)) 
                                            df=pd.DataFrame(df[df.apply(filter_fct,axis=1)].values,columns=df.columns)                
                                        dfLst.append(df)
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
         
                except Exception as e:
                    logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.error(logStrFinal) 
                    raise LxError(logStrFinal)                       

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


    def getTCsFromDf(self,df,TCsdfOPCFill=True):
        """
        returns several TC-dfs from df

        Args:
            * df: a self.get()-Result
            * TCsdfOPCFill: if True (default): fill NaNs
        
        Time curve dfs: cols:
            * Time
            * ID
            * Value

        Time curve dfs:
            * TCsdfOPC
            * TCsLDSIn
            * TCsLDSRes
            * TCsSirCalc
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
       
        try:               
            dfOPC=df[(df['SubSystem'].str.contains('^OPC')) & ~(df['Value'].isnull())]
            dfOPC=dfOPC[['ProcessTime','ID','Value']]
            #dfOPC.rename(columns={"ProcessTime": "Time"},inplace=True)
            TCsdfOPC=dfOPC.pivot(index='ProcessTime', columns='ID', values='Value')
            if TCsdfOPCFill:
                for col in TCsdfOPC.columns:    
                    TCsdfOPC[col]=TCsdfOPC[col].fillna(method='ffill')
                    TCsdfOPC[col]=TCsdfOPC[col].fillna(method='bfill')

            dfSirCalc=df[(df['SubSystem'].str.contains('^SirCalc')) & ~(df['Value'].isnull())]
            #dfSirCalc.rename(columns={"ScenTime": "Time"},inplace=True)
            TCsdfSirCalc=dfSirCalc.pivot(index='ScenTime', columns='ID', values='Value')

            dfLDS=df[(df['SubSystem'].str.contains('^LDS')) & ~(df['Value'].isnull())]

            dfLDSRes=dfLDS[(dfLDS['Direction'].str.contains('^->'))]
            dfLDSRes=dfLDSRes[['ScenTime','ID','Value']]
            #dfLDSRes.rename(columns={"ScenTime": "Time"},inplace=True)
            TCsdfLDSRes=dfLDSRes.pivot_table(index='ScenTime', columns='ID', values='Value')

            dfLDSIn=dfLDS[(dfLDS['Direction'].str.contains('^<-'))]
            dfLDSIn=dfLDSIn[['ScenTime','ID','Value']]
            #dfLDSIn.rename(columns={"ScenTime": "Time"},inplace=True)
            TCsdfLDSIn=dfLDSIn.pivot_table(index='ScenTime', columns='ID', values='Value')
                                           
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)                       
        finally:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
            return TCsdfOPC,TCsdfLDSIn,TCsdfLDSRes,TCsdfSirCalc


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

