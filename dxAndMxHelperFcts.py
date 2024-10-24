# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:36:59 2024

@author: wolters
"""

import os
from os import access, R_OK
from os.path import isfile

import sys

import re

import logging

import pandas as pd

import numpy as np

import networkx as nx    

#import importlib
import glob

import math

import pickle

import geopandas

from datetime import datetime

import subprocess




# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

try:
    from PT3S import Dx
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Dx - trying import Dx instead ... maybe pip install -e . is active ...')) 
    import Dx

try:
    from PT3S import Mx
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Mx - trying import Mx instead ... maybe pip install -e . is active ...')) 
    import Mx

try:
    from PT3S import dxDecodeObjsData
except:
    import dxDecodeObjsData


class dxWithMxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class dxWithMx():
    """Wrapper for dx with attached mx.
    """
    def __init__(self,dx,mx,crs=None):
        """
        :param dx: a Dx object
        :type dx: Dx.Dx()
        :param mx: a Mx object
        :type mx: Mx.Mx()        
        :param crs: (=coordinate reference system) Determines crs used in geopandas-Dfs (Possible value:'EPSG:25832'). If None, crs will be read from SIR 3S' database file.
        :type crs: str, optional, default=None  
                      
        .. note:: a dxWithMx object is returned by dxAndMxHelperFcts.readDxAndMx(); see also documentation there; the object is a wrapper for Dx with attached Mx  
                        
        """        
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.dx = dx
            #self.mx = mx
            
            #self.dfLAYR=self._dfLAYR()    
            
            self.dfWBLZ=dxDecodeObjsData.Wblz(self.dx)
            self.dfAGSN=dxDecodeObjsData.Agsn(self.dx)            
                        
            self.V3_ROHR=dx.dataFrames['V3_ROHR'].copy(deep=True)
            self.V3_KNOT=dx.dataFrames['V3_KNOT'].copy(deep=True)
            self.V3_FWVB=dx.dataFrames['V3_FWVB'].copy(deep=True)
            self.V3_VBEL=dx.dataFrames['V3_VBEL'].copy(deep=True)
            
            if not isinstance(mx,Mx.Mx):  
                (self.gdf_FWVB,self.gdf_ROHR,self.gdf_KNOT)=self._gdfs(crs)
                          
            if isinstance(mx,Mx.Mx):  
                
                
                self.mx = mx
                
                modellName, ext = os.path.splitext(self.dx.dbFile)
                logger.info("{0:s}{1:s}: processing dx and mx ...".format(logStr,os.path.basename(modellName)))                 
                
                # mx2Idx to V3_KNOT, V3_ROHR, V3_FWVB, etc.
                # mx2NofPts to V3_ROHR  
                # mx2Idx to V3_VBEL
                self.dx.MxSync(self.mx)
                self.V3_ROHR=dx.dataFrames['V3_ROHR'].copy(deep=True)
                self.V3_KNOT=dx.dataFrames['V3_KNOT'].copy(deep=True)
                self.V3_FWVB=dx.dataFrames['V3_FWVB'].copy(deep=True)    
                self.V3_VBEL=dx.dataFrames['V3_VBEL'].copy(deep=True)
                                
                # Vec-Results to V3_KNOT, V3_ROHR, V3_FWVB, etc.
                V3sErg=self.dx.MxAdd(self.mx)                
                self.V3_ROHR=V3sErg['V3_ROHR']
                self.V3_KNOT=V3sErg['V3_KNOT']
                self.V3_FWVB=V3sErg['V3_FWVB']
                self.V3_VBEL=V3sErg['V3_VBEL']
                
                #VBEL
                try:                                    
                     t0=pd.Timestamp(self.mx.df.index[0].strftime('%Y-%m-%d %X.%f'))
                     QM=('STAT'
                                 ,'QM'
                                 ,t0
                                 ,t0
                                 )
                     self.V3_VBEL['QM']=self.V3_VBEL[QM]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['QM'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col QM in V3_VBEL failed.'))   
                     
                try:                                                         
                     PH_i=str(('STAT'
                                 ,'KNOT~*~*~*~PH'
                                 ,t0
                                 ,t0
                                 ))+'_i'
                     self.V3_VBEL['PH_i']=self.V3_VBEL[PH_i]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['PH_i'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col PH_i in V3_VBEL failed.'))    
                     
                try:                                                         
                     PH_k=str(('STAT'
                                 ,'KNOT~*~*~*~PH'
                                 ,t0
                                 ,t0
                                 ))+'_k'
                     self.V3_VBEL['PH_k']=self.V3_VBEL[PH_k]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['PH_k'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col PH_k in V3_VBEL failed.'))                         
     
                  
                try:                                                         
                     T_i=str(('STAT'
                                 ,'KNOT~*~*~*~T'
                                 ,t0
                                 ,t0
                                 ))+'_i'
                     self.V3_VBEL['T_i']=self.V3_VBEL[T_i]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['T_i'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col T_i in V3_VBEL failed.'))     
                     
                try:                                                         
                     T_k=str(('STAT'
                                 ,'KNOT~*~*~*~T'
                                 ,t0
                                 ,t0
                                 ))+'_k'
                     self.V3_VBEL['T_k']=self.V3_VBEL[T_k]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['T_k'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col T_k in V3_VBEL failed.'))                          
        

                try:                                                         
                     H_i=str(('STAT'
                                 ,'KNOT~*~*~*~H'
                                 ,t0
                                 ,t0
                                 ))+'_i'
                     self.V3_VBEL['H_i']=self.V3_VBEL[H_i]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['H_i'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col H_i in V3_VBEL failed.'))    
                     
                try:                                                         
                     H_k=str(('STAT'
                                 ,'KNOT~*~*~*~H'
                                 ,t0
                                 ,t0
                                 ))+'_k'
                     self.V3_VBEL['H_k']=self.V3_VBEL[H_k]      
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['H_k'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col H_k in V3_VBEL failed.'))                
                     
                try:                                                         
                    RHO_i=str(('STAT'
                                ,'KNOT~*~*~*~RHO'
                                ,t0
                                ,t0
                                ))+'_i'
                    self.V3_VBEL['RHO_i']=self.V3_VBEL[RHO_i]      
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['RHO_i'] ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col RHO_i in V3_VBEL failed.'))    
                    
                try:                                                         
                    RHO_k=str(('STAT'
                                ,'KNOT~*~*~*~RHO'
                                ,t0
                                ,t0
                                ))+'_k'
                    self.V3_VBEL['RHO_k']=self.V3_VBEL[RHO_k]      
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['RHO_k'] ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col RHO_k in V3_VBEL failed.'))                                     
                     
                try:                                                                             
                    self.V3_VBEL['mlc_i']=self.V3_VBEL[PH_i]*10**5/(self.V3_VBEL[RHO_i]*9.81)+self.V3_VBEL['ZKOR_i']
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['mlc_i'] ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col mlc_i in V3_VBEL failed.'))    
                    
                try:                                                                             
                    self.V3_VBEL['mlc_k']=self.V3_VBEL[PH_k]*10**5/(self.V3_VBEL[RHO_k]*9.81)+self.V3_VBEL['ZKOR_k']
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_VBEL['mlc_k'] ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col mlc_k in V3_VBEL failed.'))                        
                                                                           
                # ROHR                                 
                try:                                    
                    #t0=pd.Timestamp(self.mx.df.index[0].strftime('%Y-%m-%d %X.%f'))
                    QMAV=('STAT'
                                ,'ROHR~*~*~*~QMAV'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['QMAVAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[QMAV]) ,axis=1)      
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['QMAVAbs'] ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col QMAVAbs=Abs(STAT ROHR~*~*~*~QMAV) in V3_ROHR failed.'))   
                    
                try:                                                        
                    VAV=('STAT'
                                ,'ROHR~*~*~*~VAV'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['VAVAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[VAV]) ,axis=1)       
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['VAVAbs'] ok so far."))                                                         
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col VAVAbs=Abs(STAT ROHR~*~*~*~VAV) in V3_ROHR failed.'))       
                    
                try:                                                        
                    PHR=('STAT'
                                ,'ROHR~*~*~*~PHR'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['PHRAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[PHR]) ,axis=1)     
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['PHRAbs'] ok so far."))                                                           
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col PHRAbs=Abs(STAT ROHR~*~*~*~PHR) in V3_ROHR failed.'))     

                try:                                                        
                    JV=('STAT'
                                ,'ROHR~*~*~*~JV'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['JVAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[JV]) ,axis=1)      
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['JVAbs'] ok so far."))                                                          
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col JVAbs=Abs(STAT ROHR~*~*~*~JV) in V3_ROHR failed.')) 
                             
                                                                            
                # ROHRVEC
                try:   
                    self.V3_ROHRVEC=self._V3_ROHRVEC(self.V3_ROHR)                
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHRVEC ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing of V3_ROHRVEC failed.'))                 
                
                    
                    
                # FWVB
                if not self.V3_FWVB.empty:
                    try:                                                         
                         W=('STAT'
                                     ,'FWVB~*~*~*~W'
                                     ,t0
                                     ,t0
                                     )
                         self.V3_FWVB['W']=self.V3_FWVB[W]
                         logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_FWVB['W'] ok so far."))                                                      
                    except Exception as e:
                         logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                         logger.debug(logStrTmp) 
                         logger.debug("{0:s}{1:s}".format(logStr,'Constructing col W in V3_FWVB failed.'))   
                         
                    try:                                             
                         QM=('STAT'
                                     ,'FWVB~*~*~*~QM'
                                     ,t0
                                     ,t0
                                     )
                         self.V3_FWVB['QM']=self.V3_FWVB[QM]
                         logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_FWVB['QM'] ok so far."))                                                      
                    except Exception as e:
                         logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                         logger.debug(logStrTmp) 
                         logger.debug("{0:s}{1:s}".format(logStr,'Constructing col QM in V3_FWVB failed.'))     
                         
                    try:     
                         TI=('STAT'
                                     ,'FWVB~*~*~*~TI'
                                     ,t0
                                     ,t0
                                     )
                         self.V3_FWVB['TI']=self.V3_FWVB[TI]
                         logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_FWVB['TI'] ok so far."))                                                      
                    except Exception as e:
                         logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                         logger.debug(logStrTmp) 
                         logger.debug("{0:s}{1:s}".format(logStr,'Constructing col TI in V3_FWVB failed.'))    
    
                    try:     
                         TK=('STAT'
                                     ,'FWVB~*~*~*~TK'
                                     ,t0
                                     ,t0
                                     )
                         self.V3_FWVB['TK']=self.V3_FWVB[TK]
                         logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_FWVB['TK'] ok so far."))                                                      
                    except Exception as e:
                         logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                         logger.debug(logStrTmp) 
                         logger.debug("{0:s}{1:s}".format(logStr,'Constructing col TK in V3_FWVB failed.'))    
                     
                
                # WBLZ
                
                try:                
                    V_WBLZ=self.dx.dataFrames['V_WBLZ']
                    df=V_WBLZ[['pk','fkDE','rk','tk','BESCHREIBUNG','NAME','TYP','AKTIV','IDIM']]
                    dfMx=mx.getVecAggsResultsForObjectType(Sir3sVecIDReExp='^WBLZ~\*~\*~\*~')
                    if dfMx.empty:
                        logger.debug("{0:s}{1:s}".format(logStr,'Adding MX-Results to V3_WBLZ: no such results.'))           
                    else:
                        dfMx.columns=dfMx.columns.to_flat_index()                    
                        self.V3_WBLZ=pd.merge(df,dfMx,left_on='tk',right_index=True)
                        logger.debug("{0:s}{1:s}".format(logStr,'Adding MX-Results to V3_WBLZ ok so far.'))                 
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing V3_WBLZ failed.'))
                
                #gdfs                
                (self.gdf_FWVB,self.gdf_ROHR,self.gdf_KNOT)=self._gdfs(crs)
                


            # G    
                                
            try:
                # Graph bauen    
                self.G=nx.from_pandas_edgelist(df=self.V3_VBEL.reset_index(), source='NAME_i', target='NAME_k', edge_attr=True) 
                nodeDct=self.V3_KNOT.to_dict(orient='index')    
                nodeDctNx={value['NAME']:value|{'idx':key} for key,value in nodeDct.items()}
                nx.set_node_attributes(self.G,nodeDctNx)     
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G ok so far.'))                           
                
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.info("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G failed.')) 


            try:               
                # Darstellungskoordinaten des Netzes bezogen auf untere linke Ecke == 0,0
                vKnot=self.dx.dataFrames['V3_KNOT']            
                vKnotNet=vKnot[    
                (vKnot['ID_CONT']==vKnot['IDPARENT_CONT'])
                ]
                xMin=vKnotNet['XKOR'].min()
                yMin=vKnotNet['YKOR'].min()            
                self.nodeposDctNx={name:(x-xMin
                              ,y-yMin)
                               for name,x,y in zip(vKnotNet['NAME']
                                                  ,vKnotNet['XKOR']
                                                  ,vKnotNet['YKOR']
                                                  )
                }
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G nodeposDctNx ok so far.'))    
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.info("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G nodeposDctNx failed.')) 
               
            # GSig
                 
            if 'V3_RVBEL' in self.dx.dataFrames.keys():  
                df=self.dx.dataFrames['V3_RVBEL'].reset_index()
                if not df.empty:
                    try:
                        # Graph Signalmodell bauen
                        self.GSig=nx.from_pandas_edgelist(df=df, source='Kn_i', target='Kn_k', edge_attr=True,create_using=nx.DiGraph())
                        nodeDct=self.dx.dataFrames['V3_RKNOT'].to_dict(orient='index')
                        nodeDctNx={value['Kn']:value|{'idx':key} for key,value in nodeDct.items()}
                        nx.set_node_attributes(self.GSig,nodeDctNx)
                        logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph GSig ok so far.'))    
                    except Exception as e:
                        logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                        logger.debug(logStrTmp) 
                        logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph GSig failed.'))            
                                
            # AGSN                        
            try:                                                        
                self.V3_AGSN=self._V3_AGSN(self.dfAGSN)                                                              
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing V3_AGSN failed.'))     

            try:                                                                        
                # Rohrvektoren 
                self.V3_AGSNVEC=self._V3_AGSNVEC(self.V3_AGSN)#.copy(deep=True))                            
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing V3_AGSNVEC failed.'))                           
                                
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))            


    def _V3_ROHRVEC(self,V3_ROHR):
        """
        V3_ROHRVEC: Expanding V3_ROHR to V3_ROHRVEC (includes interior points). V3_ROHRVEC is a dxWithMx object Attribute.
        
        :param V3_ROHR: dxWithMx Attribute
        :type V3_ROHR: df
        
        :return: V3_ROHRVEC
        :rtype: df        
        
        .. note:: 
            
            The interior points are defined by the output grid definition for pipes in the SIR 3S model. The numerical grid with which SIR 3S calculates is different from the output grid.
            The returned V3_ROHRVEC (one row per pipe and interior point) has the following columns:
                        
                - pk: Pipe-pk
                - tk: Pipe-tk                
                - ...
                - L
                - ...
                - NAME_i, NAME_k
                - mx2NofPts
                - dL (=L/(mx2NofPts-1))
                - ...
                - mx2Idx
                
                -  ('STAT|TIME|TMIN|...','ROHR...QMAV|PHR|...', a Timestamp, a Timestamp): Pipe-Results
                
                - "('STAT|TIME|TMIN|...','KNOT...PH|H|...',     a Timestamp, a Timestamp)"_i: Pipe i-NODE Results
                - "('STAT|TIME|TMIN|...','KNOT...PH|H|...',     a Timestamp, a Timestamp)"_k: Pipe k-NODE Results
                
                - QMAVAbs: Pipes STAT QMAV-Result (absolute value)
                - VAVAbs: Pipes STAT VAV-Result (absolute value)
                - PHRAbs: Pipes STAT PHR-Result (absolute value)
                - JVAbs: Pipes STAT JV-Result (absolute value)
                
                - IptIdx: an Index of the points: S: Start (i-NODE), E: End (k-NODE), interior points: 0,1,2,... 
                - IptIdxAsNo: an Index of the points starting with 0 at i-NODE: 0,1,2,...
                - IptIdxAsNoRev: an Index of the points starting with 0 at k-NODE: 0,1,2,...
                
                - SVEC: x in Edge-direction (IptIdx=S: 0.; IptIdx=E: L)
                - SVECRev (IptIdx=S: L; IptIdx=E: 0)
                - ZVEC: z
                
                - ('STAT|TIME|TMIN|...','ROHR...MVEC|PVEC|RHOVEC|TVEC|...', a Timestamp, a Timestamp): point Results
                
                - ('STAT|TIME|TMIN|...','manPVEC|mlcPVEC|barBzgPVEC|QMVEC|tMVEC|...',  a Timestamp, a Timestamp): point Results calculated by PT3S               
                                                
        """   
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try: 
            pass
                  
            vROHR=V3_ROHR
            rVecMx2Idx=[] 
            IptIdx=[] 
            #                annotieren in mx2Idx-Reihenfolge da die rVecs in mx2Idx-Reihenfolge geschrieben werden
            for row in vROHR.sort_values(['mx2Idx']).itertuples():
                            oneVecIdx=np.empty(row.mx2NofPts,dtype=int) 
                            oneVecIdx.fill(row.mx2Idx)                
                            rVecMx2Idx.extend(oneVecIdx)
                
                            oneLfdNrIdx=['S']
                            if row.mx2NofPts>2:                    
                                oneLfdNrIdx.extend(np.arange(row.mx2NofPts-2,dtype=int))
                            oneLfdNrIdx.append('E')
                            IptIdx.extend(oneLfdNrIdx)                    
            
            rVecChannels=[vec for vec in sorted(set(self.mx.dfVecAggs.index.get_level_values(1))) if re.search(Mx.regExpSir3sRohrVecAttrType,re.search(Mx.regExpSir3sVecID,vec).group('ATTRTYPE'))!= None]                                                        
            dfrVecAggs=self.mx.dfVecAggs.loc[(slice(None),rVecChannels,slice(None),slice(None)),:]
            dfrVecAggsT=dfrVecAggs.transpose()
            dfrVecAggsT.columns=dfrVecAggsT.columns.to_flat_index()
            
            cols=dfrVecAggsT.columns.to_list()
            
            #rVecAggsT annotieren mit mx2Idx
            dfrVecAggsT['mx2Idx']=rVecMx2Idx
            dfrVecAggsT['IptIdx']=IptIdx                    
            dfrVecAggsT=dfrVecAggsT.filter(['mx2Idx','IptIdx']+cols,axis=1)
            
            vROHR=pd.merge(self.V3_ROHR,dfrVecAggsT,left_on='mx2Idx',right_on='mx2Idx')
            
            # 1 Spalte SVEC
            rVecCols=[(a,b,c,d) for (a,b,c,d) in [col for col in vROHR.columns if type(col)==tuple] if re.search(Mx.regExpSir3sRohrVecAttrType,b)!=None]
            t0rVec=pd.Timestamp(self.mx.df.index[0].strftime('%Y-%m-%d %X'))#.%f'))
            SVEC=('STAT',
              'ROHR~*~*~*~SVEC',
              t0rVec,
              t0rVec)                    
            vROHR['SVEC']=vROHR[SVEC]
            sVecCols=[(a,b,c,d) for (a,b,c,d) in rVecCols if re.search('SVEC$',b)!=None]
            # andere SVEC-Spalten löschen
            vROHR=vROHR.drop(sVecCols,axis=1)   
            vROHR['SVECRev']=vROHR.apply(lambda row: row['L']-row['SVEC'],axis=1)
            
            # 1 Spalte IptIdxAsNo
            vROHR['IptIdxAsNo']=vROHR.groupby(by=['tk'])['IptIdx'].cumcount()
            # 1 Spalte IptIdxAsNoRev
            vROHR['IptIdxAsNoRev']=vROHR.apply(lambda row: row['mx2NofPts']-1-row['IptIdxAsNo'],axis=1)
            
            # 1 Spalte ZVEC                    
            ZVEC=('STAT',
              'ROHR~*~*~*~ZVEC',
              t0rVec,
              t0rVec)                    
            vROHR['ZVEC']=vROHR[ZVEC]
            zVecCols=[(a,b,c,d) for (a,b,c,d) in rVecCols if re.search('ZVEC$',b)!=None]
            # andere ZVEC-Spalten löschen
            vROHR=vROHR.drop(zVecCols,axis=1)         
                                                         
            # Druecke und Fluesse in anderen Einheiten errechnen                    
            pVecCols=[(a,b,c,d) for (a,b,c,d) in rVecCols if re.search(Mx.regExpSir3sVecID,b).group('ATTRTYPE') in ['PVEC','PVECMIN_INST','PVECMAX_INST']]
            pVecs=[b for (a,b,c,d) in pVecCols]
            pVecs=list(set(pVecs))
            
            mVecCols=[(a,b,c,d) for (a,b,c,d) in rVecCols if re.search(Mx.regExpSir3sVecID,b).group('ATTRTYPE') in ['MVEC']]
            mVecs=[b for (a,b,c,d) in mVecCols]
            mVecs=list(set(mVecs))
            
            rhoVecCols=[(a,b,c,d) for (a,b,c,d) in rVecCols if re.search(Mx.regExpSir3sVecID,b).group('ATTRTYPE') in ['RHOVEC']]
            
            pAtmosInBar=1.#0132
            try:
                vm=self.dx.dataFrames['VIEW_MODELLE']            
                vms=vm[vm['pk'].isin([self.dx.QGISmodelXk])].iloc[0]  
                ATMO=self.dx.dataFrames['ATMO']
                pAtmosInBar=ATMO[ATMO['fkDE']==vms.fkBASIS]['PATMOS'].iloc[0]   
            except:
                pass
                logger.debug(f"{logStr}pAtmos konnte nicht ermittelt werden. pAtmos=1. wird verwendet.")

            zBzg=0.
            try:
                vm=self.dx.dataFrames['VIEW_MODELLE']            
                vms=vm[vm['pk'].isin([self.dx.QGISmodelXk])].iloc[0]  
                FWBZ=self.dx.dataFrames['FWBZ']
                zBzg=FWBZ[FWBZ['fkDE']==vms.fkBASIS]['HGEBZG'].iloc[0]   
            except:
                pass
                logger.debug(f"{logStr}zBzg konnte nicht ermittelt werden. zBzg=0. wird verwendet.")
                    
            for (a,b,c,d) in rhoVecCols:
                
                for pVec in pVecs:
                    col=(a,pVec,c,d)
                    pVecAttr= re.search(Mx.regExpSir3sVecID,pVec).group('ATTRTYPE')
                    # man
                    vROHR[(a,'man'+pVecAttr,c,d)]=vROHR[col] - pAtmosInBar 
                    # mlc
                    vROHR[(a,'mlc'+pVecAttr,c,d)]=vROHR[(a,'man'+pVecAttr,c,d)]*10**5/(vROHR[(a,b,c,d)]*9.81)+vROHR['ZVEC']     
                    # barBzg
                    vROHR[(a,'barBzg'+pVecAttr,c,d)]=vROHR[(a,'man'+pVecAttr,c,d)] + (vROHR['ZVEC']-zBzg)*(vROHR[(a,b,c,d)]*9.81)*10**-5
                    
                    
                for mVec in mVecs:
                       col=(a,mVec,c,d)
                       mVecAttr= re.search(Mx.regExpSir3sVecID,mVec).group('ATTRTYPE')
                       # m3/h
                       vROHR[(a,'Q'+mVecAttr,c,d)]=vROHR[col]/vROHR[(a,b,c,d)]*3600
                       # t/h
                       vROHR[(a,'t'+mVecAttr,c,d)]=vROHR[(a,'Q'+mVecAttr,c,d)]*vROHR[(a,b,c,d)]/1000.
            
            
            return vROHR            
            
                      
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug(f"{logStr}_Done.") 


    # def _dfLAYR(self):
    #     """
    #     dfLAYR: one row per LAYR and OBJ. dfLAYR is a dxWithMx object Attribute.
                
    #     .. note:: 
            
    #         The returned dfLAYR (one row per LAYR and OBJ) has the following columns:
                
    #              LAYR:
    #                  - pk
    #                  - tk
    #                  - LFDNR (numeric)
    #                  - NAME
                
    #              LAYR-Info:
    #                  - AnzDerObjekteInGruppe
    #                  - AnzDerObjekteDesTypsInGruppe
                
    #              OBJ:
    #                  - TYPE
    #                  - ID
                
    #              OBJ-Info:
    #                  - NrDesObjektesDesTypsInGruppe
    #                  - NrDesObjektesInGruppe
    #                  - GruppenDesObjektsAnz
    #                  - GruppenDesObjektsNamen       
                      
    #     """   
                
    #     logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #     logger.debug(f"{logStr}Start.") 
        
    #     try: 
    #         dfLAYR=pd.DataFrame()
    #         dfLAYR=dxDecodeObjsData.Layr(self.dx)                                   
    #         return dfLAYR     
    #     except dxWithMxError:
    #         raise            
    #     except Exception as e:
    #         logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
    #         logger.debug(logStrFinal) 
    #         raise dxWithMxError(logStrFinal)                       
    #     finally:
    #         logger.debug(f"{logStr}_Done.") 


    def _gdfs(self,crs=None):
        """
        Create gdfs from V3-dfs.
        
        :param crs: (=coordinate reference system) Determines crs used in the geopandas-Dfs (Possible value:'EPSG:25832'). If None, crs will be read from SIR 3S' database file.
        :type crs: str, optional, default=None  
        
        :return: (gdf_FWVB, gdf_ROHR, gdf_KNOT)
        :rtype: tuple of gdfs         

        .. note:: 
            V3_FWVB, V3_ROHR, V3_KNOT and gdf_FWVB, gdf_ROHR, gdf_KNOT are dxWithMx object Attributes.
            
                - V3_FWVB: gdf_FWVB
                - V3_ROHR: gdf_ROHR
                - V3_KNOT: gdf_KNOT                
        """   
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try:
            
            gdf_FWVB=geopandas.GeoDataFrame()
            gdf_ROHR=geopandas.GeoDataFrame()
            gdf_KNOT=geopandas.GeoDataFrame()
            
            if not crs:
                try:               
                    dfSG=self.dx.dataFrames['SIRGRAF']
                    if 'SRID2' in dfSG.columns and dfSG['SRID2'].iloc[1] is not None:
                        crs = 'EPSG:' + str(int(dfSG['SRID2'].iloc[1]))
                    else:
                        crs = 'EPSG:' + str(int(dfSG['SRID'].iloc[1]))
                    logger.debug("{0:s}{1:s} {2:s}".format(logStr, 'crs reading successful: ', crs))
                except:
                    logger.debug("{0:s}{1:s}".format(logStr,'crs reading failed.'))  
                    #crs='EPSG:4326'
                    #logger.debug("{0:s}crs used: {1:s}".format(logStr,crs))  
            else:
                logger.debug("{0:s}{1:s} {2:s}".format(logStr, 'crs given value used: ', crs))
            
            try:
                                            
                gs=geopandas.GeoSeries.from_wkb(self.V3_FWVB['GEOMWKB'],crs=crs)
                gdf_FWVB=geopandas.GeoDataFrame(self.V3_FWVB,geometry=gs,crs=crs)
            
                gs=geopandas.GeoSeries.from_wkb(self.V3_ROHR['GEOMWKB'],crs=crs)
                gdf_ROHR=geopandas.GeoDataFrame(self.V3_ROHR,geometry=gs,crs=crs)
                
                gs=geopandas.GeoSeries.from_wkb(self.V3_KNOT['GEOMWKB'],crs=crs)
                gdf_KNOT=geopandas.GeoDataFrame(self.V3_KNOT,geometry=gs,crs=crs)
                
                logger.debug("{0:s}{1:s}".format(logStr,"Constructing of gdfs ok so far."))  
                
            
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing of (some) gdfs failed.'))
            
            return(gdf_FWVB,gdf_ROHR,gdf_KNOT)
    
  
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug(f"{logStr}_Done.") 



    def _V3_AGSN(self,dfAGSN):
        """
        V3_AGSN: Create V3_AGSN from dfAGSN. V3_AGSN is a dxWithMx object Attribute.
        
        :param dfAGSN: dxWithMx attribute
        :type dfAGSN: df
        
        :return: V3_AGSN: dfAGSN expanded to V3_AGSN.
        :rtype: df        
        
        .. note:: 
            
            AGSN is the German abbreviation for longitudinal sections / cuts (defined in the SIR 3S model).
            The returned V3_AGSN (one row per Edge in (Section,Layer)) has the following columns:
        
                - Pos: Position of Edge in (Section,Layer) starting with 0; Pos=-1: startNODE-row (same index as Pos=0 row)
                - pk: Section-pk
                - tk: Section-tk
                - LFDNR: Section-LFDNR (numeric)
                - NAME: Section-Name
                - XL: Section-Layer:  0: everything; 1: SL (the stuff before BLn in SIR 3S BLOB); 2: RL (the stuff after BLn in SIR 3S BLOB)     
                - compNr: Number of the connected Component in (Section,Layer) starting with 1
                - nextNODE: Name of the next Node in cut-direction reached by the Edge (startNODE-Name for Pos=-1)
                
                - OBJTYPE: Edge-Type
                - OBJID: Edge-ID
                
                - L (0 for Pos=-1)
                - DN
                - Am2
                - Vm3
                
                - NAME_CONT
                - NAME_i
                - NAME_k
                
                - ZKOR_n: nextNODEs ZKOR
                - BESCHREIBUNG_n: nextNODEs BESCHREIBUNG
                - KVR_n: nextNODEs KVR
                
                - LSum: cumulated L up to nextNODE
                - direction: XL=0,1: 1 if edge defined in cut-direction, otherwise -1; XL=2: 1 if edge defined in reverse cut-direction, otherwise -1 
                
                - PH_n: nextNODEs STAT PH-result (i.e. bar) (startNODEs result for Pos=-1)
                - H_n: nextNODEs STAT H-result (i.e. barBzg) (startNODEs result for Pos=-1)
                - mlc_n: nextNODEs STAT H-result (startNODEs result for Pos=-1) 
                - RHO_n: nextNODEs STAT RHO-result (startNODEs result for Pos=-1)
                - T_n: nextNODEs STAT T-result (startNODEs result for Pos=-1)                 
                - QM: Egde STAT QM-Result (startNODEs result for Pos=-1)
                
                -  ('STAT|TIME|TMIN|...','QM', a Timestamp, a Timestamp): Egde QM-Results
                
                - "('STAT|TIME|TMIN|...','KNOT...PH|H|...', a Timestamp, a Timestamp)"_n: nextNODEs Results
                
                - "('STAT|TIME|TMIN|...','mlc|...'        , a Timestamp, a Timestamp)"_n: nextNODEs Results calculated by PT3S 
                
                    
                
            
        """   
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try: 
            if dfAGSN[~dfAGSN['pk'].isin([-1,'-1'])].empty:
                logger.debug(f"{logStr} dfAGSN empty.") 
                return dfAGSN
        
            dfAGSN=constructNewMultiindexFromCols(dfAGSN.copy(deep=True),mColNames=['TYPE','ID']).sort_values(by=['LFDNR','XL','Pos'])
            # urspruengliche Cols
            colsAGSNBase=dfAGSN.columns.to_list()
            
            dfAGSN=pd.merge(dfAGSN,self.V3_VBEL,left_index=True,right_index=True,suffixes=('','_VBEL')).sort_values(by=['LFDNR','XL','Pos'])
            
            cols=dfAGSN.columns.to_list()
            colsErg=cols[cols.index('mx2Idx')+1:]
            
            colsVBELBase=['OBJTYPE','OBJID',
                          'L','DN','Am2','Vm3','NAME_CONT','NAME_i','NAME_k']
            
            dfAGSN=dfAGSN.filter(items=colsAGSNBase#.to_list()
                                 +colsVBELBase
                                 +['ZKOR_i','ZKOR_k'
                                  ,'BESCHREIBUNG_i','BESCHREIBUNG_k'
                                  ,'KVR_i','KVR_k'
                                  ]
                                 +colsErg)
            
            
            # Sachspalten _i,_k
            colsSach_i=['ZKOR_i','BESCHREIBUNG_i','KVR_i']
            colsSach_k=['ZKOR_k','BESCHREIBUNG_k','KVR_k']
            
            # ob VBEL in Schnittrichtung definiert anlegen
            dfAGSN['direction']=1
             
            # zugeh. Sachspalten _n anlegen
            colsSach_n=[]
            for col_i,col_k in zip(colsSach_i,colsSach_k):
                col_n=col_i.replace('_i','_n')
                #print(col_n)
                dfAGSN[col_n]=None
                colsSach_n.append(col_n)                  
                            
                        
            # Ergebnisspalten _i,_k
            colsErg_i=[col for col in colsErg if type(col) == str and re.search('_i$',col)]
            colsErg_k=[col for col in colsErg if type(col) == str and re.search('_k$',col)]
            
            # zugeh. Ergebnisspalten _n anlegen
            colsErg_n=[]
            for col_i,col_k in zip(colsErg_i,colsErg_k):
                col_n=col_i.replace('_i','_n')
                #print(col_n)
                dfAGSN[col_n]=None
                colsErg_n.append(col_n)  
                                
            #logger.debug("{0:s}dfAGSN.columns.to_list(): {1:s}".format(logStr,str(dfAGSN.columns.to_list())))       
                            
            dfAGSN=dfAGSN.reset_index().rename(columns={'level_0':'OBJTYPE','level_1':'OBJID'})
            
            #logger.debug("{0:s}dfAGSN.columns.to_list(): {1:s}".format(logStr,str(dfAGSN.columns.to_list())))
            
            # Schnittrichtung bestücken; Ergebnisspalten und Sachspalten nach Schnittrichtung bestücken
            for index, row in dfAGSN.iterrows():
                
                    if row['XL'] in [0,1]:
                        if row['nextNODE'] == row['NAME_k']:
                            pass
                        elif row['nextNODE'] == row['NAME_i']:                            
                            dfAGSN.loc[index,'direction']=-1 # VL-Fluss von links nach rechts (in Schnittr.) pos. def. aber VBEL von rechts nach links
                    else:
                        if row['nextNODE'] == row['NAME_k']:
                            dfAGSN.loc[index,'direction']=-1 # RL-Fluss von rechts nach links (entgegen Schnittr.) pos. def. aber VBEL von links nach rechts
                        elif row['nextNODE'] == row['NAME_i']:                            
                            pass
                                        
                    for col_n,col_i,col_k in zip(colsErg_n,colsErg_i,colsErg_k):        
                        if row['XL'] in [0,1]:
                            if dfAGSN.loc[index,'direction']==1:
                                dfAGSN.loc[index,col_n]= row[col_k]
                            else:
                                dfAGSN.loc[index,col_n]= row[col_i]   
                        else:
                            if dfAGSN.loc[index,'direction']==-1:
                                dfAGSN.loc[index,col_n]= row[col_k]
                            else:
                                dfAGSN.loc[index,col_n]= row[col_i]                                   
                            
                            
                    #logger.debug(f"{logStr} {row['NAME_i']} {row['NAME_k']} {dfAGSN.loc[index,'direction']} PH_i={row['PH_i']} PH_k={row['PH_k']} PH_n={dfAGSN.loc[index,'PH_n']} mlc_i={row['mlc_i']} mlc_k={row['mlc_k']} mlc_n={dfAGSN.loc[index,'mlc_n']} ") 
                            
                    for col_n,col_i,col_k in zip(colsSach_n,colsSach_i,colsSach_k):    
                        if row['XL'] in [0,1]:
                            if dfAGSN.loc[index,'direction']==1:
                                dfAGSN.loc[index,col_n]= row[col_k]
                            else:
                                dfAGSN.loc[index,col_n]= row[col_i]   
                        else:
                            if dfAGSN.loc[index,'direction']==-1:
                                dfAGSN.loc[index,col_n]= row[col_k]
                            else:
                                dfAGSN.loc[index,col_n]= row[col_i]                                  
                        
                        
                        #if dfAGSN.loc[index,'direction']==1:                                
                        #    dfAGSN.loc[index,col_n]= row[col_k]
                        #else:
                        #    dfAGSN.loc[index,col_n]= row[col_i]  
                                                                                    
            # am Anfang jedes Schnittes für jeden Leiter 1 Zeile ergänzen mit Pos=-1 (Vorlage für die ergänzte Zeile: Pos=0)
            
            # Zeilen herausfinden
            startRowIdx=[]
            for index, row in dfAGSN.iterrows():
                if row['Pos']==0:
                    #print(row)
                    startRowIdx.append(index)                        
            dfStartRows=dfAGSN.loc[startRowIdx,:].sort_values(by=['LFDNR','XL','Pos']).copy(deep=True)#.drop_duplicates()
            #dfStartRows=dfStartRows[dfStartRows['Pos']==0]       
            
            # zu ergänzende Zeilen bearbeiten
            
            # - Pos = -1
            # - L = 0
            # - nextNODE ist der Startknoten in Schnittrichtung (also nicht nextNODE im Wortsinn)
            # - Ergebnissspalten bekommen die Werte des Startknotens in Schnittrichtung
            # - index: bleibt; d.h. unter den mehrfach belegten Indices sind ergänzte Zeilen (zu erkennen an Pos = -1)
            
            dfRowsAdded=[]
            for index,row in dfStartRows.iterrows():
            
                    row['Pos']=-1
                    row['L']=0
                    
                    if row['XL'] in [0,1]:
                        if row['direction']==1:
                            row['nextNODE']=row['NAME_i']
                        else:
                            row['nextNODE']=row['NAME_k']
                    else:
                        if row['direction']==-1:
                            row['nextNODE']=row['NAME_i']
                        else:
                            row['nextNODE']=row['NAME_k']                            
                        
                    for col_n,col_i,col_k in zip(colsErg_n,colsErg_i,colsErg_k):
                        #print(col_n,col_i,col_k)
                        
                        if row['XL'] in [0,1]:                                
                            if row['direction']==1:                            
                                row[col_n]= row[col_i]
                            else:                                
                                row[col_n]= row[col_k] 
                        else:
                            if row['direction']==-1:                            
                                row[col_n]= row[col_i]
                            else:                                
                                row[col_n]= row[col_k]                                                                             
                    
                    #logger.debug(f"{logStr} Pos -1: {row['NAME_i']} {row['NAME_k']} {row['direction']} PH_i={row['PH_i']} PH_k={row['PH_k']} PH_n={row['PH_n']} mlc_i={row['mlc_i']} mlc_k={row['mlc_k']} mlc_n={row['mlc_n']} ") 
                    
                    df = pd.DataFrame([row])
                    dfRowsAdded.append(df)                 
            
            # Zeilen ergänzen
            dfAGSN=pd.concat([dfAGSN]+dfRowsAdded).sort_values(by=['LFDNR','XL','Pos'])
            
            # Ergebnisspalten _i,_k löschen
            dfAGSN=dfAGSN.drop(colsErg_i+colsErg_k,axis=1)
            
            # Sachspalten _i,_k löschen
            dfAGSN=dfAGSN.drop(colsSach_i+colsSach_k,axis=1)                
                            
            dfAGSN['L']=dfAGSN['L'].fillna(0)                
            cols=dfAGSN.columns.to_list()
            dfAGSN.insert(cols.index('L')+1,'LSum',dfAGSN.groupby(['LFDNR','XL'])['L'].cumsum())
            
            dfAGSN=dfAGSN.filter(items=colsAGSNBase
                                 +colsVBELBase
                                 +colsSach_n #(u.a. ZKOR_n)
                                 +['LSum','direction']
                                 +colsErg # die _i,_k gibt es hier bereits nicht mehr; nur die QM werden hier erfasst ...
                                 +colsErg_n)       
            
            # mlc ergaenzen (denn H ist ggf. barBzg und nicht mlc)      
            colsPH=[]
            colsRHO=[]
            colsMlc=[]
            for col in dfAGSN.columns.to_list():
                if type(col) == str and re.search('_n$',col):                                                
                    try:
                        colTuple=fStripV3Colik2Tuple(col=col, colPost='_n')                            
                        if colTuple[1]=='KNOT~*~*~*~PH_n':
                                    colsPH.append(col)
                                    colsRHO.append(col.replace('PH','RHO'))
                                    colsMlc.append(col.replace('KNOT~*~*~*~PH','mlc')) #.replace('PH','mlc'))                                                                    
                    except:
                        continue
            
            # zugeh. Ergebnisspalte anlegen                
            for col in colsMlc:
                dfAGSN[col]=None        
                #logger.debug(f"{logStr} colMlc: {col}") 
            
            # Ergebnisspalte bestücken
            for index, row in dfAGSN.iterrows():                                                                                       
                    for col_n,col_PH,col_RHO in zip(colsMlc,colsPH,colsRHO):                        
                        dfAGSN.loc[index,col_n]=row[col_PH]*10**5/(row[col_RHO]*9.81)+row['ZKOR_n']              
                    
            return dfAGSN     
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug(f"{logStr}_Done.") 

    def _V3_AGSNVEC(self,V3_AGSN):
        """
        V3_AGSNVEC: Create V3_AGSNVEC from V3_AGSN. V3_AGSNVEC is a dxWithMx object Attribute.
        
        :param V3_AGSN: dxWithMx attribute
        :type V3_AGSN: df
        
        :return: V3_AGSNVEC: V3_AGSN expanded to V3_AGSNVEC.
        :rtype: df        
        
        .. note:: 
            
            The returned V3_AGSNVEC (expand for PIPEs in (Section,Layer) one row to one row per point) has the following columns:
                V3_AGSN-columns:
                    - Pos: Pos=-1: eliminated if Start-Edge is a Pipe                     
                    - nextNODE: Pos=0: startNODE @IptIdxAsNo=0 if Start-Edge is a Pipe
                    - LSum: Pos=0: 0. @IptIdxAsNo=0 if Start-Edge is a Pipe 
                    - ...
                    - cols mapped with VEC-Results:
                    - LSum
                    - ZKOR_n
                    - PH_n
                    - H_n
                    - mlc_n
                    - T_n
                    - QM                 
                V3_ROHRVEC-columns:
                    - pk_ROHRVEC: Pipe-pk
                    - tk_ROHRVEC: Pipe-tk                
                    - ...
                    - L_ROHRVEC
                    - ...
                    - NAME_i_ROHRVEC, NAME_k_ROHRVEC
                    - mx2NofPts
                    - dL (=L/(mx2NofPts-1))
                    - ...
                    - mx2Idx
                    - IptIdx: rows S or E are eliminated for all pipes except the 1st 
                    - ...           
        """   
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try: 
            
            if V3_AGSN[~V3_AGSN['pk'].isin([-1,'-1'])].empty:
               logger.debug(f"{logStr} V3_AGSN empty.") 
               return V3_AGSN
       
            V3_AGSN=V3_AGSN.copy(deep=True)
                        
            V3_AGSNPos=V3_AGSN[
                            (
                            (V3_AGSN['XL'].isin([0,1]))
                            &
                            (V3_AGSN['direction']==1)
                            )
                            |
                            ( 
                            (V3_AGSN['XL'].isin([2]))
                            &
                            (V3_AGSN['direction']==-1)
                            )     
                            |                
                            ~(V3_AGSN['OBJTYPE'].isin(['ROHR']))
                            ]
            V3_AGSNNeg=V3_AGSN[
                            (
                            (V3_AGSN['XL'].isin([0,1]))
                            &
                            (V3_AGSN['direction']==-1)
                            )
                            |
                            ( 
                            (V3_AGSN['XL'].isin([2]))
                            &
                            (V3_AGSN['direction']==1)
                            )                     
                            ]            
                                    
            dfAGSNVecPos=pd.merge(V3_AGSNPos
                ,self.V3_ROHRVEC
                ,left_on='OBJID',right_on='tk'
                ,suffixes=('','_ROHRVEC')
                ,how='left' # denn der Schnitt kann auch über Objekte ungl. Rohr fuehren ...
            )            
            dfAGSNVecNeg=pd.merge(V3_AGSNNeg
                ,self.V3_ROHRVEC.iloc[::-1] #!
                ,left_on='OBJID',right_on='tk'
                ,suffixes=('','_ROHRVEC')            
            )    
            dfAGSNVecNeg['IptIdxAsNo']=dfAGSNVecNeg['IptIdxAsNoRev']
            dfAGSNVecNeg['SVEC']=dfAGSNVecNeg['SVECRev']
            
            dfAGSNVec=pd.concat([dfAGSNVecPos,dfAGSNVecNeg],axis=0).sort_values(by=['LFDNR','XL','Pos','IptIdxAsNo']).reset_index(drop=True)              
            dfAGSNVec=dfAGSNVec.drop(['IptIdxAsNoRev','SVECRev'],axis=1)    
                        
            dfAGSNVec['SVEC']=dfAGSNVec['SVEC'].astype(float)

            # elimination of Pos=-1 rows if Start-Edge is a Pipe              
            idxToDel=[]
            for index,row in dfAGSNVec.iterrows():
                if row['Pos'] == -1 and row['OBJTYPE']=='ROHR':
                    idxToDel.append(index)
            dfAGSNVec=dfAGSNVec.drop(idxToDel,axis=0)    
            
            # nextNODE to startNODE and LSum=0 for IptIdxAsNo=0 if Start-Edge is a Pipe 
            dfAGSNVecMinPos=dfAGSNVec.groupby(by=['LFDNR','XL'])['Pos'].min()
            for index,row in dfAGSNVec.iterrows():
                if row['Pos']!= 0:
                    continue
                if row['IptIdxAsNo']!= 0:
                    continue
                minPos=dfAGSNVecMinPos.loc[(row['LFDNR'],row['XL'])] 
                if minPos==0: # Start-Edge is a Pipe 
                    dfAGSNVec.loc[index,'LSum']=0.
                    if row['XL'] in[0,1]:
                        if row['direction']==1:
                            dfAGSNVec.loc[index,'nextNODE']=row['NAME_i']
                        else:
                            dfAGSNVec.loc[index,'nextNODE']=row['NAME_k']
                    if row['XL'] in[2]:
                        if row['direction']==-1:
                            dfAGSNVec.loc[index,'nextNODE']=row['NAME_i']
                        else:
                            dfAGSNVec.loc[index,'nextNODE']=row['NAME_k']                            
            
            # eliminate S or E for all Pipes except the 1st
            #dfAGSNVecMaxPos=dfAGSNVec.groupby(by=['LFDNR','XL'])['Pos'].max()
            indToDelete=[]
            for index,row in dfAGSNVec.iterrows():
                
                if row['OBJTYPE']!='ROHR':
                    continue
                
                minPos=dfAGSNVecMinPos.loc[(row['LFDNR'],row['XL'])] 
                #maxPos=dfAGSNVecMaxPos.loc[(row['LFDNR'],row['XL'])] 
                
                if row['Pos']==minPos: # nicht fuer das ROHR an 1. Position
                    continue
                
                #if row['Pos']==maxPos:
                #    continue                
                
                if row['XL'] in [0,1]:         
                    # im VL wird S geloescht wenn pos. def. in Schnittrichtung; sonst E
                    if row['direction']==1:
                        if row['IptIdx']=='S':
                            indToDelete.append(index)
                    elif row['direction']==-1:
                        if row['IptIdx']=='E':
                            indToDelete.append(index)     
                else:                            
                    # im RL wird E geloescht wenn pos. def. in Schnittrichtung; sonst S
                      if row['direction']==1:
                          if row['IptIdx']=='E':
                              indToDelete.append(index)
                      elif row['direction']==-1:
                          if row['IptIdx']=='S':
                              indToDelete.append(index)                                
            #        
            dfAGSNVec=dfAGSNVec.drop(indToDelete,axis=0)    
            
            # in Zeilen mit IptIdx <> S,E LSum durch LSum(Pos-1)+SVEC ersetzen    
            dfAGSNVecMaxLSum=dfAGSNVec.groupby(by=['LFDNR','XL','Pos'])['LSum'].max()            
            def fLSum(row):   
                try:                    
                    if row['IptIdx'] in ['S','E']:
                        return row['LSum']
                    if pd.isnull(row['IptIdx']):
                        return row['LSum']
                    if pd.isnull(row['Pos']==0):
                        return row['LSum']                    
                    
                    LSumPrev=dfAGSNVecMaxLSum.loc[(row['LFDNR'],row['XL'],row['Pos']-1)]
                    
                    return LSumPrev+row['SVEC']
                                                           
                except:
                    # ROHR am Anfang mit Innenpunkten
                    return 0.+row['SVEC']                        
            dfAGSNVec['LSum']=dfAGSNVec.apply(lambda row: fLSum(row),axis=1)
                            
            # cols mapped with VEC-Results
            t0rVec=pd.Timestamp(self.mx.df.index[0].strftime('%Y-%m-%d %X'))#.%f'))
            for col,colVECType in zip(['PH_n','mlc_n','H_n','QM'],['manPVEC','mlcPVEC','barBzgPVEC','QMVEC']):       
                pass
                colVEC=('STAT',colVECType,t0rVec,t0rVec)   
                #logger.debug(f"{logStr}colVEC: {colVEC}")        
                dfAGSNVec[col]=dfAGSNVec.apply(lambda row: row[col] if pd.isnull(row[colVEC]) else row[colVEC],axis=1)
                
            for col,colVECType in zip(['T_n'],['TVEC']):       
                pass
                colVEC=('STAT','ROHR~*~*~*~'+colVECType,t0rVec,t0rVec)   
                #logger.debug(f"{logStr}colVEC: {colVEC}")                
                dfAGSNVec[col]=dfAGSNVec.apply(lambda row: row[col] if pd.isnull(row[colVEC]) else row[colVEC],axis=1)      
                
            for col,colVEC in zip(['ZKOR_n'],['ZVEC']):       
                pass
                colVEC=colVEC 
                #logger.debug(f"{logStr}colVEC: {colVEC}")                
                dfAGSNVec[col]=dfAGSNVec.apply(lambda row: row[col] if pd.isnull(row[colVEC]) else row[colVEC],axis=1)                     
                                                                                                                                    
            return dfAGSNVec
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug(f"{logStr}_Done.") 

    # def setLayerContentTo(self,layerName,df):          
    #     """
    #     Updates content of layerName to df's-content.
        
    #     :param layerName: name of an existing layer
    #     :type layerName: str
        
    #     :return: None
    
    #     .. note:: 
    #         df's cols used:            
    #             - TYPE 
    #             - ID                 
    #     """           
                
    #     logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #     logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    #     try: 
                  
    #         xk=self.dfLAYR[self.dfLAYR['NAME'].isin([layerName])]['tk'].iloc[0]
            
    #         dfUpd=df.copy(deep=True)
            
    #         dfUpd['table']='LAYR'
    #         dfUpd['attrib']='OBJS'
    #         dfUpd['attribValue']=dfUpd.apply(lambda row: "{:s}~{:s}\t".format(row['TYPE'],row['ID']).encode('utf-8'),axis=1)
    #         dfUpd['xk']='tk'
    #         dfUpd['xkValue']=xk    
            
    #         dfUpd2=dfUpd.groupby(by=['xkValue']).agg({'xkValue': 'first'
    #                                             ,'table': 'first'
    #                                             ,'attrib': 'first'
    #                                             ,'xk': 'first'
    #                                             , 'attribValue': 'sum'}).reset_index(drop=True)
    #         dfUpd2['attribValue']=dfUpd2['attribValue'].apply(lambda x: x.rstrip())
              
    #         self.dx.update(dfUpd2)               
        
    #     except dxWithMxError:
    #         raise            
    #     except Exception as e:
    #         logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
    #         logger.error(logStrFinal) 
    #         raise dxWithMxError(logStrFinal)                       
    #     finally:
    #         logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      
            
            
    def switchV3DfColsToMultiindex(self):
        """
        Switches V3-Df cols to Multiindex-Cols.               
        """        
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
           
            self.V3_KNOT.columns=pd.MultiIndex.from_tuples(
                [fGetMultiindexTupleFromV3Col(col) for col in self.V3_KNOT.columns.to_list()]
                ,names=['1','2','3','4'])    
            
            self.V3_ROHR.columns=pd.MultiIndex.from_tuples(
                [fGetMultiindexTupleFromV3Col(col) for col in self.V3_ROHR.columns.to_list()]
                ,names=['1','2','3','4'])
            
            self.V3_FWVB.columns=pd.MultiIndex.from_tuples(
                [fGetMultiindexTupleFromV3Col(col) for col in self.V3_FWVB.columns.to_list()]
                ,names=['1','2','3','4'])     
            
            self.V3_VBEL.columns=pd.MultiIndex.from_tuples(
                [fGetMultiindexTupleFromV3Col(col) for col in self.V3_VBEL.columns.to_list()]
                ,names=['1','2','3','4'])                
                                
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                  
        
class readDxAndMxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class readDxAndMxGoto(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def readDxAndMx(dbFile            
                ,preventPklDump=False
                ,forceSir3sRead=False
                ,maxRecords=None
                ,mxsVecsResults2MxDf=None
                ,mxsVecsResults2MxDfVecAggs=None
                ,crs=None
                ,logPathOutputFct=os.path.relpath
                ):

    """
    Reads SIR 3S model and SIR 3S results and returns a dxWithMx object.
    
    Use maxRecords=0  to read only the model.
    Use maxRecords=1  to read only STAT (the steady state result).
    Use maxRecords=-1 to (re-)calculate the model by SirCalc.

    :param dbFile: Path to SIR 3S' database file ('modell.db3' or 'modell.mdb'). The database is read into a Dx object. The corresponding results are read into an Mx object if available.
    :type dbFile: str
    :param preventPklDump: Determines whether to prevent dumping objects read to pickle. If True, existing pickles are deleted, SIR 3S' sources are read and no pickles are written. If False 3 pickles are written or overwritten if older than SIR 3S' sources.
    :type preventPklDump: bool, optional, default=False
    :param forceSir3sRead: Determines whether to force reading from SIR 3S' sources even if newer pickles exists. By default pickles are read if newer than SIR 3S' sources.
    :type forceSir3sRead: bool, optional, default=False
    :param maxRecords: Use maxRecords=0 to read only the model. Use maxRecords=1 to read only STAT (the steady state result). Maximum number of MX-Results to read. If None, all results are read. Use maxRecords=-1 to (re-)calculate the model by SirCalc (by the newest SirCalc available below ``C:\\3S``).
    :type maxRecords: int, optional, default=None
    :param mxsVecsResults2MxDf: List of regular expressions for SIR 3S' Vector-Results to be included in mx.df. Note that integrating Vector-Results in mx.df can significantly increase memory usage. Example: ``['ROHR~\*~\*~\*~PHR', 'ROHR~\*~\*~\*~FS', 'ROHR~\*~\*~\*~DSI', 'ROHR~\*~\*~\*~DSK']``
    :type mxsVecsResults2MxDf: list, optional, default=None
    :param mxsVecsResults2MxDfVecAggs: List of timesteps for SIR 3S' Vector-Results to be included in mx.dfVecAggs. Note that integrating all timesteps in mx.dfVecAggs will increase memory usage up to MXS-Size. Example: [3,42,666]
    :type mxsVecsResults2MxDfVecAggs: list, optional, default=None
    :param crs: (=coordinate reference system) Determines crs used in geopandas-Dfs (Possible value:'EPSG:25832'). If None, crs will be read from SIR 3S' database file.
    :type crs: str, optional, default=None
    :param logPathOutputFct: func logPathOutputFct(fileName) is used for logoutput of filenames unless explicitly stated otherwise in the logoutput
    :type logPathOutputFct: func, optional, default=os.path.relpath

    :return: An object containing the SIR 3S model and SIR 3S results.
    :rtype: dxWithMx

    .. note:: Dx contains data for all models in the SIR 3S database. Mx contains only the results for one model. SYSTEMKONFIG / VIEW_MODELLE are used to determine which one.
        
        The returned dxWithMx object has the following attributes:
    
            - Model: Dx object:
                - dx.dataFrames[...]: pandas-Dfs 1:1 from SIR 3S' tables in database file
                - dx.dataFrames[...]: several pandas-Dfs derived from the 1:1 Dfs 
        
            - Results: Mx object:
                - mx.df: pandas-Df ('time curve data') from from SIR 3S' MXS file(s)
                - mx.dfVecAggs: pandas-Df ('vector data') from SIR 3S' MXS file(s)
            - Miscellaneous:   
                - wDirMx: Mx-directory of the model
                - SirCalcXmlFile: SirCalc's Xml-File of the model
                - SirCalcExeFile: SirCalc Executable used to (re-)calculate the model
    
            - pandas-Dfs with Model- AND Result-Data:
                - V3_ROHR: Pipes
                - V3_FWVB: Housestations District Heating
                - V3_KNOT: Nodes 
                - V3_VBEL: Edges
                - V3_ROHRVEC: Pipes including interior points 
                - V3_AGSN: Longitudinal Sections; AGSN is the German abbreviation for longitudinal sections / cuts (defined in the SIR 3S model)
                - V3_AGSNVEC: Longitudinal Sections including Pipe interior points 
                    
            - geopandas-Dfs based upon the Dfs above:
                - gdf_ROHR: Pipes
                - gdf_FWVB: Housestations District Heating
                - gdf_KNOT: Nodes 
                                                
            - NetworkX-Graphs:
                - G
                - GSig

        Selected functions of the returned dxWithMx object:                
                - switchV3DfColsToMultiindex(): switch cols in V3_ROHR, V3_FWVB, V3_KNOT, V3_VBEL to Multiindex

    """
    
    import os
    #import importlib
    import glob
    
    dx=None
    mx=None
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.'))     
    
    try:
        
        dx=None
        mx=None
        m=None
        SirCalcXmlFile=None # SirCalc's xmlFile
        SirCalcExeFile=None # SirCalc Executable
            
        dbFileDxPklRead=False
        dbFilename,ext=os.path.splitext(dbFile)
        dbFileDxPkl="{:s}-dx.pkl".format(dbFilename)   
        
        if preventPklDump:
            if isfile(dbFileDxPkl):
              logger.info("{logStr:s}{dbFileDxPkl:s} exists and is deleted ...".format(
                   logStr=logStr
                  ,dbFileDxPkl=logPathOutputFct(dbFileDxPkl)                        
                  )
                  )
              os.remove(dbFileDxPkl)           
                
        if not forceSir3sRead:            
            # Pkl existiert
            if os.path.exists(dbFileDxPkl):                
                # ist eine Datei und lesbar
                if isfile(dbFileDxPkl) and access(dbFileDxPkl,R_OK):
                    # ist neuer als die Modelldatenbank
                    tDb=os.path.getmtime(dbFile)
                    tPkl=os.path.getmtime(dbFileDxPkl)
                    
                    logger.debug("{:s} tDb: {:s} tPkl: {:s}".format(logStr
                                                                      ,datetime.fromtimestamp(tDb).strftime('%Y-%m-%d %H:%M:%S')
                                                                      ,datetime.fromtimestamp(tPkl).strftime('%Y-%m-%d %H:%M:%S')                                                                      
                                                                      ))    
                    
                    if tDb < tPkl:
                        logger.info("{logStr:s}{dbFileDxPkl:s} newer than {dbFile:s} and therefore read ...".format(
                             logStr=logStr
                            ,dbFileDxPkl=logPathOutputFct(dbFileDxPkl)
                            ,dbFile=logPathOutputFct(dbFile)
                            )
                            )
                        try:
                            with open(dbFileDxPkl,'rb') as f:  
                                dx=pickle.load(f)  
                            dbFileDxPklRead=True
                        except:                            
                            logger.info("{logStr:s}{dbFileDxPkl:s} read error! - reading SIR 3S raw data ...".format(
                                 logStr=logStr
                                ,dbFileDxPkl=logPathOutputFct(dbFileDxPkl)                                
                                )
                                )

        ### Modell lesen
        if not dbFileDxPklRead:
            try:
                dx=Dx.Dx(dbFile)
            except Dx.DxError:
                logStrFinal="{logStr:s}dbFile: {dbFile:s}: DxError!".format(
                    logStr=logStr
                    ,dbFile=logPathOutputFct(dbFile)
                    )     
                raise readDxAndMxError(logStrFinal)  
            
            if not preventPklDump:
                if isfile(dbFileDxPkl):
                    logger.info("{logStr:s}{dbFileDxPkl:s} exists and is overwritten...".format(
                         logStr=logStr
                        ,dbFileDxPkl=logPathOutputFct(dbFileDxPkl)                        
                        )
                        )
                else:
                    logger.info("{logStr:s}{dbFileDxPkl:s} is written ...".format(
                         logStr=logStr
                        ,dbFileDxPkl=logPathOutputFct(dbFileDxPkl)                        
                        )
                        )                                                                
                with open(dbFileDxPkl,'wb') as f:  
                    pickle.dump(dx,f)           
                    
            else:
                pass
                                                               
        ### Ergebnisse nicht lesen?!         
        if maxRecords==0:        
            m = dxWithMx(dx,None,crs)
            logStrFinal="{logStr:s}dbFile: {dbFile:s}: maxRecords==0: do not read MX-Results.".format(
                logStr=logStr
                ,dbFile=logPathOutputFct(dbFile))     
            raise readDxAndMxGoto(logStrFinal)     
                    
        ### mx Datenquelle bestimmen
                
        #!
        dbFile=os.path.abspath(dx.dbFile)        
        
        logger.debug("{logStrPrefix:s}detecting MX-Source for dx.dbFile (abspath) {dbFile:s} ...".format(
                logStrPrefix=logStr
                ,dbFile=dbFile))        
                                        
        # wDir der Db
        sk=dx.dataFrames['SYSTEMKONFIG']
        wDirDb=sk[sk['ID'].isin([1,1.])]['WERT'].iloc[0]
        logger.debug("{logStrPrefix:s}wDir from dbFile: {wDirDb:s}".format(
            logStrPrefix=logStr,wDirDb=wDirDb))
        #!
        wDir=os.path.abspath(os.path.join(os.path.dirname(dbFile),wDirDb))
        logger.debug("{logStrPrefix:s}abspath of wDir from dbFile: {wDir:s}".format(
            logStrPrefix=logStr,wDir=wDir))

        # SYSTEMKONFIG ID 3:
        # Modell-Pk des in QGIS anzuzeigenden Modells (wird von den QGIS-Views ausgewertet)
        # diese xk wird hier verwendet um das Modell in der DB zu identifizieren dessen Ergebnisse geliefert werden sollen
        try:
            vm=dx.dataFrames['VIEW_MODELLE']
            #modelXk=sk[sk['ID'].isin([3,3.])]['WERT'].iloc[0]
            vms=vm[vm['pk'].isin([dx.QGISmodelXk])].iloc[0]   
        except:
            logger.info("{logStr:s} QGISmodelXk not defined. Now the MX of 1st Model in VIEW_MODELLE is used ...".format(logStr=logStr))
            vms=vm.iloc[0]  
        
        #!                        
        wDirMx=os.path.join(
            os.path.join(
            os.path.join(wDir,vms.Basis),vms.Variante),vms.BZ)
        logger.debug("{logStrPrefix:s}wDirMx from abspath of wDir from dbFile: {wDirMx:s}".format(
            logStrPrefix=logStr,wDirMx=wDirMx))
                        
        wDirMxMx1Content=glob.glob(os.path.join(wDirMx,'*.MX1'))
        wDirMxMx1Content=sorted(wDirMxMx1Content) 

        if len(wDirMxMx1Content)>1:
            logger.info("{logStrPrefix:s}More than one ({anz:d}) MX1-Files in wDir. The 1st MX1-File is used.".format(
                logStrPrefix=logStr,anz=len(wDirMxMx1Content)))

        if len(wDirMxMx1Content)>=1:        
            mx1File= wDirMxMx1Content[0]
            logger.debug("{logStrPrefix:s}mx1File: {mx1File:s}".format(
                logStrPrefix=logStr
                ,mx1File=logPathOutputFct(mx1File)))
                    
            dbFileMxPklRead=False
            dbFileMxPkl="{:s}-mx-{:s}.pkl".format(dbFilename,re.sub('\W+','_',os.path.relpath(mx1File)))                
            logger.debug("{logStrPrefix:s}corresponding dbFileMxPkl-File: {dbFileMxPkl:s}".format(
                logStrPrefix=logStr
                ,dbFileMxPkl=logPathOutputFct(dbFileMxPkl)))
            
            if preventPklDump:
                if isfile(dbFileMxPkl):
                      logger.info("{logStr:s}{dbFileMxPkl:s} exists and is deleted...".format(
                           logStr=logStr
                          ,dbFileMxPkl=logPathOutputFct(dbFileMxPkl)                        
                          )
                          )
                      os.remove(dbFileMxPkl)        
                           
            tDb=os.path.getmtime(dbFile)  
            
            # SirCalcXml
            wDirMxXmlContent=glob.glob(os.path.join(wDirMx,'*.XML'))
            if len(wDirMxXmlContent) > 0:
                wDirMxXmlContent=sorted(wDirMxXmlContent) 
                SirCalcXmlFile= wDirMxXmlContent[0]
                tXml=os.path.getmtime(SirCalcXmlFile)       
            else:                    
                logger.debug("{logStr:s}SirCalc's xmlFile not existing.".format(logStr=logStr))  
                            
            # mx1
            if os.path.exists(mx1File):  
                tMx=os.path.getmtime(mx1File)
                if tDb>tMx:
                    logger.info("{logStr:s}\n+{dbFile:s} is newer than\n+{mx1File:s}:\n+SIR 3S' dbFile is newer than SIR 3S' mx1File\n+in this case the results are maybe dated or (worse) incompatible to the model".format(
                         logStr=logStr                    
                        ,mx1File=logPathOutputFct(mx1File)
                        ,dbFile=logPathOutputFct(dbFile)
                        )
                        )                     
                    if len(wDirMxXmlContent) > 0:
                        wDirMxXmlContent=sorted(wDirMxXmlContent) 
                        #xmlFile= wDirMxXmlContent[0]                        
                        if tMx>=tXml:
                            pass
                        else:                            
                            logger.info("{logStr:s}\n+{xmlFile:s} is newer than\n+{mx1File:s}:\n+SirCalc's xmlFile is newer than SIR 3S' mx1File\n+in this case the results are maybe dated or (worse) incompatible to the model".format(
                                 logStr=logStr                    
                                ,xmlFile=logPathOutputFct(SirCalcXmlFile)
                                ,mx1File=logPathOutputFct(mx1File)
                                )
                                )
            ### Ergebnisse neu berechnen  
            if maxRecords != None:
                if maxRecords<0 and len(wDirMxMx1Content)>0 and len(wDirMxXmlContent) > 0:
                    
                    SirCalcFiles = []
                    installDir  = r"C:\\3S" 
                    installName = "SirCalc.exe"
                    SirCalcOptions="/rstnSpezial /InteraktRgMax100 /InteraktThMax50"
                    
                    for file,_,_ in os.walk(installDir):
                        SirCalcFiles.extend(glob.glob(os.path.join(file,installName))) 
                    
                    SirCalcFiles = [f  for f in reversed(sorted(SirCalcFiles,key=lambda file: os.path.getmtime(file)) )]
                    
                    if len(SirCalcFiles)==0:                    
                        logger.info("{logStrPrefix:s}SirCalc not found. No (re-)calculation.".format(
                        logStrPrefix=logStr                    
                        ))                    
                    
                    else:
                        SirCalcExeFile=SirCalcFiles[0]
                        logger.info("{logStrPrefix:s}running {SirCalc:s} ...".format(
                        logStrPrefix=logStr
                        ,SirCalc=SirCalcExeFile
                        ))
                                                    
                        with subprocess.Popen([SirCalcExeFile,SirCalcXmlFile,SirCalcOptions]) as process:
                            process.wait()

        else:
             logger.info("{logStrPrefix:s}No MX1-File(s) in wDir. Continue without MX ...".format(
             logStrPrefix=logStr))
                
             m = dxWithMx(dx,None,crs)
                          
             logStrFinal="{0:s}{1:s}".format(logStr,'... m without MX finished.')
             logger.debug(logStrFinal)   
             raise readDxAndMxGoto(logStrFinal)                  
             
        if not forceSir3sRead:            
            # Pkl existiert
            if os.path.exists(dbFileMxPkl):                
                # ist eine Datei und lesbar
                if isfile(dbFileMxPkl) and access(dbFileMxPkl,R_OK):
                    # ist neuer als mx1File
                    tMx=os.path.getmtime(mx1File)
                    tPkl=os.path.getmtime(dbFileMxPkl)                    
                                        
                    logger.debug("{:s} tMx: {:s} tPkl: {:s}".format(logStr
                                                  ,datetime.fromtimestamp(tMx).strftime('%Y-%m-%d %H:%M:%S')
                                                  ,datetime.fromtimestamp(tPkl).strftime('%Y-%m-%d %H:%M:%S')                                                                      
                                                  ))                        
                                        
                    if tMx < tPkl:
                        logger.info("{logStr:s}{dbFileMxPkl:s} newer than {mx1File:s} and therefore read ...".format(
                             logStr=logStr
                            ,dbFileMxPkl=logPathOutputFct(dbFileMxPkl)
                            ,mx1File=logPathOutputFct(mx1File)
                            )
                            )
                        try:
                            with open(dbFileMxPkl,'rb') as f:  
                                mx=pickle.load(f)  
                            dbFileMxPklRead=True       
                        except:                            
                            logger.info("{logStr:s}{dbFileMxPkl:s} read error! - reading SIR 3S raw data ...".format(
                                 logStr=logStr
                                ,dbFileMxPkl=logPathOutputFct(dbFileMxPkl)                                
                                )
                                )                        
                        
                        
        
        if not dbFileMxPklRead:
        
            ### Modellergebnisse lesen
            try:
                mx=Mx.Mx(mx1File,maxRecords=maxRecords)
                logger.debug("{0:s}{1:s}".format(logStr,'MX read ok so far.'))   
                                             
            except Mx.MxError:
                logger.info("{0:s}{1:s}".format(logStr,'MX read failed. Continue without MX ...'))   
            
                m = dxWithMx(dx,None,crs)
                
                logStrFinal="{0:s}{1:s}".format(logStr,'... m without MX finished.')
                logger.debug(logStrFinal)   
                raise readDxAndMxGoto(logStrFinal)     
                
                
            except Exception as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal)                    
                raise
                
                
            # 
            processMxVectorResults(mx,dx,mxsVecsResults2MxDf,mxsVecsResults2MxDfVecAggs)
            
            # ### Vector-Results 2 MxDf
            # if mxsVecsResults2MxDf != None:
            #     try:                
            #         df=mx.readMxsVecsResultsForObjectType(Sir3sVecIDReExp=mxsVecsResults2MxDf,flatIndex=False)                    
            #         logger.debug("{logStr:s} df from readMxsVecsResultsForObjectType: {dfStr:s}".format(
            #             logStr=logStr,dfStr=df.head(5).to_string()))
                    
            #         # Kanalweise bearbeiten
            #         vecChannels=sorted(list(set(df.index.get_level_values(1))))
                    
            #         V3_VBEL=dx.dataFrames['V3_VBEL']
                    
                    
            #         mxVecChannelDfs={}
            #         for vecChannel in vecChannels:
                        
            #             #print(vecChannel)
                        
            #             dfVecChannel=df.loc[(slice(None),vecChannel,slice(None),slice(None)),:]
            #             dfVecChannel.index=dfVecChannel.index.get_level_values(2).rename('TIME')
            #             dfVecChannel=dfVecChannel.dropna(axis=1,how='all')
                        
            #             mObj=re.search(Mx.regExpSir3sVecIDObjAtr,vecChannel)                    
            #             OBJTYPE,ATTRTYPE=mObj.groups()
                               
            #             # Zeiten aendern wg. spaeterem concat mit mx.df
            #             dfVecChannel.index=[pd.Timestamp(t,tz='UTC') for t in dfVecChannel.index]
                        
            #             if OBJTYPE == 'KNOT':
            #                 dfOBJT=dx.dataFrames['V_BVZ_KNOT'][['tk','NAME']]
            #                 dfOBJT.index=dfOBJT['tk']
            #                 colRenDctToNamesMxDf={col:"{:s}~{!s:s}~*~{:s}~{:s}".format(OBJTYPE,dfOBJT.loc[col,'NAME'],col,ATTRTYPE) for col in dfVecChannel.columns.to_list()}
            #             else:    
            #                 dfOBJT=V3_VBEL[['pk','NAME_i','NAME_k']].loc[(OBJTYPE,slice(None)),:]
            #                 dfOBJT.index=dfOBJT.index.get_level_values(1) # die OBJID; xk
            #                 colRenDctToNamesMxDf={col:"{:s}~{!s:s}~{!s:s}~{:s}~{:s}".format(OBJTYPE,dfOBJT.loc[col,'NAME_i'],dfOBJT.loc[col,'NAME_k'],col,ATTRTYPE) for col in dfVecChannel.columns.to_list()}
                                  
            #             dfVecChannel=dfVecChannel.rename(columns=colRenDctToNamesMxDf)
                        
            #             mxVecChannelDfs[vecChannel]=dfVecChannel         
                                            
            #         l=mx.df.columns.to_list()
            #         logger.debug("{:s} Anzahl der Spalten vor Ergaenzung der Vektorspalten: {:d}".format(logStr,len(l)))
                        
            #         mx.df=pd.concat([mx.df]
            #         +list(mxVecChannelDfs.values())               
            #         ,axis=1)
                    
            #         l=mx.df.columns.to_list()
            #         logger.debug("{:s} Anzahl der Spalten nach Ergaenzung der Vektorspalten: {:d}".format(logStr,len(l)))                
                    
            #         # Test auf mehrfach vorkommende Spaltennamen                
            #         l=mx.df.loc[:,mx.df.columns.duplicated()].columns.to_list()
            #         if len(l)>0:
            #             logger.debug("{:s} Anzahl der Spaltennamen die mehrfach vorkommen: {:d}; eliminieren der mehrfach vorkommenden ... ".format(logStr,len(l)))
            #             mx.df = mx.df.loc[:,~mx.df.columns.duplicated()]
                           
            #         l=mx.df.columns.to_list()    
            #         logger.debug("{:s} Anzahl der Spalten nach Ergaenzung der Vektorspalten und nach eliminieren der mehrfach vorkommenden: {:d}".format(logStr,len(l)))
                        
                        
            #     except Mx.MxError:
            #         logStrFinal="{logStr:s}mxsVecsResults2MxDf failed".format(logStr=logStr)     
            #         raise readDxAndMxError(logStrFinal)             
        
            # ### Vector-Results 2 MxDfVecAggs
            # if mxsVecsResults2MxDfVecAggs != None:
            #     try:         
            #         for idxTime in mxsVecsResults2MxDfVecAggs:
            #             try:
            #                 aTime=mx.df.index[idxTime]
            #             except:
            #                 logger.info(f"{logStr}: Requested Timestep {idxTime} not in MX-Results.")  
            #                 continue
                        
            #             df,tL,tR=mx.getVecAggs(time1st=aTime,aTIME=True)
                                            
            #     except Mx.MxError:
            #         logStrFinal="{logStr:s}mxsVecsResults2MxDf failed".format(logStr=logStr)     
            #         raise readDxAndMxError(logStrFinal)             

        
            if not preventPklDump:
                if isfile(dbFileMxPkl):
                    logger.info("{logStr:s}{dbFileMxPkl:s} exists and is overwritten...".format(
                         logStr=logStr
                        ,dbFileMxPkl=logPathOutputFct(dbFileMxPkl)                        
                        )
                        )
                else:
                    logger.info("{logStr:s}{dbFileMxPkl:s} is written ...".format(
                         logStr=logStr
                        ,dbFileMxPkl=logPathOutputFct(dbFileMxPkl)                        
                        )
                        )                                                                
                with open(dbFileMxPkl,'wb') as f:  
                    pickle.dump(mx,f)     
            else:
                pass
                                             
        dbFileDxMxPklRead=False
        dbFileDxMxPkl="{:s}-m.pkl".format(dbFilename)        
        
        if preventPklDump:        
            if isfile(dbFileDxMxPkl):
                      logger.info("{logStr:s}{dbFileDxMxPkl:s} exists and is deleted...".format(
                           logStr=logStr
                          ,dbFileDxMxPkl=logPathOutputFct(dbFileDxMxPkl)                        
                          )
                          )
                      os.remove(dbFileDxMxPkl)        
        else:
            logger.debug("{logStrPrefix:s}corresp. dbFileDxMxPkl-File: {dbFileDxMxPkl:s}".format(
                logStrPrefix=logStr
                ,dbFileDxMxPkl=logPathOutputFct(dbFileDxMxPkl)
                ))
                
        if not forceSir3sRead:            
            # Pkl existiert
            if os.path.exists(dbFileDxMxPkl):                
                # ist eine Datei und lesbar
                if isfile(dbFileDxMxPkl) and access(dbFileDxMxPkl,R_OK):
                    # ist neuer als mx1File und dbFile
                    
                    tMx1=os.path.getmtime(mx1File)
                    tDb=os.path.getmtime(dbFile)
                    tPkl=os.path.getmtime(dbFileDxMxPkl)
                                                            
                    if (tMx1 < tPkl) and (tDb < tPkl):
                        logger.info("{logStr:s}{dbFileDxMxPkl:s} newer than {mx1File:s} and {dbFile:s} and therefore read ...".format(
                             logStr=logStr
                            ,dbFileDxMxPkl=logPathOutputFct(dbFileDxMxPkl)
                            ,mx1File=logPathOutputFct(mx1File)
                            ,dbFile=logPathOutputFct(dbFile)
                            )
                            )                        
                        try:
                           with open(dbFileDxMxPkl,'rb') as f:  
                               m=pickle.load(f)  
                           dbFileDxMxPklRead=True    
                        except:                            
                            logger.info("{logStr:s}{dbFileDxMxPkl:s} read error! - processing dx and mx ...".format(
                                 logStr=logStr
                                ,dbFileDxMxPkl=logPathOutputFct(dbFileDxMxPkl)                                
                                )
                                )                            
                                                    
        if not dbFileDxMxPklRead:
            #
            m = dxWithMx(dx,mx,crs)
            m.wDirMx=wDirMx
            if SirCalcXmlFile != None:                
                m.SirCalcXmlFile=SirCalcXmlFile
            if SirCalcExeFile != None:
                m.SirCalcExeFile=SirCalcExeFile
            
            if not preventPklDump:
                if isfile(dbFileDxMxPkl):
                    logger.info("{logStr:s}{dbFileDxMxPkl:s} exists and is overwritten...".format(
                         logStr=logStr
                        ,dbFileDxMxPkl=logPathOutputFct(dbFileDxMxPkl)                        
                        )
                        )
                else:
                    logger.info("{logStr:s}{dbFileDxMxPkl:s} is written ...".format(
                         logStr=logStr
                        ,dbFileDxMxPkl=logPathOutputFct(dbFileDxMxPkl)                        
                        )
                        )                                                                
                with open(dbFileDxMxPkl,'wb') as f:  
                    pickle.dump(m,f)       
            
            else:
                pass
                # if isfile(dbFileDxMxPkl):
                #           logger.info("{logStr:s}{dbFileDxMxPkl:s} exists and is deleted...".format(
                #                logStr=logStr
                #               ,dbFileDxMxPkl=dbFileDxMxPkl                        
                #               )
                #               )
                #           os.remove(dbFileDxMxPkl)
            
        else:
            pass
                               
    except readDxAndMxGoto:        
        pass 

    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal)      
        
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
        return m

