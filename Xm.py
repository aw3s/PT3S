"""
SIR 3S XML ModelFile To pandas DataFrames
        One DataFrame per SIR 3S Objecttype 
Some Views As pandas DataFrames
        The Views are designed to deal with tedious groundwork 
        Views are aggregated somhwat arbitrary ...
        ... however usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views 
---------------------------
DOCTEST
---------------------------
# ---
# Imports
# ---
>>> import os
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(r'testdata\OneLPipe.h5'):                        
...    os.remove(r'testdata\OneLPipe.h5')
>>> # ---
>>> # Init
>>> # ---
>>> xmlFile=r'testdata\OneLPipe.XML'
>>> xm=Xm(xmlFile=xmlFile)
>>> # ---
>>> # a View
>>> # ---
>>> v='vKNOT'
>>> v in xm.dataFrames
True
>>> type(xm.dataFrames[v])
<class 'pandas.core.frame.DataFrame'>
>>> # ---
>>> # ToH5
>>> # ---
>>> xm.ToH5()
>>> os.path.exists(xm.h5File) 
True
>>> # ---
>>> # Without Xml
>>> # ---
>>> os.rename(xm.xmlFile,xm.xmlFile+'.blind')
>>> xm=Xm(xmlFile=xmlFile)
>>> os.rename(xm.xmlFile+'.blind',xm.xmlFile)
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(xm.h5File):                        
...    os.remove(xm.h5File)
"""

import os
import sys
import logging
logger = logging.getLogger('PT3S.Xm')     
import argparse

import unittest
import doctest

import xml.etree.ElementTree as ET
import re
import pandas as pd
import numpy as np
import warnings
import tables

import h5py

import base64

class XmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Xm():
    """
    SIR 3S XML ModelFile To pandas DataFrames
            One DataFrame per SIR 3S Objecttype 
    Some Views As pandas DataFrames
            The Views are designed to deal with tedious groundwork 
            Views are aggregated somhwat arbitrary ...
            ... however usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views     
    """
    def __init__(self,xmlFile=None,NoH5Read=False):
        """
        Reads SIR 3S XML ModelFile xmlFile
        Stores all SIR 3S ModelData in DataFrames:
             self.dataFrames[tableName]
             tableName example: SWVT_ROWT
        Performs fixes and basic conversions inplace the DataFrames 
        Creates some Views as DataFrames:
            self.dataFrames[viewName]
            viewName example: vKNOT
        ---
        If a h5File exists and is newer than an (existing) xmlFile:
            The h5File is read (instead) of the xmlFile
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if type(xmlFile) == str:
                self.xmlFile=xmlFile  
                #check if xmlFile exists ...
                if not os.path.exists(self.xmlFile) and NoH5Read: 
                    logStrFinal="{0:s}{1:s}: Not existing!".format(logStr,xmlFile)                                 
                    raise XmError(logStrFinal)  
            else:
                logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,xmlFile)                                 
                raise XmError(logStrFinal)     
                              
            #Determine corresponding .h5 Filename
            (wD,fileName)=os.path.split(self.xmlFile)
            (base,ext)=os.path.splitext(fileName)
            self.h5File=wD+os.path.sep+base+'.'+'h5'

            if os.path.exists(self.xmlFile):  
                xmlFileTime=os.path.getmtime(self.xmlFile) 
            else:
                xmlFileTime=0

            #check if h5File exists 
            if os.path.exists(self.h5File):  
                #check if h5File is newer
                h5FileTime=os.path.getmtime(self.h5File)
                if(h5FileTime>xmlFileTime):
                    logger.debug("{0:s}h5File {1:s} exists and is newer than an (existing) xmlFile {2:s}:".format(logStr,self.h5File,self.xmlFile))     
                    logger.debug("{0:s}The h5File is read (instead) of the xmlFile.".format(logStr))   
                    h5Read=True  
                else:
                    logger.debug("{0:s}h5File {1:s} exists parallel but is NOT newer than xmlFile {2:s}.".format(logStr,self.h5File,self.xmlFile))     
                    h5Read=False
            else:
                h5Read=False
            
            if not h5Read:
                self.__xmlRead()
            else:
                self.FromH5(h5File=self.h5File)
                          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __xmlRead(self):
        """
        Reads SIR 3S XML ModelFile xmlFile
        Stores all SIR 3S ModelData in DataFrames:
             self.dataFrames[tableName]
             tableName example: SWVT_ROWT
        Performs fixes and basic conversions inplace the DataFrames 
        Creates some Views as DataFrames:
            self.dataFrames[viewName]
            viewName example: vKNOT       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            logger.debug("{0:s}xmlFile: {1:s} parse Xml ...".format(logStr,self.xmlFile))                     
            tree = ET.parse(self.xmlFile) # ElementTree                 
            root = tree.getroot()  # Element
            pm = {c:p for p in root.iter() for c in p}   # parentMap
            logger.debug("{0:s}xmlFile: {1:s} done.".format(logStr,self.xmlFile)) 


            logger.debug("{0:s}xmlFile: {1:s} Xml to pandas DataFrames ...".format(logStr,self.xmlFile))      
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
            logger.debug("{0:s}xmlFile: {1:s} done.".format(logStr,self.xmlFile)) 

            #fixes and conversions
            self.__convertAndFix()

            #Views
            self.__vXXXX()
                                            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def FromH5(self,h5File=None):
        """
        The h5File is read
        and self.dataFrames is filled with the dfs in the h5File   
        existing dfs in self.dataFrames are deleted
        Note that after FromH5 the content of self.dataFrames can differ from the content of self.xmlFile
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        if h5File == None:
            h5File=self.h5File

        #Check if h5File exists
        if not os.path.exists(h5File):    
            logStrFinal="{0:s}{1:s}: Not Existing!".format(logStr,h5File)                                 
            raise XmError(logStrFinal)           
  
        try:
            self.dataFrames={}   
            with pd.HDFStore(h5File) as h5Store:
                h5Keys=h5Store.keys()
                for h5Key in h5Keys:
                    match=re.search('(/)(\w+$)',h5Key)
                    key=match.group(2)
                    logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to tableName {3:s}.".format(logStr,h5File,h5Key,key)) 
                    self.dataFrames[key]=h5Store[h5Key]
                

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                                            
      
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def ToH5(self,h5File=None):
        """
        Stores all Dataframes in a .h5 File        
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if h5File == None:
                h5File=self.h5File

            #Delete .h5 File if exists
            if os.path.exists(h5File):                        
                logger.debug("{0:s}{1:s}: Delete ...".format(logStr,h5File))     
                os.remove(h5File)

            #Determine .h5 BaseKey

            #XmlFile=r'C:\3S\Modelle\MVV_FW.XML'
            relPath2XmlromCurDir=os.path.normpath(os.path.relpath(os.path.normpath(self.xmlFile),start=os.path.normpath(os.path.curdir))) # ..\..\..\..\..\3S\Modelle\MVV_FW.XML
            #print(repr(relPath2XmlromCurDir)) # '..\\..\\..\\..\\..\\3S\\Modelle\\MVV_FW.XML'
            h5KeySep='/'
            h5KeyCharForDot='_'
            h5KeyCharForMinus='_'
            relPath2XmlromCurDirH5BaseKey=re.sub('\.',h5KeyCharForDot,re.sub(r'\\',h5KeySep,re.sub('-',h5KeyCharForMinus,re.sub('.xml','',relPath2XmlromCurDir,flags=re.IGNORECASE))))
            #__/__/__/__/__/3S/Modelle/MVV_FW

            warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
            warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)
                         
            #Write .h5 File
            logger.debug("{0:s}pd.HDFStore({1:s}) ...".format(logStr,h5File))                 
            with pd.HDFStore(h5File) as h5Store: 
                for tableName,table in self.dataFrames.items():
                    h5Key=relPath2XmlromCurDirH5BaseKey+h5KeySep+tableName      
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,tableName,h5Key))                                                
                    h5Store.put(h5Key,table)#,format='table')                  

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                                           
            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __convertAndFix(self):
        """
        Performs fixes and basic conversions inplace the DataFrames
        Fixes and conbversions here are integrity-oriented
        Usage-oriented conversions (i.e. pd.to_numeric and base64.b64decode) are done in the vXXXX-functions
        conversions: 
        - , > . (converted in: SWVT_ROWT, LFKT_ROWT, QVAR_ROWT)
        fixes:
        - 1st Time without Value?! (fixed in: SWVT_ROWT, LFKT_ROWT, QVAR_ROWT)       
        - in new Models constructed from SIR 3S in Xml not all Attrubutes of an Object are written?!   
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
            
            
            # TE only in Waermemodels ? ...
            try:
                isinstance(self.dataFrames['KNOT']['TE'],pd.core.series.Series)
            except:
                self.dataFrames['KNOT']['TE']=pd.Series()     

            # Models with only one Standard LTGR ...
            try:
                isinstance(self.dataFrames['LTGR']['BESCHREIBUNG'],pd.core.series.Series)
            except:
                self.dataFrames['LTGR']['BESCHREIBUNG']=pd.Series()    

            # Models with no CONTs ...
            try:
                isinstance(self.dataFrames['CONT']['LFDNR'],pd.core.series.Series)
            except:
                self.dataFrames['CONT']['LFDNR']=pd.Series()    

            try:
                isinstance(self.dataFrames['CONT']['GRAF'],pd.core.series.Series)
            except:
                self.dataFrames['CONT']['GRAF']=pd.Series()    
                        
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)             
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __vXXXX(self):
        """
        Creates some Views as DataFrames:
            self.vXXX[viewName]=pd.merge(...)
            viewName example: vKNOT

        The Views are designed to deal with tedious groundwork 
        Views are aggregated somhwat arbitrary ...
        ... however usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views 

        View-Data:
        Most Colummn-Names will be unchanged
        If suitable renames (i.e. pd.to_numeric and base64.b64decode) are performed inplace

        Some Model-oriented calculations are performed
         
        Most types will be unchanged (pandas' Object-Type)
        If suitable conversions (i.e. pd.to_numeric and base64.b64decode) are performed inplace

        Views created:
            #Ansichtsgruppen
            vLAYR

            #time-Tables
            vLFKT
            vQVAR
            vSWVT

            #Signal-Model
            vRSLW
            
            #Block-Nodes    
            vVKNO
            
            #Nodes
            vKNOT
            
            #Pipes
            vROHR
            
            #House-Stations (district heating)
            vFWVB        
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            #Layr
            self.dataFrames['vLAYR']=self.__vLAYR()

            #time-Tables
            self.dataFrames['vLFKT']=self.__vLFKT()          
            self.dataFrames['vSWVT']=self.__vSWVT()
            self.dataFrames['vRSLW']=self.__vRSLW(vSWVT=self.dataFrames['vSWVT']
                                             ) #SWVT-Usage

            #time-Tables
            self.dataFrames['vQVAR']=self.__vQVAR()
            
            #nodes    
            self.dataFrames['vVKNO']=self.__vVKNO()
            self.dataFrames['vKNOT']=self.__vKNOT(
                 vVKNO=self.dataFrames['vVKNO']
                ,vQVAR=self.dataFrames['vQVAR']
                )

            #elements
            self.dataFrames['vROHR']=self.__vROHR(vKNOT=self.dataFrames['vKNOT'])
            self.dataFrames['vFWVB']=self.__vFWVB(vKNOT=self.dataFrames['vKNOT']
                                            ,vLFKT=self.dataFrames['vLFKT']
                                            )                                             
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __vLAYR(self):
        """
            vLAYR:
                One row per LAYR and OBJ:
                #LAYR_DATA (vLAYR_DATA)
                'LFDNR'
                ,'NAME'
                #LAYR_OBJS (vLAYR_OBJS)
                ,'OBJID' #pk (or tk?!) of a LAYR OBJ
                ,'OBJTYPE' #type (i.e.ROHR) of a LAYR OBJ
                #IDs (of the LAYR)
                ,'pk','tk'                   
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vLAYR=None

            vLAYR_DATA=self.dataFrames['LAYR'][pd.notnull(self.dataFrames['LAYR']['OBJS'])][['LFDNR','NAME','OBJS','pk','tk']]
            vLAYR_DATA['OBJS']=vLAYR_DATA['OBJS'].apply(lambda x: base64.b64decode(x)).str.decode('utf-8')
            vLAYR_DATA['LFDNR']=pd.to_numeric(vLAYR_DATA.LFDNR,errors='coerce').fillna(-1).astype(np.int64)

            vLAYR_OBJS=pd.concat(
            [
             pd.Series(
             row['LFDNR'],
             row['OBJS'].split('\t')
              )              
            for _, row in vLAYR_DATA.iterrows() 
            ]
            ).reset_index() # When we reset the index, the old index is added as a column, and a new sequential index is used

            vLAYR_DATA.drop(['OBJS'],axis=1,inplace=True)
            
            vLAYR_OBJS.rename(columns={'index':'ETYPEEID',0:'LFDNR'},inplace=True)
            vLAYR_OBJS=vLAYR_OBJS[vLAYR_OBJS['ETYPEEID'].notnull()]
            vLAYR_OBJS=vLAYR_OBJS[vLAYR_OBJS['ETYPEEID'].str.len()>5]
            vLAYR_OBJS['OBJID']=vLAYR_OBJS['ETYPEEID'].str[5:]
            vLAYR_OBJS['OBJTYPE']=vLAYR_OBJS['ETYPEEID'].str[:4]

            vLAYR_OBJS.drop(['ETYPEEID'],axis=1,inplace=True)

            vLAYR=pd.merge(vLAYR_DATA,vLAYR_OBJS,left_on='LFDNR',right_on='LFDNR')

            vLAYR=vLAYR[[
            'LFDNR'
            ,'NAME'
            #from LAYR's OBJS: 
            ,'OBJID' #pk (or tk?!) of a LAYR OBJ
            ,'OBJTYPE' #type (i.e.ROHR) of a LAYR OBJ
            #IDs (of the LAYR)
            ,'pk','tk'
            ]]
          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vLAYR,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vLAYR=pd.DataFrame()                   
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vLAYR

    def __vLFKT(self):
        """
        vLFKT:
            One row per Loadfactor time-Table:
            #LFKT
             'NAME'
            ,'BESCHREIBUNG'
            ,'INTPOL'
            ,'ZEITOPTION'
            #ROWT
            ,'LF' #1st Value
            #time-Table aggregates:
            ,'LF_min','LF_max'
            #ID (of the LFKT)
            ,'pk'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vLFKT=None
            vLFKT=pd.merge(self.dataFrames['LFKT'],self.dataFrames['LFKT_ROWT'],left_on='pk',right_on='fk')
            vLFKT['ZEIT']=pd.to_numeric(vLFKT['ZEIT']) 
            vLFKT['LF']=pd.to_numeric(vLFKT['LF']) 
            vLFKT['ZEIT_RANG']=vLFKT.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vLFKT_gLF=vLFKT.groupby(['pk_x'], as_index=False).agg({'LF':[np.min,np.max]})
            vLFKT_gLF.columns= [tup[0]+tup[1] for tup in zip(vLFKT_gLF.columns.get_level_values(0),vLFKT_gLF.columns.get_level_values(1))]
            vLFKT_gLF.rename(columns={'LFamin':'LF_min','LFamax':'LF_max'},inplace=True)
            #
            vLFKT=pd.merge(vLFKT,vLFKT_gLF,left_on='pk_x',right_on='pk_x')
            #
            vLFKT=vLFKT[vLFKT['ZEIT_RANG']==1]
            #
            vLFKT=vLFKT[['NAME','BESCHREIBUNG','LF','LF_min','LF_max','INTPOL','ZEITOPTION','pk_x']]
            #
            vLFKT.rename(columns={'pk_x':'pk'},inplace=True)
            #
            vLFKT=vLFKT[[
                'NAME','BESCHREIBUNG'
                ,'LF','LF_min','LF_max'
                ,'INTPOL','ZEITOPTION'
                ,'pk'
                ]]
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vLFKT  

    def __vSWVT(self):
        """
        vSWVT:
            #SWVT
             'NAME'
            ,'BESCHREIBUNG'
            ,'INTPOL','ZEITOPTION'
            #ROWT
            ,'W' #1st Value
            #time-Table aggregates:
            ,'W_min','W_max'
            #ID (of the SWVT)
            ,'pk'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vSWVT = None
            vSWVT=pd.merge(self.dataFrames['SWVT'],self.dataFrames['SWVT_ROWT'],left_on='pk',right_on='fk')
            vSWVT['ZEIT']=pd.to_numeric(vSWVT['ZEIT']) 
            vSWVT['W']=pd.to_numeric(vSWVT['W']) 
            vSWVT['ZEIT_RANG']=vSWVT.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vSWVT_g=vSWVT.groupby(['pk_x'], as_index=False).agg({'W':[np.min,np.max]})
            vSWVT_g.columns= [tup[0]+tup[1] for tup in zip(vSWVT_g.columns.get_level_values(0),vSWVT_g.columns.get_level_values(1))]
            vSWVT_g.rename(columns={'Wamin':'W_min','Wamax':'W_max'},inplace=True)
            #
            vSWVT=pd.merge(vSWVT,vSWVT_g,left_on='pk_x',right_on='pk_x')
            #
            vSWVT=vSWVT[vSWVT['ZEIT_RANG']==1]
            #
            vSWVT=vSWVT[['NAME','BESCHREIBUNG','INTPOL','ZEITOPTION','W','W_min','W_max','pk_x']]
            #
            vSWVT.rename(columns={'pk_x':'pk'},inplace=True)
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return vSWVT   

    def __vRSLW(self,vSWVT=None):
        """
        vRSLW:
            # RSLW
            'KA'
            ,'BESCHREIBUNG'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'CONT' #(NAME)
            ,'ID'          
            # vSWVT
            ,'SWVT' #(NAME)
            ,'BESCHREIBUNG_SWVT' #(BESCHREIBUNG)
            ,'INTPOL','ZEITOPTION'
            ,'W','W_min','W_max'
            # RSLW IDs   
            ,'pk','tk'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:      
            vRSLW=None                  
                         
            vRSLW=pd.merge(self.dataFrames['RSLW'],self.dataFrames['RSLW_BZ'],left_on='pk',right_on='fk')
            vRSLW=pd.merge(vRSLW,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')

            vRSLW=vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON','fkSWVT' 
            # CONT
            ,'NAME','ID'
            # RSLW IDs   
            ,'pk_x', 'tk_x'
                 ]]

            vRSLW=pd.merge(vRSLW,vSWVT,left_on='fkSWVT',right_on='pk',how='left')

            vRSLW=vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG_x'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'NAME_x','ID'          
            # vSWVT
            ,'NAME_y', 'BESCHREIBUNG_y', 'W', 'W_min', 'W_max', 'INTPOL','ZEITOPTION'
            # RSLW IDs   
            ,'pk_x', 'tk_x'
                 ]]            

            vRSLW.rename(columns=
            {'BESCHREIBUNG_x': 'BESCHREIBUNG',
             'BESCHREIBUNG_y': 'BESCHREIBUNG_SWVT',
             'NAME_x': 'CONT',
             'NAME_y': 'SWVT',
             'pk_x': 'pk',
             'tk_x': 'tk'}
            ,inplace=True)

            vRSLW=vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'CONT','ID'          
            # vSWVT
            ,'SWVT', 'BESCHREIBUNG_SWVT', 'W', 'W_min', 'W_max', 'INTPOL','ZEITOPTION'
            # RSLW IDs   
            ,'pk','tk'
                 ]]          
            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vRSLW,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vRSLW=pd.DataFrame()              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vRSLW

    def __vQVAR(self):
        """
        vQVAR:
            'NAME'
           ,'BESCHREIBUNG'
           ,'INTPOL'
           ,'ZEITOPTION'
           ,'QM'
           ,'QM_min','QM_max'
           ,'pk'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vQVAR = None
            vQVAR=pd.merge(self.dataFrames['QVAR'],self.dataFrames['QVAR_ROWT'],left_on='pk',right_on='fk')
            vQVAR['ZEIT']=pd.to_numeric(vQVAR['ZEIT']) 
            vQVAR['QM']=pd.to_numeric(vQVAR['QM']) 
            vQVAR['ZEIT_RANG']=vQVAR.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vQVAR_gQM=vQVAR.groupby(['pk_x'], as_index=False).agg({'QM':[np.min,np.max]})
            vQVAR_gQM.columns= [tup[0]+tup[1] for tup in zip(vQVAR_gQM.columns.get_level_values(0),vQVAR_gQM.columns.get_level_values(1))]
            vQVAR_gQM.rename(columns={'QMamin':'QM_min','QMamax':'QM_max'},inplace=True)
            #
            vQVAR=pd.merge(vQVAR,vQVAR_gQM,left_on='pk_x',right_on='pk_x')
            #
            vQVAR=vQVAR[vQVAR['ZEIT_RANG']==1]
            #
            vQVAR=vQVAR[['NAME','BESCHREIBUNG','INTPOL','ZEITOPTION','QM','QM_min','QM_max','pk_x']]
            #
            vQVAR.rename(columns={'pk_x':'pk'},inplace=True)
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vQVAR
            
    def __vVKNO(self):
        """
        vVKNO:
           'NAME' # der Name des Knotens
          ,'CONT' # der Blockname des Blockes fuer den der Knoten Blockknoten ist
          ,'fkKNOT'
          ,'fkCONT'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:     
            vVKNO=None        
            vVKNO=pd.merge(self.dataFrames['VKNO'],self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            vVKNO=pd.merge(vVKNO,self.dataFrames['KNOT'],left_on='fkKNOT',right_on='pk')

            vVKNO=vVKNO[[
               'NAME_x'     
              ,'NAME_y'     
              ,'fkCONT_x','fkKNOT' 
            ]]
            vVKNO.rename(columns={'NAME_x':'CONT','NAME_y':'NAME','fkCONT_x':'fkCONT'},inplace=True)

            vVKNO=vVKNO[[
                'NAME' # der Name des Knotens
               ,'CONT' # der Blockname des Blockes fuer den der Knoten Blockknoten ist
               ,'fkKNOT'
               ,'fkCONT'
            ]]
                               
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vVKNO,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vVKNO=pd.DataFrame()       
                vVKNO['NAME']=pd.Series()     
                vVKNO['CONT']=pd.Series()     
                vVKNO['fkKNOT']=pd.Series()     
                vVKNO['fkCONT']=pd.Series()                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vVKNO

    def __vKNOT(self,vVKNO=None,vQVAR=None):
        """
        vKNOT:
            'NAME'
           ,'BESCHREIBUNG'
           ,'IDREFERENZ'
           ,'CONT' # aus KNOT>CONT (der Blockname des Knotens)
           ,'CONT_ID' # aus KNOT>CONT
           ,'CONT_LFDNR' # aus KNOT>CONT
           ,'CONT_VKNO' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
           ,'KTYP'
           ,'LFAKT','QM_EIN'
           ,'QVAR_NAME'
           ,'QM','QM_min','QM_max'     
           ,'KVR' 
           ,'TE','TM' 
           ,'XKOR','YKOR','ZKOR'
           ,'pk','tk'
           #plotCors
           ,'pXCor' # x-self.pXCorZero 
           ,'pYCor' # x-self.pYCorZero 
          
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            vKNOT=None

            vKNOT=pd.merge(self.dataFrames['KNOT'],self.dataFrames['KNOT_BZ'],left_on='pk',right_on='fk')
            vKNOT=pd.merge(vKNOT,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            vKNOT=pd.merge(vKNOT,vVKNO,left_on='pk_x',right_on='fkKNOT',how='left')
            
          
            vKNOT=vKNOT[[
                    'NAME_x'
                   ,'BESCHREIBUNG','IDREFERENZ'
                   ,'NAME_y' # aus KNOT>CONT (der Blockname des Knotens)
                   ,'ID' # aus KNOT>CONT
                   ,'LFDNR' # aus KNOT>CONT
                   ,'CONT' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
                   ,'KTYP'
                   ,'LFAKT','QM_EIN','fkQVAR'       
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk_x','tk_x'
                ]]

            vKNOT.rename(columns={'NAME_x':'NAME'
                                       ,'NAME_y':'CONT'
                                       ,'ID':'CONT_ID'
                                       ,'LFDNR':'CONT_LFDNR'
                                       ,'ID':'CONT_ID','LFDNR':'CONT_LFDNR'
                                       ,'CONT':'CONT_VKNO'
                                       ,'pk_x':'pk'
                                       ,'tk_x':'tk'},inplace=True)

            vKNOT=pd.merge(vKNOT,vQVAR,left_on='fkQVAR',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'QVAR_NAME'},inplace=True)
            vKNOT.rename(columns={'pk_x':'pk'},inplace=True)

            vKNOT=vKNOT[[
                    'NAME'
                   ,'BESCHREIBUNG'
                   ,'IDREFERENZ'
                   ,'CONT' # aus KNOT>CONT (der Blockname des Knotens)
                   ,'CONT_ID' # aus KNOT>CONT
                   ,'CONT_LFDNR' # aus KNOT>CONT
                   ,'CONT_VKNO' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
                   ,'KTYP'
                   ,'LFAKT','QM_EIN'
                   ,'QVAR_NAME'
                   ,'QM','QM_min','QM_max'     
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]
          
            self.pXCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & 
                (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['XKOR'].astype(float).min()

            vKNOT['pXCor'] = [
                 x-self.pXCorZero 
                 if 
                 y==1001 and not z
                 else
                 x
                 for x,y,z in zip(vKNOT['XKOR'].astype(float)
                             ,vKNOT['CONT_ID'].astype(int)
                             ,vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element')
                             )
                ] 

            self.pYCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['YKOR'].astype(float).min()

            vKNOT['pYCor'] = [
                 x-self.pYCorZero 
                 if 
                 y==1001 and not z
                 else
                 x
                 for x,y,z in zip(vKNOT['YKOR'].astype(float)
                             ,vKNOT['CONT_ID'].astype(int)
                             ,vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element')
                             )
                ] 

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vKNOT

    def __vROHR(self,vKNOT=None):
        """
        vROHR:
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT','DA','DI','DN','KT','PN','REHABILITATION','REPARATUR','S','WSTEIG','WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'DTRO_NAME'
                    ,'DTRO_BESCHREIBUNG'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                    #IDs 
                    ,'pk','tk'
                    ,'GEOM_x','GRAF_x'
                    #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                    #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                    #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                    #Ki
                    ,'NAME_i'
                    ,'KVR_i','TM_i'
                    ,'XKOR_i','YKOR_i','ZKOR_i'                 
                    #Kk
                    ,'NAME_k'
                    ,'KVR_k','TM_k'
                    ,'XKOR_k','YKOR_k','ZKOR_k'
                    #plotCors
                    ,'pXCor_i','pYCor_i'
                    ,'pXCor_k','pYCor_k'
                    ,'pXCors','pYCors' # matplotlibs's .plot(pXCors,pYCors,...)
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vROHR=None            
                                         
            vROHR=pd.merge(self.dataFrames['ROHR'],self.dataFrames['ROHR_BZ'],left_on='pk',right_on='fk')

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #Ref.
                    ,'fkCONT'
                    ,'fkDTRO_ROWD'
                    ,'fkLTGR','fkSTRASSE'
                    ,'fkKI','fkKK'
                   #IDs 
                    ,'pk_x','tk'
                    ,'GEOM','GRAF'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                            ]]

            vROHR.rename(columns={'pk_x':'pk'},inplace=True)
            vROHR=pd.merge(vROHR,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')

            vROHR=vROHR[[
             'BESCHREIBUNG'
            ,'IDREFERENZ'
            #Asset
            ,'BAUJAHR','HAL'
            ,'IPLANUNG','KENNUNG'
            #Reibung
            ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
            ,'JLAMBS','LAMBDA0'
            #inst.
            ,'ASOLL','INDSCHALL'
            #FW
            ,'fk2LROHR','KVR'
            #Ref.
            ,'fkDTRO_ROWD'
            ,'fkLTGR','fkSTRASSE'
            ,'fkKI','fkKK'
           #IDs 
            ,'pk_x','tk_x'
            ,'GEOM_x','GRAF_x'
           #BZ
            ,'IRTRENN'
            ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
           #Rest
            ,'QSVB'
            ,'ZVLIMPTNZ'
            ,'KANTENZV'
           #CONT
            ,'NAME' 
            ,'ID'
            ,'LFDNR'
                    ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'},inplace=True)    
            vROHR=pd.merge(vROHR,self.dataFrames['DTRO_ROWD'],left_on='fkDTRO_ROWD',right_on='pk')   

            vROHR=vROHR[[
             'BESCHREIBUNG'
            ,'IDREFERENZ'
            #Asset
            ,'BAUJAHR','HAL'
            ,'IPLANUNG','KENNUNG'
            #Reibung
            ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
            ,'JLAMBS','LAMBDA0'
            #inst.
            ,'ASOLL','INDSCHALL'
            #FW
            ,'fk2LROHR','KVR'
            #DTRO_ROWD
            ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
            #Ref.
            ,'fkLTGR','fkSTRASSE'
            ,'fkKI','fkKK'
           #IDs 
            ,'pk_x','tk_x'
            ,'GEOM_x','GRAF_x'
           #BZ
            ,'IRTRENN'
            ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
           #Rest
            ,'QSVB'
            ,'ZVLIMPTNZ'
            ,'KANTENZV'
           #CONT
            ,'CONT' 
            ,'CONT_ID'
            ,'CONT_LFDNR'
                    ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk'},inplace=True)
            vROHR=pd.merge(vROHR,self.dataFrames['LTGR'],left_on='fkLTGR',right_on='pk')

            vROHR=vROHR[[
             'BESCHREIBUNG_x'
            ,'IDREFERENZ'
            #Asset
            ,'BAUJAHR','HAL'
            ,'IPLANUNG','KENNUNG'
            #Reibung
            ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
            ,'JLAMBS','LAMBDA0'
            #inst.
            ,'ASOLL','INDSCHALL'
            #FW
            ,'fk2LROHR','KVR'
            #DTRO_ROWD
            ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
            #LTGR
            ,'NAME','BESCHREIBUNG_y','SICHTBARKEIT','VERLEGEART','fkDTRO','fkSRAT'
            #Ref.
            ,'fkSTRASSE'
            ,'fkKI','fkKK'
           #IDs 
            ,'pk_x','tk_x'
            ,'GEOM_x','GRAF_x'
           #BZ
            ,'IRTRENN'
            ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
           #Rest
            ,'QSVB'
            ,'ZVLIMPTNZ'
            ,'KANTENZV'
           #CONT
            ,'CONT' 
            ,'CONT_ID'
            ,'CONT_LFDNR'
                    ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'LTGR_NAME','BESCHREIBUNG_y':'LTGR_BESCHREIBUNG','BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART','fkDTRO','fkSRAT'
                    #Ref.
                    ,'fkSTRASSE'
                    ,'fkKI','fkKK'
                   #IDs 
                    ,'pk','tk'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                            ]]
                                 
            vROHR=pd.merge(vROHR,self.dataFrames['DTRO'],left_on='fkDTRO',right_on='pk')

            vROHR=vROHR[[
                     'BESCHREIBUNG_x'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'NAME'
                    ,'BESCHREIBUNG_y'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                    ,'fkKI','fkKK'
                   #IDs 
                    ,'pk_x','tk_x'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                            ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'DTRO_NAME','BESCHREIBUNG_y':'DTRO_BESCHREIBUNG','BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)
            
            vROHR=pd.merge(vROHR,vKNOT,left_on='fkKI',right_on='pk')   
            vROHR.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ'
                                       ,'pk_x':'pk','tk_x':'tk'
                                       ,'CONT_ID_x':'CONT_ID','CONT_LFDNR_x':'CONT_LFDNR'
                                       },inplace=True) 

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR_x'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'DTRO_NAME'
                    ,'DTRO_BESCHREIBUNG'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                    ,'fkKK'
                   #IDs 
                    ,'pk','tk'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT_x' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                   #Ki
                   ,'NAME'
                   ,'KVR_y','TM'
                   ,'XKOR','YKOR','ZKOR'
                   ,'pXCor','pYCor'
                            ]]

            vROHR.rename(columns={'NAME':'NAME_i','KVR_x':'KVR','KVR_y':'KVR_i','TM':'TM_i','CONT_x':'CONT'},inplace=True)  
            vROHR.rename(columns={'XKOR':'XKOR_i','YKOR':'YKOR_i','ZKOR':'ZKOR_i'
                                       ,'pXCor':'pXCor_i'
                                       ,'pYCor':'pYCor_i'
                                       },inplace=True)    
            
            vROHR=pd.merge(vROHR,vKNOT,left_on='fkKK',right_on='pk')    
            vROHR.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ'
                                       ,'pk_x':'pk','tk_x':'tk'
                                       ,'CONT_ID_x':'CONT_ID','CONT_LFDNR_x':'CONT_LFDNR'
                                       },inplace=True)  

            vROHR.rename(columns={'NAME':'NAME_k','KVR_x':'KVR','KVR_y':'KVR_k','TM':'TM_k','CONT_x':'CONT'},inplace=True)  
            vROHR.rename(columns={'XKOR':'XKOR_k','YKOR':'YKOR_k','ZKOR':'ZKOR_k'
                                       ,'pXCor':'pXCor_k'
                                       ,'pYCor':'pYCor_k'
                                       },inplace=True)                                   

            vROHR['pXCors']=[[xi,xk] for xi,xk in zip(vROHR['pXCor_i'],vROHR['pXCor_k'])]
            vROHR['pYCors']=[[xi,xk] for xi,xk in zip(vROHR['pYCor_i'],vROHR['pYCor_k'])]
            
            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'DTRO_NAME'
                    ,'DTRO_BESCHREIBUNG'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                   #IDs 
                    ,'pk','tk'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                   #Ki
                   ,'NAME_i'
                   ,'KVR_i','TM_i'
                   ,'XKOR_i','YKOR_i','ZKOR_i'                 
                   #Kk
                   ,'NAME_k'
                   ,'KVR_k','TM_k'
                   ,'XKOR_k','YKOR_k','ZKOR_k'
                   #plotCors
                   ,'pXCor_i','pYCor_i'
                   ,'pXCor_k','pYCor_k'
                   ,'pXCors','pYCors' # matplotlibs's .plot(pXCors,pYCors,...)
                            ]]

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)           
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))         
            return vROHR 

    def __vFWVB(self,vKNOT=None,vLFKT=None):
        """
        vFWVB:
             'BESCHREIBUNG'
            ,'IDREFERENZ'
            ,'W0'
            ,'LFK' ,'TVL0' ,'TRS0'
            #LFKT
            ,'LFKT'
            ,'W','W_min','W_max'
            #FWVB contd.
            ,'INDTR' ,'TRSK'
            ,'VTYP' ,'IMBG' ,'IRFV'
            #FWVB IDs
            ,'pk','tk'  
            #Ki
            ,'NAME_i'
            ,'KVR_i','TM_i'
            ,'XKOR_i','YKOR_i','ZKOR_i'
            ,'pXCor_i','pYCor_i'
            #Kk
            ,'NAME_k'
            ,'KVR_k','TM_k'
            ,'XKOR_k','YKOR_k','ZKOR_k'  
            ,'pXCor_k','pYCor_k'
            #CONT
            ,'CONT' 
            ,'CONT_ID'
            ,'CONT_LFDNR' 
            #Categories
            ,'W0cat'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:         
            vFWVB=None
                            
            vFWVB=pd.merge(self.dataFrames['FWVB'],self.dataFrames['FWVB_BZ'],left_on='pk',right_on='fk')
            #
            vFWVB=vFWVB[vFWVB['W0'].notnull()]
            vFWVB['W0']=vFWVB['W0'].str.replace(',', '.')
            vFWVB['W0']=pd.to_numeric(vFWVB['W0']) 
            #
            vFWVB['LFK']=pd.to_numeric(vFWVB['LFK']) 
            vFWVB['TVL0']=pd.to_numeric(vFWVB['TVL0']) 
            vFWVB['TRS0']=pd.to_numeric(vFWVB['TRS0'])  
            vFWVB['INDTR']=pd.to_numeric(vFWVB['INDTR'])  
            vFWVB['TRSK']=pd.to_numeric(vFWVB['TRSK'])  
            vFWVB['VTYP']=pd.to_numeric(vFWVB['VTYP'])  
            vFWVB['IMBG']=pd.to_numeric(vFWVB['IMBG']) 
            vFWVB['IRFV']=pd.to_numeric(vFWVB['IRFV']) 
            
            #
            vFWVB=pd.merge(vFWVB,vLFKT,left_on='fkLFKT',right_on='pk')
            #
            vFWVB['W']      = vFWVB.apply(lambda row: row.LF     * row.W0, axis=1)
            vFWVB['W_min']  = vFWVB.apply(lambda row: row.LF_min * row.W0, axis=1)
            vFWVB['W_max']  = vFWVB.apply(lambda row: row.LF_max * row.W0, axis=1)
            #
            vFWVB=vFWVB[[
                    'BESCHREIBUNG_x','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                   ,'W','W_min','W_max'
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                   ,'pk_x','tk'
                   ,'NAME','BESCHREIBUNG_y'
                   ,'fkKI','fkKK'
                   ,'fkCONT'
                 ]]
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','pk_x':'pk','NAME':'LFKT'},inplace=True)       
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                   ,'fkKI','fkKK'   
                   ,'fkCONT'            
                 ]]    

            vFWVB=pd.merge(vFWVB,vKNOT,left_on='fkKI',right_on='pk')   
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ','pk_x':'pk','tk_x':'tk'},inplace=True)  
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                    #Ki
                   ,'NAME'
                   ,'KVR','TM'
                   ,'XKOR','YKOR','ZKOR'
                   ,'pXCor','pYCor'
                   ,'fkKK'    
                   ,'fkCONT'           
                 ]]     
            vFWVB.rename(columns={'NAME':'NAME_i','KVR':'KVR_i','TM':'TM_i'},inplace=True)  
            vFWVB.rename(columns={'XKOR':'XKOR_i','YKOR':'YKOR_i','ZKOR':'ZKOR_i'
                                       ,'pXCor':'pXCor_i'
                                       ,'pYCor':'pYCor_i'},inplace=True)    
            
            vFWVB=pd.merge(vFWVB,vKNOT,left_on='fkKK',right_on='pk')    
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ','pk_x':'pk','tk_x':'tk'},inplace=True)  
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                    #Ki
                   ,'NAME_i'
                   ,'KVR_i','TM_i'
                   ,'XKOR_i','YKOR_i','ZKOR_i'
                   ,'pXCor_i','pYCor_i'
                    #Kk
                   ,'NAME'
                   ,'KVR','TM'
                   ,'XKOR','YKOR','ZKOR'  
                   ,'pXCor','pYCor'
                   ,'fkCONT'        
                 ]]     
            vFWVB.rename(columns={'NAME':'NAME_k','KVR':'KVR_k','TM':'TM_k'},inplace=True)  
            vFWVB.rename(columns={'XKOR':'XKOR_k','YKOR':'YKOR_k','ZKOR':'ZKOR_k'
                                       ,'pXCor':'pXCor_k'
                                       ,'pYCor':'pYCor_k'},inplace=True)     
                        
            vFWVB=pd.merge(vFWVB,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')  
            vFWVB.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'},inplace=True)    
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                    #Ki
                   ,'NAME_i'
                   ,'KVR_i','TM_i'
                   ,'XKOR_i','YKOR_i','ZKOR_i'
                   ,'pXCor_i','pYCor_i'
                    #Kk
                   ,'NAME_k'
                   ,'KVR_k','TM_k'
                   ,'XKOR_k','YKOR_k','ZKOR_k'  
                   ,'pXCor_k','pYCor_k'
                    #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR' 
                     ]]

            # Last Kategorien (Load Categories); kategorisieren der FWVB nach Anschlusswert
            Load=vFWVB.W0

            bins=[]
            binlabels=[]

            bins.append(0)
            binlabels.append('=0')

            epsZero=0.001 #to distinguish FWVB Cat. with W0=0 from those with W0>0
            bins.append(epsZero)
            binlabels.append('>0')

            bins.append(Load.quantile(.25))
            binlabels.append('>=25%-Quart.')

            if Load.median() < Load.mean(): #50%-Quartil < Mittelwert
                bins.append(Load.median()) 
                binlabels.append('>=Median')

            bins.append(Load.mean())
            binlabels.append('>=Mittelwert')

            bins.append(bins[-1]*2)
            binlabels.append('>=2xMittelw.')

            if bins[-1] < Load.std():
                bins.append(Load.std())
                binlabels.append('>=Standardabw.')

            if bins[-1] < 2*Load.std():
                bins.append(2*Load.std())
                binlabels.append('>=2*Standardabw.')

            if bins[-1] < Load.quantile(.90):
                bins.append(Load.quantile(.90))
                binlabels.append('>=90%-Quartil')
            else: 
                if bins[-1] < Load.quantile(.95):
                    bins.append(Load.quantile(.95))
                    binlabels.append('>=95%-Quartil')

            bins.append(Load.max())
            binlabels.append('Max.')

            W0cat=pd.cut(Load,bins,include_lowest=True,right=True,precision=1)

            W0catLabels=[x + '-: ' +  re.sub('\]$','[',re.sub('\(' ,'[', y))  for x,y in zip(binlabels[:-1],W0cat.cat.categories)]
            W0catLabels[-1]=re.sub('\[$',']',W0catLabels[-1])

            W0cat.cat.rename_categories(W0catLabels,inplace=True)

            #vFWVB['W0cat']=W0cat
            #vFWVB.groupby('W0Cat').describe()
            #vFWVB.groupby('W0Cat').W0.sum()

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vFWVB,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vFWVB=pd.DataFrame()                 
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return vFWVB             

    def vFWVB_Plt_Hist(self
                       ,epsZero=0.001 #to distinguish FWVB Cat. with W0=0 from those with W0>0
                       ,spaceBetweenCats=0.3 #the Space between the Categories; 1.0: no Space 
                       ):
        """
        Plots a Histogram-alike Presentation on gca().  
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:  
            #Categories 
            bins=[]
            binlabels=[]

            bins.append(0)
            binlabels.append('=0')

            bins.append(epsZero)
            binlabels.append('>0')

            bins.append(vFWVB.W0.quantile(.25))
            binlabels.append('>=25%-Quart.')

            if vFWVB.W0.median() < vFWVB.W0.mean(): #50%-Quartil < Mittelwert
                bins.append(vFWVB.W0.median()) 
                binlabels.append('>=Median')

            bins.append(vFWVB.W0.mean())
            binlabels.append('>=Mittelwert')

            bins.append(bins[-1]*2)
            binlabels.append('>=2xMittelw.')

            if bins[-1] < vFWVB.W0.std():
                bins.append(vFWVB.W0.std())
                binlabels.append('>=Standardabw.')

            if bins[-1] < vFWVB.W0.quantile(.95):
                bins.append(vFWVB.W0.quantile(.95))
                binlabels.append('>=95%-Quartil')

            bins.append(vFWVB.W0.max())
            binlabels.append('Max.')

            W0cat=pd.cut(vFWVB.W0,bins,include_lowest=True,right=True,precision=1)

            W0catLabels=[x + '-: ' +  re.sub('\]$','[',re.sub('\(' ,'[', y))  for x,y in zip(binlabels[:-1],W0cat.cat.categories)]
            W0catLabels[-1]=re.sub('\[$',']',W0catLabels[-1])

            #Category Data
            W0catSumPercent=vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.sum()  /vFWVB[vFWVB.W0>=0].W0.sum() # kW Summe
            W0catAnzPercent=vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.count()/vFWVB[vFWVB.W0>=0].W0.count() # Anzahl Summe

            W0catSumPercentcs=W0catSumPercent.cumsum()
            W0catAnzPercentcs=W0catAnzPercent.cumsum()

            #Bar Layout
            numOfBarsPerCat=2 # MW u. Anzahl
            numOfCats=len(W0cat.cat.categories)
            widthPerBar=numOfCats/(numOfCats*numOfBarsPerCat)*min(1.-spaceBetweenCats,1.0)
            xCats0=np.arange(numOfCats) # the x-Coordinate of the left-most Bar per Cat


            ax=plt.gca()

            #1st MW Bars
            barsW0catSumPercent = ax.bar(xCats0,W0catSumPercent,widthPerBar)
            norm = colors.Normalize(W0catSumPercentcs.min(),W0catSumPercentcs.max())
            colorSumPercent=[]
            for thisfrac, thisbar in zip(W0catSumPercentcs,barsW0catSumPercent):
                color = plt.cm.cool(norm(thisfrac))
                thisbar.set_facecolor(color)
                colorSumPercent.append(color)

            #2nd Anz Bars
            barsW0catAnzPercent = ax.bar(xCats0+widthPerBar,W0catAnzPercent,widthPerBar)
            norm = colors.Normalize(W0catAnzPercentcs.min(),W0catAnzPercentcs.max())
            colorAnzPercent=[]
            for thisfrac, thisbar in zip(W0catAnzPercentcs,barsW0catAnzPercent):
                color = plt.cm.autumn(norm(thisfrac))
                thisbar.set_facecolor(color)
                colorAnzPercent.append(color)

            #xTicks
            xTicks=ax.set_xticks(xCats0+numOfBarsPerCat*widthPerBar/2) #xTicks in the Middle of each Cat.
            xTickValues=ax.get_xticks()

            #xLabels
            xTickLabels=ax.set_xticklabels(W0catLabels,rotation='vertical')
            for xTickLabel in xTickLabels:
                x,y=xTickLabel.get_position()
                xTickLabel.set_position((x,y-0.0625*numOfBarsPerCat)) #Space for Cat Datanumbers (one row per Measure)

            #yTicks rechts (0-1)
            yTicksR=[x/10 for x in np.arange(10)+1]
            yTicksR.insert(0,0)

            #yTicks links
            # 10 Abstaende / 11 Ticks wie die r. y-Achse
            yMaxL=max(W0catSumPercent.max(),W0catAnzPercent.max())
            dyMinL=yMaxL/(len(yTicksR)-1)
            dyMinLr=round(dyMinL,2)
            if dyMinLr*(len(yTicksR)-1) < yMaxL:
                dyL=dyMinLr+0.01
            else:
                dyL=dyMinLr
            yTicksL=[x*dyL for x in np.arange(10)+1]
            yTicksL.insert(0,0)
            yTicksLObjects=ax.set_yticks(yTicksL)
            yTicksL=ax.get_yticks()

            #r. y-Achse
            ax2 = ax.twinx()
            yTicksRObjects=ax2.set_yticks(yTicksR)
            yTicksR=ax2.get_yticks()

            #Sum Curves
            lineW0catSumPercent,=ax2.plot(xTickValues,W0catSumPercentcs,color='gray',linewidth=1.0, ls='-',marker='s',clip_on=False)
            lineW0catAnzPercent,=ax2.plot(xTickValues,W0catAnzPercentcs,color='gray',linewidth=1.0, ls='-',marker='o',clip_on=False)

            # Cat Datanumbers (one row per Measure)
            measureIdx=1

            for kWSum, x,color in zip(vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.sum(),xTickValues,colorSumPercent):
                txt="{0:.0f}".format(float(kWSum)/1000)
                ax.annotate(txt 
                            ,xy=(x, 0), xycoords=('data', 'axes fraction')
                            ,xytext=(0, measureIdx*-10), textcoords='offset points', va='top', ha='center'
                            ,color=color
                           )
            ax.annotate("{0:.0f} MW Ges.".format(float(vFWVB[vFWVB.W0>=0].W0.sum())/1000) 
                            ,xy=(x, 0), xycoords=('data', 'axes fraction')
                            ,xytext=(+20,measureIdx*-10), textcoords='offset points', va='top', ha='left'
                       )             

            measureIdx=measureIdx+1
            for count,x,color in zip(vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.count(),xTickValues,colorAnzPercent):
                txt="{0:d}".format(int(count))
                ax.annotate(txt
                           ,xy=(x, 0),xycoords=('data', 'axes fraction')
                           ,xytext=(0, measureIdx*-10),textcoords='offset points', va='top', ha='center'
                           ,color=color
                           )
            ax.annotate("{0:d} Anz Ges.".format(int(vFWVB[vFWVB.W0>=0].W0.count())) 
                          ,xy=(x, 0),xycoords=('data', 'axes fraction')
                          ,xytext=(+20, measureIdx*-10), textcoords='offset points', va='top', ha='left'
                       )  
            
            #y-Labels 
            txyl=ax.set_ylabel('MW/MW Ges. u. Anz/Anz Ges.')
            txyr=ax2.set_ylabel('MW kum. in % u. Anz kum. in %')

            legend=plt.legend([lineW0catSumPercent,lineW0catAnzPercent],['MW kum. in %','Anz kum. in %'],loc='upper left')
            plt.grid()

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                
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

