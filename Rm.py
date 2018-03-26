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
>>> print("'''{:s}'''".format(repr(pFWVB[['Measure','MCategory','GCategory']]).replace('\\n','\\n   ')))
'''    Measure MCategory  GCategory
   0  1.000000       Top  BLNZ1u5u7
   1  0.941650    Middle           
   2  0.932884    Middle  BLNZ1u5u7
   3  0.926353    Middle  BLNZ1u5u7
   4  0.967076       Top           '''
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

def pltNetNodes( 
                # ALLG
                 pDf 
                ,pMeasure3Classes=True # 

                ,CBFixedLimits=True
                ,CBFixedLimitLow=0. 
                ,CBFixedLimitHigh=1. 
                # FWVB 
                ,pMeasure='Measure'  # colName                                                                                                                       
                ,pAttribute='Attrib' # colName 

                ,pXCor='pXCor_i'  # colName 
                ,pYCor='pYCor_i'  # colName 
             
                ,pSizeFactor=1. 
                                 
                ,pMeasureColorMap=plt.cm.autumn 
                ,pMeasureAlpha=0.9 
                ,pMeasureClip=False    

                ,pMCategory='MCategory' # colName                    
                ,pMCatTopTxt='Top'     
                ,pMCatMidTxt='Middle'             
                ,pMCatBotTxt='Bottom'    
                             
                ,limitTopColor='palegreen'
                ,limitTopAlpha=0.9 
                ,limitTopClip=False            

                ,limitMiddleColorMap=plt.cm.autumn 
                ,limitMiddleAlpha=0.9 
                ,limitMiddleClip=False  
                                                                        
                ,limitBottomColor='violet' 
                ,limitBottomAlpha=0.9 
                ,limitBottomClip=False                                                 
                ):
    """
    zeichnet Symbole auf gca()
    Größenskalierung mit pSizeFactor * pAttribute in Pts
    Farbe nach pMeasure und pMeasureColorMap      
    return:
            (pcN, vmin, vmax)
            pcN sind die mit pMeasureColorMap gezeichneten Symbole
            vmin/vmax sind die für die Farbskala verwendeten Extremalwerte
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try: 

        logger.debug("{:s}pAttribute={:s} pMeasure={:s}".format(logStr,pAttribute,pMeasure)) 
        logger.debug("{:s}pSizeFactor={:10.3f}".format(logStr,pSizeFactor)) 
        logger.debug("{:s}pMeasure3Classes={!s:s}".format(logStr,pMeasure3Classes)) 
 
        ax=plt.gca()
                     
        if pMeasure3Classes:

            pN_top=pDf[(pDf[pMCategory]==pMCatTopTxt)] 
            pN_mid=pDf[(pDf[pMCategory]==pMCatMidTxt)]     
            pN_bot=pDf[(pDf[pMCategory]==pMCatBotTxt)] 

            pN_top_Anz,col=pN_top.shape
            pN_mid_Anz,col=pN_mid.shape
            pN_bot_Anz,col=pN_bot.shape

            pcN_top=ax.scatter(    
                    pN_top[pXCor],pN_top[pYCor]                 
                ,s=pSizeFactor*pN_top[pAttribute]
                ,color=limitTopColor
                ,alpha=limitTopAlpha
                ,edgecolors='face'             
                ,clip_on=limitTopClip)        
            logger.debug("{:s}Anzahl mit fester Farbe Top gezeichneter Symbole={:d}".format(logStr,pN_top_Anz))                        

            if not CBFixedLimits:
                vmin=pN_mid[pMeasure].min()
                vmax=pN_mid[pMeasure].max()
            else:
                vmin=CBFixedLimitLow
                vmax=CBFixedLimitHigh

            pcN=ax.scatter(    
                    pN_mid[pXCor],pN_mid[pYCor]       
                ,s=pSizeFactor*pN_mid[pAttribute]
                # Farbskala
                ,cmap=limitMiddleColorMap
                # Normierung Farbe
                ,vmin=vmin
                ,vmax=vmax
                # Farbwert
                ,c=pN_mid[pMeasure] 
                ,alpha=limitMiddleAlpha
                ,edgecolors='face'
                ,clip_on=limitMiddleClip
                )
            logger.debug("{:s}Anzahl mit Farbskala gezeichneter Symbole={:d}".format(logStr,pN_mid_Anz))    

            pcN_bot=ax.scatter(    
                    pN_bot[pXCor],pN_bot[pYCor]                 
                ,s=pSizeFactor*pN_bot[pAttribute]
                ,color=limitBottomColor
                ,alpha=limitBottomAlpha
                ,edgecolors='face'             
                ,clip_on=limitBottomClip)              
            logger.debug("{:s}Anzahl mit fester Farbe Bot gezeichneter Symbole={:d}".format(logStr,pN_bot_Anz))     
                          
        else:

            pN_Anz,col=pDf.shape

            if not CBFixedLimits:
                vmin=pDf[pMeasure].min()
                vmax=pDf[pMeasure].max()
            else:
                vmin=CBFixedLimitLow
                vmax=CBFixedLimitHigh
                                         
            pcN=ax.scatter(    
                    pDf[pXCor],pDf[pYCor]       
                ,s=pSizeFactor*pDf[pAttribute]
                # Farbskala
                ,cmap=pMeasureColorMap
                # Normierung Farbe
                ,vmin=vmin
                ,vmax=vmax
                # Farbwert
                ,c=pDf[pMeasure] 
                ,alpha=pMeasureAlpha
                ,edgecolors='face'
                ,clip_on=pMeasureClip
                )            
            logger.debug("{:s}Anzahl mit Farbskala gezeichneter Symbole={:d}".format(logStr,pN_Anz))                           
        
        logger.debug("{:s}Farbskala vmin={:10.3f} Farbskala vmax={:10.3f}".format(logStr,vmin,vmax)) 
                                                                                          
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:       
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))            
        return (pcN, vmin, vmax)

def pltNetColorbar( 
                pc # die einzufaerbenden Objekte; werden für die Erzeugung der colorbar zwingend benoetigt   
                 
                # wird nur benötigt wenn CBFixedLimitLow/High _nicht gelten:
                #>...                     
                ,pDf=None # df            
                ,pMeasure='Measure'  # colName                 
                # pMeasure3Classes True: CBFixedLimitLow/High gelten; CBFixedLimits spielt keine Rolle
                # False: CBFixedLimitLow/High gelten wenn CBFixedLimits
                # sonst: pDf[pMeasure].min()/.max() sind die Limits 
                 #...<

                ,pMeasureInPerc=True # Measure wird interpretiert in Prozent [0-1] 
                ,pMeasure3Classes=True 

                # Ticks (TickLabels und TickValues)
                ,CBFixedLimits=False
                ,CBFixedLimitLow=0 
                ,CBFixedLimitHigh=1        
                
                # Label
                ,pMeasureUNIT='[]'
                ,pMeasureTYPE=''

                ,CBTicklabelsHPad=0.

                # Geometrie
                ,CBFraction=0.05  # fraction of original axes to use for colorbar
                ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
                ,CBLabelPad=0. # Label unmittelbar rechts neben der Colorbar
               
                ,CBAspect=10. # ratio of long to short dimension
                ,CBShrink=1. # Colorbar füllt dann y von ax ganz aus 
                ,CBAnchorHorizontal=0. # horizontaler Fußpunkt der colorbar in Plot-% von ax
                ,CBAnchorVertical=0. # vertikaler Fußpunkt der colorbar in Plot-% von ax       
                
                # Legend 3Classes
                ,pAttribute='Attrib' 
                ,pSizeFactor=1.

                ,pMCategory='MCategory'
                ,pMCatTopTxt='Top'
                ,pMCatMidTxt='Middle'
                ,pMCatBotTxt='Bottom'

                ,limitBottomColor='violet'                 
                ,limitTopColor='palegreen' 

                ,CBLe3cTopVPad=1+1*1/4                 
                ,CBLe3cMiddleVPad=.5                                                                         
                ,CBLe3cBottomVPad=0-1*1/4  
                                                                    
                ):
    """
    pltNetColorbarBar:
        erzeugt aus ax=gca() cax für die Colorbar
        zeichnet die Colorbar     
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try: 
        ax=plt.gca()
        pltNetColorbarBar(
                #
                 pc # PathCollection aus pltNetNodes                     
                #
                ,pDf=pDf                                                                                                       
                ,pMeasure=pMeasure 
                #
                ,pMeasureInPerc=pMeasureInPerc
                ,pMeasure3Classes=pMeasure3Classes         
                # Label                
                ,pMeasureUNIT=pMeasureUNIT
                ,pMeasureTYPE=pMeasureTYPE
                # Ticks (TickLabels und TickValues)
                ,CBFixedLimits=CBFixedLimits
                ,CBFixedLimitLow=CBFixedLimitLow
                ,CBFixedLimitHigh=CBFixedLimitHigh

                ,CBTicklabelsHPad=CBTicklabelsHPad

                # Geometrie
                ,CBFraction=CBFraction
                ,CBHpad=CBHpad              
                ,CBLabelPad=CBLabelPad                
                ,CBAspect=CBAspect 
                ,CBShrink=CBShrink 
                ,CBAnchorHorizontal=CBAnchorHorizontal 
                ,CBAnchorVertical=CBAnchorVertical                    
            )
        
        cax=plt.gca()
        
        TBAnchorVertical=1.                         
        if pMeasure3Classes:                                                                   
             bbTop, bbMid, bbBot  = pltNetColorbarLegend3Classes( 
                pDf

               ,CBShrink=CBShrink 
               ,CBAnchorHorizontal=CBAnchorHorizontal 
               ,CBAnchorVertical=CBAnchorVertical     
               
               ,pAttribute=pAttribute  
               ,pSizeFactor=pSizeFactor

               ,pMCategory=pMCategory
               ,pMCatTopTxt=pMCatTopTxt
               ,pMCatMidTxt=pMCatMidTxt
               ,pMCatBotTxt=pMCatBotTxt

               ,limitBottomColor=limitBottomColor                 
               ,limitTopColor=limitTopColor    
               
               ,CBLe3cTopVPad=CBLe3cTopVPad #1+1*1/4                 
               ,CBLe3cMiddleVPad=CBLe3cMiddleVPad #.5                                                                         
               ,CBLe3cBottomVPad=CBLe3cBottomVPad #0-1*1/4                                                                                                                     
             )
             TBAnchorVertical=bbTop.y1
                                                                                                                
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
        return (cax,TBAnchorVertical)