def processMxVectorResults(mx,dx
                ,mxsVecsResults2MxDf=None
                ,mxsVecsResults2MxDfVecAggs=None              
                ):

    """
    Processes Mx-Vector-Results.
    
    :param mx: Mx object
    :type mx: Mx.Mx
    :param dx: Dx object
    :type dx: Dx.Dx    
    :param mxsVecsResults2MxDf: List of regular expressions for SIR 3S' Vector-Results to be included in mx.df. Note that integrating Vector-Results in mx.df can significantly increase memory usage. Example: ``['ROHR~\*~\*~\*~PHR', 'ROHR~\*~\*~\*~FS', 'ROHR~\*~\*~\*~DSI', 'ROHR~\*~\*~\*~DSK']``
    :type mxsVecsResults2MxDf: list, optional, default=None
    :param mxsVecsResults2MxDfVecAggs: List of timesteps for SIR 3S' Vector-Results to be included in mx.dfVecAggs. Note that integrating all timesteps in mx.dfVecAggs will increase memory usage up to MXS-Size. Example: [3,42,666]
    :type mxsVecsResults2MxDfVecAggs: list, optional, default=None                    
    """
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.'))     
    
    try:
                        
            ### Vector-Results 2 MxDf
            if mxsVecsResults2MxDf != None:
                try:                
                    df=mx.readMxsVecsResultsForObjectType(Sir3sVecIDReExp=mxsVecsResults2MxDf,flatIndex=False)                    
                    logger.debug("{logStr:s} df from readMxsVecsResultsForObjectType: {dfStr:s}".format(
                        logStr=logStr,dfStr=df.head(5).to_string()))
                    
                    # Kanalweise bearbeiten
                    vecChannels=sorted(list(set(df.index.get_level_values(1))))
                    
                    V3_VBEL=dx.dataFrames['V3_VBEL']
                    
                    
                    mxVecChannelDfs={}
                    for vecChannel in vecChannels:
                        
                        #print(vecChannel)
                        
                        dfVecChannel=df.loc[(slice(None),vecChannel,slice(None),slice(None)),:]
                        dfVecChannel.index=dfVecChannel.index.get_level_values(2).rename('TIME')
                        dfVecChannel=dfVecChannel.dropna(axis=1,how='all')
                        
                        mObj=re.search(Mx.regExpSir3sVecIDObjAtr,vecChannel)                    
                        OBJTYPE,ATTRTYPE=mObj.groups()
                               
                        # Zeiten aendern wg. spaeterem concat mit mx.df
                        dfVecChannel.index=[pd.Timestamp(t,tz='UTC') for t in dfVecChannel.index]
                        
                        if OBJTYPE == 'KNOT':
                            dfOBJT=dx.dataFrames['V_BVZ_KNOT'][['tk','NAME']]
                            dfOBJT.index=dfOBJT['tk']
                            colRenDctToNamesMxDf={col:"{:s}~{!s:s}~*~{:s}~{:s}".format(OBJTYPE,dfOBJT.loc[col,'NAME'],col,ATTRTYPE) for col in dfVecChannel.columns.to_list()}
                        else:    
                            dfOBJT=V3_VBEL[['pk','NAME_i','NAME_k']].loc[(OBJTYPE,slice(None)),:]
                            dfOBJT.index=dfOBJT.index.get_level_values(1) # die OBJID; xk
                            colRenDctToNamesMxDf={col:"{:s}~{!s:s}~{!s:s}~{:s}~{:s}".format(OBJTYPE,dfOBJT.loc[col,'NAME_i'],dfOBJT.loc[col,'NAME_k'],col,ATTRTYPE) for col in dfVecChannel.columns.to_list()}
                                  
                        dfVecChannel=dfVecChannel.rename(columns=colRenDctToNamesMxDf)
                        
                        mxVecChannelDfs[vecChannel]=dfVecChannel         
                                            
                    l=mx.df.columns.to_list()
                    logger.debug("{:s} Anzahl der Spalten vor Ergaenzung der Vektorspalten: {:d}".format(logStr,len(l)))
                        
                    mx.df=pd.concat([mx.df]
                    +list(mxVecChannelDfs.values())               
                    ,axis=1)
                    
                    l=mx.df.columns.to_list()
                    logger.debug("{:s} Anzahl der Spalten nach Ergaenzung der Vektorspalten: {:d}".format(logStr,len(l)))                
                    
                    # Test auf mehrfach vorkommende Spaltennamen                
                    l=mx.df.loc[:,mx.df.columns.duplicated()].columns.to_list()
                    if len(l)>0:
                        logger.debug("{:s} Anzahl der Spaltennamen die mehrfach vorkommen: {:d}; eliminieren der mehrfach vorkommenden ... ".format(logStr,len(l)))
                        mx.df = mx.df.loc[:,~mx.df.columns.duplicated()]
                           
                    l=mx.df.columns.to_list()    
                    logger.debug("{:s} Anzahl der Spalten nach Ergaenzung der Vektorspalten und nach eliminieren der mehrfach vorkommenden: {:d}".format(logStr,len(l)))
                        
                        
                except Mx.MxError:
                    logStrFinal="{logStr:s}mxsVecsResults2MxDf failed".format(logStr=logStr)     
                    raise readDxAndMxError(logStrFinal)             
        
            ### Vector-Results 2 MxDfVecAggs
            if mxsVecsResults2MxDfVecAggs != None:
                try:         
                    for idxTime in mxsVecsResults2MxDfVecAggs:
                        try:
                            aTime=mx.df.index[idxTime]
                        except:
                            logger.info(f"{logStr}: Requested Timestep {idxTime} not in MX-Results.")  
                            continue
                        
                        df,tL,tR=mx.getVecAggs(time1st=aTime,aTIME=True)
                                            
                except Mx.MxError:
                    logStrFinal="{logStr:s}mxsVecsResults2MxDf failed".format(logStr=logStr)     
                    raise readDxAndMxError(logStrFinal)             

        

                               
    except readDxAndMxGoto:        
        pass 

    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal)      
        
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
        #return m

class readMxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def readMx(wDirMx, logPathOutputFct=os.path.relpath):
    """
    Reads SIR 3S results and returns a Mx object.

    :param wDirMx: Path to Mx-Directory. The results are read into a Mx object via the Mx files.
    :type wDirMx: str
    :param logPathOutputFct: func logPathOutputFct(fileName) is used for logoutput of filenames unless explicitly stated otherwise in the logoutput. Defaults to os.path.relpath.
    :type logPathOutputFct: func, optional, default=os.path.relpath

    :return: Mx object with two attributes: 
             - mx.df: pandas-Df ('time curve data') from from SIR 3S' MXS file(s)
             - mx.dfVecAggs: pandas-Df ('vector data') from SIR 3S' MXS file(s)
    :rtype: Mx object
    """
    
    mx=None
    
    logStrPrefix = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}Start.".format(logStrPrefix))   
    
    try:
        # Use glob to find all MX1 files in the directory
        mx1_files = glob.glob(os.path.join(wDirMx, '**', '*.MX1'), recursive=True)

        # Get the parent directories of the MX1 files
        parent_dirs = set(os.path.dirname(file) for file in mx1_files)

        # Check the number of directories found
        if len(parent_dirs) > 1:
            logger.error("{0:s}Mehr als ein Verzeichnis mit MX1-Dateien gefunden.".format(logStrPrefix))
            for dir in parent_dirs:
                logger.error("{0:s}Verzeichnis: {1:s}".format(logStrPrefix, dir))
            raise readMxError("Mehr als ein Verzeichnis mit MX1-Dateien gefunden.")
        elif len(parent_dirs) == 1:
            wDirMx = list(parent_dirs)[0]
        else:
            logger.error("{0:s}Keine Verzeichnisse mit MX1-Dateien gefunden.".format(logStrPrefix))
            raise readMxError("Keine Verzeichnisse mit MX1-Dateien gefunden.")
    except Exception as e:
        logger.error("{0:s}Ein Fehler ist aufgetreten beim Suchen von MX1-Verzeichnissen: {1:s}".format(logStrPrefix, str(e)))
        raise
    
    try:
        logger.debug("{0:s}wDirMx von abspath von wDir von dbFile: {1:s}".format(logStrPrefix, wDirMx))
        
        wDirMxMx1Content=glob.glob(os.path.join(wDirMx,'*.MX1'))
        wDirMxMx1Content=sorted(wDirMxMx1Content) 

        if len(wDirMxMx1Content)>1:
            logger.debug("{0:s}Mehr als 1 ({1:d}) MX1 in wDirMx vorhanden.".format(logStrPrefix, len(wDirMxMx1Content)))
        mx1File= wDirMxMx1Content[0]
        logger.debug("{0:s}mx1File: {1:s}".format(logStrPrefix, logPathOutputFct(mx1File)))
        
    except:
        logger.info("{0:s}Problem mit dem MX1-Dateipfad".format(logStrPrefix))
        
    try:
        mx=Mx.Mx(mx1File)
        logger.debug("{0:s}MX wurde bisher erfolgreich gelesen. {1:s}".format(logStrPrefix, mx1File))   
    except Mx.MxError:  
        logger.info("{0:s}MX1-Datei konnte nicht gelesen werden".format(logStrPrefix))
    finally:
        logger.debug("{0:s}_Done.".format(logStrPrefix)) 
    
    return mx

