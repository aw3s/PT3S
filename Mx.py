"""
SIR 3S MX-Interface (short: MX):
---------------------------
MX is a file based, channel-oriented interface for SIR 3S' calculation results.
Module Mx contains stuff to utilize SIR 3S' MX calculation results in pure Python.  
SIR 3S MX calculation results:
---------------------------
Binary .MXS-Files contain the SIR 3S calculations results. 
A Model calculation run creates at least one .MXS-File (Result-File).
There is one .MX1-File (an XML-File) for each SIR 3S Model calculation run.    
This .MX1-File defines in XML a sequence of MX-Channels. 
And - as a result - the Byte-Layout of a single MX3-Record in .MXS.
A MX3-Record contains calculation results for one Timestamp.
A .MXS-File contains at least one MX3-Record.
---------------------------
A MX-Channel can be 
a single Value or a
Vector: Sequence of calculation results of the same AType
    of all Objects of a certain OType or (called Vectorchannels)
    of all interior Points for all Pipes (called Pipevectorchannels)
    and Vectors with ATTRTYPE in: {'SVEC', 'PVECMIN_INST', 'PVECMAX_INST'}.
For Vectorchannels and Pipevectorchannels the sequence of Objects is defined in the .MX2-File. 
For Pipevectorchannels the Number of interior Points per Pipe is defined in the .MX2-File. 
---------------------------
DOCTEST
---------------------------
>>> # ---
>>> # Imports
>>> # ---
>>> import logging
>>> logger = logging.getLogger('PT3S.Mx')  
>>> import os
>>> import zipfile
>>> import pandas
>>> # ---
>>> # Init
>>> # ---
>>> mx1File=r'testdata\WDOneLPipe\B1\V0\BZ1\M-1-0-1.MX1'
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> isinstance(mx.mx1Df,pandas.core.frame.DataFrame) # MX1-Content
True
>>> isinstance(mx.df,type(None)) # MXS-Content
True
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...    os.remove(mx.h5FileMxsVecs)
>>> # ---
>>> # 1st Read MXS
>>> # ---
>>> logger.debug("{0:s}: 1st Read MXS".format('DOCTEST')) 
>>> mx.setResultsToMxsFile() # looks for M-1-0-1.MXS in same Dir 
>>> isinstance(mx.df,pandas.core.frame.DataFrame) # MXS-Content
True
>>> rowsDf,colsDf = mx.df.shape
>>> (firstTime,lastTime,rows)=mx._checkMxsVecsFile()
>>> rowsDf==rows
True
>>> mx.df.index[0]==firstTime
True
>>> # ---
>>> # Write H5
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...      os.remove(mx.h5File)
>>> mx.ToH5() # M-1-0-1.h5 in same Dir 
>>> os.path.exists(mx.h5File)
True
>>> # ---
>>> # Init with H5
>>> # ---
>>> mx=Mx(mx1File=mx1File) # looks for M-1-0-1.h5 in same Dir 
>>> # and reads the .h5 if newer than .MX1 and newer than an existing .MXS 
>>> isinstance(mx.mx1Df,pandas.core.frame.DataFrame) # MX1-Content
True
>>> isinstance(mx.df,pandas.core.frame.DataFrame) # MXS-Content
True
>>> # ---
>>> # 1st Read MXS Zip
>>> # ---
>>> # create the Zip first
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
>>> logger.debug("{0:s}: 1st Read MXS Zip".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile() # looks for M-1-0-1.ZIP in same Dir
>>> isinstance(mx.df,pandas.core.frame.DataFrame) # MXS-Content
True
>>> rowsMxs,colsMxs = mx.df.shape
>>> mx.df.index.is_unique # all setResultsTo... will ensure this uniqueness under all circumstances
True
>>> # uniqueness under all circumstances: also when add=True (setResultsTo... shall add the MXS-Content) is used
>>> # ---
>>> # 1st Add same MXS (for testing ensuring uniqueness) 
>>> # ---
>>> oldShape=mx.df.shape
>>> logger.debug("{0:s}: 1st Add same MXS (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # 1st Add same Zip (for testing ensuring uniqueness) 
>>> # ---
>>> logger.debug("{0:s}: 1st Add same Zip (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile(add=True) # looks for M-1-0-1.ZIP in same Dir 
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # 1st Read MXS Zip with overlapping Timestamps (for testing ensuring uniqueness) 
>>> # ---
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...      myzip.write(mx.mxsFile)  
...      myzip.write(mx.mxsFile,arcname=mx.mxsFile+'.2')  
>>> logger.debug("{0:s}: 1st Read MXS Zip with overlapping Timestamps (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile() # looks for M-1-0-1.ZIP in same Dir 
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # shift to younger Timestamps (for testing purposes) 
>>> # ---
>>> lastTimestamp=mx.df.index[-1]
>>> firstTimestamp=mx.df.index[0]
>>> timeSpan=lastTimestamp-firstTimestamp
>>> if len(mx.df.index)>1:
...      timeStep=mx.df.index[-1]-mx.df.index[-2]
... else:
...      timeStep=pd.to_timedelta('1 second')
>>> mx.df.index=mx.df.index-(timeSpan+timeStep)
>>> # ---
>>> # 1st Read MXS (with the original Timestamps)
>>> # ---
>>> logger.debug("{0:s}: 1st Read MXS (with the original Timestamps)".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
>>> rowsNew,colsNew=mx.df.shape
>>> rowsOld,colsOld=oldShape
>>> rowsNew==2*rowsOld
True
>>> colsNew==colsOld
True
>>> # ---
>>> # shift to older Timestamps (for testing purposes) 
>>> # ---
>>> lastTimestamp=mx.df.index[-1]
>>> firstTimestamp=mx.df.index[0]
>>> timeSpan=lastTimestamp-firstTimestamp
>>> if len(mx.df.index)>1:
...      timeStep=mx.df.index[-1]-mx.df.index[-2]
... else:
...      timeStep=pd.to_timedelta('1 second')
>>> mx.df.index=mx.df.index+(timeSpan+timeStep)
>>> # ---
>>> # 2nd Read MXS (with the original Timestamps)
>>> # ---
>>> logger.debug("{0:s}: 2nd Read MXS (with the original Timestamps)".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
>>> rowsNew,colsNew=mx.df.shape
>>> rowsNew==3*rowsOld
True
>>> colsNew==colsOld
True
>>> # ---
>>> # Write Dump
>>> # ---
>>> mx.dumpInMxsFormat() # dumps to .MXS.dump-File in same Dir
>>> # ---
>>> # Read Dump
>>> # ---
>>> logger.debug("{0:s}: Read Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(mxsFile=mxsDumpFile)
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
...     myzip.write(mxsDumpFile)  
>>> # ---
>>> # Read Zip with Orig and Dump
>>> # ---
>>> logger.debug("{0:s}: Read Zip with Orig and Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile()
>>> rowsZip,colsZip = mx.df.shape
>>> rowsZip==rowsOld
True
>>> # ---
>>> # Without MX1, MXS
>>> # ---
>>> os.rename(mx.mx1File,mx.mx1File+'.blind')
>>> os.rename(mx.mxsFile,mx.mxsFile+'.blind')
>>> mx=Mx(mx1File=mx1File)  
>>> os.rename(mx.mx1File+'.blind',mx.mx1File)
>>> os.rename(mx.mxsFile+'.blind',mx.mxsFile)
>>> # ---
>>> mx.mx1Df['Sir3sID'][mx.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].index[0]   
0
>>> mx.mx1Df['unpackIdx'][mx.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].iloc[0]
0
>>> mx.df.shape
(4, 41)
>>> isinstance(mx.df.index[0],pandas.tslib.Timestamp)
True
>>> str(mx.df.index[0])
'2018-03-03 00:00:00+00:00'
>>> ts=mx.df['KNOT~I~~5642914844465475844~QM']
>>> isinstance(ts,pandas.core.series.Series)
True
>>> "{:06.2f}".format(round(ts.iloc[0],2))
'176.71'
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...     os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...     os.remove(mx.mxsZipFile)
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...    os.remove(mx.h5FileMxsVecs)
"""