def pltNetColorbarBar( 
                pc # die einzufaerbenden Objekte; werden für die Erzeugung der colorbar zwingend benoetigt   
                 
                # wird nur benötigt wenn CBFixedLimitLow/High _nicht gelten:
                #>...                     
                ,pDf=None # df            
                ,pMeasure='Measure'  # colName   
                # pMeasure3Classes True: CBFixedLimitLow/High gelten; CBFixedLimits spielt keine Rolle
                # False: CBFixedLimitLow/High gelten wenn CBFixedLimits
                # sonst: pDf[pMeasure].min()/.max() sind die Limits 
                 #...<

                ,pMeasureInPerc=True # Measure wird interpretiert in Prozent [0-1] 
                ,pMeasure3Classes=True 
                
                # Label
                ,pMeasureUNIT='[]'
                ,pMeasureTYPE=''

                # Ticks (TickLabels und TickValues)
                ,CBFixedLimits=False
                ,CBFixedLimitLow=0 
                ,CBFixedLimitHigh=1        
                
                ,CBTicklabelsHPad=0        

                # Geometrie
                ,CBFraction=0.05  # fraction of original axes to use for colorbar
                ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
                ,CBLabelPad=0. # Label unmittelbar rechts neben der Colorbar               
                ,CBAspect=10. # ratio of long to short dimension
                ,CBShrink=1. # Colorbar füllt dann y von ax ganz aus 
                ,CBAnchorHorizontal=0. # horizontaler Fußpunkt der colorbar in Plot-% von ax
                ,CBAnchorVertical=0. # vertikaler Fußpunkt der colorbar in Plot-% von ax
                                           
                ):
    """
    erzeugt cax (Colorbar-Axes) aus ax (gca()) und positioniert darauf (gca() steht auf cax nach return)
        zeichnet die Colorbar 
        mit Ticks, TickLabels, Label          
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try: 
          
        ax=plt.gca()
        fig=plt.gcf()   

        # cax              
        cax,kw=make_axes(ax
                        ,location='right'
                        ,fraction=CBFraction # fraction of original axes to use for colorbar
                        ,pad=CBHpad # fraction of original axes between colorbar and new image axes
                        ,anchor=(CBAnchorHorizontal,CBAnchorVertical) # the anchor point of the colorbar axes
                        ,aspect=CBAspect # ratio of long to short dimension
                        ,shrink=CBShrink # fraction by which to shrink the colorbar
                        )         

        # colorbar
        colorBar=fig.colorbar(pc
                    ,cax=cax
                    ,**kw
                    )        

        # tick Values  
        if pMeasure3Classes:
            minCBtickValue=CBFixedLimitLow
            maxCBtickValue=CBFixedLimitHigh             
        else:
            if CBFixedLimits and isinstance(CBFixedLimitHigh,float) and isinstance(CBFixedLimitLow,float):
                minCBtickValue=CBFixedLimitLow
                maxCBtickValue=CBFixedLimitHigh                      
            else:
                minCBtickValue=pDf[pMeasure].min()
                maxCBtickValue=pDf[pMeasure].max()           
        colorBar.set_ticks([minCBtickValue,minCBtickValue+.5*(maxCBtickValue-minCBtickValue),maxCBtickValue])  

        # tick Labels
        if pMeasureInPerc:
            if pMeasure3Classes:
                minCBtickLabel=">{:3.0f}%".format(minCBtickValue*100)
                maxCBtickLabel="<{:3.0f}%".format(maxCBtickValue*100)                             
            else:
                minCBtickLabel="{:3.0f}%".format(minCBtickValue*100)
                maxCBtickLabel="{:3.0f}%".format(maxCBtickValue*100) 
        else:
            if pMeasure3Classes:
                minCBtickLabel=">{:6.2f}".format(minCBtickValue)
                maxCBtickLabel="<{:6.2f}".format(maxCBtickValue)    
            else:
                minCBtickLabel="{:6.2f}".format(minCBtickValue)
                maxCBtickLabel="{:6.2f}".format(maxCBtickValue)    
        logger.debug("{:s}minCBtickLabel={:s} maxCBtickLabel={:s}".format(logStr,minCBtickLabel,maxCBtickLabel))    
        colorBar.set_ticklabels([minCBtickLabel,'',maxCBtickLabel])        
        colorBar.ax.yaxis.set_tick_params(pad=CBTicklabelsHPad)     
                         
        
        # Label
        if pMeasureInPerc:
                CBLabelText="{:s} in [%]".format(pMeasureTYPE)                                                                
        else:
                CBLabelText="{:s} in {:s}".format(pMeasureTYPE,pMeasureUNIT)
         
        colorBar.set_label(CBLabelText,labelpad=CBLabelPad)
                                                                                                                
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    

def pltNetColorbarLegend3Classes( 
                pDf

               ,CBShrink=1.
               ,CBAnchorHorizontal=0.
               ,CBAnchorVertical=0.

               ,pAttribute='Attrib' # colName 
               ,pSizeFactor=1.

               ,pMCategory='MCategory'
               ,pMCatTopTxt='Top'
               ,pMCatMidTxt='Middle'
               ,pMCatBotTxt='Bottom'

               ,limitBottomColor='violet' 
               ,limitTopColor='palegreen'           
                                  
               ,CBLe3cTopVPad=1+1*1/4                 
               ,CBLe3cMiddleVPad=.5                                                                         
               ,CBLe3cBottomVPad=0-1*1/4                          
                ):
    """
    zeichnet die Legende bei 3 Klassen     
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try: 
        pass

        cax=plt.gca()
        
        pDf_top=pDf[(pDf[pMCategory]==pMCatTopTxt)] 
        pDf_mid=pDf[(pDf[pMCategory]==pMCatMidTxt)]     
        pDf_bot=pDf[(pDf[pMCategory]==pMCatBotTxt)] 

        pDf_top_Anz,col=pDf_top.shape
        pDf_mid_Anz,col=pDf_mid.shape
        pDf_bot_Anz,col=pDf_bot.shape

        legendSymbolSize=pSizeFactor*pDf[pAttribute].max()
        
        if pDf_bot_Anz > 0:
            po=cax.scatter( CBAnchorHorizontal,CBLe3cBottomVPad                   
                            ,s=legendSymbolSize
                            ,c=limitBottomColor
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False
                            )
            # Text dazu
            o=po.findobj(match=None) 
            p=o[0]           
            bbBot=p.get_datalim(cax.transAxes)                               

        #    a=plt.annotate(limitBottomText                                     
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cBottomVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'  
        #                    ,color=limitBottomColor 
        #                    )
        #    # weiterer Text dazu
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_bot_Anz)                                
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cBottomVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'  
        #                    ,color=limitBottomColor 
        #                    )

        if pDf_top_Anz > 0:
            po=cax.scatter( CBAnchorHorizontal,CBLe3cTopVPad                          
                            ,s=legendSymbolSize
                            ,c=limitTopColor
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False                                 
                            )
            # Text dazu
            o=po.findobj(match=None) 
            p=o[0]           
            bbTop=p.get_datalim(cax.transAxes)      


        #        #Text dazu
        #    o=po.findobj(match=None) 
        #    p=o[0]           
        #    bb=p.get_datalim(cax.transAxes)     
        #    bbTop=bb      
        #    a=plt.annotate(limitTopText                                
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cTopVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'    
        #                    ,color=limitTopColor                            
        #                    )

        #        #weiterer Text dazu                  
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_top_Anz)                                       
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad++CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cTopVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'    
        #                    ,color=limitTopColor                            
        #                    )


        if pDf_mid_Anz > 0:           
            po=cax.scatter( CBAnchorHorizontal,CBLe3cMiddleVPad                                    
                            ,s=legendSymbolSize
                            ,c='lightgrey'
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False
                            ,visible=False # es erden nur die Koordinaten benoetigt
                            )
            # Text dazu
            o=po.findobj(match=None) 
            p=o[0]           
            bbMid=p.get_datalim(cax.transAxes)  


        #        #Text dazu
        #    o=po.findobj(match=None) 
        #    p=o[0]
        #    bb=p.get_datalim(cax.transAxes)
        #    a=plt.annotate(limitMiddleText                                    
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cMiddleVpad)                                                                                 
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'
        #                    ,color=limitMiddleColor   
        #                        ,visible=False
        #    )
        #        #weiterer Text dazu                
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_mid_Anz)                                              
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cMiddleVpad)                                                                                 
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'
        #                    ,color=limitMiddleColor   
        #                        ,visible=False
        #    )        
      
      
                                                                                                                
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
        return (bbTop, bbMid, bbBot)  

