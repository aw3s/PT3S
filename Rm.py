"""
---------------------------
DOCTEST
---------------------------
>>> # ---
>>> # Imports
>>> # ---
>>> import logging
>>> logger = logging.getLogger('PT3S.Rm')  
>>> import os
>>> import pandas as pd
>>> import matplotlib.pyplot as plt
>>> path = os.path.dirname(__file__)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> xmlFile=os.path.join(path,'testdata\LocalHeatingNetwork.XML')
>>> xm=Xm.Xm(xmlFile=xmlFile)
>>> mx1File=os.path.join(path,'testdata\WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1.MX1')
>>> mx=Mx.Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> mx.setResultsToMxsFile(NewH5Vec=True)
>>> xm.Mx(mx=mx)
>>> rm=Rm(xm=xm,mx=mx)
>>> plt.close('all')
>>> fig=plt.figure(
...  frameon=True
... ,linewidth=1.
... ,edgecolor='k') # black
>>> timeDeltaToT=mx.df.index[1]-mx.df.index[0]
>>> pd.set_option('display.max_columns',None)
>>> pd.set_option('display.width',666666)
>>> pFWVB=rm.pltNetDHUS(timeDeltaToT=timeDeltaToT)
>>> print("'''{:s}'''".format(repr(pFWVB).replace('\\n','\\n   ')))
'''  BESCHREIBUNG IDREFERENZ   W0  LFK  TVL0  TRS0 LFKT   W  W_min  W_max  INDTR  TRSK  VTYP  IMBG  IRFV                   pk                   tk  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  pXCor_i  pYCor_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_k  pYCor_k                                      CONT CONT_ID CONT_LFDNR                         WBLZ   Measure MCategory GCategory
   0            1         -1  200  0.8    90    50  NaN NaN    NaN    NaN      1    55     1     0   0.0  4643800032883366034  4643800032883366034  V-K002     1   90  2541059  5706265     20    319.0     56.0  R-K002     2   60  2541059  5706265     20    319.0     56.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  [BLNZ1, BLNZ1u5, BLNZ1u5u7]  1.000002       Top     BLNZ1
   1            3         -1  200  1.0    90    65  NaN NaN    NaN    NaN      1    65     1     0   0.0  4704603947372595298  4704603947372595298  V-K004     1   90  2541539  5706361     20    799.0    152.0  R-K004     2   60  2541539  5706361     20    799.0    152.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           []  1.000008       Top          
   2            4         -1  200  0.8    90    60  NaN NaN    NaN    NaN      1    60     1     0   0.0  5121101823283893406  5121101823283893406  V-K005     1   90  2541627  5706363     20    887.0    154.0  R-K005     2   60  2541627  5706363     20    887.0    154.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  [BLNZ1u5, BLNZ1u5u7, BLNZ5]  1.000010       Top     BLNZ5
   3            5         -1  200  0.8    90    55  NaN NaN    NaN    NaN      1    55     1     0   0.0  5400405917816384862  5400405917816384862  V-K007     1   90  2541899  5706325     20   1159.0    116.0  R-K007     2   60  2541899  5706325     20   1159.0    116.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                  [BLNZ1u5u7]  1.000029       Top          
   4            2         -1  200  0.6    90    60  NaN NaN    NaN    NaN      1    62     1     0   0.0  5695730293103267172  5695730293103267172  V-K003     1   90  2541457  5706345     20    717.0    136.0  R-K003     2   60  2541457  5706345     20    717.0    136.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           []  1.000006       Top          '''
>>> (wD,fileName)=os.path.split(xm.xmlFile)
>>> (base,ext)=os.path.splitext(fileName)
>>> plotFileName=wD+os.path.sep+base+'.'+'pdf'
>>> if os.path.exists(plotFileName):                        
...    os.remove(plotFileName)
>>> plt.savefig(plotFileName,dpi=300)
>>> os.path.exists(plotFileName)
True
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...   os.remove(mx.h5FileMxsVecs)
>>> if os.path.exists(plotFileName):                        
...   pass #os.remove(plotFileName)
"""
"""
#>>> # ---
#>>> # Test
#>>> # ---
#>>> rootDir=r'C:\\3S\Modelle'
#>>> xmlFile=os.path.join(rootDir,'MVV_FWv12(Bericht Version 1.2)_TLN2_Szenarium.XML')
#>>> xm=Xm.Xm(xmlFile=xmlFile)
#>>> (wDir,modelDir,modelName)=xm.getWDirModelDirModelName()
#>>> mx1File=os.path.join(wDir,os.path.join(modelDir,modelName))+'.MX1'            
#>>> mx=Mx.Mx(mx1File=mx1File)
#>>> mx=Mx.Mx(mx1File=mx1File)
#>>> rm=Rm(xm=xm,mx=mx)
#>>> plt.close('all')
#>>> fig=plt.figure(
#...   frameon=True
#...  ,linewidth=1.
#...  ,edgecolor='k') # black
#>>> timeDeltaToT=pd.to_timedelta('8 minutes 5 seconds')
#>>> rm.pltNetDHUS(timeDeltaToT=timeDeltaToT,pROHRAttributeRefSize=100.)
#>>> (wD,fileName)=os.path.split(xm.xmlFile)
#>>> (base,ext)=os.path.splitext(fileName)
#>>> plotFileName=wD+os.path.sep+base+'.'+'pdf'
#>>> if os.path.exists(plotFileName):                        
#...    os.remove(plotFileName)
#>>> plt.savefig(plotFileName,dpi=300)
#>>> os.path.exists(plotFileName)
#True
"""

