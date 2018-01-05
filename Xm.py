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

                self.__vLFKT()
                self.__vQVAR()
                
                self.__vFWVB()
                self.__vVKNO()
                self.__vKNOT()
                
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
        except MemoryError as e:
            logStrFinal="{0:s}xmlFile: {1!s}: MemoryError. In Notebook: Try: Kernel/Restart.".format(logStr,self.xmlFile)
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

            self.dataFrames['QVAR_ROWT'].ZEIT=self.dataFrames['QVAR_ROWT'].ZEIT.str.replace(',', '.')
            self.dataFrames['QVAR_ROWT'].QM=self.dataFrames['QVAR_ROWT'].QM.str.replace(',', '.')

            self.dataFrames['SWVT_ROWT']=self.dataFrames['SWVT_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
            self.dataFrames['LFKT_ROWT']=self.dataFrames['LFKT_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
            self.dataFrames['QVAR_ROWT']=self.dataFrames['QVAR_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
                      
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __vLFKT(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.vLFKT=pd.merge(self.dataFrames['LFKT'],self.dataFrames['LFKT_ROWT'],left_on='pk',right_on='fk')
            self.vLFKT['ZEIT']=pd.to_numeric(self.vLFKT['ZEIT']) 
            self.vLFKT['LF']=pd.to_numeric(self.vLFKT['LF']) 
            self.vLFKT['ZEIT_RANG']=self.vLFKT.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vLFKT_gLF=self.vLFKT.groupby(['pk_x'], as_index=False).agg({'LF':[np.min,np.max]})
            vLFKT_gLF.columns= [tup[0]+tup[1] for tup in zip(vLFKT_gLF.columns.get_level_values(0),vLFKT_gLF.columns.get_level_values(1))]
            vLFKT_gLF=vLFKT_gLF.rename(columns={'LFamin':'LF_min','LFamax':'LF_max'})
            #
            self.vLFKT=pd.merge(self.vLFKT,vLFKT_gLF,left_on='pk_x',right_on='pk_x')
            #
            self.vLFKT=self.vLFKT[self.vLFKT['ZEIT_RANG']==1]
            #
            self.vLFKT=self.vLFKT[['NAME','BESCHREIBUNG','LF','LF_min','LF_max','INTPOL','ZEITOPTION','pk_x']]
                                 
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    

    def __vSWVT(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.vSWVT=pd.merge(self.dataFrames['SWVT'],self.dataFrames['SWVT_ROWT'],left_on='pk',right_on='fk')
            self.vSWVT['ZEIT']=pd.to_numeric(self.vSWVT['ZEIT']) 
            self.vSWVT['W']=pd.to_numeric(self.vSWVT['W']) 
            self.vSWVT['ZEIT_RANG']=self.vSWVT.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vSWVT_g=self.vSWVT.groupby(['pk_x'], as_index=False).agg({'W':[np.min,np.max]})
            vSWVT_g.columns= [tup[0]+tup[1] for tup in zip(vSWVT_g.columns.get_level_values(0),vSWVT_g.columns.get_level_values(1))]
            vSWVT_g=vSWVT_g.rename(columns={'Wamin':'W_min','Wamax':'W_max'})
            #
            self.vSWVT=pd.merge(self.vSWVT,vSWVT_g,left_on='pk_x',right_on='pk_x')
            #
            self.vSWVT=self.vSWVT[self.vSWVT['ZEIT_RANG']==1]
            #
            self.vSWVT=self.vSWVT[['NAME','BESCHREIBUNG','W','W_min','W_max','INTPOL','ZEITOPTION','pk_x']]
                                 
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def __vQVAR(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.vQVAR=pd.merge(self.dataFrames['QVAR'],self.dataFrames['QVAR_ROWT'],left_on='pk',right_on='fk')
            self.vQVAR['ZEIT']=pd.to_numeric(self.vQVAR['ZEIT']) 
            self.vQVAR['QM']=pd.to_numeric(self.vQVAR['QM']) 
            self.vQVAR['ZEIT_RANG']=self.vQVAR.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vQVAR_gQM=self.vQVAR.groupby(['pk_x'], as_index=False).agg({'QM':[np.min,np.max]})
            vQVAR_gQM.columns= [tup[0]+tup[1] for tup in zip(vQVAR_gQM.columns.get_level_values(0),vQVAR_gQM.columns.get_level_values(1))]
            vQVAR_gQM=vQVAR_gQM.rename(columns={'QMamin':'QM_min','QMamax':'QM_max'})
            #
            self.vQVAR=pd.merge(self.vQVAR,vQVAR_gQM,left_on='pk_x',right_on='pk_x')
            #
            self.vQVAR=self.vQVAR[self.vQVAR['ZEIT_RANG']==1]
            #
            self.vQVAR=self.vQVAR[['NAME','BESCHREIBUNG','QM','QM_min','QM_max','INTPOL','ZEITOPTION','pk_x']]
                                 
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            
    def __vFWVB(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            self.vFWVB=pd.merge(self.dataFrames['FWVB'],self.dataFrames['FWVB_BZ'],left_on='pk',right_on='fk')
            #
            self.vFWVB=self.vFWVB[self.vFWVB['W0'].notnull()]
            self.vFWVB['W0']=self.vFWVB['W0'].str.replace(',', '.')
            self.vFWVB['W0']=pd.to_numeric(self.vFWVB['W0']) 
            #
            self.vFWVB['LFK']=pd.to_numeric(self.vFWVB['LFK']) 
            self.vFWVB['TVL0']=pd.to_numeric(self.vFWVB['TVL0']) 
            self.vFWVB['TRS0']=pd.to_numeric(self.vFWVB['TRS0'])  
            self.vFWVB['INDTR']=pd.to_numeric(self.vFWVB['INDTR'])  
            self.vFWVB['TRSK']=pd.to_numeric(self.vFWVB['TRSK'])  
            self.vFWVB['VTYP']=pd.to_numeric(self.vFWVB['VTYP'])  
            self.vFWVB['IMBG']=pd.to_numeric(self.vFWVB['IMBG']) 
            self.vFWVB['IRFV']=pd.to_numeric(self.vFWVB['IRFV']) 
            
            #
            self.vFWVB=pd.merge(self.vFWVB,self.vLFKT,left_on='fkLFKT',right_on='pk_x')
            #
            self.vFWVB['W']      = self.vFWVB.apply(lambda row: row.LF     * row.W0, axis=1)
            self.vFWVB['W_min']  = self.vFWVB.apply(lambda row: row.LF_min * row.W0, axis=1)
            self.vFWVB['W_max']  = self.vFWVB.apply(lambda row: row.LF_max * row.W0, axis=1)
            #
            self.vFWVB=self.vFWVB[[
                    'BESCHREIBUNG_x','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                   ,'W','W_min','W_max'
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                   ,'pk_x_x','tk'
                   ,'NAME','BESCHREIBUNG_y'
                 ]]
                               
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                

    def __vVKNO(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            pass
            self.vVKNO=pd.merge(self.dataFrames['VKNO'],self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            self.vVKNO=pd.merge(self.vVKNO,self.dataFrames['KNOT'],left_on='fkKNOT',right_on='pk')

            self.vVKNO=self.vVKNO[[
               'NAME_x'     
              ,'NAME_y'     
              ,'KTYP'
              ,'fkCONT_x','fkKNOT'
              ,'LFAKT','QM_EIN'  
            ]]
            self.vVKNO=self.vVKNO.rename(columns={'NAME_x':'CONT','NAME_y':'NAME','fkCONT_x':'fkCONT'})
                               
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    def __vKNOT(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            pass
            self.vKNOT=pd.merge(self.dataFrames['KNOT'],self.dataFrames['KNOT_BZ'],left_on='pk',right_on='fk')
            self.vKNOT=pd.merge(self.vKNOT,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            self.vKNOT=pd.merge(self.vKNOT,self.vVKNO,left_on='pk_x',right_on='fkKNOT',how='left')

            self.vKNOT=self.vKNOT[[
                    'NAME_x'
                   ,'BESCHREIBUNG','IDREFERENZ'
                   ,'NAME_y'
                   ,'CONT' # vVKNO
                   ,'KTYP_x'
                   ,'LFAKT_x','QM_EIN_x','fkQVAR'       
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                ]]
            self.vKNOT=self.vKNOT.rename(columns={'NAME_x':'NAME','NAME_y':'CONT','KTYP_x':'KTYP','LFAKT_x':'LFAKT','QM_EIN_x':'QM_EIN','CONT':'CONT_VKNO'})

            self.vKNOT=pd.merge(self.vKNOT,self.vQVAR,left_on='fkQVAR',right_on='pk_x',how='left')
            self.vKNOT=self.vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'QVAR'})

            self.vKNOT=self.vKNOT[[
                    'NAME'
                   ,'BESCHREIBUNG','IDREFERENZ'
                   ,'CONT'
                   ,'CONT_VKNO' # vVKNO
                   ,'KTYP'
                   ,'LFAKT','QM_EIN','QVAR','QM','QM_min','QM_max'     
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                ]]
          
        except:
            logStrFinal="{0:s}Error.".format(logStr)
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

