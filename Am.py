"""

"""

__version__='90.12.3.2.dev1'



import os
import sys


import re
import pandas as pd
import numpy as np
import warnings
import tables

import h5py
import time

import base64
import struct

import logging

import glob


import math

import pyodbc

# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

# ---
# --- main Imports
# ---
import argparse
import unittest
import doctest
   
class AmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Am():
    """SIR 3S AccessDB to pandas DataFrames.

    Args:
        * accFile (str): SIR 3S AccessDB
           
    Attributes:
       
    Raises:
        AmError
    """

               
    def __init__(self,accFile):

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            if os.path.exists(accFile):  
                if os.access(accFile,os.W_OK):
                    pass
                else:
                    logStrFinal="{:s}{:s}: Not writetable!".format(logStr,accFile)     
                    raise XmError(logStrFinal)  
            else:
                logStrFinal="{:s}{:s}: Not existing!".format(logStr,accFile)     
                raise XmError(logStrFinal)  

            Driver=[x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
            if Driver == []:
                logStrFinal="{:s}{:s}: No Microsoft Access Driver!".format(logStr,accFile)     
                raise XmError(logStrFinal)  

            conStr=(
                r'DRIVER={'+Driver[0]+'};'
                r'DBQ='+accFile+';'
                )
            logger.debug("{0:s}conStr: {1:s}".format(logStr,conStr)) 

            con = pyodbc.connect(conStr)
            cur = con.cursor()

            # all Tables in DB
            tableNames=[table_info.table_name for table_info in cur.tables(tableType='TABLE')]
            logger.debug("{0:s}tableNames: {1:s}".format(logStr,str(tableNames))) 
            allTables=set(tableNames)

            #pairTypes=['_BZ','_ROWS','_ROWT','_ROWD']
            #tablePairsBVBZ=[(re.search('(?P<BV>[A-Z]+)('+pairType+')$',table_info.table_name).group('BV'),table_info.table_name) for table_info in cur.tables(tableType='TABLE') if re.search('(?P<BV>[A-Z]+)('+pairType+')$',table_info.table_name) != None]




           
          
            self.dataFrames={}


            # process pairTables
            pairTables=set()

            pairViews=set()
            pairViews_BZ=set()
            pairViews_ROWS=set()
            pairViews_ROWT=set()
            pairViews_ROWD=set()

            for pairType in ['_BZ','_ROWS','_ROWT','_ROWD']:
                logger.debug("{0:s}pairType: {1:s}: ####".format(logStr,pairType)) 
                tablePairsBVBZ=[(re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name).group('BV'),table_info.table_name) for table_info in cur.tables(tableType='TABLE') if re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name) != None]
                for (BV,BZ) in tablePairsBVBZ:
                    
                    if BZ == 'PGRP_PUMP_BZ': # BV: PUMP BVZ: PGRP_PUMP_BZ V: V_PUMP - Falsch!
                        continue

                    pairTables.add(BV)
                    pairTables.add(BZ)
                                        
                    sql='select * from '+BZ+' inner join '+BV+' on '+BZ+'.fk='+BV+'.pk'
                    df=pd.read_sql(sql,con)
                    VName='V_BVZ_'+BV
                    logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s}".format(logStr,BV,BZ,VName)) 
                    self.dataFrames[VName]=df

                    pairViews.add(VName)
                    if pairType=='_BZ':
                        pairViews_BZ.add(VName)
                    elif pairType=='_ROWS':
                        pairViews_ROWS.add(VName)
                    elif pairType=='_ROWT':
                        pairViews_ROWT.add(VName)
                    elif pairType=='_ROWD':
                        pairViews_ROWD.add(VName)

            for (BV,BZ) in [('PGRP_PUMP','PGRP_PUMP_BZ')]:
                                       
                    pairTables.add(BV)
                    pairTables.add(BZ)
                                        
                    sql='select * from '+BZ+' inner join '+BV+' on '+BZ+'.fk='+BV+'.pk'
                    df=pd.read_sql(sql,con)
                    VName='V_BVZ_'+BV
                    logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s}".format(logStr,BV,BZ,VName)) 
                    self.dataFrames[VName]=df

                    pairViews.add(VName)
                    pairViews_BZ.add(VName)

            
            notInPairTables=sorted(allTables-pairTables)
            logger.debug("{0:s}not in  pairTables: {1:s}".format(logStr,str(notInPairTables))) 
 
            notInPairTables=[
               'AB_DEF', 'AGSN', 'ARRW', 'ATMO'
              ,'BENUTZER', 'BREF'
             , 'CIRC', 'CONT', 'CRGL'
             , 'DATENEBENE', 'DPGR_DPKT', 'DPKT', 'DRNP'
             , 'ELEMENTQUERY'
             , 'FSTF', 'FWBZ'
             , 'GKMP', 'GMIX', 'GRAV', 'GTXT'
             , 'HAUS'
             , 'LAYR', 'LTGR'
             , 'MODELL', 'MWKA'
             , 'NRCV'
             , 'OVAL'
             , 'PARV', 'PGPR', 'PLYG', 'POLY', 'PROZESSE', 'PZON'
             , 'RCON', 'RECT', 'REGP', 'RMES_DPTS', 'ROHR_VRTX', 'RPFL', 'RRCT'
             , 'SIRGRAF', 'SOKO', 'SPLZ', 'STRASSE', 'SYSTEMKONFIG'
             , 'TIMD', 'TRVA'
             , 'UTMP'
             , 'VARA', 'VARA_CSIT', 'VARA_WSIT'
             , 'VERB', 'VKNO', 'VRCT'
             , 'WBLZ']


            # process Not pairTables
            notPairViews=set()
            for tableName in  notInPairTables:

                 sql='select * from '+tableName 
                 df=pd.read_sql(sql,con)
                 VName='V_'+tableName
                 logger.debug("{0:s}V: {1:s}".format(logStr,BV,BZ,VName)) 
                 self.dataFrames[VName]=df

                 notPairViews.add(VName)


            self.viewSets={}

            self.viewSets['pairViews']=sorted(pairViews)
            self.viewSets['pairViews_BZ']=sorted(pairViews_BZ)
            self.viewSets['pairViews_ROWS']=sorted(pairViews_ROWS)
            self.viewSets['pairViews_ROWT']=sorted(pairViews_ROWT)
            self.viewSets['pairViews_ROWD']=sorted(pairViews_ROWD)
            self.viewSets['notPairViews']=sorted(notPairViews)








           
                          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise AmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

  