def pltNetTitleblock( 
              TBAnchorVertical=1.
             ,TBHSpace=0.4 
             ,Projekt='Projekt' 
             ,Planer='Planer' 
             ,Inst='Inst' 
             ,Model='M: ...'   
             ,Result='E: ...'    
             ,Times='TRef: ... T: ...'                                       
                ):
    """
    zeichnet das Schriftfeld      
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try: 
        cax=plt.gca()
            
        a=plt.annotate(Projekt, xy=(0.-1*TBHSpace,TBAnchorVertical)
                        ,family='monospace'
                        ,size='smaller'                    
                        ,xycoords=cax.transAxes 
                        ,rotation='vertical'
                        ,va='bottom'
                        ,ha='left'
        )
       

        a=plt.annotate(Planer, xy=(0.+0*TBHSpace,TBAnchorVertical)
                        ,family='monospace'
                        ,size='smaller'                  
                        ,xycoords=cax.transAxes 
                        ,rotation='vertical'
                        ,va='bottom'
                        ,ha='left'   
        )

        a=plt.annotate(Inst, xy=(0.+1*TBHSpace,TBAnchorVertical)
                        ,family='monospace'
                        ,size='smaller'                   
                        ,xycoords=cax.transAxes 
                        ,rotation='vertical'
                        ,va='bottom'
                        ,ha='left'   
        )        

        a=plt.annotate(Model, xy=(0.+2*TBHSpace,TBAnchorVertical)
                        ,family='monospace'
                        ,size='smaller'                  
                        ,xycoords=cax.transAxes 
                        ,rotation='vertical'
                        ,va='bottom'
                        ,ha='left'   
        )  
        
        a=plt.annotate(Result, xy=(0.+3*TBHSpace,TBAnchorVertical)
                        ,family='monospace'
                        ,size='smaller'                   
                        ,xycoords=cax.transAxes 
                        ,rotation='vertical'
                        ,va='bottom'
                        ,ha='left'   
        )        
        
        a=plt.annotate(Times, xy=(0.+4*TBHSpace,TBAnchorVertical)
                        ,family='monospace'
                        ,size='smaller'                  
                        ,xycoords=cax.transAxes 
                        ,rotation='vertical'
                        ,va='bottom'
                        ,ha='left'   
        )                              
                                                                                                                      
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

def pltNetPipes(
                pDf
               ,pAttribute='DI'  # Line
               ,pMeasure='Measure'  # Marker

               ,pClip=False
               ,pAttributeLs='-'  
               ,pMeasureMarker='.' 

               ,pAttríbuteColorMap=plt.cm.binary    
               ,pAttríbuteColorMapUsageStart=1./3                           
               ,pAttributeSizeFactor=1. # in diesem Fall ist die Linienbreite in Pts = dem pAttribute-Wert         

               ,pMeasureColorMap=plt.cm.binary    
               ,pMeasureColorMapUsageStart=1./3
               ,pMeasureSizeFactor=1. # in diesem Fall ist die Symbolgröße in Pts = dem pMeasure-Wert                                                                          
               ):
    """
    plottet Lines mit Marker auf gca()
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try: 
        ax=plt.gca()

        minLine=pDf[pAttribute].min()
        maxLine=pDf[pAttribute].max()
        logger.debug("{:s}minLine (Attribute): {:6.2f}".format(logStr,minLine))
        logger.debug("{:s}maxLine (Attribute): {:6.2f}".format(logStr,maxLine))
        normLine=colors.Normalize(minLine,maxLine)
        usageLineValue=minLine+pAttríbuteColorMapUsageStart*(maxLine-minLine)
        usageLineColor=pAttríbuteColorMap(normLine(usageLineValue)) 

        minMarker=pDf[pMeasure].min()
        maxMarker=pDf[pMeasure].max()
        normMarker=colors.Normalize(minMarker,maxMarker)
        usageMarkerValue=minMarker+pMeasureColorMapUsageStart*(maxMarker-minMarker)
        usageMarkerColor=pMeasureColorMap(normMarker(usageMarkerValue)) 

        for xs,ys,vLine,vMarker in zip(pDf['pWAYPXCors'],pDf['pWAYPYCors'],pDf[pAttribute],pDf[pMeasure]):        
            if vLine >= usageLineValue:
                colorLine=pAttríbuteColorMap(normLine(vLine)) 
            else:
                colorLine=usageLineColor
            if vMarker >= usageMarkerValue:
                colorMarker=pMeasureColorMap(normMarker(vMarker))
            else:
                colorMarker=usageMarkerColor

            colorMarker=pMeasureColorMap(normMarker(vMarker))
            pcLines=ax.plot(xs,ys
                            ,color=colorLine
                            ,linewidth=pAttributeSizeFactor*vLine 
                            ,ls=pAttributeLs
                            ,marker=pMeasureMarker
                            ,mfc=colorMarker 
                            ,mec=colorMarker  
                            ,mfcalt=colorMarker  
                            ,mew=0
                            ,ms=pMeasureSizeFactor*vMarker                                                    
                            ,markevery=[0,len(xs)-1]
                            ,aa=True
                            ,clip_on=pClip
                           )            
            #logger.debug("{:s}pcLines: {!s:s}".format(logStr,pcLines))
      
                                                                                          
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:       
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                   