import os
import sys
import logging
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

import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colorbar import make_axes

# ---
# --- PT3S Imports
# ---
import PT3S
import Xm
import Mx

logger = logging.getLogger('PT3S.Rm')  

DINA4_x=8.2677165354
DINA4_y=11.6929133858

class RmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Rm():
    """
      
    """
    def __init__(self,xm=None,mx=None): 
        """
          
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if isinstance(xm,Xm.Xm) or isinstance(xm,PT3S.Xm.Xm):
                self.xm=xm
            else:
                logStrFinal="{:s}{:s} not {:s}. Type: {!s:s}".format(logStr,'xm','Xm-Type',type(xm))
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
            if isinstance(mx,Mx.Mx) or isinstance(mx,PT3S.Mx.Mx):
                self.mx=mx
            else:
                logStrFinal="{:s}{:s} not {:s} Type: {!s:s}.".format(logStr,'xm','Xm-Type',type(mx))
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)    
            
            try:
                vNRCV_Mx1=self.xm.dataFrames['vNRCV_Mx1'] # d.h. Sachdaten bereits annotiert mit MX1-Wissen
            except:
                logger.debug("{:s}{:s} not in {:s}. Sachdaten mit MX1-Wissen zu annotieren wird nachgeholt ...".format(logStr,'vNRCV_Mx1','dataFrames'))
                self.xm.Mx(mx=self.mx)                      
                                                       
        except RmError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def pltNetDHUS(self
                   # Times
                   ,timeDeltaToRef=pd.to_timedelta('0 seconds') # Referenzzeit als TIMEDELTA zu Szenariumbeginn 
                   ,timeDeltaToT=None # Zeit als TIMEDELTA zu Szenariumbeginn                    
                  
                   # Attribute (Sachdatum) & Measure (Ergebnis)
                   # FWVB
                   ,pFWVBAttribute='W0' # nur Objekte mit >0 werden dargestellt - astype(float) muss möglich sein
                   ,pFWVBAttributeAsc=False # False: je größer Attribute, desto niedriger die z-Order ("kleine" auf "großen")
                   ,pFWVBMeasure='FWVB~*~*~*~W' # float()  muss möglich sein
                   ,pFWVBMeasureInRefPerc=True # Measure wird verarbeitet in Prozent T zu Ref 
                   ,pFWVBMeasure3Classes=True # Measure wird dargestellt in 3 Klassen
                   ,pFWVBVICsDf=None # df with VICs; Kundenname, Knotenname (NAME_I)
                   ,pFWVBGCategory=['BLNZ1','BLNZ5'] # ['Süd','Innenstadt','Nord Rest','Nord PWS','NordOst BHW','Ost PWF/PSE','Ost HWV']
                   
                   # Attribute (Sachdatum) & Measure (Ergebnis)
                   # ROHR
                   ,pROHRAttribute='DI' # nur Objekte mit >0 werden dargestellt - astype(float) muss möglich sein
                   ,pROHRAttributeAsc=False # False: je größer Attribute, desto niedriger die z-Order ("kleine" auf "großen")
                   # Attribute wirkt auf die Linie (Breite, Farbe)
                   # Measure wirkt auf die Marker (Größe, Farbe)
                   ,pROHRMeasure='ROHR~*~*~*~QMAV' # float()  muss möglich sein
                   ,pROHRMeasureAbs=True #  Measure wird verarbeitet als Absolutwert 
                  
                   # Filterkriterien (haben ggf. Einfluss auf die Abmessungen der Darstellung)
                   ,KVRisIn=[2]
                   ,CONT_IDisIn=[1001]                  
                   # 3-Klassen Darstellung FWVB; die Kriterien beziehen sich auf pFWVBMeasure (ggf. verarbeitet in Prozent T/Ref)
                   ,limitTop=0.95 # >= in Top
                   ,limitBottom=0.10 # <= in Bottom
                   # bei pFWVBMeasureInRefPerc=False muss für die Limits der pFWVBMeasure-Wertebereich angegeben werden 

                   # Selektionskriterien (haben KEINEN Einfluss auf die Abmessungen der Darstellung)
                   # sondern auf die Objekte, die dargestellt werden
                   # wirkt auf Attribute
                   ,quantil_pROHRAttributeHigh=1. # die 25% gößten hier 'DI' also
                   ,quantil_pROHRAttributeLow=.75 
                   ,quantil_pFWVBAttributeHigh=1. # alle 'W0' also
                   ,quantil_pFWVBAttributeLow=0. 
                   
                   # reine Darstellungsparametrierung (keine Filterung/Selektion mehr)
                   # -------------------------------------------------------------------------

                   # Plot
                   ,pltTitle='pltNetDHUS' # plt.title not f.suptitle

                   # Figure
                   ,figFrameon=True # set whether the figure frame (background) is displayed or invisible
                   #,figLinewidth=1.
                   ,figEdgecolor='white' # set the edge color of the Figure rectangle
                   ,figFacecolor='white' # set the face color of the Figure rectangle

                   # Darstellung FWVB
                   # Größe basierend auf pFWVBAttribute
                   ,pFWVBrefSize=10 # Groesse der FWVB-Symbole bei Attribute-Referenzwert; je größer desto größer
                   ,pFWVBrefScale=2 # Skalierung Groesse der FWVB-Symbole bei Attribute-Referenzwert; je größer desto kleiner
                   # Attribute-Referenzwert ist die Standardabweichung; wenn diese <1 ist der Mittelwert
                   
                   # Farbe basierend auf pFWVBMeasure
                   ,pFWVBMeasureColorMap=plt.cm.autumn 
                   ,pFWVBMeasureAlpha=0.9 
                   ,pFWVBMeasureClip=False    

                   # # Farbe basierend auf pFWVBMeasure - pFWVBMeasure3Classes=True                  
                   ,limitTopColor='palegreen'
                   ,limitTopAlpha=0.9 
                   ,limitTopClip=False            
                   ,limitTopText='OK' 
                   ,limitTopSizeQuantil=.95 
                                                    
                   ,limitBottomColor='violet' # 'orchid'
                   ,limitBottomAlpha=0.9 
                   ,limitBottomClip=False    
                   ,limitBottomText='NOK' 
                   ,limitBottomSizeQuantil=.95 

                   ,limitMiddleColorMap=plt.cm.autumn 
                   ,limitMiddleAlpha=0.9 
                   ,limitMiddleClip=False    
                   ,limitMiddleText='dazwischen'
                   ,limitMiddleSizeQuantil=.95 

                   # Darstellung ROHR
                   
                   # pROHRAttribute wirkt auf die Linie (Breite, Farbe)                   
                   ,pROHRAttributeColorMap=plt.cm.binary    
                   ,pROHRAttributeRefSize=1.0 # Dicke der Linie bei Attribute-Referenzwert; je größer desto dicker
                   # Attribute-Referenzwert ist das Maximum                                
                   ,pROHRClip=False
                   ,pROHRAttributeLs='-'
                   
                   # Measure wirkt auf die Marker (Größe, Farbe)
                   ,pROHRMeasureColorMap=plt.cm.binary #plt.cm.autumn
                   ,pROHRMeasureRefSizeFactor=1.0 # Größe des Markers bei Measure-Referenzwert im Verhältnis zu pROHRAttributeRefSize ; je größer desto größer
                   # Measure-Referenzwert ist das Maximum; je nach dem umhüllt die Liniendicke den Marker oder nicht
                   ,pROHRMeasureMarker='.'                 
                
                   # Colorbar
                   ,CBfraction=0.05  # fraction of original axes to use for colorbar
                   ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
                   ,CBlabelPad=-50
               
                   ,CBaspect=10. # ratio of long to short dimension
                   ,CBshrink=0.3 # fraction by which to shrink the colorbar
                   ,CBanchorHorizontal=0. # horizontaler Fußpunkt der colorbar in Plot-%
                   ,CBanchorVertical=0.2 # vertikaler Fußpunkt der colorbar in Plot-%

                   # nicht relevant bei 3Classes...; limitTop und limitBottom gelten bei 3Classes... 
                   ,CBFixedMinMax=False 
                   ,CBFixedMin=None
                   ,CBFixedMax=None

                   # ColorbarLegend (3Classes)
                   # Position der Repräsentantensymbole 
                   # dabei sind:
                   # 0 = colorbar unten
                   # 1 = colorbar oben
                   # "1" ist alsp die colorbar-Länge; die Länge von "1" im Plot wird von CBaspect und CBshrink beeinflusst                       
                   ,CBLe3cTopVpad=1+1*1/4
                   # "1"
                   ,CBLe3cMiddleVpad=.5                                                                         
                   ,CBLe3cBottomVpad=0-1*1/4  
                 
                   ,CBLe3cHpadSymbol=0.2 # 0.1  
                   ,CBLe3cHpad=1.2 # 1.4 # fixer Abstand Repräsentantentext zu Repräsentantensymbol      
                   ,CBLe3cTextSpaceFactor=0.5 # plus Abstandsfaktor Repräsentantentext zu Repräsentantensymbol

                   #Schriftfeld
                   ,titleBlockHStart=-0.18
                   ,titleBlockHSpace=0.45
                   ,titleBlockVSpace=0.2 # von Top(ggf. Symbol) der Colorbar
                   ): 
        """
          
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            # 2 Szenrariumzeiten ermitteln ===============================================
            firstTime=self.mx.df.index[0]
            if isinstance(timeDeltaToRef,pd.Timedelta):
                timeRef=firstTime+timeDeltaToRef
            else:
                logStrFinal="{:s}{:s} not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
            if isinstance(timeDeltaToT,pd.Timedelta):
                timeT=firstTime+timeDeltaToT
            else:
                logStrFinal="{:s}{:s} not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
           
            # Vektorergebnisse zu den 2 Zeiten holen ===============================================
            timesReq=[]
            timesReq.append(timeRef)
            timesReq.append(timeT)           
            plotTimeDfs=self.mx.getMxsVecsFileData(timesReq=timesReq)
            timeRefIdx=0
            timeTIdx=1

            # Sachdatenbasis ===============================================
            vROHR=self.xm.dataFrames['vROHR'] 
            vKNOT=self.xm.dataFrames['vKNOT']
            vFWVB=self.xm.dataFrames['vFWVB']
            vNRCV_Mx1=self.xm.dataFrames['vNRCV_Mx1']

            if isinstance(pFWVBVICsDf,pd.core.frame.DataFrame):
                df=vFWVB.merge(pFWVBVICsDf,left_on='NAME_i',right_on='Knotenname')
                vFWVB=vFWVB.assign(VIC=df['Kundenname'])
           
            # Einheit der Measures ermitteln (fuer Annotationen)
            pFWVBMeasureCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(pFWVBMeasure)]
            pFWVBMeasureUNIT=pFWVBMeasureCh.iloc[0].UNIT
            pFWVBMeasureATTRTYPE=pFWVBMeasureCh.iloc[0].ATTRTYPE

            pROHRMeasureCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(pROHRMeasure)]
            pROHRMeasureUNIT=pROHRMeasureCh.iloc[0].UNIT
            pROHRMeasureATTRTYPE=pROHRMeasureCh.iloc[0].ATTRTYPE

            # Sachdaten annotieren mit Spalte Measure >pXXXX ===============================================

            # FWVB            
            pFWVBMeasureValue=plotTimeDfs[timeTIdx][pFWVBMeasure].iloc[0] 
            if pFWVBMeasureInRefPerc:  # auch in diesem Fall trägt die Spalte Measure das Ergebnis               
                pFWVBMeasureValueRef=plotTimeDfs[timeRefIdx][pFWVBMeasure].iloc[0] 
                pFWVBMeasureValue=[float(m)/float(mRef) if float(mRef) >0 else 1 for m,mRef in zip(pFWVBMeasureValue,pFWVBMeasureValueRef)]
            pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValue)) #!

            # Sachdaten annotieren mit Spalte MCategory            
            pFWVBCat=[]
            for index, row in pFWVB.iterrows():
                if row.Measure >= limitTop:
                    pFWVBCat.append('Top')
                elif row.Measure <= limitBottom:
                    pFWVBCat.append('Bottom')
                else:
                    pFWVBCat.append('Middle')
            pFWVB=pFWVB.assign(MCategory=pd.Series(pFWVBCat)) 

            # Sachdaten annotieren mit Spalte GCategory               
            sCatReq=set(pFWVBGCategory)       
            pFWVBCat=[]
            for index, row in pFWVB.iterrows():
                gCat=row.WBLZ
                sCat=set(gCat)
                s=sCat.intersection(sCatReq)
                if len(s) == 0:
                    pFWVBCat.append('')
                elif len(s) > 1:
                    pFWVBCat.append("{!s:s}".format(s)) 
                else:
                    pFWVBCat.append(s.pop())
            pFWVB=pFWVB.assign(GCategory=pd.Series(pFWVBCat)) 

            # ROHR
            pROHRMeasureValueRaw=plotTimeDfs[timeTIdx][pROHRMeasure].iloc[0]   
            pROHRMeasureValue=[None for m in pROHRMeasureValueRaw]
            for idx in range(len(pROHRMeasureValueRaw)):                   
                mx2Idx=vROHR['mx2Idx'].iloc[idx]
                m=pROHRMeasureValueRaw[mx2Idx]
                m=float(m)
                if pROHRMeasureAbs:
                    pROHRMeasureValue[idx]=math.fabs(m)
                else:
                    pROHRMeasureValue[idx]=m
            pROHR=vROHR.assign(Measure=pd.Series(pROHRMeasureValue)) #!

            # Filtern >pltXXXX ===============================================
            # (haben ggf. Einfluss auf die Abmessungen der Darstellung)
            pltROHR=pROHR
            pltFWVB=pFWVB

            # ROHR
            pltROHR=pltROHR[(pltROHR['CONT_ID'].astype(int).isin(CONT_IDisIn))]
            pltROHR=pltROHR[(pltROHR['KVR'].astype(int).isin(KVRisIn))]
            row,col=pltROHR.shape
            logger.debug("{:s}pltROHR nach filtern: {:d}".format(logStr,row))     

            # FWVB
            pltFWVB=pltFWVB[(pltFWVB['CONT_ID'].astype(int).isin(CONT_IDisIn))]

            # Ausdehnung des Plots ===============================================
            dx=max(pltFWVB['pXCor_i'].max(),max(pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pXCor_i'].max(),pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pXCor_k'].max()))
            dy=max(pltFWVB['pYCor_i'].max(),max(pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pYCor_i'].max(),pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pYCor_k'].max()))

            logger.debug("{:s}dx={:10.2f} dy={:10.2f}".format(logStr,dx,dy))     

            # erf. Verhältnis bei verzerrungsfreier Darstellung
            dydx=dy/dx 

            if(dydx>=1):
                dxInch=DINA4_x # Hochformat
            else:
                dxInch=DINA4_y # Querformat
    
            figwidth=dxInch

            #verzerrungsfrei: Blattkoordinatenverhaeltnis = Weltkoordinatenverhaeltnis
            factor=1-(CBfraction+CBHpad)
            # verzerrungsfreie Darstellung sicherstellen
            figheight=figwidth*dydx*factor
       
            # Weltkoordinatenbereich
            xlimLeft=0
            ylimBottom=0
            xlimRight=dx
            ylimTop=dy

            # =========================================             
            pltFWVB[pFWVBAttribute]=pltFWVB[pFWVBAttribute].astype(float)
            pltROHR[pROHRAttribute]=pltROHR[pROHRAttribute].astype(float)
            
            # Selektionen ===============================================
            pltFWVB=pltFWVB[pltFWVB[pFWVBAttribute]>0] 
            pltROHR=pltROHR[pltROHR[pROHRAttribute]>0] 

            pltFWVB=pltFWVB[(pltFWVB[pFWVBAttribute]<=pltFWVB[pFWVBAttribute].quantile(quantil_pFWVBAttributeHigh))
                            &
                            (pltFWVB[pFWVBAttribute]>=pltFWVB[pFWVBAttribute].quantile(quantil_pFWVBAttributeLow))
                           ]

            pltROHR=pltROHR[(pltROHR[pROHRAttribute]<=pltROHR[pROHRAttribute].quantile(quantil_pROHRAttributeHigh))
                            &
                            (pltROHR[pROHRAttribute]>=pltROHR[pROHRAttribute].quantile(quantil_pROHRAttributeLow))
                           ]

            row,col=pltROHR.shape
            logger.debug("{:s}pltROHR nach selektieren: {:d}".format(logStr,row))     

            # Grundsortierung z-Order
            pltFWVB=pltFWVB.sort_values(by=[pFWVBAttribute],ascending=pFWVBAttributeAsc) 
            pltROHR=pltROHR.sort_values(by=[pROHRAttribute],ascending=pROHRAttributeAsc) 
           
            pltFWVB_top=pltFWVB[(pltFWVB['MCategory']=='Top')] 
            pltFWVB_mid=pltFWVB[(pltFWVB['MCategory']=='Middle')]     
            pltFWVB_bot=pltFWVB[(pltFWVB['MCategory']=='Bottom')] 

            #pltFWVB_top=pltFWVB[(pltFWVB['Measure']>=limitTop)] 
            #pltFWVB_mid=pltFWVB[(pltFWVB['Measure']<limitTop) & (pltFWVB['Measure']>limitBottom)]     
            #pltFWVB_bot=pltFWVB[(pltFWVB['Measure']<=limitBottom)] 

            pltFWVB_top_Anz,col=pltFWVB_top.shape
            pltFWVB_mid_Anz,col=pltFWVB_mid.shape
            pltFWVB_bot_Anz,col=pltFWVB_bot.shape

            # ============================================================
            # Plotten
            # ============================================================
            fig = plt.gcf()  
            fig.set_figwidth(figwidth)
            fig.set_figheight(figheight)

            logger.debug("{:s}dx={:10.2f} dy={:10.2f}".format(logStr,dx,dy))     
            logger.debug("{:s}figwidth={:10.2f} figheight={:10.2f}".format(logStr,figwidth,figheight))   

            ax=plt.subplot()
            ax.set_xlim(left=xlimLeft)
            ax.set_ylim(bottom=ylimBottom)
            ax.set_xlim(right=xlimRight)
            ax.set_ylim(top=ylimTop)

            xTicks=ax.get_xticks()
            dxTick = xTicks[1]-xTicks[0]
            yTicks=ax.set_yticks([idx*dxTick for idx in range(math.floor(dy/dxTick)+1)])

            plt.title(pltTitle)              
            fig.set_frameon(figFrameon) 
            fig.set_edgecolor(figEdgecolor)
            fig.set_facecolor(figFacecolor)
            #plt.setp(fig,linewidth=figLinewidth)

            pFWVBrefSizeValue=pltFWVB[pFWVBAttribute].std()
            if pFWVBrefSizeValue < 1:
                pFWVBrefSizeValue=pltFWVB[pFWVBAttribute].mean()

            logger.debug("{:s}pFWVBrefSizeValue (Attributwert): {:6.2f}".format(logStr,pFWVBrefSizeValue)) 
                     
            if pFWVBMeasure3Classes:
                pcFWVB_top=ax.scatter(    
                     pltFWVB_top['pXCor_i'],pltFWVB_top['pYCor_i']                 
                    ,s=pFWVBrefSize*pltFWVB_top[pFWVBAttribute]/(pFWVBrefScale*pFWVBrefSizeValue)   
                    ,color=limitTopColor
                    ,alpha=limitTopAlpha
                    ,edgecolors='face'             
                    ,clip_on=limitTopClip)        

                pcFWVB_mid=ax.scatter(    
                     pltFWVB_mid['pXCor_i'],pltFWVB_mid['pYCor_i']       
                    ,s=pFWVBrefSize*pltFWVB_mid[pFWVBAttribute]/(pFWVBrefScale*pFWVBrefSizeValue)   
                    # Farbskala
                    ,cmap=limitMiddleColorMap
                    # Normierung Farbe
                    ,vmin=limitBottom
                    ,vmax=limitTop
                    # Farbwert
                    ,c=pltFWVB_mid['Measure'] 
                    ,alpha=limitMiddleAlpha
                    ,edgecolors='face'
                    ,clip_on=limitMiddleClip
                   )
                pcFWVB_bot=ax.scatter(    
                     pltFWVB_bot['pXCor_i'],pltFWVB_bot['pYCor_i']                 
                    ,s=pFWVBrefSize*pltFWVB_bot[pFWVBAttribute]/(pFWVBrefScale*pFWVBrefSizeValue)   
                    ,color=limitBottomColor
                    ,alpha=limitBottomAlpha
                    ,edgecolors='face'             
                    ,clip_on=limitBottomClip)   
            else:                
                pcFWVB=ax.scatter(    
                     pltFWVB['pXCor_i'],pltFWVB['pYCor_i']       
                    ,s=pFWVBrefSize*pltFWVB[pFWVBAttribute]/(pFWVBrefScale*pFWVBrefSizeValue)   
                    # Farbskala
                    ,cmap=pFWVBMeasureColorMap
                    # Normierung Farbe
                    ,vmin=pltFWVB['Measure'].min()
                    ,vmax=pltFWVB['Measure'].max()
                    # Farbwert
                    ,c=pltFWVB['Measure'] 
                    ,alpha=pFWVBMeasureAlpha
                    ,edgecolors='face'
                    ,clip_on=pFWVBMeasureClip
                   )

            # ROHR
            minLine=pltROHR[pROHRAttribute].min()
            maxLine=pltROHR[pROHRAttribute].max()
            logger.debug("{:s}minLine (Attribute): {:6.2f}".format(logStr,minLine))
            logger.debug("{:s}maxLine (Attribute): {:6.2f}".format(logStr,maxLine))
            normLine=colors.Normalize(minLine,maxLine)

            minMarker=pltROHR['Measure'].min()
            maxMarker=pltROHR['Measure'].max()
            normMarker=colors.Normalize(minMarker,maxMarker)

            for xs,ys,vLine,vMarker in zip(pltROHR['pWAYPXCors'],pltROHR['pWAYPYCors'],pltROHR[pROHRAttribute],pltROHR['Measure']):        
                colorLine=pROHRAttributeColorMap(normLine(vLine)) 
                colorMarker=pROHRMeasureColorMap(normMarker(vMarker))
                pcLines=ax.plot(xs,ys
                                ,color=colorLine
                                ,linewidth=pROHRAttributeRefSize*vLine/maxLine
                                ,ls=pROHRAttributeLs
                                ,marker=pROHRMeasureMarker
                                ,mfc=colorMarker 
                                ,ms=pROHRMeasureRefSizeFactor*pROHRAttributeRefSize*vMarker/maxMarker
                                ,mew=0.
                                ,markevery=[0,len(xs)-1]
                                ,aa=True
                                ,clip_on=pROHRClip
                               )            
                logger.debug("{:s}pcLines: {!s:s}".format(logStr,pcLines))

            # Colormap
            # ============================================================                
            cax,kw=make_axes(ax
                             ,location='right'
                             ,fraction=CBfraction # fraction of original axes to use for colorbar
                             ,pad=CBHpad # fraction of original axes between colorbar and new image axes
                             ,anchor=(CBanchorHorizontal,CBanchorVertical) # the anchor point of the colorbar axes
                             ,aspect=CBaspect # ratio of long to short dimension
                             ,shrink=CBshrink # fraction by which to shrink the colorbar
                            )         

            # CB -----------------------------------------------
            if pFWVBMeasure3Classes:
                colorBar=fig.colorbar(pcFWVB_mid
                            ,cax=cax
                            ,**kw
                           )                             
            else:                
                colorBar=fig.colorbar(pcFWVB
                            ,cax=cax
                            ,**kw
                           )        
            # ticks Value  
            if pFWVBMeasure3Classes:
                minCBtickValue=limitBottom
                maxCBtickValue=limitTop                
            else:
                if CBFixedMinMax and isinstance(CBFixedMin,float) and isinstance(CBFixedMax,float):
                    minCBtickValue=CBFixedMin
                    maxCBtickValue=CBFixedMax                       
                else:
                    minCBtickValue=pltFWVB['Measure'].min()
                    maxCBtickValue=pltFWVB['Measure'].max()           
            colorBar.set_ticks([minCBtickValue,maxCBtickValue])  

            # ticks Label
            if pFWVBMeasureInRefPerc:
                if pFWVBMeasure3Classes:
                    minCBtickLabel=">{:3.0f}%".format(minCBtickValue*100)
                    maxCBtickLabel="<{:3.0f}%".format(maxCBtickValue*100)                             
                else:
                    minCBtickLabel="{:3.0f}%".format(minCBtickValue*100)
                    maxCBtickLabel="{:3.0f}%".format(maxCBtickValue*100) 
            else:
                if pFWVBMeasure3Classes:
                    minCBtickLabel=">{:6.2f} {:s}".format(minCBtickValue,pFWVBMeasureUNIT)
                    maxCBtickLabel="<{:6.2f} {:s}".format(maxCBtickValue,pFWVBMeasureUNIT)    
                else:
                    minCBtickLabel="{:6.2f} {:s}".format(minCBtickValue,pFWVBMeasureUNIT)
                    maxCBtickLabel="{:6.2f} {:s}".format(maxCBtickValue,pFWVBMeasureUNIT)    
            colorBar.set_ticklabels([minCBtickLabel,maxCBtickLabel])
                              
            # Label text
            if pFWVBMeasureInRefPerc:
                    CBLabelText="{:s} in % von Referenzzustand".format(pFWVBMeasureUNIT)                                                                
            else:
                    CBLabelText="{:s} in {:s}".format(pFWVBMeasureATTRTYPE,pFWVBMeasureUNIT)
         
            colorBar.set_label(CBLabelText,labelpad=CBlabelPad)
                           
            if pFWVBMeasure3Classes:                                                        
                # CB Legend 3Classes -----------------------------------------------         
                fig.sca(cax)
                if pltFWVB_bot_Anz > 0:
                    po=cax.scatter( CBHpad+CBLe3cHpadSymbol,CBLe3cBottomVpad                            
                                    ,s=pFWVBrefSize*pltFWVB[pFWVBAttribute].max()/(pFWVBrefScale*pFWVBrefSizeValue)                                                                                                                      
                                    ,c=limitBottomColor
                                    ,alpha=0.9
                                    ,edgecolors='face'             
                                    ,clip_on=False
                                   )
                    # Text dazu
                    o=po.findobj(match=None) 
                    p=o[0]           
                    bb=p.get_datalim(cax.transAxes)                               
                    a=plt.annotate(limitBottomText                                     
                                 ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cBottomVpad)
                                 ,xycoords=cax.transAxes 
                                 ,rotation='vertical' #90
                                 ,va='center'
                                 ,ha='center'  
                                 ,color=limitBottomColor 
                                 )
                    # weiterer Text dazu
                    a=plt.annotate("Anz HA: {:6d}".format(pltFWVB_bot_Anz)                                
                                 ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cBottomVpad)
                                 ,xycoords=cax.transAxes 
                                 ,rotation='vertical' #90
                                 ,va='center'
                                 ,ha='center'  
                                 ,color=limitBottomColor 
                                 )

                if pltFWVB_top_Anz > 0:
                    po=cax.scatter( CBHpad+CBLe3cHpadSymbol,CBLe3cTopVpad                        
                                    ,s=pFWVBrefSize*pltFWVB[pFWVBAttribute].max()/(pFWVBrefScale*pFWVBrefSizeValue)                
                                    ,c=limitTopColor
                                    ,alpha=0.9
                                    ,edgecolors='face'             
                                    ,clip_on=False                                 
                                   )
                    # Text dazu
                    o=po.findobj(match=None) 
                    p=o[0]           
                    bb=p.get_datalim(cax.transAxes)     
                    bbTop=bb      
                    a=plt.annotate(limitTopText                                
                                 ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cTopVpad)
                                 ,xycoords=cax.transAxes 
                                 ,rotation='vertical' #90
                                 ,va='center'
                                 ,ha='center'    
                                 ,color=limitTopColor                            
                                 )

                    # weiterer Text dazu                  
                    a=plt.annotate("Anz HA: {:6d}".format(pltFWVB_top_Anz)                                       
                                 ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad++CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cTopVpad)
                                 ,xycoords=cax.transAxes 
                                 ,rotation='vertical' #90
                                 ,va='center'
                                 ,ha='center'    
                                 ,color=limitTopColor                            
                                 )


                if pltFWVB_mid_Anz > 0:
                    # Farbe 
                    limitMiddleColorMapNorm=colors.Normalize(limitBottom,limitTop)
                    #value=pltFWVB_mid['Measure'].loc[pltFWVB_mid[pFWVBAttribute].idxmax()]
                    value=limitBottom+.5*(limitTop-limitBottom)
                    limitMiddleColor=limitMiddleColorMap(limitMiddleColorMapNorm(value))               
                    # Symbol              
                    po=cax.scatter( CBHpad+CBLe3cHpadSymbol,CBLe3cMiddleVpad                            
                                    ,s=pFWVBrefSize*pltFWVB[pFWVBAttribute].max()/(pFWVBrefScale*pFWVBrefSizeValue)                  
                                    ,c=limitMiddleColor
                                    ,alpha=0.9
                                    ,edgecolors='face'             
                                    ,clip_on=False
                                    ,visible=False # es erden nur die Koordinaten benoetigt
                                  )
                    # Text dazu
                    o=po.findobj(match=None) 
                    p=o[0]
                    bb=p.get_datalim(cax.transAxes)
                    a=plt.annotate(limitMiddleText                                    
                                   ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cMiddleVpad)                                                                                 
                                   ,xycoords=cax.transAxes 
                                   ,rotation='vertical' #90
                                   ,va='center'
                                   ,ha='center'
                                   ,color=limitMiddleColor   
                                 #  ,visible=False
                    )
                    # weiterer Text dazu                
                    a=plt.annotate("Anz HA: {:6d}".format(pltFWVB_mid_Anz)                                              
                                   ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cMiddleVpad)                                                                                 
                                   ,xycoords=cax.transAxes 
                                   ,rotation='vertical' #90
                                   ,va='center'
                                   ,ha='center'
                                   ,color=limitMiddleColor   
                                 #  ,visible=False
                    )
                                                  
            # Legende Modellschriftfeld ---------------------------------------------------------------------
            fig.sca(cax)

            if bbTop != None:
                vModelTitleBlock=bbTop.y1+titleBlockVSpace
            else:
                vModelTitleBlock=1+titleBlockVSpace
            
            Projekt=self.xm.dataFrames['MODELL']['PROJEKT'].iloc[0]
            Planer=self.xm.dataFrames['MODELL']['PLANER'].iloc[0]
            Inst=self.xm.dataFrames['MODELL']['INST'].iloc[0]
            
            a=plt.annotate(Projekt, xy=(titleBlockHStart,vModelTitleBlock)
                         ,xycoords=cax.transAxes 
                         ,rotation='vertical'
                         ,va='bottom'
                         ,ha='left'
            )

            a=plt.annotate(Planer, xy=(titleBlockHStart+1*titleBlockHSpace,vModelTitleBlock)
                         ,xycoords=cax.transAxes 
                         ,rotation='vertical'
                         ,va='bottom'
                         ,ha='left'   
            )

            a=plt.annotate(Inst, xy=(titleBlockHStart+2*titleBlockHSpace,vModelTitleBlock)
                         ,xycoords=cax.transAxes 
                         ,rotation='vertical'
                         ,va='bottom'
                         ,ha='left'   
            )

            xmFileName,ext = os.path.splitext(os.path.basename(self.xm.xmlFile))
            a=plt.annotate("M: {:s}".format(xmFileName), xy=(titleBlockHStart+3*titleBlockHSpace,vModelTitleBlock)
                           ,xycoords=cax.transAxes 
                           ,rotation='vertical'
                           ,va='bottom'
                           ,ha='left'   
            )
            (wDir,modelDir,modelName)=self.xm.getWDirModelDirModelName()
            a=plt.annotate("E: {:s}".format(os.path.join(os.path.basename(wDir),os.path.join(modelDir,modelName))+'.MX1')
                           ,xy=(titleBlockHStart+4*titleBlockHSpace,vModelTitleBlock), xycoords=cax.transAxes 
                           ,rotation='vertical'
                           ,va='bottom'
                           ,ha='left'   
            )

            txt="TRef: {!s:s} T: {!s:s}".format(timeDeltaToRef,timeDeltaToT).replace('days','Tage')
            a=plt.annotate(txt
                           ,xy=(titleBlockHStart+5*titleBlockHSpace,vModelTitleBlock)
                           ,xycoords=cax.transAxes 
                           ,rotation='vertical'
                           ,va='bottom'
                           ,ha='left'   
            )

            # ---------------------------------------------------------------------
            # NumAnz 
            fig.sca(ax)

            patWBLZ='WBLZ~[\S ]+~\S*~\S+~\S+'
            patDH='KNOT~K0001~\S*~\S+~QM'
            for index, row in vNRCV_Mx1[
             (
               (vNRCV_Mx1['Sir3sID'].str.contains(patWBLZ)) 
                 |
               (vNRCV_Mx1['Sir3sID'].str.contains(patDH)) 
              )  
            &
             (vNRCV_Mx1['CONT_ID'].astype(int) == 1001)  
            ].iterrows():
                s=self.mx.df[row.Sir3sID]
                sCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(row.Sir3sID)]

                v=s[timeT]                
                
                if sCh.iloc[0].ATTRTYPE=='WVB':
                    v0=s[timeRef]
                    vp=v/v0*100               
                                
                x,y = row.pXYLB                
                if x<0:
                    x=0
                if y<0:
                    continue
               
                if sCh.iloc[0].ATTRTYPE=='WVB':
                    if sCh.iloc[0].NAME1=='InnenNo': # or sCh.iloc[0].NAME1=='WärmeblnzGes':
                        rotation='vertical'
                        va='center'
                        ha='right'
                    else:
                        rotation='horizontal'
                        va='bottom'
                        ha='center' 

                    a=plt.annotate("{:s}: {:6.1f} {:s} {:6.1f}%".format(sCh.iloc[0].NAME1,v,sCh.iloc[0].UNIT,vp), xy=(round(x,0),round(y,0)), xycoords='data'                        
                             ,va=va
                             ,ha=ha
                             ,rotation=rotation
                            ,clip_on=False
                    )
                else:
                    a=plt.annotate("{:s}: {:6.1f} {:s}".format('Kontrollwert DH',v,sCh.iloc[0].UNIT), xy=(round(x,0),round(y,0)), xycoords='data'                        
                             ,va='bottom'
                             ,ha='center' 
                            ,clip_on=False
                    )

            # ---------------------------------------------------------------------
            # VICs
            if isinstance(pFWVBVICsDf,pd.core.frame.DataFrame):
                fig.sca(ax)
                xStart=9000.
                yStart=1000.
                fontsize=8
                distance=50
                idx=0
                for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():      
                        kunde=row.VIC                         
                        a=plt.annotate("{:s}".format(kunde), xy=(xStart,yStart+fontsize*distance*idx), xycoords='data'                              
                                    ,fontsize=fontsize    
                                    ,va='bottom'
                                    ,ha='left' 
                                ,clip_on=False
                                    )
                        idx=idx+1

                idx=0
                if pFWVBMeasureInRefPerc:
                    unit='%'
                else:
                    unit=pFWVBMeasureUNIT
                for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():
                        v=pFWVB['Measure'].loc[index]
                        a=plt.annotate("{:6.2f} {:s}".format(v*100,unit), xy=(xStart+6000,yStart+fontsize*distance*idx), xycoords='data'                             
                                    ,fontsize=fontsize    
                                    ,va='bottom'
                                    ,ha='left' 
                                ,clip_on=False
                                        )
                        idx=idx+1  
                                                              
        except RmError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return pFWVB 

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
