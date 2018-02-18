"""
SIR 3S MX-Interface (short: MX):
--------------------------------
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
DOCTEST
---------------------------
>>> # ---
>>> # Imports
>>> import os
>>> import logging
>>> import __init__ # PT3S' __init__.py
>>> logger = logging.getLogger('PT3S.Mx')  
>>> # ---
>>> # Init
>>> # ---
>>> mx1File=r'C:\\3S\Modelle\WDMVV_FW\B1\V0\BZ1\M-1-0-1.MX1'
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> type(mx.mx1Df) # MX1-Content
<class 'pandas.core.frame.DataFrame'>
>>> type(mx.df) # MXS-Content
<class 'NoneType'>
>>> # ---
>>> # Read MXS
>>> # ---
>>> mx.setResultsToMxsFile() # looks for M-1-0-1.MXS in same Dir 
>>> type(mx.df) # MXS-Content
<class 'pandas.core.frame.DataFrame'>
>>> # ---
>>> # Write H5
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...      os.remove(mx.h5File)
>>> mx.ToH5() # M-1-0-1.h5 in same Dir 
>>> os.path.exists(mx.h5File)
True
>>> mx.ToH5() # M-1-0-1.h5 in same Dir is deleted if exists before written again
>>> os.path.exists(mx.h5File)
True
>>> # ---
>>> # Init with H5
>>> # ---
>>> mx=Mx(mx1File=mx1File) # looks for M-1-0-1.h5 in same Dir 
>>> # and reads the .h5 if newer than .MX1 and newer than an existing .MXS 
>>> type(mx.mx1Df) # MX1-Content
<class 'pandas.core.frame.DataFrame'>
>>> type(mx.df) # MXS-Content
<class 'pandas.core.frame.DataFrame'>
>>> # ---
>>> # Read MXS Zip
>>> # ---
>>> import zipfile # create the Zip first
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
>>> mx.setResultsToMxsZipFile() # looks for M-1-0-1.ZIP in same Dir
>>> type(mx.df) # MXS-Content
<class 'pandas.core.frame.DataFrame'>
>>> rowsMxs,colsMxs = mx.df.shape
>>> mx.df.index.is_unique # all setResultsTo... will ensure this uniqueness under all circumstances
True
>>> # uniqueness under all circumstances: also when add=True (setResultsTo... shall add the MXS-Content) is used
>>> # ---
>>> # Add same MXS (for testing ensuring uniqueness) 
>>> # ---
>>> oldShape=mx.df.shape
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # Add same MXS Zip (for testing ensuring uniqueness) 
>>> # ---
>>> mx.setResultsToMxsZipFile(add=True) # looks for M-1-0-1.ZIP in same Dir 
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # Read MXS Zip with overlapping Timestamps (for testing ensuring uniqueness) 
>>> # ---
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...      myzip.write(mx.mxsFile)  
...      myzip.write(mx.mxsFile,arcname=mx.mxsFile+'.2')  
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
...      timeStep=pd.Timestamp(0)-pd.Timestamp(0)
>>> mx.df.index=mx.df.index-(timeSpan+timeStep)
>>> # ---
>>> # Read MXS (with the original Timestamps)
>>> # ---
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
...      timeStep=pd.Timestamp(0)-pd.Timestamp(0)
>>> mx.df.index=mx.df.index+(timeSpan+timeStep)
>>> # ---
>>> # Read MXS (with the original Timestamps)
>>> # ---
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
>>> rowsNew,colsNew=mx.df.shape
>>> rowsNew==3*rowsOld
True
>>> colsNew==colsOld
True
>>> # ---
>>> # Dump (for testing purposes)
>>> # ---
>>> logger.debug("{0:s}: Shape before Dump: {1!s} Uniqueness: {2!s} First Time: {3!s} Last Time: {4!s}.".format('DOCTEST',mx.df.shape,mx.df.index.is_unique,mx.df.index[0],mx.df.index[-1])) 
>>> mx.dumpInMxsFormat() # dumps to .MXS.dump-File in same Dir
>>> rowsDump,colsDump = mx.df.shape
>>> # ---
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> mx.setResultsToMxsFile(mxsFile=mxsDumpFile)
>>> logger.debug("{0:s}: Shape after Reading Dump: {1!s} Uniqueness: {2!s} First Time: {3!s} Last Time: {4!s}.".format('DOCTEST',mx.df.shape,mx.df.index.is_unique,mx.df.index[0],mx.df.index[-1])) 
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
...     myzip.write(mxsDumpFile)  
>>> mx.setResultsToMxsZipFile()
>>> logger.debug("{0:s}: Shape after Reading Zip with original Mxs + Dump: {1!s} Uniqueness: {2!s} First Time: {3!s} Last Time: {4!s}.".format('DOCTEST',mx.df.shape,mx.df.index.is_unique,mx.df.index[0],mx.df.index[-1])) 
>>> rowsZip,colsZip = mx.df.shape
>>> rowsZip==rowsMxs+rowsDump
True
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...     os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...     os.remove(mx.mxsZipFile)
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
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


class MxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """
    Class Mx holds 2 Dataframes:
    the .MX1-File Definition    self.mx1Df and 
    the .MXS-File Data (if any) self.df.
    ---
    the .MXS-File Data: calculations results 
    index:   Timestamps 
             scenario time (UTC, not localized)
    columns: Values  
             The following (String-)ID - called Sir3sID - is used as Column-Label:
             OBJTYPE~NAME1~NAME2~NAME3~ATTRTYPE 
             A Sir3sID consists of ~ seperated MX1-File terms.
    """
    def __init__(self,mx1File=None,NoH5Read=False,NoMxsRead=False): 
        """
        (re-)initialize the Set with an MX1-File.
        ---
        NoH5Read False:
        If a .h5-File exists _parallel _and is newer than .MX1-File _and newer than an (_existing) .MXS-File:
            The .h5-File is read _instead of the .MX1-File
        ---
        NoMxsRead False:
        If a .MXS-File exists _parallel _and is newer than .MX1-File and .h5 is not read:
            The .MXS-File is read.           
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            if type(mx1File) == str:
                    self.mx1File=mx1File  
                    #check if mx1File exists ...
                    if not os.path.exists(self.mx1File): 
                        logStrFinal="{0:s}{1:s}: Not existing!".format(logStr,mx1File)                                 
                        raise XmError(logStrFinal)  
            else:
                    logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,mx1File)                                 
                    raise XmError(logStrFinal)     

            #Determine corresponding .MX2 Filename
            (wD,fileName)=os.path.split(self.mx1File)
            (base,ext)=os.path.splitext(fileName)
            self.mx2File=wD+os.path.sep+base+'.'+'MX2'        
                                          
            #Determine corresponding .h5 Filename
            self.h5File=wD+os.path.sep+base+'.'+'h5'        
            
            #Determine corresponding .MXS Filename
            self.mxsFile=wD+os.path.sep+base+'.'+'MXS'  
          
            #Determine corresponding .MXS Zip-Filename
            self.mxsZipFile=wD+os.path.sep+base+'.'+'ZIP'   

            #check if h5File exists parallel 
            if os.path.exists(self.h5File):  
                #check if h5File is newer
                mx1FileTime=os.path.getmtime(self.mx1File) 
                h5FileTime=os.path.getmtime(self.h5File)
                if(h5FileTime>mx1FileTime):
                    if os.path.exists(self.mxsFile):  
                        mxsFileTime=os.path.getmtime(self.mxsFile)
                        if(h5FileTime>mxsFileTime):
                            logger.debug("{0:s}h5File {1:s} exists _parallel _and is newer than mx1File {2:s} _and newer than mxsFile {3:s}:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of the mx1File.".format(logStr))   
                            h5Read=True
                        else:                                 
                            logger.debug("{0:s}h5File {1:s} exists _parallel but ===NO h5Read=== because mxsFile {2:s} newer.".format(logStr,self.h5File,self.mxsFile))     
                            h5Read=False  
                    else:
                        logger.debug("{0:s}h5File {1:s} exists _parallel _and is newer than mx1File {2:s} and there is no mxsFile like {3:s}:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                        logger.debug("{0:s}The h5File is read _instead of the mx1File.".format(logStr))   
                        h5Read=True  
                else:
                    logger.debug("{0:s}h5File {1:s} exists _parallel but ===NO h5Read=== because mx1File {2:s} is newer.".format(logStr,self.h5File,self.mx1File))     
                    h5Read=False
            else:
                h5Read=False

            self.df=None   
            self.mx1Df=None

            if not h5Read or NoH5Read:               
                self.__initWithMx1(mx1File)    
                if os.path.exists(self.mxsFile):  
                    mx1FileTime=os.path.getmtime(self.mx1File) 
                    mxsFileTime=os.path.getmtime(self.mxsFile)
                    if(mxsFileTime>mx1FileTime) and not NoMxsRead:
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
        (re-)builds MxRecordStructUnpackFmtString  
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

            #tsElement=MxRoot.find('./XL1[@OBJTYPE="ALLG"]/.[@ATTRTYPE="TIMESTAMP"]')
            #dfTsIdx = self.mx1Df.index[(self.mx1Df['OBJTYPE']=='ALLG') & (self.mx1Df['ATTRTYPE']=='TIMESTAMP')] 
            #self.channelTsIdx=dfTsIdx.tolist()[0] #channelNumber of the TimeStamp
            #logger.debug("{0:s}mx1File: {1:s}: channelNumber of the TimeStamp: {2:d}.".format(logStr,self.mx1File,self.channelTsIdx))    
            
            #Sir3sID
            sep='~'
            self.mx1Df['Sir3sID']=self.mx1Df['OBJTYPE']+sep+self.mx1Df['NAME1']+sep+self.mx1Df['NAME2']+sep+self.mx1Df['NAME3']+sep+self.mx1Df['ATTRTYPE']
            self.mx1Df['Sir3sID']=self.mx1Df['Sir3sID'].astype(str)

            #markVectorChannels
            self.mx1Df['isVectorChannel']=[True if int(cDLength/cDTypeLength)>1 else False for cDLength,cDTypeLength in zip(self.mx1Df['DATALENGTH'],self.mx1Df['DATATYPELENGTH'])] 
            #Bei Datenpunkten dieser Art muss zwischen Rohrvektor-Datenpunkten und  Vektor-Datenpunkten (zu denen auch die Vektor- Rohrvektor-Datenpunkte gehören) unterschieden werden. 
            #Die Rohrvektor-Datenpunkte enthalten DATALENGTH/ DATATYPELENGTH Werte an aufeinanderfolgenden äquidistanten Stützstellen am Rohr, beginnend am Rohranfang (KI) und endend am Rohrende (KK). 
            # Ein Vektordatenpunkt hingegen enthält die Attributwerte für alle Objekte eines Typs (z. B. alle Knotendrücke „KNOT.P“ oder die Rohrvektor-Drücke aller Rohre „ROHR.PVEC“). 
            # Ein Vektordatenpunkt ist dadurch gekennzeichnet, dass das 3. Bit (2²) im FELD FLAGS gesetzt ist und wird zusätzlich durch einen „*“  im Feld OBJTYPE_PK markiert.

            logger.debug("{0:s}mx1Df after some generated Columns: Shape: {1!s}.".format(logStr,self.mx1Df.shape))    

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

    def __buildMxRecordStructUnpackFmtString(self):
        """    
        (re-)builds mxRecordStructFmtString and releated stuff:      
            >self.mxRecordStructFmtString: struct.unpack(self.mxRecordStructFmtString,mxRecord)       
            >self.bytesUnpacked
            >self.mx1Df['unpackIdx']
            >self.mxColumnNames=[] 
            >self.idxTIMESTAMP
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

                if isVectorChannel:
                    toBeUnpacked=False
                else:
                    toBeUnpacked=True
                                                                                   
                cDType=row.DATATYPE 
                cDTypeLength=row.DATATYPELENGTH 
                cDLength=row.DATALENGTH 
                items=int(cDLength/cDTypeLength)
                
                if cDType=='CHAR':
                    if toBeUnpacked:   
                        unpackIdx.append(idxUnpack)    
                        if isVectorChannel:                                                                                  
                            for idx in range(items):
                                fmtItem+=(str(cDTypeLength)+'s') 
                            idxUnpack+=items                            
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
                            fmtItem=str(items)+'i'                    
                            idxUnpack+=items                           
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
                            fmtItem=str(items)+'f'                    
                            idxUnpack+=items                           
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
                        fmtItem=str(items)+'f'                    
                        idxUnpack+=items                             
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

            MxRecordLengthMx1=self.mx1Df['DATAOFFSET'].iloc[-1]+self.mx1Df['DATALENGTH'].iloc[-1] # Die Byte-Laenge des ganzen Ergebnisdatensatzes berechnet sich demnach aus DATAOFFSET+ DATALENGTH des letzten Datenpunktes der MX1    
            MxRecordLengthFmt=struct.calcsize(self.mxRecordStructFmtString)            
            if MxRecordLengthMx1 != MxRecordLengthFmt:
                logStrFinal="{0:s}Bytes per MX-Record from MX-Channels={1:d} <> Bytes from struct fmt-String for MX-Records={2:d}?! Error.".format(logStr,MxRecordLengthMx1,MxRecordLengthFmt)
                raise MxError(logStrFinal)    

            self.bytesUnpacked = MxRecordLengthFmt - bytesSkipped
            logger.debug("{0:s}Bytes per MX-Record={1:d}. Bytes Unpacked={2:d} (making up {3:06.2f} Bytes-%).".format(logStr,MxRecordLengthMx1,self.bytesUnpacked,self.bytesUnpacked/MxRecordLengthFmt*100))                                                  

            self.mx1Df['unpackIdx']=pd.Series(unpackIdx)
            self.mx1Df['unpackIdx']=self.mx1Df['unpackIdx'].astype('int64')      
            logger.debug("{0:s}mx1Df after generated Column: Shape: {1!s}.".format(logStr,self.mx1Df.shape))            
                        
            self.mxColumnNames=[] # used in Pandas 
            for idxChannel,idxUnpack in [(idxChannel,idxUnpack)  for idxChannel,idxUnpack in enumerate(self.mx1Df['unpackIdx']) if idxUnpack >=0]:                 
                sir3sID=self.mx1Df['Sir3sID'].iloc[idxChannel]
                idxUnpack=self.mx1Df['unpackIdx'].iloc[idxChannel]
                logger.debug("{0:s}Channel-Nr. {1:d} Sir3sID {2:s} idxUnpack {3:d}.".format(logStr,idxChannel,sir3sID,idxUnpack))  
                self.mxColumnNames.append(sir3sID)

            self.idxTIMESTAMP=self.mxColumnNames.index('ALLG~~~~TIMESTAMP')
            del self.mxColumnNames[self.idxTIMESTAMP] # remove Timestamp (index not value)

            logger.debug("{0:s}Columns (without Timestamp): {1:d}.".format(logStr,len(self.mxColumnNames)))                  
                                                                              
        except MxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def setResultsToMxsFile(self,mxsFile=None,add=False,maxRecords=None):
        """
        Sets or adds the MXS-Results to the set.          
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
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            # Mxs specification ...
            if mxsFile == None:
                logger.debug("{0:s}Mxs: Implicit specified ...".format(logStr))                                
                mxsFile=self.mxsFile
                       
            logger.debug("{0:s}Mxs: {1:s} ...".format(logStr,mxsFile))                
            with open(mxsFile,'rb') as f:
                 # Mxs exists ...
                logger.debug("{0:s}Mxs: {1:s} reading ...".format(logStr,mxsFile))                
                # Mxs reading ...
                dfMxs=self._readMxsFile(f,maxRecords=maxRecords)     
                           
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
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def setResultsToMxsZipFile(self,mxsZipFile=None,add=False,maxRecords=None):
        """
        Sets or adds the MXS-Results in the Zip to the set.                 
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
            
            # Zip reading ...              
            recsReadFromZip=0            
            dfZip=None
            for mxsFileName in sorted(z.namelist()):  
                # Mxs reading ...                        
                with z.open(mxsFileName,'r') as f: 
                    logger.debug("{0:s}Zip: {1:s}: {2:s} reading ...".format(logStr,mxsZipFile,mxsFileName))       
                    dfMxs=self._readMxsFile(f,maxRecords=maxRecords)

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
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def _readMxsFile(self,mxsFilePtr=None,maxRecords=None):
        """
        Returns the File-Content as df.  
        ---
        It is implied that the calculation results in the File originate from self.mx1File.  
        ---
        TIMESTAMP is used as index.
        ---
        df.index.is_unique 
        might be False 
        because of SIR 3S'
        1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:   
            df = None #Returns the File-Content as df.  
                                                       
            mxTimes=[]
            mxValues=[]           
            
            MxRecordLength=struct.calcsize(self.mxRecordStructFmtString)    
            if isinstance(maxRecords,int):
                maxRecordsLimit=True
            else:
                maxRecordsLimit=False   
                                         
            recsReadFromFile=0                                                          
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

                        # process record
                        try:
                            timeISO8601 = recordData[self.idxTIMESTAMP] #b'2017-10-20 00:00:00.000000+01:00'
                            time = pd.to_datetime(timeISO8601)                                              
                            values =recordData[0:self.idxTIMESTAMP] + recordData[self.idxTIMESTAMP+1:] # remove Timestamp (index not value)        
                            logger.debug("{0:s}Time read={1!s}: Values (without Timestamp): {2:d}.".format(logStr,time,len(values)))                                                             
                        except:
                            logStrFinal="{0:s}process record failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                                                                                                          
                                                  
                        # store record
                        try:
                            mxTimes.append(time)                         
                            mxValues.append(values)
                        except:
                            logStrFinal="{0:s}store record failed at Time={1!s}. Error.".format(logStr,timeISO8601)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                                   

                        # next record                            
                        recsReadFromFile+=1                               
                        if maxRecordsLimit:
                            if recsReadFromFile == maxRecords:
                                logger.debug("{0:s}maxRecords={1:d} read.".format(logStr,maxRecords))  
                                raise EOFError   
                                                   
                except EOFError:                    
                    logger.debug("{0:s}Last Time read={1!s}. File finished.".format(logStr,timeISO8601))                                                                                             
                except:
                    logStrFinal="{0:s}Last Time read={1!s}. Error.".format(logStr,timeISO8601)
                    logger.error(logStrFinal) 
                    raise MxError(logStrFinal)    
                                  
            logger.debug("{0:s}File finished: Records read={1:d}. Last Time read={2!s}. MB read={3:07.2f}. MB unpacked={4:07.2f} (making up {5:06.2f} %). ".format(logStr                                                                                                                                         
                                                                                                                                          ,recsReadFromFile
                                                                                                                                          ,timeISO8601
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

    def ToH5(self,h5File=None):
        """
        Stores both Dataframes 
        mx1Df h5Key: .../MX1 and 
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
                logger.debug("{0:s}{1:s}: Delete ...".format(logStr,h5File))     
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
                if isinstance(self.df,pd.core.frame.DataFrame):    
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MXS'  
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'df',h5Key))         
                    h5Store.put(h5Key,self.df)

            #regExpCompiledPerfWarnI=re.compile('ALLG~(\S*)~(\S*)~(\S*)~CVERSO|SNAPSHOTTYPE') 
            #perfWarnColsI=[column for column in self.pdf.columns if regExpCompiledPerfWarnI.search(column) != None]

            #regExpCompiledPerfWarnII=re.compile('(\S+)~(\S+)~(\S+)~(\S*)~RART') 
            #perfWarnColsII=[column for column in self.pdf.columns if regExpCompiledPerfWarnII.search(column) != None]

            #perfWarnCols=perfWarnColsI+perfWarnColsII
            #self.pdf.loc[:,perfWarnCols] =  self.pdf[ perfWarnCols].applymap(str)

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
        and 
        self.mx1Df (h5Key: .../MX1) and
        self.df    (h5Key: .../MXS) 
        are overwritten with the Dataframes in the h5File if any.     
        ---
        /MX1 in h5File:
        mxRecordStructUnpackFmtString and releated stuff is (re-)builded
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
                h5Keys=h5Store.keys()
                for h5Key in h5Keys:
                    h5KeySep='/'
                    match=re.search('('+h5KeySep+')(\w+$)',h5Key)
                    key=match.group(2)
                    if key == 'MX1':                            
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.mx1Df=h5Store[h5Key]
                        self.__buildMxRecordStructUnpackFmtString()      
                    if key == 'MXS':                           
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.df=h5Store[h5Key]

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

                for idx,row in enumerate(self.df.itertuples(index=False)):
                    values=list(row)
                    scenTime=self.df.index[idx]
                    scenTimeStr=scenTime.strftime("%Y-%m-%d %H:%M:%S.%f+01:00") 
                    values.insert(self.idxTIMESTAMP,scenTimeStr.encode('utf-8'))                   
                    bytes=struct.pack(self.mxRecordStructFmtString,*values)
                    f.write(bytes)      
               
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

        #mx=Mx(r'C:\3S\Modelle\WDMVV_FW\B1\V0\BZ1\M-1-0-1.MX1')
        #mx.setResultsToMxsFile()

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
