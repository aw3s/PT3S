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
>>> rm.pltNetDHUS(timeDeltaToT=timeDeltaToT)
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
...   os.remove(plotFileName)
>>> # ---
>>> # Test
>>> # ---
>>> rootDir=r'C:\\3S\Modelle'
>>> xmlFile=os.path.join(rootDir,'MVV_FWv12(Bericht Version 1.2)_TLN2_Szenarium.XML')
>>> xm=Xm.Xm(xmlFile=xmlFile)
>>> (wDir,modelDir,modelName)=xm.getWDirModelDirModelName()
>>> mx1File=os.path.join(wDir,os.path.join(modelDir,modelName))+'.MX1'            
>>> mx=Mx.Mx(mx1File=mx1File)
>>> mx=Mx.Mx(mx1File=mx1File)
>>> rm=Rm(xm=xm,mx=mx)
>>> plt.close('all')
>>> fig=plt.figure(
...   frameon=True
...  ,linewidth=1.
...  ,edgecolor='k') # black
>>> timeDeltaToT=pd.to_timedelta('8 minutes 5 seconds')
>>> rm.pltNetDHUS(timeDeltaToT=timeDeltaToT)
>>> (wD,fileName)=os.path.split(xm.xmlFile)
>>> (base,ext)=os.path.splitext(fileName)
>>> plotFileName=wD+os.path.sep+base+'.'+'pdf'
>>> if os.path.exists(plotFileName):                        
...    os.remove(plotFileName)
>>> plt.savefig(plotFileName,dpi=300)
>>> os.path.exists(plotFileName)
True
"""

import os
import sys
import logging
logger = logging.getLogger('PT3S.Rm')  
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

import Xm
import Mx

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
            if isinstance(xm,Xm.Xm):
                self.xm=xm
            else:
                logStrFinal="{:s}{:s} not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
            if isinstance(mx,Mx.Mx):
                self.mx=mx
            else:
                logStrFinal="{:s}{:s} not {:s}.".format(logStr,'xm','Xm-Type')
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
                  
                   # Attribute & Measure
                   # FWVB
                   ,pFWVBAttribute='W0' # nur Objekte mit >0 werden dargestellt - astype(float) muss möglich sein
                   ,pFWVBAttributeAsc=False # False: je größer Attribute, desto niedriger die z-Order ("kleine" auf "großen")
                   ,pFWVBMeasure='FWVB~*~*~*~W' # float()  muss möglich sein
                   ,pFWVBMeasureInRefPerc=True # Measure wird verarbeitet in Prozent T zu Ref 
                   ,pFWVBMeasure3Classes=True # Measure wird dargestellt in 3 Klassen
                   
                   # Attribute & Measure
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

                   # Selektionskriterien (haben KEINEN Einfluss auf die Abmessungen der Darstellung)
                   # sondern auf die Objekte, die dargestellt werden
                   # wirkt auf Attribute
                   ,quantil_pROHRAttributeHigh=1. # die 25% gößten hier 'DI' also
                   ,quantil_pROHRAttributeLow=.75 
                   ,quantil_pFWVBAttributeHigh=0. # alle 'W0' also
                   ,quantil_pFWVBAttributeLow=1. 
                   
                   # reine Darstellungsparametrierung (keine Filterung/Selektion mehr)
                   # -------------------------------------------------------------------------

                   # Darstellung FWVB
                   # Größe basierend auf pFWVBAttribute
                   ,pFWVBrefSize=10 # Groesse der FWVB-Symbole bei Attribute-Referenzwert; je größer desto größer
                   ,pFWVBrefScale=2 # Skalierung Groesse der FWVB-Symbole bei Attribute-Referenzwert; je größer desto kleiner
                   # Attribute-Referenzwert ist die Standardabweichung
                   
                   # Farbe basierend auf pFWVBMeasure
                   ,pFWVBMeasureColorMap=plt.cm.autumn 
                   ,pFWVBMeasureAlpha=0.9 
                   ,pFWVBMeasureClip=False    

                   # # Farbe basierend auf pFWVBMeasure - pFWVBMeasure3Classes=True                  
                   ,limitTopColor='palegreen'
                   ,limitTopAlpha=0.9 
                   ,limitTopClip=False             
                                                    
                   ,limitBottomColor='violet' # 'orchid'
                   ,limitBottomAlpha=0.9 
                   ,limitBottomClip=False    

                   ,limitMiddleColorMap=plt.cm.autumn 
                   ,limitMiddleAlpha=0.9 
                   ,limitMiddleClip=False    

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
                   ,cBfraction=0.05  # fraction of original axes to use for colorbar
                   ,CBpad=0.05 # fraction of original axes between colorbar and new image axes
                   ,cBanchorVertical=0.15 # vertikaler Fußpunkt der colorbar
                   ,CBaspect=10. # ratio of long to short dimension
                   ,CBshrink=0.25 # fraction by which to shrink the colorbar
                   ,CBlabelpad=-1
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
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
            if isinstance(timeDeltaToT,pd.Timedelta):
                timeT=firstTime+timeDeltaToT
            else:
                logStrFinal="{:s}{:s] not {:s}.".format(logStr,'xm','Xm-Type')
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

            # Sachdaten annotieren mit Spalte Measure >pXXXX ===============================================

            # FWVB            
            pFWVBMeasureValue=plotTimeDfs[timeTIdx][pFWVBMeasure].iloc[0] 
            if pFWVBMeasureInRefPerc:                
                pFWVBMeasureValueRef=plotTimeDfs[timeRefIdx][pFWVBMeasure].iloc[0] 
                pFWVBMeasureValue=[float(m)/float(mRef) if float(mRef) >0 else 1 for m,mRef in zip(pFWVBMeasureValue,pFWVBMeasureValueRef)]
            pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValue)) #!

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

            # FWVB
            pltFWVB=pltFWVB[(pltFWVB['CONT_ID'].astype(int).isin(CONT_IDisIn))]

            # Ausdehnung des Plots ===============================================
            dx=max(pltFWVB['pXCor_i'].max(),max(pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pXCor_i'].max(),pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pXCor_k'].max()))
            dy=max(pltFWVB['pYCor_i'].max(),max(pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pYCor_i'].max(),pltROHR[(pltROHR['CONT_ID'].astype(int).isin([1001]))]['pYCor_k'].max()))

            # erf. Verhältnis bei verzerrungsfreier Darstellung
            dydx=dy/dx 

            if(dydx>=1):
                dxInch=DINA4_x # Hochformat
            else:
                dxInch=DINA4_y # Querformat
    
            figwidth=dxInch

            #verzerrungsfrei: Blattkoordinatenverhaeltnis = Weltkoordinatenverhaeltnis
            factor=1-(cBfraction+CBpad)
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

            # Grundsortierung z-Order
            pltFWVB=pltFWVB.sort_values(by=[pFWVBAttribute],ascending=pFWVBAttributeAsc) 
            pltROHR=pltROHR.sort_values(by=[pROHRAttribute],ascending=pROHRAttributeAsc) 
           
            # FWVB Kategorien
            pltFWVB_top=pltFWVB[(pltFWVB['Measure']>=limitTop)] 
            pltFWVB_mid=pltFWVB[(pltFWVB['Measure']<limitTop) & (pltFWVB['Measure']>limitBottom)]     
            pltFWVB_bot=pltFWVB[(pltFWVB['Measure']<=limitBottom)] 

            # ============================================================
            # Plotten
            # ============================================================
            fig = plt.gcf()  
            fig.set_figwidth(figwidth)
            fig.set_figheight(figheight)

            ax=plt.subplot()
            ax.set_xlim(left=xlimLeft)
            ax.set_ylim(bottom=ylimBottom)
            ax.set_xlim(right=xlimRight)
            ax.set_ylim(top=ylimTop)

            if pFWVBMeasure3Classes:
                pcFWVB_top=ax.scatter(    
                     pltFWVB_top['pXCor_i'],pltFWVB_top['pYCor_i']                 
                    ,s=pFWVBrefSize*pltFWVB_top[pFWVBAttribute]/(pFWVBrefScale*pltFWVB[pFWVBAttribute].std())   
                    ,color=limitTopColor
                    ,alpha=limitTopAlpha
                    ,edgecolors='face'             
                    ,clip_on=limitTopClip)        

                pcFWVB_mid=ax.scatter(    
                     pltFWVB_mid['pXCor_i'],pltFWVB_mid['pYCor_i']       
                    ,s=pFWVBrefSize*pltFWVB_mid[pFWVBAttribute]/(pFWVBrefScale*pltFWVB[pFWVBAttribute].std())   
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
                    ,s=pFWVBrefSize*pltFWVB_bot[pFWVBAttribute]/(pFWVBrefScale*pltFWVB[pFWVBAttribute].std())   
                    ,color=limitBottomColor
                    ,alpha=limitBottomAlpha
                    ,edgecolors='face'             
                    ,clip_on=limitBottomClip)   
            else:                
                pcFWVB=ax.scatter(    
                     pltFWVB['pXCor_i'],pltFWVB['pYCor_i']       
                    ,s=pFWVBrefSize*pltFWVB[pFWVBAttribute]/(pFWVBrefScale*pltFWVB[pFWVBAttribute].std())   
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

            # Colormap
            # ============================================================                
            cax,kw=make_axes(ax
                             ,location='right'
                             ,fraction=cBfraction # fraction of original axes to use for colorbar
                             ,pad=CBpad # fraction of original axes between colorbar and new image axes
                             ,anchor=(0.,cBanchorVertical) # the anchor point of the colorbar axes
                             ,aspect=CBaspect # ratio of long to short dimension
                             ,shrink=CBshrink # fraction by which to shrink the colorbar
                            )         
           
            if pFWVBMeasure3Classes:
                colorBar=fig.colorbar(pcFWVB_mid
                            ,cax=cax
                            ,**kw
                           )
                colorBar.set_ticks([limitBottom,limitTop])
                colorBar.set_ticklabels([">{:3.0f}%".format(limitBottom*100),"<{:3.0f}%".format(limitTop*100)])
                colorBar.set_label('Measure in % T/TRef',labelpad=CBlabelpad)
            else:                
                colorBar=fig.colorbar(pcFWVB
                            ,cax=cax
                            ,**kw
                           )
                m=re.match(Mx.reSir3sIDcompiled,pFWVBMeasure)
                colorBar.set_ticks([pltFWVB['Measure'].min(),pltFWVB['Measure'].max()])
                colorBar.set_ticklabels(["{:6.2f} {:s}".format(pltFWVB['Measure'].min(),m.group(5)),"{:6.2f} {:s}".format(pltFWVB['Measure'].max(),m.group(5))])
                colorBar.set_label("{:s}".format(m.group(5)),labelpad=CBlabelpad)
                         
                                                                         
        except RmError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                       
        finally:
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