def constructNewMultiindexFromCols(df=pd.DataFrame(),mColNames=['OBJTYPE','OBJID'],mIdxNames=['OBJTYPE','OBJID']):
        """Constructs a new Multiindex from existing cols and returns the constructed df.

        Args:
            * df: dataFrame without Multiindex              
            * mColNames: list of columns which shall be used as Multiindex; the columns must exist; the columns will be droped
            * mIdxNames: list of names for the indices for the Cols above

        Returns:
            * df with Multiindex       
            * empty DataFrame is returned if an Error occurs
                   
        >>> d = {'OBJTYPE': ['ROHR', 'VENT'], 'pk': [123, 345], 'data': ['abc', 'def']}
        >>> import pandas as pd
        >>> df = pd.DataFrame(data=d)
        >>> from Xm import Xm
        >>> df=Xm.constructNewMultiindexFromCols(df=df,mColNames=['OBJTYPE','pk'],mIdxNames=['OBJTYPE','OBJID'])
        >>> df['data']
        OBJTYPE  OBJID
        ROHR     123      abc
        VENT     345      def
        Name: data, dtype: object
        """

        logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
        #logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
    
        try:    
            
            arrays=[]
            for col in mColNames:
                logger.debug(f"{col}: {type(df[col])}")
                arrays.append(df[col].tolist())
            tuples = list(zip(*(arrays)))
            index = pd.MultiIndex.from_tuples(tuples,names=mIdxNames)
            df.drop(mColNames,axis=1,inplace=True)   
            df=pd.DataFrame(df.values,index=index,columns=df.columns)
            #df = df.sort_index() # PerformanceWarning: indexing past lexsort depth may impact performance.
            return df
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal)    
            raise #df=pd.DataFrame()
        finally:
            pass
            #logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            #return df  
            