import os
import sys
import logging
logger = logging.getLogger('PT3S.Mx')  
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

def getMicrosecondsFromRefTime(refTime=None,time=None):
    """
    returns microseconds since refTime
    """
    pass
    try:
        timeH5=time-refTime
        h5Key=int(math.floor(timeH5.total_seconds())*1000+timeH5.microseconds)
    except:
        pass
    finally:
        return h5Key

class MxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """
    Class Mx holds the following Dataframes:
    the .MX1-File Definition    self.mx1Df  
    the .MX2-File Definition    self.mx2Df  
    the .MXS-File Data (if any) self.df (Non Vectorchannels Only)
    ---
    the .MXS-File Data: calculations results 
    index:   TIMESTAMP (scenario time)
    columns: Values  
             The following (String-)ID - called Sir3sID - is used as Column-Label:
             OBJTYPE~NAME1~NAME2~OBJTYPE_PK~ATTRTYPE 
             A Sir3sID consists of ~ seperated MX1-File terms.
    ---
    Note the following implicit Effect:
        Calls To setResultsTo... 
        will dump Vectorchannel Data to .MXS.vec.h5    
    """
    def __init__(self,mx1File=None,NoH5Read=False,NoMxsRead=False): 
        """
        (re-)initialize the Set with an MX1-File.
        ---
        NoH5Read False:
        If a .h5-File exists _and is newer than an (existing) .MX1-File _and newer than an (existing) .MXS-File:
            The .h5-File is read _instead of the .MX1-File
        ---
        NoMxsRead False:
        If a .MXS-File exists _and is newer than .MX1-File and .h5-File is not read:
            The .MXS-File is read.           
        """
        logger = logging.getLogger('PT3S.Mx')  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            if type(mx1File) == str:
                    self.mx1File=mx1File  
            else:
                    logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,mx1File)                                 
                    raise MxError(logStrFinal)     

            #Determine corresponding .MX2 Filename
            (wD,fileName)=os.path.split(self.mx1File)
            (base,ext)=os.path.splitext(fileName)
            self.mx2File=wD+os.path.sep+base+'.'+'MX2'   
                                                     
            #Determine corresponding .h5 Filename(s)
            self.h5File=wD+os.path.sep+base+'.'+'h5'    # mx1Df, mx2Df, df (Non Vectordata Only)
            self.h5FileMxsVecs=wD+os.path.sep+base+'.'+'vec'+'.'+'h5' # (Vectordata)           
            
            #Determine corresponding .MXS Filename
            self.mxsFile=wD+os.path.sep+base+'.'+'MXS'  
          
            #Determine corresponding .MXS Zip-Filename
            self.mxsZipFile=wD+os.path.sep+base+'.'+'ZIP'   

            #check if mx1File exists ...
            if os.path.exists(self.mx1File):
                mx1FileThere=True
                mx1FileTime=os.path.getmtime(self.mx1File) 
            else:
                mx1FileThere=False
                mx1FileTime=0
                logger.debug("{0:s}{1:s}: Not existing!".format(logStr,mx1File))     
             
            #check if h5File exists 
            if os.path.exists(self.h5File):  
                #check if h5File is newer               
                h5FileTime=os.path.getmtime(self.h5File)
                if(h5FileTime>mx1FileTime):
                    if os.path.exists(self.mxsFile):  
                        mxsFileTime=os.path.getmtime(self.mxsFile)
                        if(h5FileTime>mxsFileTime and not NoH5Read):
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an (existing) mx1File {2:s} _and is newer than an (existing) mxsFile {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an (existing) mx1File (mxsFile exists).".format(logStr))   
                            h5Read=True
                        else:                                                             
                            h5Read=False  
                    else:
                        if not NoH5Read:
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an (existing) mx1File {2:s} _and there is no mxsFile like {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an (existing) mx1File.".format(logStr))   
                            h5Read=True  
                        else:
                            h5Read=False  
                else:                    
                    h5Read=False
            else:
                h5Read=False

            self.df=None   
            self.mx1Df=None

            if not h5Read:
                if not mx1FileThere:
                   logStrFinal="{0:s}{1:s}: Not existing! Error.".format(logStr,mx1File)                                 
                   raise MxError(logStrFinal)                 
                self.__initWithMx1(mx1File)                    
                if os.path.exists(self.mxsFile):  
                    mx1FileTime=os.path.getmtime(self.mx1File) 
                    mxsFileTime=os.path.getmtime(self.mxsFile)
                    if(mxsFileTime>mx1FileTime) and not NoMxsRead:
                        logger.debug("{:s}mxsFile {:s} exists _and is newer than mx1File {:s} _and NoMxsRead False:".format(logStr,self.mxsFile,self.mx1File))     
                        logger.debug("{:s}The mxsFile is read.".format(logStr))   
                        self.setResultsToMxsFile()                     
            else:                
                self.FromH5(h5File=self.h5File)
                             
        except MxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __initWithMx1(self,mx1File):
        """
        (re-)initialize the set with an existing MX1-File:
            self.mx1Df = MX1-File Content           
        self.__parseMx2()    
        self.__buildMxRecordStructUnpackFmtString()  
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            logger.debug("{0:s}mx1File: {1:s} reading ...".format(logStr,self.mx1File))    
            # read mx1File To Dataframe
            Mx1Tree = ET.parse(self.mx1File)
            Mx1Root = Mx1Tree.getroot()

            logger.debug("{0:s}mx1File: {1:s} parsing ...".format(logStr,self.mx1File))    
            all_records = []
            for mxChannel in Mx1Root.findall('XL1'): # returns a list containing all matching elements in document order
                record = {}
                for attrName in sorted(mxChannel.keys()):
                    attrValue=mxChannel.get(attrName)
                    record[attrName]=attrValue 
                all_records.append(record)
            self.mx1Df=pd.DataFrame(all_records) 
            logger.debug("{0:s}mx1File: {1:s} mx1Df read. Shape: {2!s}.".format(logStr,self.mx1File,self.mx1Df.shape))    

            #Conversions
            self.mx1Df['DATALENGTH']=self.mx1Df['DATALENGTH'].astype('int64')
            self.mx1Df['DATATYPELENGTH']=self.mx1Df['DATATYPELENGTH'].astype('int64')
            self.mx1Df['DATAOFFSET']=self.mx1Df['DATAOFFSET'].astype('int64')
            self.mx1Df['FLAGS']=self.mx1Df['FLAGS'].astype('int64')

            #XPath-Example:
            #tsElement=MxRoot.find('./XL1[@OBJTYPE="ALLG"]/.[@ATTRTYPE="TIMESTAMP"]')
            #dfTsIdx = self.mx1Df.index[(self.mx1Df['OBJTYPE']=='ALLG') & (self.mx1Df['ATTRTYPE']=='TIMESTAMP')] 
            #self.channelTsIdx=dfTsIdx.tolist()[0] #channelNumber of the TimeStamp
            #logger.debug("{0:s}mx1File: {1:s}: channelNumber of the TimeStamp: {2:d}.".format(logStr,self.mx1File,self.channelTsIdx))    
            
            #Sir3sID
            sep='~'
            self.mx1Df['Sir3sID']=self.mx1Df['OBJTYPE']+sep+self.mx1Df['NAME1']+sep+self.mx1Df['NAME2']+sep+self.mx1Df['OBJTYPE_PK']+sep+self.mx1Df['ATTRTYPE']
            self.mx1Df['Sir3sID']=self.mx1Df['Sir3sID'].astype(str)

            #markVectorChannels (vectorChannel-Definition here := more than 1 Item)
            self.mx1Df['NOfItems']=[int(cDLength/cDTypeLength) for cDLength,cDTypeLength in zip(self.mx1Df['DATALENGTH'],self.mx1Df['DATATYPELENGTH'])] 
            #self.mx1Df['isVectorChannel']=[True if int(cDLength/cDTypeLength)>1 else False for cDLength,cDTypeLength in zip(self.mx1Df['DATALENGTH'],self.mx1Df['DATATYPELENGTH'])] 
            self.mx1Df['isVectorChannel']=[True if nItems>1 else False for nItems in self.mx1Df['NOfItems']] 
           
            #set(mx.mx1Df['DATATYPE'])
            #{'RVEC', 'CHAR', 'INT4', 'REAL'}
          
            #markMx2DefinedVectorChannels
            #True for all Mx2-defined-Types
            self.mx1Df['isVectorChannelMx2']=[True if isVectorChannel and bit3rd and flagStr[-3]=='1' else False for isVectorChannel,flagStr,bit3rd in zip(self.mx1Df['isVectorChannel'],self.mx1Df['FLAGS'].apply(bin),self.mx1Df['FLAGS'].apply(lambda x: True if x >=4 else False))] 
            #True for a special Mx2-defined-Type (Mx2 AttrType = N_OF_POINTS) 
            self.mx1Df['isVectorChannelMx2Rvec']=[True if isVectorChannelMx2 and dataType=='RVEC' else False for isVectorChannelMx2,dataType in zip(self.mx1Df['isVectorChannelMx2'],self.mx1Df['DATATYPE'])] 

            logger.debug("{0:s}mx1Df after some generated Columns: Shape: {1!s}.".format(logStr,self.mx1Df.shape))    

            self.__parseMx2()     
            self.__buildMxRecordStructUnpackFmtString()      
                            
        except FileNotFoundError as e:
            logStrFinal="{0:s}mx1File: {1!s}: FileNotFoundError.".format(logStr,mx1File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except OSError as e:
            logStrFinal="{0:s}mx1File: {1!s}: OSError.".format(logStr,mx1File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}mx1File: {1!s}: TypeError.".format(logStr,mx1File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)    
        except MxError:
            raise            
        except:
            logStrFinal="{0:s}mx1File: {1!s}: Error.".format(logStr,mx1File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __parseMx2(self):
        """
        >self.mx2Df
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            logger.debug("{0:s}mx2File: {1:s} parsing ...".format(logStr,self.mx2File))    

            headerFmtString='12s12s4si28xi'
            with open(self.mx2File,'rb') as f:               
                offsetToNextHeader=0
                all_records = []
                while True:
                    header=f.read(64)
                    headerLength=len(header)

                    if headerLength!=64:
                        if headerLength != 0:
                            logger.error("{:s}:headerLength: {:d} != 0?".format(logStr,headeLength))      
                        self.mx2Df=pd.DataFrame(all_records)                       
                        break

                    record = {}
                    headerData = struct.unpack(headerFmtString,header)  

                    ObjType=headerData[0].decode('utf-8')
                    AttrType=headerData[1].decode('utf-8')
                    DataType=headerData[2].decode('utf-8')
                    DataTypeLength=headerData[3]
                    DataLength=headerData[4]                   
                    
                    record['ObjType']=ObjType
                    record['AttrType']=AttrType
                    record['DataType']=DataType
                    record['DataTypeLength']=DataTypeLength
                    record['DataLength']=DataLength
                    NOfItems=int(DataLength/DataTypeLength)
                    record['NOfItems']=NOfItems

                    if DataType=='CHAR':
                        fmtItem=str(DataTypeLength)+'s'
                        dataFmtString=fmtItem*NOfItems 
                    elif DataType=='INT4':
                        fmtItem='i'
                        dataFmtString=fmtItem*NOfItems 
                    else:
                        fmtItem='x'
                        dataFmtString=str(DataLength)+fmtItem

                    dataBytes=f.read(DataLength)
                    Data = struct.unpack(dataFmtString,dataBytes)  

                    if DataType=='CHAR':
                        Data=list(map(lambda x: x.decode('utf-8').rstrip(),Data)) #20 vs. 19?!

                    record['Data']=Data

                    all_records.append(record)
                                                           
                    offsetToNextHeader=offsetToNextHeader+64+DataLength
                    if f.tell() != offsetToNextHeader:
                        logger.error("{:s}:offsetToNextHeader: {:d} != {:d}?".format(logStr,offsetToNextHeader,f.tell()))     
                        f.seek(offsetToNextHeader)                    

                    logger.debug("{:s}ObjType:{:s} AttrType:{:s} DataType:{:s} DataTypeLength:{:>3d} DataLength:{:>8d} Data[0]:{!s:>20s} Data[-1]:{!s:>20s} offsetToNextHeader:{:>11d}".format(logStr
                           ,ObjType #headerData[0]
                           ,AttrType #headerData[1]
                           ,DataType #headerData[2]
                           ,DataTypeLength #headerData[3]
                           ,DataLength #headerData[4]
                           ,Data[0]
                           ,Data[-1]
                           ,offsetToNextHeader
                           )
                                 )    
                                                            
        except FileNotFoundError as e:
            logStrFinal="{0:s}mx2File: {1!s}: FileNotFoundError.".format(logStr,self.mx2File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except OSError as e:
            logStrFinal="{0:s}mx2File: {1!s}: OSError.".format(logStr,self.mx2File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}mx2File: {1!s}: TypeError.".format(logStr,self.mx2File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)    
        except MxError:
            raise            
        except:
            logStrFinal="{0:s}mx2File: {1!s}: Error.".format(logStr,self.mx2File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __buildMxRecordStructUnpackFmtString(self):
        """    
        (re-)builds mxRecordStructFmtString and releated stuff:      
            >self.mxRecordStructFmtString: recordData = struct.unpack(self.mxRecordStructFmtString,record)              
            >self.bytesUnpacked
            >self.mx1Df['unpackIdx']
            >self.idxTIMESTAMP (idx of TIMESTAMP in MX1)
            >self.unpackIdxTIMESTAMP (idx of TIMESTAMP in recordData)
            >self.mxColumnNames=[] (of Non Vector Channels without TIMESTAMP in MX1-Sequence)
            >self.mxColumnNamesVecs=[] (of Vector Channels without TIMESTAMP in MX1-Sequence)
            >self.idxUnpackNonVectorChannels[] (idx in recordData)
            >self.idxUnpackVectorChannels[] (idx in recordData of the 1st ([0]) Element of the Vector)
            >self.idxOfNonVectorChannels[] (idx in MX1 without TIMESTAMP)
            >self.idxVectorChannels[] (idx in MX1)
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            self.mxRecordStructFmtString=''
            unpackIdx=[]
            idxUnpack=0
            bytesSkipped=0

            for row in self.mx1Df.itertuples():

                idxChannel=int(row.Index)

                fmtItem='' # End of Loop: self.mxRecordStructUnpackFmtString+=fmtItem

                sir3sID=row.Sir3sID

                isVectorChannel=row.isVectorChannel

                #if isVectorChannel:
                #    toBeUnpacked=False
                #else:
                #    toBeUnpacked=True

                toBeUnpacked=True
                                                                                   
                cDType=row.DATATYPE 
                cDTypeLength=row.DATATYPELENGTH 
                cDLength=row.DATALENGTH 
                nItems=row.NOfItems                
                
                if cDType=='CHAR':
                    if toBeUnpacked:   
                        unpackIdx.append(idxUnpack)    
                        if isVectorChannel:                                                                                  
                            for idx in range(nItems):
                                fmtItem+=(str(cDTypeLength)+'s') 
                            idxUnpack+=nItems                            
                        else:                            
                            fmtItem=str(cDLength)+'s'                         
                            idxUnpack+=1 
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'  
                        unpackIdx.append(-1)
                                                    
                elif cDType=='INT4':    
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)     
                        unpackIdx.append(idxUnpack)        
                        if isVectorChannel:                                                                                                                                                                                                                                                                                            
                            fmtItem=str(nItems)+'i'                    
                            idxUnpack+=nItems                           
                        else:                            
                            fmtItem='i'                         
                            idxUnpack+=1    
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x' 
                        unpackIdx.append(-1)                                     
                            
                elif cDType=='REAL':
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)    
                        unpackIdx.append(idxUnpack)        
                        if isVectorChannel:                                                                                                                                                                                                                                                                                            
                            fmtItem=str(nItems)+'f'                    
                            idxUnpack+=nItems                           
                        else:                            
                            fmtItem='f'                         
                            idxUnpack+=1    
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'
                        unpackIdx.append(-1)
                                                                                     
                elif cDType=='RVEC':
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        unpackIdx.append(idxUnpack)                                                                                                                                                                                                                                                                                                                            
                        fmtItem=str(nItems)+'f'                    
                        idxUnpack+=nItems                             
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'
                        unpackIdx.append(-1)
                else:                       
                    if toBeUnpacked:
                         logStrFinal="{0:s}sir3sID: {1:s}: UNKNOWN DATATYPE={2:s}. Error.".format(logStr,sir3sID,cDType)     
                         logger.error(logStrFinal) 
                         raise MxError(logStrFinal)                                                
                    else:
                         logStrFinal="{0:s}sir3sID: {1:s}: UNKNOWN DATATYPE={2:s}. Skipped!".format(logStr,sir3sID,cDType)     
                         logger.debug(logStrFinal)                                               
                    bytesSkipped+=cDLength
                    fmtItem=str(cDLength)+'x'
                    unpackIdx.append(-1)
                    
                self.mxRecordStructFmtString+=fmtItem

            MxRecordLengthMx1=self.mx1Df['DATAOFFSET'].iloc[-1]+self.mx1Df['DATALENGTH'].iloc[-1]     
            MxRecordLengthFmt=struct.calcsize(self.mxRecordStructFmtString)            
            if MxRecordLengthMx1 != MxRecordLengthFmt:
                logStrFinal="{0:s}Bytes per MX-Record from MX-Channels={1:d} <> Bytes from struct fmt-String for MX-Records={2:d}?! Error.".format(logStr,MxRecordLengthMx1,MxRecordLengthFmt)
                raise MxError(logStrFinal)    

            self.bytesUnpacked = MxRecordLengthFmt - bytesSkipped
            logger.debug("{0:s}Bytes per MX-Record={1:d}. Bytes Unpacked={2:d} (making up {3:06.2f} Bytes-%).".format(logStr,MxRecordLengthMx1,self.bytesUnpacked,self.bytesUnpacked/MxRecordLengthFmt*100))                                                  

            self.mx1Df['unpackIdx']=pd.Series(unpackIdx)
            self.mx1Df['unpackIdx']=self.mx1Df['unpackIdx'].astype('int64')      
            logger.debug("{0:s}mx1Df after generated Column: Shape: {1!s}.".format(logStr,self.mx1Df.shape))        
            
            # idxTIMESTAMP
            self.idxTIMESTAMP=self.mx1Df['Sir3sID'][self.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].index[0]
            # unpackIdxTIMESTAMP
            self.unpackIdxTIMESTAMP=self.mx1Df['unpackIdx'][self.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].iloc[0]    
            logger.debug("{:s}idxTIMESTAMP={:d} (idx in MX1) unpackIdxTIMESTAMP={:d} (idx in recordData).".format(logStr,self.idxTIMESTAMP,self.unpackIdxTIMESTAMP))                    
            
            # columnNames used in Pandas        
            self.mxColumnNames=[]  
            self.mxColumnNamesVecs=[]  
            for idxChannel,idxUnpack in [(idxChannel,idxUnpack)  for idxChannel,idxUnpack in enumerate(self.mx1Df['unpackIdx']) if idxUnpack >=0]:                 
                sir3sID=self.mx1Df['Sir3sID'].iloc[idxChannel]        
                isVectorChannel=self.mx1Df['isVectorChannel'].iloc[idxChannel]        
                if not isVectorChannel:                   
                    self.mxColumnNames.append(sir3sID)
                else:
                    self.mxColumnNamesVecs.append(sir3sID)

            # remove Timestamp in mxColumnNamesVecs (index not value)
            idxTIMESTAMP=self.mxColumnNames.index('ALLG~~~-1~TIMESTAMP')
            del self.mxColumnNames[idxTIMESTAMP] 
            columns=len(self.mxColumnNames)
            logger.debug("{0:s}NOfColumns (without TIMESTAMP): {1:d}.".format(logStr,columns))                
            logger.debug("{0:s}NOfColumnsVecs: {1:d}.".format(logStr,len(self.mxColumnNamesVecs)))                  

            # unpack Idx of Non Vector Channels (without unpack Idx of TIMESTAMP)
            self.idxUnpackNonVectorChannels=[self.mx1Df['unpackIdx'].iloc[idx] for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if not isVectorChannel]
            self.idxUnpackNonVectorChannels.remove(self.unpackIdxTIMESTAMP) 
            idxUnpackNonVectorChannelsLen=len(self.idxUnpackNonVectorChannels)
            logger.debug("{:s}idxUnpackNonVectorChannelsLen: {:d}.".format(logStr,idxUnpackNonVectorChannelsLen))

            # check NonVectorChannels
            if idxUnpackNonVectorChannelsLen != columns:
                logger.error("{:s}idxUnpackNonVectorChannelsLen: {:d} != NOfColumns (without Timestamp): {:d}?!".format(logStr,idxUnpackNonVectorChannelsLen,columns))               

            # unpack Idx of Vector Channels
            self.idxUnpackVectorChannels=[self.mx1Df['unpackIdx'].iloc[idx] for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if isVectorChannel]
            idxUnpackVectorChannelsLen=len(self.idxUnpackVectorChannels)
            logger.debug("{:s}idxUnpackVectorChannelsLen: {:d}.".format(logStr,idxUnpackVectorChannelsLen))

            # check AllValueChannels
            rows,cols=self.mx1Df.shape
            valueChannels=idxUnpackVectorChannelsLen+idxUnpackNonVectorChannelsLen
            if (valueChannels != rows-1):
                logger.error("{:s}valueChannels: {:d} != mx1Df rows -1 {:d}?!".format(logStr,valueChannels,rows-1))               

            # Idx of Non Vector Channels
            self.idxOfNonVectorChannels=[idx for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if not isVectorChannel]
            self.idxOfNonVectorChannels.remove(self.idxTIMESTAMP) 
            logger.debug("{:s}idxOfNonVectorChannels: Len: {:d}.".format(logStr,len(self.idxOfNonVectorChannels)))

            # Idx of Vector Channels
            self.idxOfVectorChannels=[idx for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if isVectorChannel]
            logger.debug("{:s}idxOfVectorChannels:    Len: {:d}.".format(logStr,len(self.idxOfVectorChannels)))

            # check AllChannels
            allChannels=len(self.idxOfNonVectorChannels)+len(self.idxOfVectorChannels)
            if allChannels != rows-1:
                logger.error("{:s}allChannels: {:d} != mx1Df rows-1 {:d}?!".format(logStr,allChannels,rows-1))   
                
            # list all Channels with their relevant attributes         
            for idxChannel,idxUnpack in [(idxChannel,idxUnpack)  for idxChannel,idxUnpack in enumerate(self.mx1Df['unpackIdx']) if idxUnpack >=0]:                 
                sir3sID=self.mx1Df['Sir3sID'].iloc[idxChannel]
                idxUnpack=self.mx1Df['unpackIdx'].iloc[idxChannel]
                isVectorChannel=self.mx1Df['isVectorChannel'].iloc[idxChannel]
                isVectorChannelMx2=self.mx1Df['isVectorChannelMx2'].iloc[idxChannel]             
                isVectorChannelMx2Rvec=self.mx1Df['isVectorChannelMx2Rvec'].iloc[idxChannel]
                logger.debug("{:s}Channel-Nr. {:>6d} Sir3sID {:>60s} idxUnpack {:>6d}  isVectorChannel {!s:>6s} isVectorChannelMx2 {!s:>6s} isVectorChannelMx2Rvec {!s:>6s}.".format(logStr
                         ,idxChannel
                         ,sir3sID
                         ,idxUnpack
                         ,isVectorChannel
                         ,isVectorChannelMx2
                         ,isVectorChannelMx2Rvec))  
                                                                                     
        except MxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _readMxsFile(self,mxsFilePtr=None,mxsVecsH5StorePtr=None,firstTime=None,maxRecords=None):

        """
        Returns the File-Content (Non Vectordata Only) as df.  
        ---
        It is implied that the calculation results in the File originate from self.mx1File.  
        ---
        TIMESTAMP is used as index.
        ---
        df.index.is_unique 
        might be False 
        because of SIR 3S'
        1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
        ---        
        Writes the Vectordata in mxsFilePtr with mxsVecsH5StorePtr: 
            Key:   microseconds from firstTime 
            Value: dfVecs (df with Vectordata for one TIMESTAMP):
                 TIMESTAMP is used as index.
            ---
            the Vectordata for a TIMESTAMP is only written
                when the Key does _not exist 
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:   
            df = None 
                                                       
            mxTimes=[]
            mxTimesVecs=[]
            mxValues=[]      
            mxValuesVecs=[]           
            
            MxRecordLength=struct.calcsize(self.mxRecordStructFmtString)    
            if isinstance(maxRecords,int):
                maxRecordsLimit=True
            else:
                maxRecordsLimit=False   
                      
            recsReadFromFile=0     
            firstTime=None    
            
            if mxsVecsH5StorePtr != None:
                keysAtStart=mxsVecsH5StorePtr.keys()
                                                                     
            with mxsFilePtr: 
                try:                    
                    while True:   # while f.tell() != os.fstat(f.fileno()).st_size does NOT work with Zip's file objects ...    
                            
                        # read record 
                        try: 
                            record=mxsFilePtr.read(MxRecordLength)
                            recordData = struct.unpack(self.mxRecordStructFmtString,record)  
                        except:
                            logger.debug("{0:s}record=f.read(MxRecordLength) failed (EOF probably).".format(logStr))  
                            raise EOFError
                        else:
                            timeISO8601=None

                        # process record time
                        try:
                            timeISO8601 = recordData[self.unpackIdxTIMESTAMP] #b'2017-10-20 00:00:00.000000+01:00' for scenTime 2017-10-20 00:00:00
                            time = pd.to_datetime(timeISO8601,utc=True) 
                            time_read_after_to_datetime=time.strftime("%Y-%m-%d %H:%M:%S.%f%z") #%z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive)        
                            time = time + pd.to_timedelta('1 hour')   
                            time_read_finally=time.strftime("%Y-%m-%d %H:%M:%S.%f%z")       
                            if recsReadFromFile==0 and firstTime==None:
                                firstTime=time                                                                                                                                                                                                                                                                             
                        except:
                            logStrFinal="{0:s}process record time failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                
                        
                        # process record
                        try:                                                                                                                 
                            # Filter NonVectorChannels and Skip Timestamp (index not value)     
                            values=[recordData[idx] for idx in self.idxUnpackNonVectorChannels]
                            #recordData[0:self.idxTIMESTAMP]
                            #+recordData[self.idxTIMESTAMP+1:]                              
                            
                            # Vecs
                            valuesVecs=[] # all Vectors For One Timestep
                            for idxOf,idxUnpack in zip(self.idxOfVectorChannels,self.idxUnpackVectorChannels):                                                            
                                valueVec=recordData[idxUnpack:idxUnpack+self.mx1Df['NOfItems'].iloc[idxOf]] # one Vector For One Timestep
                                valuesVecs.append(valueVec)                            
                                                                                       
                        except:
                            logStrFinal="{0:s}process record failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                                                                                                          
                                                  
                        # store record in memory
                        try:                            
                            mxTimes.append(time)                         
                            mxValues.append(values)                           
                        except:
                            logStrFinal="{0:s}store record in memory failed at Time={1!s}. Error.".format(logStr,time_read_finally)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        
                        h5DumpLog="{:s} NO (no Dumpfile).".format('H5Dump:')
                        if mxsVecsH5StorePtr != None:
                            # store record as df in H5
                            try:      
                                 h5DumpLog="{:s} NO.".format('H5Dump:')
                                 h5Key=getMicrosecondsFromRefTime(refTime=firstTime,time=time)   
                                 
                                 if '/'+str(h5Key) not in keysAtStart:                                                                                                      
                                     keys=mxsVecsH5StorePtr.keys()
                                 
                                     if '/'+str(h5Key) not in keys:      
                                        mxTimesVecs=[]            
                                        mxValuesVecs=[]                                                            
                                        mxTimesVecs.append(time)     
                                        mxValuesVecs.append(valuesVecs)
                                        dfVecs = pd.DataFrame.from_records(mxValuesVecs,index=mxTimesVecs,columns=self.mxColumnNamesVecs)                                                                                                      
                                        #H5
                                        warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
                                        warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)                          
                                        mxsVecsH5StorePtr.put(str(h5Key),dfVecs)   
                                        h5DumpLog="{:s} Writing DataFrame {:s} with h5Key=/{!s:>20s}".format('H5Dump:','dfVecs',h5Key) 
                                                              
                            except:
                                logStrFinal="{0:s}store record as df in H5 failed at Time={1!s}. Error.".format(logStr,time_read_finally)
                                logger.error(logStrFinal) 
                                raise MxError(logStrFinal)                                                           


                        logger.debug("{:s}TimeNr. {:>6d} read and processed finally={!s:s} Time read after to_datetime: {!s:s} timeISO8601 read: {!s:s} Values (without TIMESTAMP): {:d} - {:s}.".format(logStr
                                        ,recsReadFromFile+1
                                        ,time_read_finally
                                        ,time_read_after_to_datetime
                                        ,timeISO8601
                                        ,len(values)
                                        ,h5DumpLog))  

                        # next record                            
                        recsReadFromFile+=1                               
                        if maxRecordsLimit:
                            if recsReadFromFile == maxRecords:
                                logger.debug("{0:s}maxRecords={1:d} read.".format(logStr,maxRecords))  
                                raise EOFError   
                                                   
                except EOFError:                    
                    logger.debug("{0:s}Last Time read={1!s}. File finished.".format(logStr,time_read_finally))                                                                                             
                except:
                    logStrFinal="{0:s}Last Time read={1!s}. Error.".format(logStr,time_read_finally)
                    logger.error(logStrFinal) 
                    raise MxError(logStrFinal)    
                                  
            logger.debug("{0:s}File finished: Records read={1:d}. Last Time read={2!s}. MB read={3:07.2f}. MB unpacked={4:07.2f} (making up {5:06.2f} %). ".format(logStr                                                                                                                                         
                                                                                    ,recsReadFromFile
                                                                                    ,time_read_finally
                                                                                    ,recsReadFromFile*MxRecordLength/pow(10,6)
                                                                                    ,recsReadFromFile*self.bytesUnpacked/pow(10,6)
                                                                                    ,self.bytesUnpacked/MxRecordLength*100
                                                                                                                                                 )
                        )                                                                     

            df = pd.DataFrame.from_records(mxValues,index=mxTimes,columns=self.mxColumnNames)                
            logger.debug("{0:s}df.shape(): {1!s}.".format(logStr,df.shape))   
                                                                                  
        except MxError:
            raise
        except MemoryError as e:
            logStrFinal="{0:s}MemoryError.".format(logStr)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)      
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                    
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return df

    def _checkMxsVecsFile(self):
        """
        returns (firstTime,lastTime,NOfTimes)
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:         
            with pd.HDFStore(self.h5FileMxsVecs) as mxsVecsH5Store: 
                                                                                                                                               
                keys=sorted([int(key.replace('/','')) for key in mxsVecsH5Store.keys()])

                for idx,key in enumerate([ '/'+str(key) for key in keys]):                
                    dfVecs=mxsVecsH5Store[key]  
                    time=dfVecs.index[0]
                    if idx==0:
                        firstTime=time
                    logger.debug("{:s}TimeNr. {:>6d} with key {!s:>20s} and TIMESTAMP {!s:s}.".format(logStr,idx+1,key,time))         
                lastTime=time
                                                                                                                
        except MxError:
            raise
                               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return (firstTime,lastTime,idx+1)     
            
    def setResultsToMxsFile(self,mxsFile=None,add=False,maxRecords=None):
        """
        Sets or adds the MXS-Results to self.df.          
        ---
        Implicit specified is a MXS-File .MXS in the same directory as the MX1-File .MX1.  
        ---
        It is implied that the calculation results in the MXS-File originate from self.mx1File.        
        ---
        TIMESTAMP is used as index.
        ---
        self.df.index.is_unique 
        will be True 
            because in SIR 3S'
            1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
            +TIME       is dropped                                
            +TMIN/TMAX are dropped   
            ---
            and because resulting overlapping TIMESTAMPs due to intersections (add=True) are also dropped      
        ---        
        Note the following implicit Effect:
            File .vec.h5 is deleted if existing _and older than mxsFile.                              
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 

            # Mxs specification 
            if mxsFile == None:
                logger.debug("{0:s}Mxs: Implicit specified.".format(logStr))                                
                mxsFile=self.mxsFile
        
            # .vec.h5 Handling 
            if os.path.exists(self.h5FileMxsVecs):      
            
                mxsFileTime=os.path.getmtime(mxsFile) 
                mxsH5FileTime=os.path.getmtime(self.h5FileMxsVecs)

                if mxsFileTime>mxsH5FileTime:
                    # die zu lesende Mxs ist neuer als der Dump: Dump loeschen
                    if not add:                    
                        logger.debug("{:s}Delete H5VecDump because Mxs {:s} To Read is newer than H5VecDump {:s} ...".format(logStr,mxsFile,self.h5FileMxsVecs))     
                    else:
                        logger.warning("{:s}Delete H5VecDump because Mxs {:s} To Read is newer than the H5VecDump {:s} ...".format(logStr,mxsFile,self.h5FileMxsVecs))     
                    os.remove(self.h5FileMxsVecs)
                
            mxsVecH5Store=pd.HDFStore(self.h5FileMxsVecs) 
                                                                                      
            if isinstance(self.df,pd.core.frame.DataFrame):   
                firstTime=self.df.index[0]
            else:
                firstTime=None
            
            #Mxs reading ...           
            logger.debug("{0:s}Mxs: {1:s} opening ...".format(logStr,mxsFile))                
            with open(mxsFile,'rb') as f:
                 # Mxs exists ...
                logger.debug("{0:s}Mxs: {1:s} reading ...".format(logStr,mxsFile))                
                # Mxs reading ...
                dfMxs=self._readMxsFile(f,mxsVecsH5StorePtr=mxsVecH5Store,firstTime=firstTime,maxRecords=maxRecords)                                     
                           
            if isinstance(dfMxs,pd.core.frame.DataFrame):                                     
                # Unique index ...
                if not dfMxs.index.is_unique:                        
                     logger.debug("{0:s}Mxs: {1:s}: NOT unique TIMESTAMPS: Their dfMxs Shape: {2!s}.".format(logStr,mxsFile,dfMxs[dfMxs.index.duplicated()].shape))    
                     dfMxs=dfMxs[dfMxs.index.duplicated() == False]     
                     logger.debug("{0:s}Mxs: {1:s}: New unique                   dfMxs Shape: {2!s}.".format(logStr,mxsFile,dfMxs.shape))   
                if not add or not isinstance(self.df,pd.core.frame.DataFrame): 
                    self.df=dfMxs
                    logger.debug("{0:s}Mxs: {1:s}: Assigned.     df Shape: {2!s}.".format(logStr,mxsFile,self.df.shape))    
                else:
                    self.df=pd.concat([self.df,dfMxs])
                    logger.debug("{0:s}Mxs: {1:s}: Added.    New df Shape: {2!s}.".format(logStr,mxsFile,self.df.shape))    
                    if not self.df.index.is_unique:                        
                        logger.debug("{0:s}Mxs: {1:s}: NOT unique TIMESTAMPS added (intersection): Their df Shape: {2!s}.".format(logStr,mxsFile,self.df[self.df.index.duplicated()].shape))    
                        self.df=self.df[self.df.index.duplicated() == False] 
                        logger.debug("{0:s}Mxs: {1:s}: New unique                                        df Shape: {2!s}.".format(logStr,mxsFile,self.df.shape))       
                # sort
                if add:
                    self.df.sort_index(inplace=True)    
                logger.debug("{0:s}RESULT after {1:s}: df Shape: {2!s} First Time: {3!s} Last Time: {4!s}.".format(logStr,mxsFile,self.df.shape,self.df.index[0],self.df.index[-1]))                                             
            else:
                logger.error("{0:s}Mxs: {1:s}: Reading failed.".format(logStr,mxsFile))    
                          
        except FileNotFoundError as e:
            logStrFinal="{0:s}mxsFile: {1!s}: FileNotFoundError.".format(logStr,mxsFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                
        except OSError as e:
            logStrFinal="{0:s}mxsFile: {1!s}: OSError.".format(logStr,mxsFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}mxsFile: {1!s}: TypeError.".format(logStr,mxsFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)        
        except MemoryError as e:
            logStrFinal="{0:s}mxsFile: {1!s}: MemoryError.".format(logStr,mxsFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                             
        except MxError:
            raise
        except:
            logStrFinal="{0:s}mxsFile: {1!s}: Error.".format(logStr,mxsFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                    
        else:
            mxsVecH5Store.close()
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def setResultsToMxsZipFile(self,mxsZipFile=None,add=False,maxRecords=None):
        """
        Sets or adds the MXS-Results in the Zip to self.df.                 
        ---
        Implicit specified is a Zip-File .ZIP in the same directory as the MX1-File .MX1.  
        ---
        It is implied that all calculation results in the Zip-File originate from self.mx1File.   
        ---
        The Mxs-Files in the Zip-File are read in alphabetical order.    
        ---
        TIMESTAMP is used as index.
        ---
        self.df.index.is_unique 
        will be True 
            because in SIR 3S' 
            1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
            +TIME       is  dropped                                
            +TMIN/TMAX  are dropped 
            ---
            and because resulting overlapping TIMESTAMPs due to intersections between the Zip-MXS (or due to add=True) are also dropped
        ---        
        Note the following implicit Effect:
            File .vec.h5 is deleted if existing _and older than mxsZipFile.          
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            # Zip specification ...
            if mxsZipFile == None:
                mxsZipFile=self.mxsZipFile
            
            # Zip existence ... 
            logger.debug("{0:s}Zip: {1:s} ...".format(logStr,mxsZipFile))                               
            with open(mxsZipFile,'rb') as f:   
                pass     

            # Zip opening ...
            logger.debug("{0:s}Zip: {1:s} opening ...".format(logStr,mxsZipFile)) 
            try:
                z = zipfile.ZipFile(mxsZipFile,'r')
            except:
                logStrFinal="{0:s}{1:s}: opening the Zip failed. Error.".format(logStr,mxsZipFile)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)   

            # maxRecords-Check
            if isinstance(maxRecords,int):
                maxRecordsLimit=True
            else:
                maxRecordsLimit=False   

            # .vec.h5 Handling 
            if os.path.exists(self.h5FileMxsVecs):      
            
                mxsZipFileTime=os.path.getmtime(mxsZipFile) 
                mxsH5FileTime=os.path.getmtime(self.h5FileMxsVecs)

                if mxsZipFileTime>mxsH5FileTime:
                    # die zu lesende MxsZip ist neuer als der Dump: Dump loeschen
                    if not add:                    
                        logger.debug("{:s}Delete H5VecDump because MxsZip {:s} To Read is newer than H5VecDump {:s} ...".format(logStr,mxsZipFile,self.h5FileMxsVecs))     
                    else:
                        logger.warning("{:s}Delete H5VecDump because MxsZip {:s} To Read is newer than H5VecDump {:s} ...".format(logStr,mxsZipFile,self.h5FileMxsVecs))     
                    os.remove(self.h5FileMxsVecs)
                
            mxsVecH5Store=pd.HDFStore(self.h5FileMxsVecs) 
                                                                                      
            if isinstance(self.df,pd.core.frame.DataFrame):   
                firstTime=self.df.index[0]
            else:
                firstTime=None
          
            # Zip reading ...              
            recsReadFromZip=0            
            dfZip=None
            for mxsFileName in sorted(z.namelist()):  
                # Mxs reading ...                        
                with z.open(mxsFileName,'r') as f: 
                    logger.debug("{0:s}Zip: {1:s}: {2:s} reading ...".format(logStr,mxsZipFile,mxsFileName))       
                    dfMxs=self._readMxsFile(f,mxsVecsH5StorePtr=mxsVecH5Store,firstTime=firstTime,maxRecords=maxRecords)   

                if isinstance(dfMxs,pd.core.frame.DataFrame):                                                                                      
                    # Unique index ...
                    if not dfMxs.index.is_unique:                        
                         logger.debug("{0:s}Mxs: {1:s}: NOT unique TIMESTAMPS: Their dfMxs Shape: {2!s}.".format(logStr,mxsFileName,dfMxs[dfMxs.index.duplicated()].shape))    
                         dfMxs=dfMxs[dfMxs.index.duplicated() == False]     
                         logger.debug("{0:s}Mxs: {1:s}: New unique                   dfMxs Shape: {2!s}.".format(logStr,mxsFileName,dfMxs.shape))                                                                            
                    recsReadFromZip+=len(dfMxs.index)
                else:
                    logger.warning("{0:s}Zip: {1:s}: {2:s}: Reading failed.".format(logStr,mxsZipFile,mxsFileName))    
                    continue   

                if not isinstance(dfZip,pd.core.frame.DataFrame):
                    # 1st Mxs
                    dfZip=dfMxs
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: Assigned. Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip.shape))    
                else:                    
                    dfZip=pd.concat([dfZip,dfMxs])
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: Added.    Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip.shape))    
                # Unique index ...
                if not dfZip.index.is_unique:                        
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: NOT unique TIMESTAMPS added (intersection): Their Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip[dfZip.index.duplicated()].shape))    
                    dfZip=dfZip[dfZip.index.duplicated() == False] 
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: New unique Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip.shape))             
                
                if maxRecordsLimit:
                    if recsReadFromZip >= maxRecords:
                        logger.debug("{0:s}>=maxRecords ({1:d}) read.".format(logStr,maxRecords))  
                        break

            if isinstance(dfZip,pd.core.frame.DataFrame):
                logger.debug("{0:s}Zip: {1:s}: Final dfZip Shape: {2!s}.".format(logStr,mxsZipFile,dfZip.shape))  

                if not add or not isinstance(self.df,pd.core.frame.DataFrame): 
                    self.df = dfZip   
                    logger.debug("{0:s}Zip: {1:s}: Assigned dfZip To df. df     Shape: {2!s}.".format(logStr,mxsZipFile,self.df.shape))    
                else:
                    self.df=pd.concat([self.df,dfZip])
                    logger.debug("{0:s}Zip: {1:s}: Added    dfZip To df. New df Shape: {2!s}.".format(logStr,mxsZipFile,self.df.shape))    
                # Unique index ...
                if not self.df.index.is_unique:                        
                    logger.debug("{0:s}Zip: {1:s}: NOT unique TIMESTAMPS added (intersection): Their df Shape: {2!s}.".format(logStr,mxsZipFile,self.df[self.df.index.duplicated()].shape))    
                    self.df=self.df[self.df.index.duplicated() == False] 
                    logger.debug("{0:s}Zip: {1:s}: New unique                                        df Shape: {2!s}.".format(logStr,mxsZipFile,self.df.shape))   
                
                # sort
                self.df.sort_index(inplace=True)  
                logger.debug("{0:s}RESULT after {1:s}: df Shape: {2!s} First Time: {3!s} Last Time: {4!s}.".format(logStr,mxsZipFile,self.df.shape,self.df.index[0],self.df.index[-1]))                

            else:
                logger.error("{0:s}Zip: {1:s}: Reading failed.".format(logStr,mxsZipFile))                                          
                                                                    
        except FileNotFoundError as e:
            logStrFinal="{0:s}mxsZipFile: {1!s}: FileNotFoundError.".format(logStr,mxsZipFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                
        except OSError as e:
            logStrFinal="{0:s}mxsZipFile: {1!s}: OSError.".format(logStr,mxsZipFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}mxsZipFile: {1!s}: TypeError.".format(logStr,mxsZipFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)        
        except MemoryError as e:
            logStrFinal="{0:s}mxsZipFile: {1!s}: MemoryError.".format(logStr,mxsZipFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                             
        except MxError:
            raise
        except:
            logStrFinal="{0:s}mxsZipFile: {1!s}: Error.".format(logStr,mxsZipFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                    
        else:
            mxsVecH5Store.close()
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def ToH5(self,h5File=None):
        """
        Stores the Dataframes 
        mx1Df h5Key: .../MX1 
        mx2Df h5Key: .../MX2 
        df    h5Key: .../MXS  
        in a .h5-File.      
        ---
        If the .h5-File exists it is !DELETED! before.          
        ---
        Implicit specified is a .h5-File in the same directory as the .mx1-File.  
        ---
        If mx1Df is not defined mx1Df is not stored.
        If df    is not defined    df is not stored.
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            if h5File == None:
                h5File=self.h5File

            if os.path.exists(h5File):                        
                logger.debug("{0:s}{1:s}: Delete H5 ...".format(logStr,h5File))     
                os.remove(h5File)

            relPath2Mx1FromCurDir=os.path.normpath(os.path.relpath(os.path.normpath(self.mx1File),start=os.path.normpath(os.path.curdir)))
            h5KeySep='/'
            h5KeyCharForDot='_'
            h5KeyCharForMinus='_'
            relPath2Mx1FromCurDirH5BaseKey=re.sub('\.',h5KeyCharForDot,re.sub(r'\\',h5KeySep,re.sub('-',h5KeyCharForMinus,re.sub('.mx1','',relPath2Mx1FromCurDir,flags=re.IGNORECASE))))
                       
            warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
            warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)
                                      
            logger.debug("{0:s}pd.HDFStore({1:s}) ...".format(logStr,h5File))                 
            with pd.HDFStore(h5File) as h5Store:  
                if isinstance(self.mx1Df,pd.core.frame.DataFrame):      
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MX1' 
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'mx1Df',h5Key))           
                    h5Store.put(h5Key,self.mx1Df)
                if isinstance(self.mx2Df,pd.core.frame.DataFrame):      
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MX2' 
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'mx2Df',h5Key))           
                    h5Store.put(h5Key,self.mx2Df)
                if isinstance(self.df,pd.core.frame.DataFrame):    
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MXS'  
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'df',h5Key))         
                    h5Store.put(h5Key,self.df)

        except OSError as e:
            logStrFinal="{0:s}h5File: {1!s}: OSError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}h5File: {1!s}: TypeError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)        
        except PermissionError as e:
            logStrFinal="{0:s}h5File: {1!s}: PermissionError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        except MxError:
            raise
        except:
            logStrFinal="{0:s}h5File: {1!s}: Error.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                    
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def FromH5(self,h5File=None):
        """
        The h5File is read
        and the following Dataframes
        self.mx1Df (h5Key: .../MX1) 
        self.mx2Df (h5Key: .../MX1) 
        self.df    (h5Key: .../MXS) 
        are overwritten with the Dataframes in the h5File if any.     
        ---
        /MX1 in h5File:
        mxRecordStructUnpackFmtString and releated stuff is (re-)builded
        /MX2 in h5File: Check if .vec.h5 corresponds
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))  
        
        try:

            #Check if h5File exists
            if not os.path.exists(h5File):    
                logStrFinal="{0:s}{1:s}: Not Existing!".format(logStr,h5File)                                 
                raise MxError(logStrFinal)           
  
            #Read
            with pd.HDFStore(h5File) as h5Store:
                h5Keys=sorted(h5Store.keys())
                for h5Key in h5Keys:
                    h5KeySep='/'
                    match=re.search('('+h5KeySep+')(\w+$)',h5Key)
                    key=match.group(2)
                    if key == 'MX1':                            
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.mx1Df=h5Store[h5Key]
                        self.__buildMxRecordStructUnpackFmtString()      
                    if key == 'MX2':                            
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.mx2Df=h5Store[h5Key]                         
                    if key == 'MXS':                           
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.df=h5Store[h5Key]
                        # Check if .vec.h5 corresponds
                        firstTime=self.df.index[0]
                        lastTime=self.df.index[-1]
                        rows,cols=self.df.shape
                        tupleDf=(firstTime,lastTime,rows)
                        tupleVecH5=self._checkMxsVecsFile()
                        if tupleDf != tupleVecH5:                            
                            logger.warning("{:s}{:s}: tupleDf {!s:s} != tupleVecH5 {!s:s}.".format(logStr,h5File,tupleDf,tupleVecH5))              

        except FileNotFoundError as e:
            logStrFinal="{0:s}h5File: {1!s}: FileNotFoundError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                
        except OSError as e:
            logStrFinal="{0:s}h5File: {1!s}: OSError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}h5File: {1!s}: TypeError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)        
        except MemoryError as e:
            logStrFinal="{0:s}h5File: {1!s}: MemoryError.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                             
        except MxError:
            raise
        except:
            logStrFinal="{0:s}h5File: {1!s}: Error.".format(logStr,h5File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                    
        else:             
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                

    def dumpInMxsFormat(self,mxsDumpFile=None):
        """
        Dumps Data (self.df) in MXS-Format to mxsDumpFile (for testing purposes). 
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            if mxsDumpFile == None:
                mxsDumpFile=self.mxsFile+'.dump'

            with open(mxsDumpFile,'wb') as f:

                # ueber alle Zeiten in self.df ...
                idxDumped=0
                for idx,row in enumerate(self.df.itertuples(index=False)):
                    
                    # TIMESTAMP herrichten
                    try:                        
                        scenTime=self.df.index[idx]                                                                                               
                        #timeISO8601 read:          b'2017-10-20 00:00:00.000000+01:00' - the original timeISO8601 read is marked as UTC +1 written as +01:00
                        #Time read after to_datetime: 2017-10-19 23:00:00.000000+0000   - the result after pd.to_datetime(timeISO8601,utc=True) 
                        #Time read finally            2017-10-20 00:00:00.000000+0000   - the time used - "corrected" manually +1 hour 
                        #+01:00 instead of %z because %z will be +0000 ...  
                        scenTimeStr=scenTime.strftime("%Y-%m-%d %H:%M:%S.%f+01:00") 
                        scenTimeStrBytes=scenTimeStr.encode('utf-8')
                    except:
                        logStrFinal="{0:s}h5File: {1!s}: TIMESTAMP herrichten: Error.".format(logStr,mxsDumpFile)
                        logger.error(logStrFinal) 
                        raise MxError(logStrFinal)    

                    # Values herrichten und Satz schreiben
                    try:    
                        valuesNonVec=list(row)
                        # valuesVec
                        # h5Key aus scenTime
                        firstTime=self.df.index[0]
                        h5Key=getMicrosecondsFromRefTime(refTime=firstTime,time=scenTime)
                        
                        h5Key='/'+str(h5Key)
                        # dfVecs lesen
                        with pd.HDFStore(self.h5FileMxsVecs) as mxsVecsH5Store: 
                            dfVecs=mxsVecsH5Store[h5Key]  
                        for row in dfVecs.itertuples(index=False):
                            # one row
                            valuesVec=list(row)
                        # Gesamt anlegen
                        rows,cols = self.mx1Df.shape
                        values=[]
                        for idx in range(rows):
                            values.append(None)
                        # Gesamt bestuecken
                        for idx,idxOf in enumerate(self.idxOfVectorChannels):
                            values[idxOf]=valuesVec[idx]
                        for idx,idxOf in enumerate(self.idxOfNonVectorChannels):
                            values[idxOf]=valuesNonVec[idx]                        
                        # TIMESTAMP einpflegen
                        values[self.idxTIMESTAMP]=scenTimeStrBytes      
                        # Gesamt Einzelvalues
                        valuesSingle=[]
                        for idx,value in enumerate(values):
                            if idx not in self.idxOfVectorChannels:
                                valuesSingle.append(value)
                            else:
                                for vecItem in value:
                                    valuesSingle.append(vecItem)                                                                                                                                  
                        # Satz schreiben
                        bytes=struct.pack(self.mxRecordStructFmtString,*valuesSingle)
                        f.write(bytes)        
                        logger.debug("{:s}mxsDumpFile: {:s}: TimeNr. {:>6d} with TIMESTAMP: {:s}: Dumped.".format(logStr,mxsDumpFile,idxDumped,scenTimeStr))    
                        idxDumped=idxDumped+1                                                                 
                    except:
                        logger.debug("{:s}mxsDumpFile: {:s}: TIMESTAMP: {:s}: Exception. Continue.".format(logStr,mxsDumpFile,scenTimeStr))                                                     
                        continue                      
                                                                            
        except OSError as e:
            logStrFinal="{0:s}h5File: {1!s}: OSError.".format(logStr,mxsDumpFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)
        except TypeError as e:
            logStrFinal="{0:s}h5File: {1!s}: TypeError.".format(logStr,mxsDumpFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)        
        except PermissionError as e:
            logStrFinal="{0:s}h5File: {1!s}: PermissionError.".format(logStr,mxsDumpFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        except MxError:
            raise
        except:
            logStrFinal="{0:s}h5File: {1!s}: Error.".format(logStr,mxsDumpFile)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                    
        else:
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