def pltNetFigAx(
                pDf
               ,pXCor_i='pXCor_i'  # colName 
               ,pYCor_i='pYCor_i'  # colName          
               ,pXCor_k='pXCor_k'  # colName 
               ,pYCor_k='pYCor_k'  # colName   

               ,CBFraction=0.05  # fraction of original axes to use for colorbar
               ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes            

               # Plot
               ,pltTitle='pltNetFigAx' # plt.title not f.suptitle
               ,figFrameon=True # set whether the figure frame (background) is displayed or invisible
               #,figLinewidth=1.
               ,figEdgecolor='black' # set the edge color of the Figure rectangle
               ,figFacecolor='white' # set the face color of the Figure rectangle
                                                                                           
               ):
    """
    Fig- und Ax-Parametrierungen
    ax wird erzeugt
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    try:         
        dx=max(pDf[pXCor_i].max(),pDf[pXCor_k].max())
        dy=max(pDf[pYCor_i].max(),pDf[pYCor_k].max())

        # erf. Verhältnis bei verzerrungsfreier Darstellung
        dydx=dy/dx 

        if(dydx>=1):
            dxInch=DINA4_x # Hochformat
        else:
            dxInch=DINA4_y # Querformat
    
        figwidth=dxInch

        #verzerrungsfrei: Blattkoordinatenverhaeltnis = Weltkoordinatenverhaeltnis
        factor=1-(CBFraction+CBHpad)
        # verzerrungsfreie Darstellung sicherstellen
        figheight=figwidth*dydx*factor

        # Weltkoordinatenbereich
        xlimLeft=0
        ylimBottom=0
        xlimRight=dx
        ylimTop=dy

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
                                                                                          
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:       
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))               



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
                   # TIME ----------------------------------------------------------------------------------------
                   ,timeDeltaToRef=pd.to_timedelta('0 seconds') # Referenzzeit als TIMEDELTA zu Szenariumbeginn 
                   ,timeDeltaToT=None # Zeit als TIMEDELTA zu Szenariumbeginn                    
                  
                   # FILTER  (haben ggf. Einfluss auf die Abmessungen der Darstellung) ---------------------------
                   ,KVRisIn=[2]
                   ,CONT_IDisIn=[1001]                  
             
                   # SELECT (haben KEINEN Einfluss auf die Abmessungen der Darstellung) --------------------------                   
                   ,quantil_pROHRAttributeHigh=1. # die 25% gößten hier 'DI' also
                   ,quantil_pROHRAttributeLow=.75 
                   ,quantil_pFWVBAttributeHigh=1. # alle 'W0LFK' also
                   ,quantil_pFWVBAttributeLow=0. 
                   
                   # ALLG ----------------------------------------------------------------------------------------
                   ,pFWVBMeasureInRefPerc=True # Measure wird verarbeitet in Prozent T zu Ref 
                   ,pFWVBMeasure3Classes=False # Measure wird dargestellt in 3 Klassen

                   ,pFWVBMeasureCBFixedLimits=False
                   ,pFWVBMeasureCBFixedLimitLow=.10 
                   ,pFWVBMeasureCBFixedLimitHigh=.95 

                   # FWVB ----------------------------------------------------------------------------------------
                   ,pFWVBAttribute='W0LFK' 
                   ,pFWVBAttributeAsc=False # False: je größer Attribute, desto niedriger die z-Order ("kleine" auf "großen")
                   ,pFWVBMeasure='FWVB~*~*~*~W' 

                   ,pFWVBGCategory=['BLNZ1u5u7'] # ['Süd','Nord','Innenstadt','Nord PWS','NordOst BHW','Ost HWV','Ost PWF/PSE','Nord Rest'] # NAMEn von WBLZ
                   ,pFWVBGCategoryXStart=.1
                   ,pFWVBGCategoryYStart=.9
                   ,pFWVBGCategoryYSpace=-.01

                   ,pFWVBAttributeRefSize=10                   
                   
                   ,pFWVBMeasureColorMap=plt.cm.autumn 
                   ,pFWVBMeasureAlpha=0.9 
                   ,pFWVBMeasureClip=False    
                
                   ,limitTopColor='palegreen'
                   ,limitTopAlpha=0.9 
                   ,limitTopClip=False            
                   ,limitTopText='Top' 
                                                    
                   ,limitBottomColor='violet'
                   ,limitBottomAlpha=0.9 
                   ,limitBottomClip=False    
                   ,limitBottomText='Bottom' 

                   ,limitMiddleColorMap=plt.cm.autumn 
                   ,limitMiddleAlpha=0.9 
                   ,limitMiddleClip=False    
                   ,limitMiddleText='Middle'     
                   
                   # CB   -----------------------------------------------------------------------------------------
                   ,CBFraction=0.05  # fraction of original axes to use for colorbar
                   ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
                   ,CBLabelPad=-50         
                   ,CBTicklabelsHPad=0.      
                   ,CBAspect=10. # ratio of long to short dimension
                   ,CBShrink=0.3 # fraction by which to shrink the colorbar
                   ,CBAnchorHorizontal=0. # horizontaler Fußpunkt der colorbar in Plot-%
                   ,CBAnchorVertical=0.2 # vertikaler Fußpunkt der colorbar in Plot-%                                

                   # ROHR -----------------------------------------------------------------------------------------
                   ,pROHRAttribute='DI'              
                   ,pROHRAttributeAsc=False # False: je größer Attribute, desto niedriger die z-Order ("kleine" auf "großen")                                      
                   ,pROHRMeasure='ROHR~*~*~*~QMAV' 
                   ,pROHRMeasureAbs=True #  Measure wird verarbeitet als Absolutwert 

                   ,pROHRClip=False
                   ,pROHRAttributeLs='-'
                   ,pROHRMeasureMarker='.'              
                                            
                   ,pROHRAttributeColorMap=plt.cm.binary   
                   ,pROHRAttríbuteColorMapUsageStart=1./3        
                   ,pROHRAttributeRefSize=1.0 
                                                                                                                                                              
                   ,pROHRMeasureColorMap=plt.cm.cool 
                   ,pROHRMeasureColorMapUsageStart=0.        
                   ,pROHRMeasureRefSize=1.0 
                                                   
                   # CBLegend (3Classes) --------------------------------------------------------------------------
                   # Position der Repräsentantensymbole             
                   ,CBLe3cTopVPad=1+1*1/4
                   # "1"
                   ,CBLe3cMiddleVPad=.5                                                                         
                   ,CBLe3cBottomVPad=0-1*1/4  
                 
                   # TB --------------------------------------------------------------------------------------------
                   ,TBVSpace=0.2 
                   ,TBHSpace=0.4 

                   # FIG -------------------------------------------------------------------------------------------                  
                   ,pltTitle='pltNetDHUS' 
                   ,figFrameon=True                    
                   ,figEdgecolor='black' 
                   ,figFacecolor='white' 
                   
                  


                 
                 
                   ,pFWVBVICsDf=None # df with VICs; Kundenname, Knotenname (NAME_I)
                
                   
                   # Attribute (Sachdatum) & Measure (Ergebnis)
                   # ROHR
              
                 
                   # Attribute wirkt auf die Linie (Breite, Farbe)
                   # Measure wirkt auf die Marker (Größe, Farbe)
             
                 


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
                pFWVBMeasureValuePerc=[float(m)/float(mRef) if float(mRef) >0 else 1 for m,mRef in zip(pFWVBMeasureValue,pFWVBMeasureValueRef)]
                pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValuePerc)) #!
            else:
                pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValue)) #!

            # Sachdaten annotieren mit Spalte MCategory           
            if  not pFWVBMeasureCBFixedLimits and pFWVBMeasure3Classes:
                logger.error("Bei 3-Klassendarstellung Wahr muss FixedLimits Wahr sein.")

            pFWVBCat=[]
            for index, row in pFWVB.iterrows():
                if row.Measure >= pFWVBMeasureCBFixedLimitHigh:
                    pFWVBCat.append(limitTopText)
                elif row.Measure <= pFWVBMeasureCBFixedLimitLow:
                    pFWVBCat.append(limitBottomText)
                else:
                    pFWVBCat.append(limitMiddleText)
            pFWVB=pFWVB.assign(MCategory=pd.Series(pFWVBCat)) 

            # Sachdaten annotieren mit Spalte GCategory      
            if isinstance(pFWVBGCategory,list):         
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
            else:
                pFWVB=pFWVB.assign(GCategory=pd.Series()) 

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
           
            # ############################################################
            # ============================================================
            # Plotten
            # ============================================================
            # ############################################################
            pltNetFigAx(
                pDf=pltROHR
               ,pXCor_i='pXCor_i'  # colName 
               ,pYCor_i='pYCor_i'  # colName          
               ,pXCor_k='pXCor_k'  # colName 
               ,pYCor_k='pYCor_k'  # colName   

               ,CBFraction=CBFraction 
               ,CBHpad=CBHpad              

               ,pltTitle=pltTitle
               ,figFrameon=figFrameon
               #,figLinewidth=1.
               ,figEdgecolor=figEdgecolor 
               ,figFacecolor=figFacecolor                                                                                            
            )
            fig = plt.gcf()  
            ax=plt.gca()

            pFWVBrefSizeValue=pltFWVB[pFWVBAttribute].std()
            if pFWVBrefSizeValue < 1:
                pFWVBrefSizeValue=pltFWVB[pFWVBAttribute].mean()
            logger.debug("{:s}pFWVBrefSizeValue (Attributwert): {:6.2f}".format(logStr,pFWVBrefSizeValue)) 
            pFWVBSizeFactor=pFWVBAttributeRefSize/pFWVBrefSizeValue
            
            pcFWVB, CBLimitLow, CBLimitHigh = pltNetNodes(
                # ALLG
                 pDf=pltFWVB   
                ,pMeasure3Classes=pFWVBMeasure3Classes 

                ,CBFixedLimits=pFWVBMeasureCBFixedLimits
                ,CBFixedLimitLow=pFWVBMeasureCBFixedLimitLow 
                ,CBFixedLimitHigh=pFWVBMeasureCBFixedLimitHigh 
                # FWVB
                ,pMeasure='Measure' 
                ,pAttribute=pFWVBAttribute 
                                             
                ,pSizeFactor=pFWVBSizeFactor
                   
                ,pMeasureColorMap=pFWVBMeasureColorMap 
                ,pMeasureAlpha=pFWVBMeasureAlpha
                ,pMeasureClip=pFWVBMeasureClip    
   
                ,pMCategory='MCategory' 
                ,pMCatTopTxt='Top'     
                ,pMCatBotTxt='Bottom'    
                ,pMCatMidTxt='Middle'             
               
                ,limitTopColor=limitTopColor
                ,limitTopAlpha=limitTopAlpha
                ,limitTopClip=limitTopClip   
                                                                        
                ,limitBottomColor=limitBottomColor 
                ,limitBottomAlpha=limitBottomAlpha
                ,limitBottomClip=limitBottomClip
                  
                ,limitMiddleColorMap=limitMiddleColorMap
                ,limitMiddleAlpha=limitMiddleAlpha
                ,limitMiddleClip=limitMiddleClip
            )

            cax,TBAnchorVertical=pltNetColorbar(
                # ALLG
                 pc=pcFWVB # PathCollection aus pltNetNodes                                        
                ,pDf=pltFWVB 
                ,pMeasureInPerc=pFWVBMeasureInRefPerc 
                ,pMeasure3Classes=pFWVBMeasure3Classes      
                
                # Ticks (TickLabels und TickValues)
                ,CBFixedLimits=pFWVBMeasureCBFixedLimits
                ,CBFixedLimitLow=pFWVBMeasureCBFixedLimitLow
                ,CBFixedLimitHigh=pFWVBMeasureCBFixedLimitHigh                       

                #
                ,pMeasure='Measure'           
         
                # Label
                ,pMeasureUNIT=pFWVBMeasureUNIT
                ,pMeasureTYPE=pFWVBMeasureATTRTYPE

                ,CBTicklabelsHPad=CBTicklabelsHPad

                # Geometrie
                ,CBFraction=CBFraction  
                ,CBHpad=CBHpad          
                ,CBLabelPad=CBLabelPad              
                ,CBAspect=CBAspect 
                ,CBShrink=CBShrink 
                ,CBAnchorHorizontal=CBAnchorHorizontal 
                ,CBAnchorVertical=CBAnchorVertical 

                # Legend 3 Classes
                ,pAttribute=pFWVBAttribute  
                ,pSizeFactor=pFWVBSizeFactor                   
                ,pMCategory='MCategory' 
                ,pMCatTopTxt=limitTopText     
                ,pMCatBotTxt=limitBottomText       
                ,pMCatMidTxt=limitMiddleText     

                ,limitBottomColor=limitBottomColor 
                ,limitTopColor=limitTopColor 

                ,CBLe3cTopVPad=CBLe3cTopVPad #1+1*1/4                 
                ,CBLe3cMiddleVPad=CBLe3cMiddleVPad #.5                                                                         
                ,CBLe3cBottomVPad=CBLe3cBottomVPad #0-1*1/4  


            )

            fig.sca(ax)
            pltNetPipes(
                pltROHR
               ,pAttribute=pROHRAttribute  # Line
               ,pMeasure='Measure'  # Marker

               ,pClip=pROHRClip
               ,pAttributeLs=pROHRAttributeLs 
               ,pMeasureMarker=pROHRMeasureMarker

               ,pAttríbuteColorMap=pROHRAttributeColorMap 
               ,pAttríbuteColorMapUsageStart=pROHRAttríbuteColorMapUsageStart 
               ,pAttributeSizeFactor=pROHRAttributeRefSize/pltROHR[pROHRAttribute].max()              

               ,pMeasureColorMap=pROHRMeasureColorMap 
               ,pMeasureColorMapUsageStart=pROHRMeasureColorMapUsageStart             
               ,pMeasureSizeFactor=pROHRMeasureRefSize/pltROHR['Measure'].max()        
            )

            fig.sca(cax)
            xmFileName,ext = os.path.splitext(os.path.basename(self.xm.xmlFile))
            (wDir,modelDir,modelName)=self.xm.getWDirModelDirModelName()
            pltNetTitleblock( 
              TBAnchorVertical=TBAnchorVertical+TBVSpace
             ,TBHSpace=TBHSpace  
             ,Projekt=self.xm.dataFrames['MODELL']['PROJEKT'].iloc[0]
             ,Planer=self.xm.dataFrames['MODELL']['PLANER'].iloc[0]
             ,Inst=self.xm.dataFrames['MODELL']['INST'].iloc[0]       
             ,Model="M: {:s}".format(xmFileName)   
             ,Result="E: {:s}".format(os.path.join(os.path.basename(wDir),os.path.join(modelDir,modelName))+'.MX1')   
             ,Times="TRef: {!s:s} T: {!s:s}".format(timeDeltaToRef,timeDeltaToT).replace('days','Tage')             
            )

                                               
            # ---------------------------------------------------------------------
            # NumAnz 
            fig.sca(ax)


            patWBLZ='WBLZ~[\S ]+~\S*~\S+~\S+'
            patWBLZ_WVB='WBLZ~[\S ]+~\S*~\S+~WVB' # Verbrauch
            patWBLZ_WES='WBLZ~[\S ]+~\S*~\S+~WES' # Einspeisung

            patWBLZ_WVB_GES='WBLZ~WärmeblnzGes~\S*~\S+~WVB' # Verbrauch Gesamt
            #patWBLZ_WES_GES='WBLZ~WärmeblnzGes+~\S*~\S+~WES' # Einspeisung Gesamt

            sCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.contains(patWBLZ_WVB_GES)].iloc[0]
            s=self.mx.df[sCh.Sir3sID]
                
            v=s[timeT]                
            v0=s[timeRef]
            vp=v/v0*100               
                                                              
            x,y=pFWVBGCategoryXStart,pFWVBGCategoryYStart            

            txt="{:12s}: {:6.1f} {:4s} {:6.1f}%".format(sCh.NAME1,v,sCh.UNIT,vp)
            a=plt.annotate(txt
                            ,xy=(x,y)
                            ,family='monospace'
                            ,size='smaller'                   
                            ,xycoords=ax.transAxes #'data'  
                            ,rotation='horizontal'
                            ,va='bottom'
                            ,ha='left'   
                            ,clip_on=False
            )     

            vWBLZ=self.xm.dataFrames['vWBLZ']
            df=pd.merge(vNRCV_Mx1,vWBLZ,left_on='fkOBJTYPE',right_on='pk')
            df=df[['Sir3sID','NAME','IDIM']].drop_duplicates()
            # Sir3sID NAME
            # alle NumAnz die definiert sind und WVB einer Wärmebilanz referenzieren
            idx=0
            for NAME in pFWVBGCategory: # verlangte Wärmebilanzen       
                try:         
                    row=df[df['NAME']==NAME].iloc[0]
                except:
                    logger.debug("{:s} verlangte Wärmebilanz (aus pFWVBGCategory)={:s} nicht definiert.".format(logStr,NAME))    
                    continue

                sCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(row.Sir3sID)].iloc[0]
                s=self.mx.df[row.Sir3sID]
                
                v=s[timeT]                
                v0=s[timeRef]
                vp=v/v0*100               
                                                              
                x,y=pFWVBGCategoryXStart,pFWVBGCategoryYStart+pFWVBGCategoryYSpace*(idx+1)
                idx=idx+1

                txt="{:12s}: {:6.1f} {:4s} {:6.1f}%".format(sCh.NAME1,v,sCh.UNIT,vp)
                a=plt.annotate(txt
                              ,xy=(x,y)
                              ,family='monospace'
                              ,size='smaller'                   
                              ,xycoords=ax.transAxes #'data'  
                              ,rotation='horizontal'
                              ,va='bottom'
                              ,ha='left'   
                              ,clip_on=False
                )     
                   
               


            ## ---------------------------------------------------------------------
            ## VICs
            #if isinstance(pFWVBVICsDf,pd.core.frame.DataFrame):
            #    fig.sca(ax)
            #    xStart=9000.
            #    yStart=1000.
            #    fontsize=8
            #    distance=50
            #    idx=0
            #    for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():      
            #            kunde=row.VIC                         
            #            a=plt.annotate("{:s}".format(kunde), xy=(xStart,yStart+fontsize*distance*idx), xycoords='data'                              
            #                        ,fontsize=fontsize    
            #                        ,va='bottom'
            #                        ,ha='left' 
            #                    ,clip_on=False
            #                        )
            #            idx=idx+1

            #    idx=0
            #    if pFWVBMeasureInRefPerc:
            #        unit='%'
            #    else:
            #        unit=pFWVBMeasureUNIT
            #    for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():
            #            v=pFWVB[pMeasure].loc[index]
            #            a=plt.annotate("{:6.2f} {:s}".format(v*100,unit), xy=(xStart+6000,yStart+fontsize*distance*idx), xycoords='data'                             
            #                        ,fontsize=fontsize    
            #                        ,va='bottom'
            #                        ,ha='left' 
            #                    ,clip_on=False
            #                            )
            #            idx=idx+1  
                                                              
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