def fStripV3Colik2Tuple(col="('STAT', 'KNOT~*~*~*~PH', Timestamp('2024-09-01 08:00:00'), Timestamp('2024-09-01 08:00:00'))_i"
                        ,colPost='_i'):
    
    colRstrip=col.replace(colPost,'')
    colStrip=colRstrip[1:-1]            
    colStrip=colStrip.replace("'",'')            
    colTupleLst=str(colStrip).split(',')
                
    colTuple=(colTupleLst[0].strip()
             ,colTupleLst[1].strip()+colPost
             ,pd.Timestamp(colTupleLst[2].strip().replace('Timestamp','')[1:-1])
             ,pd.Timestamp(colTupleLst[3].strip().replace('Timestamp','')[1:-1])
    )
    return colTuple

def fGetMultiindexTupleFromV3Col(col):
    
    if isinstance(col,tuple):        
        return col
    
    elif isinstance(col,str):
        
        # ergaenzte Knotenwerte
        
        mObj=re.search('\)(?P<Postfix>_i)$',col)        
        if mObj != None:        
            return fStripV3Colik2Tuple(col,mObj.group('Postfix')) 
        
        mObj=re.search('\)(?P<Postfix>_k)$',col)        
        if mObj != None:                
            return fStripV3Colik2Tuple(col,mObj.group('Postfix')) 
        
        mObj=re.search('\)(?P<Postfix>_n)$',col)        
        if mObj != None:                
            return fStripV3Colik2Tuple(col,mObj.group('Postfix')) 
            
        # keine ergaenzte Knotenwerte    
        return (col,None,None,None)   