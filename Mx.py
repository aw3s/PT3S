"""
 SIR 3S MX-Interface.
 MX is a SIR 3S file based channel-oriented interface for SIR 3S calculation results.
 Modul contains classes useful for dealing with MX in Python.  
"""

import os
import shutil
import sys
import logging
logger = logging.getLogger(__name__)     
import argparse
import unittest
import doctest

import xml.etree.ElementTree as ET
import re
import struct
import collections
import zipfile
import pandas as pd

class MxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """
    Process Calculation Results from SIR 3S MX Files.
    A binary MXS File contains SIR 3S Calculations Results. 
    A Model Calculation-Run creates at least one MXS File (Result File).
    There is one MX1 File (an XML File) for each SIR 3S Model Calculation-Run.    
    This MX1 File defines a sequence of MX-Channels in XML. 
    And - as a result - the Byte-Layout of an MX-Record.
    A MXS File contains at least one MX-Record.
    """
    def __init__(self,mx1File=None 
                     ,unpackVectorChannels=False
                     ,channelsNotToBeProcessedSir3sIDRegExp=
                     [
                         r'(\S+)~(\S+)~(\S+)~(\S+)~*INST*'
                        ,r'^ROHR_VRTX' # surprise: not a VectorChannel?!
                        ,r'^ROHR~(\S+)~(\S+)~(\S*)~QM[I,K]{1}'
                        ,r'^VENT~(\S+)~(\S+)~(\S*)~OEFFNET'
                        ,r'^VENT~(\S+)~(\S+)~(\S*)~SCHLIESST'
                        ,r'^VENT~(\S+)~(\S+)~(\S*)~AUF'
                        ,r'^VENT~(\S+)~(\S+)~(\S*)~ZU'
                        ,r'^KNOT~(\S+)~(\S*)~(\S*)~T'
                        ,r'^KNOT~(\S+)~(\S*)~(\S*)~PDAMPF'
                        ,r'^KNOT~(\S+)~(\S*)~(\S*)~RHO'
                        ,r'^PUMP'
                        ,r'^PGRP'
                        ,r'^R\S+~(\S+)~(\S*)~(\S*)~X\S+'
                     ]):
        """
        Initialize an SIR 3S MX Calculation Result Set with an MX1 File. 
        >self.mx1File
        MX-Channels can be Vectors. Default is not to process (read) VectorChannels.
        Following (String-)ID - called Sir3sID - is used to identify an MX-Channel:
        OBJTYPE~NAME1~NAME2~NAME3~ATTRTYPE                
        channlesNot... is a list of RegExps of MX-Channels not to process (read).
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

        #FileNotFoundError
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
        Read the MX-Channel Definitions from the MX1 File.
        >self.mxChannels[]
        >self.mxChannelsSir3sIDs[]     
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        try:
            # XML Channel Def 
            Mx1Tree = ET.parse(self.mx1File)
            Mx1Root = Mx1Tree.getroot()
            self.mxChannels=Mx1Root.findall(r'XL1')
            logger.debug("{0:s}mx1File: {1:s}: MX-Channels={2:d}.".format(logStr,self.mx1File,len(self.mxChannels)))      

            # Sir3sID
            self.mxChannelsSir3sIDs=[]
            for idxChannel,mxChannel in enumerate(self.mxChannels):               
                sir3sID=self.__getSir3sID(idxChannel)
                self.mxChannelsSir3sIDs.append(sir3sID)

            # test if Sir3sID is unique
            duplicateSir3sIDs = [item for item, count in collections.Counter(self.mxChannelsSir3sIDs).items() if count > 1]
            for duplicateSir3sID in duplicateSir3sIDs:
                indices = [i for i, x in enumerate(self.mxChannelsSir3sIDs) if x == duplicateSir3sID]
                logger.debug("{0:s}mx1File: {1:s}: Sir3sID: {2:s} is NOT unique! NoDuplicates={3:s}.".format(logStr,self.mx1File,duplicateSir3sID,str(indices)))      
                
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
        finally:
            pass    
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
                cDTypeLength=int(mxChannel.get(r'DATATYPELENGTH'))
                cDLength=int(mxChannel.get(r'DATALENGTH'))
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
        Build the struct.unpack fmt-String: unpackedValues = struct.unpack(self.mxRecordStructUnpackFmtString,mxRecord)
        >self.mxRecordStructUnpackFmtString
        >self.mxRecordChannelsToStructMapping  
            a list [] of tuples:
                (idxChannel,idxUnpack)
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
                                                                                   
                cDType=mxChannel.get(r'DATATYPE')
                cDTypeLength=int(mxChannel.get(r'DATATYPELENGTH'))
                cDLength=int(mxChannel.get(r'DATALENGTH'))
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
                         logStrFinal="{0:s}sir3sID: {1:s}: UNKNOWN DATATYPE={2:s}. Skipped".format(logStr,sir3sID,cDType)     
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

    def getPdfFromMxsZipFile(self,mxsZipFile=None,maxRecords=None):
        """
        Returns a Pandas Data Frame.
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            if mxsZipFile == None:
                (WDir,Mx1FileName)=os.path.split(self.mx1File)
                (base,ext)=os.path.splitext(Mx1FileName)
                mxsZipFile=WDir+os.path.sep+base+'.'+'ZIP'
                           
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
            z = zipfile.ZipFile(mxsZipFile,'r')
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
            pdf = pd.DataFrame.from_records(mxValues,index=mxTimes,columns=mxColumnNames)              
            logger.debug("{0:s}{1:s}: pdf.head(10): {2!s}.".format(logStr,mxsFileName,pdf.head(10)))                  
                                
        #FileNotFoundError
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
            return pdf

if __name__ == "__main__":
    """.
    .
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
        parser = argparse.ArgumentParser()
        parser.add_argument("--mx1File",type=str, help=".mx1 File", default='./testdata/M-1-0-1.MX1')                        
        parser.add_argument("-v","--verbose", help="Debug Messages On", action="store_true")               
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)                   
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        mx = Mx(args.mx1File)
        pdf = mx.getPdfFromMxsZipFile()

        pass 
       
                                                     
    except:
        logger.error("{0:s}{1:s}".format(logStr,'logging.exception!')) 
        logging.exception('')  
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.')) 
        sys.exit(0)
