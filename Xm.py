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

import base64

import matplotlib.pyplot as plt
from matplotlib import colors

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

                #repairs
                self.__convertAndFix()

                #Layr
                self.__vLAYR()

                #time-Tables
                self.__vLFKT()
                self.__vQVAR()
                self.__vSWVT()

                self.__vRSLW()
                
                self.__vVKNO()
                self.__vKNOT()

                self.__vROHR()

                self.__vFWVB()
                
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

    def __vLAYR(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.vLAYR_DATA=self.dataFrames['LAYR'][pd.notnull(self.dataFrames['LAYR']['OBJS'])][['LFDNR','NAME','OBJS','pk','tk']]
            self.vLAYR_DATA['OBJS']=self.vLAYR_DATA['OBJS'].apply(lambda x: base64.b64decode(x)).str.decode('utf-8')
            self.vLAYR_DATA['LFDNR']=pd.to_numeric(self.vLAYR_DATA.LFDNR,errors='coerce').fillna(-1).astype(np.int64)

            self.vLAYR_OBJS=pd.concat(
            [
             pd.Series(
             row['LFDNR'],
             row['OBJS'].split('\t')
              )              
            for _, row in self.vLAYR_DATA.iterrows() 
            ]
            ).reset_index() # When we reset the index, the old index is added as a column, and a new sequential index is used

            self.vLAYR_DATA.drop(['OBJS'],axis=1,inplace=True)
            
            self.vLAYR_OBJS.rename(columns={'index':'ETYPEEID',0:'LFDNR'},inplace=True)
            self.vLAYR_OBJS=self.vLAYR_OBJS[self.vLAYR_OBJS['ETYPEEID'].notnull()]
            self.vLAYR_OBJS=self.vLAYR_OBJS[self.vLAYR_OBJS['ETYPEEID'].str.len()>5]
            self.vLAYR_OBJS['OBJID']=self.vLAYR_OBJS['ETYPEEID'].str[5:]
            self.vLAYR_OBJS['OBJTYPE']=self.vLAYR_OBJS['ETYPEEID'].str[:4]

            self.vLAYR_OBJS.drop(['ETYPEEID'],axis=1,inplace=True)

            self.vLAYR=pd.merge(self.vLAYR_DATA,self.vLAYR_OBJS,left_on='LFDNR',right_on='LFDNR')
          
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
            vLFKT_gLF.rename(columns={'LFamin':'LF_min','LFamax':'LF_max'},inplace=True)
            #
            self.vLFKT=pd.merge(self.vLFKT,vLFKT_gLF,left_on='pk_x',right_on='pk_x')
            #
            self.vLFKT=self.vLFKT[self.vLFKT['ZEIT_RANG']==1]
            #
            self.vLFKT=self.vLFKT[['NAME','BESCHREIBUNG','LF','LF_min','LF_max','INTPOL','ZEITOPTION','pk_x']]
            #
            self.vLFKT.rename(columns={'pk_x':'pk'},inplace=True)
            #
            self.vLFKT=self.vLFKT[[
                'NAME','BESCHREIBUNG'
                ,'LF','LF_min','LF_max'
                ,'INTPOL','ZEITOPTION'
                ,'pk'
                ]]
                                 
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    

    def __vSWVT(self):
        """
        # SWVT
        'NAME'
        ,'BESCHREIBUNG'
        # SWVT_ROWT
        ,'W','W_min','W_max','INTPOL','ZEITOPTION'
        # SWVT ID
        ,'pk'       
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
            vSWVT_g.rename(columns={'Wamin':'W_min','Wamax':'W_max'},inplace=True)
            #
            self.vSWVT=pd.merge(self.vSWVT,vSWVT_g,left_on='pk_x',right_on='pk_x')
            #
            self.vSWVT=self.vSWVT[self.vSWVT['ZEIT_RANG']==1]
            #
            self.vSWVT=self.vSWVT[['NAME','BESCHREIBUNG','W','W_min','W_max','INTPOL','ZEITOPTION','pk_x']]
            #
            self.vSWVT.rename(columns={'pk_x':'pk'},inplace=True)

            # nb-Print
            self.pSWVT=self.vSWVT[['NAME','BESCHREIBUNG','W','W_min','W_max','INTPOL','ZEITOPTION']]
                                 
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def __vRSLW(self):
        """
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
        ,'W','W_min','W_max','INTPOL','ZEITOPTION'
        # RSLW IDs   
        ,'pk','tk'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                         
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

            vRSLW=pd.merge(vRSLW,self.vSWVT,left_on='fkSWVT',right_on='pk',how='left')

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

            self.vRSLW=vRSLW

            # nb-Print
            self.pRSLW=self.vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG'            
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'CONT'        
            # vSWVT
            ,'SWVT', 'BESCHREIBUNG_SWVT', 'W', 'W_min', 'W_max'
                 ]]          

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
            vQVAR_gQM.rename(columns={'QMamin':'QM_min','QMamax':'QM_max'},inplace=True)
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
            
    def __vVKNO(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            self.vVKNO=pd.merge(self.dataFrames['VKNO'],self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            self.vVKNO=pd.merge(self.vVKNO,self.dataFrames['KNOT'],left_on='fkKNOT',right_on='pk')

            self.vVKNO=self.vVKNO[[
               'NAME_x'     
              ,'NAME_y'     
              ,'KTYP'
              ,'fkCONT_x','fkKNOT'
              ,'LFAKT','QM_EIN'  
            ]]
            self.vVKNO.rename(columns={'NAME_x':'CONT','NAME_y':'NAME','fkCONT_x':'fkCONT'},inplace=True)

            self.vVKNO=self.vVKNO[[
                'NAME' # der Name des Knotens
               ,'CONT' # der Blockname des Blockes fuer den der Knoten Blockknoten ist
               ,'fkCONT','fkKNOT'
               #,'KTYP', 'LFAKT', 'QM_EIN'
            ]]
                               
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
            self.vKNOT.rename(columns={'NAME_x':'NAME'
                                       ,'NAME_y':'CONT'
                                       ,'ID':'CONT_ID'
                                       ,'LFDNR':'CONT_LFDNR'
                                       ,'ID':'CONT_ID','LFDNR':'CONT_LFDNR'
                                       ,'CONT':'CONT_VKNO'
                                       ,'pk_x':'pk'
                                       ,'tk_x':'tk'},inplace=True)

            self.vKNOT=pd.merge(self.vKNOT,self.vQVAR,left_on='fkQVAR',right_on='pk_x',how='left')
            self.vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'QVAR'},inplace=True)

            self.vKNOT=self.vKNOT[[
                    'NAME'
                   ,'BESCHREIBUNG','IDREFERENZ'
                   ,'CONT' # aus KNOT>CONT (der Blockname des Knotens)
                   ,'CONT_ID' # aus KNOT>CONT
                   ,'CONT_LFDNR' # aus KNOT>CONT
                   ,'CONT_VKNO' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
                   ,'KTYP'
                   ,'LFAKT','QM_EIN','QVAR','QM','QM_min','QM_max'     
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]
          
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    def __vROHR(self):
        """
       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:      
            
            self.vROHR=pd.merge(self.dataFrames['ROHR'],self.dataFrames['ROHR_BZ'],left_on='pk',right_on='fk')

            self.vROHR=self.vROHR[[
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

            self.vROHR.rename(columns={'pk_x':'pk'},inplace=True)
            self.vROHR=pd.merge(self.vROHR,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')

            self.vROHR=self.vROHR[[
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
            self.vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'},inplace=True)    
            self.vROHR=pd.merge(self.vROHR,self.dataFrames['DTRO_ROWD'],left_on='fkDTRO_ROWD',right_on='pk')   

            self.vROHR=self.vROHR[[
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
            self.vROHR.rename(columns={'pk_x':'pk','tk_x':'tk'},inplace=True)
            self.vROHR=pd.merge(self.vROHR,self.dataFrames['LTGR'],left_on='fkLTGR',right_on='pk')

            self.vROHR=self.vROHR[[
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
            self.vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'LTGR_NAME','BESCHREIBUNG_y':'LTGR_BESCHREIBUNG','BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)

            self.vROHR=self.vROHR[[
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
                                 
            self.vROHR=pd.merge(self.vROHR,self.dataFrames['DTRO'],left_on='fkDTRO',right_on='pk')

            self.vROHR=self.vROHR[[
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
            self.vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'DTRO_NAME','BESCHREIBUNG_y':'DTRO_BESCHREIBUNG','BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)
            
            self.vROHR=pd.merge(self.vROHR,self.vKNOT,left_on='fkKI',right_on='pk')   
            self.vROHR.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ'
                                       ,'pk_x':'pk','tk_x':'tk'
                                       ,'CONT_ID_x':'CONT_ID','CONT_LFDNR_x':'CONT_LFDNR'
                                       },inplace=True) 

            self.vROHR=self.vROHR[[
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
                            ]]

            self.vROHR.rename(columns={'NAME':'NAME_i','KVR_x':'KVR','KVR_y':'KVR_i','TM':'TM_i','CONT_x':'CONT'},inplace=True)  
            self.vROHR.rename(columns={'XKOR':'XKOR_i','YKOR':'YKOR_i','ZKOR':'ZKOR_i'},inplace=True)    
            
            self.vROHR=pd.merge(self.vROHR,self.vKNOT,left_on='fkKK',right_on='pk')    
            self.vROHR.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ'
                                       ,'pk_x':'pk','tk_x':'tk'
                                       ,'CONT_ID_x':'CONT_ID','CONT_LFDNR_x':'CONT_LFDNR'
                                       },inplace=True)  

            self.vROHR.rename(columns={'NAME':'NAME_k','KVR_x':'KVR','KVR_y':'KVR_k','TM':'TM_k','CONT_x':'CONT'},inplace=True)  
            self.vROHR.rename(columns={'XKOR':'XKOR_k','YKOR':'YKOR_k','ZKOR':'ZKOR_k'},inplace=True)                                   

            self.vROHR=self.vROHR[[
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
                            ]]

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
            self.vFWVB=pd.merge(self.vFWVB,self.vLFKT,left_on='fkLFKT',right_on='pk')
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
                   ,'pk_x','tk'
                   ,'NAME','BESCHREIBUNG_y'
                   ,'fkKI','fkKK'
                   ,'fkCONT'
                 ]]
            self.vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','pk_x':'pk','NAME':'LFKT'},inplace=True)       
            self.vFWVB=self.vFWVB[[
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

            self.vFWVB=pd.merge(self.vFWVB,self.vKNOT,left_on='fkKI',right_on='pk')   
            self.vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ','pk_x':'pk','tk_x':'tk'},inplace=True)  
            self.vFWVB=self.vFWVB[[
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
                   ,'fkKK'    
                   ,'fkCONT'           
                 ]]     
            self.vFWVB.rename(columns={'NAME':'NAME_i','KVR':'KVR_i','TM':'TM_i'},inplace=True)  
            self.vFWVB.rename(columns={'XKOR':'XKOR_i','YKOR':'YKOR_i','ZKOR':'ZKOR_i'},inplace=True)    
            
            self.vFWVB=pd.merge(self.vFWVB,self.vKNOT,left_on='fkKK',right_on='pk')    
            self.vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ','pk_x':'pk','tk_x':'tk'},inplace=True)  
            self.vFWVB=self.vFWVB[[
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
                    #Kk
                   ,'NAME'
                   ,'KVR','TM'
                   ,'XKOR','YKOR','ZKOR'  
                   ,'fkCONT'        
                 ]]     
            self.vFWVB.rename(columns={'NAME':'NAME_k','KVR':'KVR_k','TM':'TM_k'},inplace=True)  
            self.vFWVB.rename(columns={'XKOR':'XKOR_k','YKOR':'YKOR_k','ZKOR':'ZKOR_k'},inplace=True)     
                        
            self.vFWVB=pd.merge(self.vFWVB,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')  
            self.vFWVB.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'},inplace=True)    
            self.vFWVB=self.vFWVB[[
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
                    #Kk
                   ,'NAME_k'
                   ,'KVR_k','TM_k'
                   ,'XKOR_k','YKOR_k','ZKOR_k'  
                    #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR' 
                     ]]
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))             

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

            bins.append(self.vFWVB.W0.quantile(.25))
            binlabels.append('>=25%-Quart.')

            if self.vFWVB.W0.median() < self.vFWVB.W0.mean(): #50%-Quartil < Mittelwert
                bins.append(self.vFWVB.W0.median()) 
                binlabels.append('>=Median')

            bins.append(self.vFWVB.W0.mean())
            binlabels.append('>=Mittelwert')

            bins.append(bins[-1]*2)
            binlabels.append('>=2xMittelw.')

            if bins[-1] < self.vFWVB.W0.std():
                bins.append(self.vFWVB.W0.std())
                binlabels.append('>=Standardabw.')

            if bins[-1] < self.vFWVB.W0.quantile(.95):
                bins.append(self.vFWVB.W0.quantile(.95))
                binlabels.append('>=95%-Quartil')

            bins.append(self.vFWVB.W0.max())
            binlabels.append('Max.')

            W0cat=pd.cut(self.vFWVB.W0,bins,include_lowest=True,right=True,precision=1)

            W0catLabels=[x + '-: ' +  re.sub('\]$','[',re.sub('\(' ,'[', y))  for x,y in zip(binlabels[:-1],W0cat.cat.categories)]
            W0catLabels[-1]=re.sub('\[$',']',W0catLabels[-1])

            #Category Data
            W0catSumPercent=self.vFWVB[self.vFWVB.W0>=0].groupby(W0cat).W0.sum()  /self.vFWVB[self.vFWVB.W0>=0].W0.sum() # kW Summe
            W0catAnzPercent=self.vFWVB[self.vFWVB.W0>=0].groupby(W0cat).W0.count()/self.vFWVB[self.vFWVB.W0>=0].W0.count() # Anzahl Summe

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

            for kWSum, x,color in zip(self.vFWVB[self.vFWVB.W0>=0].groupby(W0cat).W0.sum(),xTickValues,colorSumPercent):
                txt="{0:.0f}".format(float(kWSum)/1000)
                ax.annotate(txt 
                            ,xy=(x, 0), xycoords=('data', 'axes fraction')
                            ,xytext=(0, measureIdx*-10), textcoords='offset points', va='top', ha='center'
                            ,color=color
                           )
            ax.annotate("{0:.0f} MW Ges.".format(float(self.vFWVB[self.vFWVB.W0>=0].W0.sum())/1000) 
                            ,xy=(x, 0), xycoords=('data', 'axes fraction')
                            ,xytext=(+20,measureIdx*-10), textcoords='offset points', va='top', ha='left'
                       )             

            measureIdx=measureIdx+1
            for count,x,color in zip(self.vFWVB[self.vFWVB.W0>=0].groupby(W0cat).W0.count(),xTickValues,colorAnzPercent):
                txt="{0:d}".format(int(count))
                ax.annotate(txt
                           ,xy=(x, 0),xycoords=('data', 'axes fraction')
                           ,xytext=(0, measureIdx*-10),textcoords='offset points', va='top', ha='center'
                           ,color=color
                           )
            ax.annotate("{0:d} Anz Ges.".format(int(self.vFWVB[self.vFWVB.W0>=0].W0.count())) 
                          ,xy=(x, 0),xycoords=('data', 'axes fraction')
                          ,xytext=(+20, measureIdx*-10), textcoords='offset points', va='top', ha='left'
                       )  
            
            #y-Labels 
            txyl=ax.set_ylabel('MW/MW Ges. u. Anz/Anz Ges.')
            txyr=ax2.set_ylabel('MW kum. in % u. Anz kum. in %')

            legend=plt.legend([lineW0catSumPercent,lineW0catAnzPercent],['MW kum. in %','Anz kum. in %'],loc='upper left')
            plt.grid()

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

