"""
SIR 3S MX-Interface (short: MX):
--------------------------------
MX is a SIR 3S file based, channel-oriented interface for SIR 3S calculation results.
Module Mx contains useful stuff to utilize MX (utilize SIR 3S calculation results) in pure Python.  
SIR 3S calculation results:
---------------------------
A binary MXS-File contains SIR 3S calculations results. 
A Model calculation run creates at least one MXS-File (Result-File).
There is one MX1-File (an XML-File) for each SIR 3S Model calculation run.    
This MX1-File defines in XML a sequence of MX-Channels. 
And - as a result - the Byte-Layout of a single MX-Record.
A MX-Record contains calculation results for one Timestamp.
A MXS-File contains at least one MX-Record.
"""

import os
import sys
import logging
logger = logging.getLogger(__name__)     
import argparse
import unittest
import timeit

import xml.etree.ElementTree as ET
import re
import struct
import collections
import zipfile
import pandas as pd
import h5py

class MxTest(unittest.TestCase):

    WithTimeItTests=False

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01__init__FileNotFoundError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="Mx(mx1File='./testdata/None.MX1')"):
                Mx(mx1File='./testdata/None.MX1')
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_02__init__OsError(self):     
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="Mx(mx1File=666)"):
                Mx(mx1File=666)
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_03__init__TypeError(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        with self.assertLogs(logger=logger,level='ERROR')as cm:     
            with self.assertRaises(MxError,msg="Mx()"):
                Mx()
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_04__init__ParseError(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        with self.assertLogs(logger=logger,level='ERROR')as cm:     
            with self.assertRaises(MxError,msg="Mx(mx1File='./testdata/M-1-0-1.txt')"):
                Mx(mx1File='./testdata/M-1-0-1.txt')  
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    @unittest.skipIf(WithTimeItTests==False,"test_21__init__timeit")
    def test_21__init__timeit(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))                 
        t=timeit.timeit(stmt="Mx.Mx(mx1File='./testdata/M-1-0-1.MX1')",setup="import Mx",number=1)                      
        logger.debug("{0:s}Timeit: Mx.Mx(mx1File='./testdata/M-1-0-1.MX1':{1:06.2f}s".format(logStr,t))         
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    

    def test_21__init__(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='INFO') as cm:                                
            MxTest.mx=Mx(mx1File='./testdata/M-1-0-1.MX1')            
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_41_initMxsZip_FileNotFoundError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/None.ZIP')"):
                MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/None.ZIP')                              
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_42_initMxsZip_OsError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="MxTest.mx.setResultsToMxsZipfile(mxsZipFile=666)"):
                MxTest.mx.setResultsToMxsZipfile(mxsZipFile=666)                              
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def test_44_initMxsZip_ZipError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/M-1-0-1.txt')"):
                MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/M-1-0-1.txt')                              
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def test_51_setResultsToMxsZipfile(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='INFO') as cm:                 
            MxTest.mx.setResultsToMxsZipfile()
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_52_wrtResultsToH5File(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))     
        
        wD,base,ext = MxTest.mx.getMx1FilenameSplit()
        h5Filename=wD+os.path.sep+base+'.'+'h5'    # ./testdata\M-1-0-1.h5
        if os.path.exists(h5Filename):                        
            logger.debug("{0:s}{1:s}: Delete ...".format(logStr,h5Filename))     
            os.remove(h5Filename)

        MxTest.mx.wrtResultsToH5File()

        self.assertTrue(os.path.exists(h5Filename),msg='os.path.exists({0!s})'.format(h5Filename))        

        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
        
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

        
class MxTestH5(unittest.TestCase):

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01_readFromH5(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))  
        
        with pd.HDFStore('./testdata/M-1-0-1.h5')  as h5Store:
        
            keys=h5Store.keys()
            h5Key=keys[0]
            #MxTestH5.df = pd.read_hdf(h5Store,h5Key)  
            MxTestH5.df=h5Store[h5Key]
            metadata=h5Store.get_storer(h5Key).attrs.metadata

        for r in metadata:             
            setattr(MxTestH5.df,r,metadata[r])

        logger.debug("{0:s}df.head(10): {1!s}.".format(logStr,MxTestH5.df.head(10)))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
        
        
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """
    Class Mx holds a MX1-File defined SIR 3S calculation result set in a pandas DataFrame (self.pdf).
    --------------------------------------------------------------------------------------
    __init__:
    ---------
    (re-)initializes the set with a MX1-File. 
    setResultsToMxsZipfile:
    ------------------
    equalizes self.pdf to the results in the Zip  
    --------------------------------------------------------------------------------------
    pandas DataFrame:
    -----------------
    index: Timestamps (UTC, not localized) - scenario time; 1st Channel in MX-Record
    ---
    columns: >= 2nd Channel in MX-Record  
    ---
    The following (String-)ID - called Sir3sID - is used as column-label:
    OBJTYPE~NAME1~NAME2~NAME3~ATTRTYPE 
    A Sir3sID consists of ~ seperated MX1-File terms.
    """
    def __init__(self,mx1File=None 
                     ,unpackVectorChannels=False
                     ,channelsNotToBeProcessedSir3sIDRegExp=
                     [
                         '(\S+)~(\S+)~(\S+)~(\S+)~*INST*'
                        ,'^ROHR_VRTX' # surprise: not a VectorChannel?!
                        ,'^ROHR~(\S+)~(\S+)~(\S*)~QM[I,K]{1}'
                        ,'^VENT~(\S+)~(\S+)~(\S*)~OEFFNET'
                        ,'^VENT~(\S+)~(\S+)~(\S*)~SCHLIESST'
                        ,'^VENT~(\S+)~(\S+)~(\S*)~AUF'
                        ,'^VENT~(\S+)~(\S+)~(\S*)~ZU'
                        ,'^KNOT~(\S+)~(\S*)~(\S*)~T'
                        ,'^KNOT~(\S+)~(\S*)~(\S*)~PDAMPF'
                        ,'^KNOT~(\S+)~(\S*)~(\S*)~RHO'
                        ,'^PUMP'
                        ,'^PGRP'
                        ,'^R\S+~(\S+)~(\S*)~(\S*)~X\S+'
                     ]):
        """
        __init__:
        ---------
        (re-)initialize the set with the MX1-File. 
        ---------
        >self.mx1File       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            with open(mx1File,'r') as f: 
                pass
            self.mx1File=mx1File  
            logger.debug("{0:s}mx1File: {1:s}.".format(logStr,self.mx1File))     
            self.__readMxChannelDefinitions()
            self.__evalMxChannelsToBeProcessed(unpackVectorChannels,channelsNotToBeProcessedSir3sIDRegExp)
            self.__buildMxRecordStructUnpackFmtString()      
            self.pdf=None                    
       
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

    def __readMxChannelDefinitions(self):
        """
        Read the MX-Channel Definitions from the MX1-File.
        >self.mxChannels[]
        >self.mxChannelsSir3sIDs[]     
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            # XML Channel Def 
            try:
                Mx1Tree = ET.parse(self.mx1File)
            except:
                logStrFinal="{0:s}mx1File: {1:s}: ET.parse: Error.".format(logStr,self.mx1File)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)      

            Mx1Root = Mx1Tree.getroot()
            self.mxChannels=Mx1Root.findall('XL1')
            logger.info("{0:s}mx1File: {1:s}: MX-Channels={2:d}.".format(logStr,self.mx1File,len(self.mxChannels)))      

            # Sir3sID
            self.mxChannelsSir3sIDs=[]
            for idxChannel,mxChannel in enumerate(self.mxChannels):               
                sir3sID=self.__getSir3sID(idxChannel)
                self.mxChannelsSir3sIDs.append(sir3sID)

            # test if Sir3sID is unique
            duplicateSir3sIDs = [item for item, count in collections.Counter(self.mxChannelsSir3sIDs).items() if count > 1]
            for duplicateSir3sID in duplicateSir3sIDs:
                indices = [i for i, x in enumerate(self.mxChannelsSir3sIDs) if x == duplicateSir3sID]
                logger.debug("{0:s}mx1File: {1:s}: Sir3sID: {2:s} is NOT unique! NoOfDuplicates={3:s}.".format(logStr,self.mx1File,duplicateSir3sID,str(indices)))      
                
            if len(duplicateSir3sIDs)>0:
                logStrFinal="{0:s}mx1File: {1:s}: Sir3sIDs are not unique! Error.".format(logStr,self.mx1File)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)      

        except MxError:
            raise                      
        except:
            logStrFinal="{0:s}mx1File: {1:s}: Error.".format(logStr,self.mx1File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                 
        else:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __evalMxChannelsToBeProcessed(self
                                  ,unpackVectorChannels=True
                                  ,channelsNotToBeProcessedSir3sIDRegExp=None):
        """              
        >self.mxChannelsToBeProcessed[]
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
                      
            # mark Channels to be processed
            self.mxChannelsToBeProcessed=[]
            # aspect unpackVectorChannels
            for idxChannel,mxChannel in enumerate(self.mxChannels):
                Sir3sID=self.mxChannelsSir3sIDs[idxChannel]
                cDTypeLength=int(mxChannel.get('DATATYPELENGTH'))
                cDLength=int(mxChannel.get('DATALENGTH'))
                items=int(cDLength/cDTypeLength)
                if items>1 and not unpackVectorChannels:
                    self.mxChannelsToBeProcessed.append(False)
                    logger.debug("{0:s}MX-Channel: {1:s} will NOT be processed because not unpackVectorChannels matches.".format(logStr,Sir3sID))      
                else:
                    self.mxChannelsToBeProcessed.append(True)

            # aspect RegExp
            channelsNotToBeProcessedSir3sIDRegExpCompiled=[]
            for idx, regExp in enumerate(channelsNotToBeProcessedSir3sIDRegExp):
                regExpCompiled=re.compile(regExp)
                channelsNotToBeProcessedSir3sIDRegExpCompiled.append(regExpCompiled)
            
            for idxChannel,Sir3sID in enumerate(self.mxChannelsSir3sIDs):
                if not self.mxChannelsToBeProcessed[idxChannel]:
                    continue
                tbProcessed=True
                for idxRegExp, regExpCompiled in enumerate(channelsNotToBeProcessedSir3sIDRegExpCompiled):
                    m=regExpCompiled.search(Sir3sID)
                    if m != None:
                        tbProcessed=False
                        logger.debug("{0:s}MX-Channel: {1:s} will NOT be processed because -v regExp {2:s} matches.".format(logStr,Sir3sID,channelsNotToBeProcessedSir3sIDRegExp[idxRegExp]))      
                        break
                self.mxChannelsToBeProcessed[idxChannel]=tbProcessed

            for idxChannel,Sir3sID in enumerate(self.mxChannelsSir3sIDs):
                if self.mxChannelsToBeProcessed[idxChannel]:
                    logger.debug("{0:s}MX-Channel: {1:s} will be processed.".format(logStr,Sir3sID))      
            idxList = [i for i in range(len(self.mxChannelsToBeProcessed)) if self.mxChannelsToBeProcessed[i]]
            logger.info("{0:s}{1:d} from {2:d} MX-Channels will be processed (making up {3:06.2f} Channel-%).".format(logStr,len(idxList),len(self.mxChannels),len(idxList)/len(self.mxChannels)*100))            
           
        except:
            logStrFinal="{0:s}mx1File: {1:s}: Error.".format(logStr,self.mx1File)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                 
        else:           
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __getSir3sID(self,mxChannelIdx=0):
        """
        Returns the Sir3sID (a String) for the MX-Channel Idx.
        """

        return self.mxChannels[mxChannelIdx].get('OBJTYPE')+'~'+self.mxChannels[mxChannelIdx].get('NAME1')+'~'+self.mxChannels[mxChannelIdx].get('NAME2')+'~'+self.mxChannels[mxChannelIdx].get('NAME3')+'~'+self.mxChannels[mxChannelIdx].get('ATTRTYPE')                

    def __buildMxRecordStructUnpackFmtString(self):
        """        
        >self.mxRecordStructUnpackFmtString: struct.unpack(self.mxRecordStructUnpackFmtString,mxRecord)
        >self.mxRecordChannelsToStructMapping: [(idxChannel,idxUnpack),...]  
        >self.bytesUnpacked
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            self.mxRecordStructUnpackFmtString=''
            self.mxRecordChannelsToStructMapping=[]
            idxUnpack=0
            bytesSkipped=0

            for idxChannel,mxChannel in enumerate(self.mxChannels):

                fmtItem='' # End of Loop: self.mxRecordStructUnpackFmtString+=fmtItem

                sir3sID=self.mxChannelsSir3sIDs[idxChannel]
                toBeUnpacked=self.mxChannelsToBeProcessed[idxChannel]
                                                                                   
                cDType=mxChannel.get('DATATYPE')
                cDTypeLength=int(mxChannel.get('DATATYPELENGTH'))
                cDLength=int(mxChannel.get('DATALENGTH'))
                items=int(cDLength/cDTypeLength)

                if items>1:
                    isVectorChannel=True
                else:
                    isVectorChannel=False
                
                if cDType=='CHAR':
                    if toBeUnpacked:
                        self.mxRecordChannelsToStructMapping.append((idxChannel,idxUnpack))             
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
                                                    
                elif cDType=='INT4':    
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        self.mxRecordChannelsToStructMapping.append((idxChannel,idxUnpack))             
                        if isVectorChannel:                                                                                                                                                                                                                                                                                            
                            fmtItem=str(items)+'i'                    
                            idxUnpack+=items                           
                        else:                            
                            fmtItem='i'                         
                            idxUnpack+=1    
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'                                      
                            
                elif cDType=='REAL':
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        self.mxRecordChannelsToStructMapping.append((idxChannel,idxUnpack))             
                        if isVectorChannel:                                                                                                                                                                                                                                                                                            
                            fmtItem=str(items)+'f'                    
                            idxUnpack+=items                           
                        else:                            
                            fmtItem='f'                         
                            idxUnpack+=1    
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'
                                                                                     
                elif cDType=='RVEC':
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        self.mxRecordChannelsToStructMapping.append((idxChannel,idxUnpack))                                                                                                                                                                                                                                                                                                                                
                        fmtItem=str(items)+'f'                    
                        idxUnpack+=items                             
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'
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
                    
                self.mxRecordStructUnpackFmtString+=fmtItem

            MxRecordLengthMx1=int(self.mxChannels[-1].get('DATAOFFSET'))+int(self.mxChannels[-1].get('DATALENGTH'))
            MxRecordLengthFmt=struct.calcsize(self.mxRecordStructUnpackFmtString)            
            if MxRecordLengthMx1 != MxRecordLengthFmt:
                logStrFinal="{0:s}Bytes per MX-Record from MX-Channels={1:d} <> Bytes from struct fmt-String for MX-Records={2:d}?! Error.".format(logStr,MxRecordLengthMx1,MxRecordLengthFmt)
                raise MxError(logStrFinal)    

            self.bytesUnpacked = MxRecordLengthFmt - bytesSkipped
            logger.info("{0:s}Bytes per MX-Record={1:d}. Bytes Unpacked={2:d} (making up {3:06.2f} Bytes-%).".format(logStr,MxRecordLengthMx1,self.bytesUnpacked,self.bytesUnpacked/MxRecordLengthFmt*100))                                                  

        except MxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def getMx1FilenameSplit(self):
        """
        Returns wD,base,ext of the MX1-File.
        MX1-Filename: wD+os.path.sep+base+'.'+ext         
        """
        (wD,Mx1FileName)=os.path.split(self.mx1File)
        (base,ext)=os.path.splitext(Mx1FileName)
        return wD,base,ext        

    def setResultsToMxsZipfile(self,mxsZipFile=None,maxRecords=None):
        """
        Equalizes self.pdf to the results in the Zip.  
        ---
        Implicit specified is a Zip-File .ZIP in the same directory as the MX1-File .MX1.  
        ---
        It is implied that all calculation results in the Zip-File originate from the same MX1-File -  
        from self.mx1File - and from the same Model operated with different input data at different scenario times.
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            if mxsZipFile == None:
                wD,base,ext = self.getMx1FilenameSplit() 
                mxsZipFile=wD+os.path.sep+base+'.'+'ZIP'
                           
            with open(mxsZipFile,'rb') as f:   
                pass     
       
            # ... some Work tbd before reading the Zip ...                                  
            mxTimes=[]
            mxValues=[]           
            mxColumnNames=[] # used in Pandas
            for idx, (idxChannel,idxStruct) in enumerate(self.mxRecordChannelsToStructMapping):                               
                mxColumnNames.append(self.mxChannelsSir3sIDs[idxChannel])
            del mxColumnNames[0] # remove Timestamp (index not value)
            MxRecordLength=struct.calcsize(self.mxRecordStructUnpackFmtString)    
            if isinstance(maxRecords,int):
                maxRecordsLimit=True
            else:
                maxRecordsLimit=False   

            # reading the Zip ...
            logger.debug("{0:s}Zip: {1:s} ...".format(logStr,mxsZipFile)) 
            try:
                z = zipfile.ZipFile(mxsZipFile,'r')
            except:
                logStrFinal="{0:s}{1:s}: reading the Zip failed. Error.".format(logStr,mxsZipFile)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)   
                               
            recsReadFromZip=0
            for mxsFileName in sorted(z.namelist()):
                logger.debug("{0:s}{1:s} ...".format(logStr,mxsFileName))                                                        
                with z.open(mxsFileName,'r') as f: 
                    try:
                        recsReadFromZipFile=0
                        while True:   # while f.tell() != os.fstat(f.fileno()).st_size does NOT work with Zip's file objects ...    
                            
                            # read record 
                            try: 
                                record=f.read(MxRecordLength)
                                recordData = struct.unpack(self.mxRecordStructUnpackFmtString,record)  
                            except:
                                logger.debug("{0:s}{1:s}: record=f.read(MxRecordLength) failed (EOF probably).".format(logStr,mxsFileName))  
                                raise EOFError
                            else:
                                timeISO8601=None

                            # process record
                            try:
                                timeISO8601 = recordData[0]
                                time = pd.to_datetime(timeISO8601)                               
                                values = recordData[1:]                                                           
                            except:
                                logStrFinal="{0:s}{1:s}: process record failed. Error.".format(logStr,mxsFileName)
                                logger.error(logStrFinal) 
                                raise MxError(logStrFinal)                                                                                                          
                                                  
                            # store record
                            try:
                                mxTimes.append(time)                         
                                mxValues.append(values)
                            except:
                                logStrFinal="{0:s}{1:s}: store record failed at Time={2!s}. Error.".format(logStr,mxsFileName,timeISO8601)
                                logger.error(logStrFinal) 
                                raise MxError(logStrFinal)                                   

                            # next record                            
                            recsReadFromZipFile+=1                               
                            if maxRecordsLimit:
                                if recsReadFromZipFile == maxRecords:
                                    logger.debug("{0:s}{1:s}: maxRecords={2:d} read.".format(logStr,mxsFileName,maxRecords))  
                                    raise EOFError   
                                                   
                    except EOFError:
                        recsReadFromZip+=recsReadFromZipFile
                        logger.debug("{0:s}{1:s}: Last Time read={2!s}. File finished.".format(logStr,mxsFileName,timeISO8601))                                                                                             
                    except:
                        logStrFinal="{0:s}{1:s}: Last Time read={2!s}. Error.".format(logStr,mxsFileName,timeISO8601)
                        logger.error(logStrFinal) 
                        raise MxError(logStrFinal)    
                                  
            logger.info("{0:s}Zip: {1:s}: finished: Records read={2:d}. Last Time read={3!s}. MB read={4:07.2f}. MB unpacked={5:07.2f} (making up {6:06.2f} %). ".format(logStr
                                                                                                                                          ,mxsZipFile
                                                                                                                                          ,recsReadFromZip
                                                                                                                                          ,timeISO8601
                                                                                                                                          ,recsReadFromZip*MxRecordLength/pow(10,6)
                                                                                                                                          ,recsReadFromZip*self.bytesUnpacked/pow(10,6)
                                                                                                                                          ,self.bytesUnpacked/MxRecordLength*100
                                                                                                                                                 )
                        )                                                                     
            self.pdf = pd.DataFrame.from_records(mxValues,index=mxTimes,columns=mxColumnNames)              
            logger.debug("{0:s}{1:s}: pdf.head(10): {2!s}.".format(logStr,mxsFileName,self.pdf.head(10)))                  

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
            return self.pdf

    def wrtResultsToH5File(self,h5File=None):
        """
        Writes self.pdf to the h5File.  
        Implicit specified is a .h5-File in the same directory as the .mx1-File.  
        ---
        The h5Key used imitates a relative path from .h5 to .mx1.        
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            wD,base,ext = self.getMx1FilenameSplit()
            if h5File == None:
                h5File=wD+os.path.sep+base+'.'+'h5'

            # h5Key
            # '__/M_1_0_1' if .mx1-File is in parent dir
            # 'M_1_0_1' if .mx1-File is in same dir
            relPath=os.path.relpath(os.path.normpath(self.mx1File),start=os.path.normpath(h5File))
            h5Key=re.sub('-','_'
                    ,re.sub('\.','_'
                           ,re.sub('^/',''
                                   ,re.sub('.mX1',''
                                                 ,re.sub('^\.{2}','',re.sub(r'\\+','/',relPath))
                                                 ,flags=re.IGNORECASE                                                  
                                           )
                                   )
                           )
                        )
                        
            logger.debug("{0:s}pd.HDFStore({1:s}) ...".format(logStr,h5File))                 
            with pd.HDFStore(h5File) as h5Store:               
                logger.debug("{0:s}{1:s}: write data with key={2:s} ...".format(logStr,h5File,h5Key))     
                #self.pdf.to_hdf(h5Store,h5Key,mode='w') 
                h5Store.put(h5Key,self.pdf)
                logger.debug("{0:s}{1:s}: write data with key={2:s} ... done.".format(logStr,h5File,h5Key))    
                metadata = dict(mx1File=relPath)
                h5Store.get_storer(h5Key).attrs.metadata=metadata
                logger.debug("{0:s}{1:s}: write metadata={2!s} done.".format(logStr,h5File,metadata))     

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

if __name__ == "__main__":
    """
    Run Mx-Stuff or/and perform Mx-Unittests.
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
        parser = argparse.ArgumentParser(description='Run Mx-Stuff or/and perform Mx-Unittests.'
        ,epilog='''
        UsageExample#1: (without parameter): -v -u --x ./testdata/M-1-0-1.MX1 --z ./testdata/M-1-0-1.ZIP      
        '''                                 
        )
        parser.add_argument('--x','--mx1File',type=str, help='.mx1 File (default: ./testdata/M-1-0-1.MX1)',default='./testdata/M-1-0-1.MX1')  

        group = parser.add_mutually_exclusive_group()                
        group.add_argument('--z','--mxsZipFile',type=str, help='parse .zip File (default: ./testdata/M-1-0-1.ZIP)',default='./testdata/M-1-0-1.ZIP')  
        group.add_argument('--s','--mxsFile',type=str, help='parse .mxs File (default: ./testdata/M-1-0-1.MXS)',default='./testdata/M-1-0-1.MXS')  
        group.add_argument('-a',help='parse all .mxs Files in MX1-Directory - NIY',action="store_true",default=False)    
        group.add_argument('--r','--regExp',type=str,help='parse all Files (.mxs, .zip) in MX1-Directory matching RegExp - NIY',default=False)   
        
        group = parser.add_mutually_exclusive_group()                   
        group.add_argument("-u","--unittest", help="Perform all Mx-Unittests", action="store_true",default=True)   
        group.add_argument("-w","--unittestH5", help="Perform Mx-Unittests starting from read H5", action="store_true",default=False)   

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")                  
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        if args.unittestH5:
            #suite=unittest.TestSuite()
            #suite.addTest(MxTestH5('test_01_readFromH5'))
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(MxTestH5)
            unittest.TextTestRunner().run(suite)           
        elif args.unittest:
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(MxTest)
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(MxTestH5))
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

