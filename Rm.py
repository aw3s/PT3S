"""
>>> # ---
>>> # SETUP
>>> # ---
>>> import os
>>> try:
...   path = os.path.dirname(__file__)
... except NameError:
...   path = '.'
...   import PT3S
...   import Mx
...   import Xm
...   from Rm import Rm
>>> import logging
>>> logger = logging.getLogger('PT3S.Rm')  
>>> import pandas as pd
>>> import matplotlib.pyplot as plt
>>> #
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
>>> pFWVB=rm.pltNetDHUS(timeDeltaToT=timeDeltaToT,pFWVBMeasure3Classes=True,pFWVBMeasureCBFixedLimits=True)
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> if os.path.exists(mx.h5FileVecs):                        
...   os.remove(mx.h5FileVecs)
>>> if os.path.exists(plotFileName):                        
...   pass #os.remove(plotFileName)
"""
import os
import sys
import logging


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

# ---
# --- main Imports
# ---
import argparse
import unittest
import doctest

DINA4_x=8.2677165354
DINA4_y=11.6929133858

class RmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

from matplotlib import markers
from matplotlib.path import Path

def align_marker(marker, halign='center', valign='middle',):
    """
    create markers with specified alignment.

    Parameters
    ----------

    marker : a valid marker specification.
      See mpl.markers

    halign : string, float {'left', 'center', 'right'}
      Specifies the horizontal alignment of the marker. *float* values
      specify the alignment in units of the markersize/2 (0 is 'center',
      -1 is 'right', 1 is 'left').

    valign : string, float {'top', 'middle', 'bottom'}
      Specifies the vertical alignment of the marker. *float* values
      specify the alignment in units of the markersize/2 (0 is 'middle',
      -1 is 'top', 1 is 'bottom').

    Returns
    -------

    marker_array : numpy.ndarray
      A Nx2 array that specifies the marker path relative to the
      plot target point at (0, 0).

    Notes
    -----
    The mark_array can be passed directly to ax.plot and ax.scatter, e.g.::

        ax.plot(1, 1, marker=align_marker('>', 'left'))

    """

    if isinstance(halign,str):
        halign = {'right': -1.,
                  'middle': 0.,
                  'center': 0.,
                  'left': 1.,
                  }[halign]

    if isinstance(valign,str):
        valign = {'top': -1.,
                  'middle': 0.,
                  'center': 0.,
                  'bottom': 1.,
                  }[valign]

    # Define the base marker
    bm = markers.MarkerStyle(marker)

    # Get the marker path and apply the marker transform to get the
    # actual marker vertices (they should all be in a unit-square
    # centered at (0, 0))
    m_arr = bm.get_path().transformed(bm.get_transform()).vertices

    # Shift the marker vertices for the specified alignment.
    m_arr[:, 0] += halign / 2
    m_arr[:, 1] += valign / 2

    return Path(m_arr, bm.get_path().codes)


def pltNetNodes( 
                # ALLG
                 pDf 
                ,pMeasure3Classes=True 

                ,CBFixedLimits=True
                ,CBFixedLimitLow=0. 
                ,CBFixedLimitHigh=1. 
                
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
                             
                ,pMCatTopColor='palegreen'
                ,pMCatTopAlpha=0.9 
                ,pMCatTopClip=False            

                ,pMCatMiddleColorMap=plt.cm.autumn 
                ,pMCatMiddleAlpha=0.9 
                ,pMCatMiddleClip=False  
                                                                        
                ,pMCatBottomColor='violet' 
                ,pMCatBottomAlpha=0.9 
                ,pMCatBottomClip=False                                                 
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
                ,color=pMCatTopColor
                ,alpha=pMCatTopAlpha
                ,edgecolors='face'             
                ,clip_on=pMCatTopClip)        
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
                ,cmap=pMCatMiddleColorMap
                # Normierung Farbe
                ,vmin=vmin
                ,vmax=vmax
                # Farbwert
                ,c=pN_mid[pMeasure] 
                ,alpha=pMCatMiddleAlpha
                ,edgecolors='face'
                ,clip_on=pMCatMiddleClip
                )
            logger.debug("{:s}Anzahl mit Farbskala gezeichneter Symbole={:d}".format(logStr,pN_mid_Anz))    

            pcN_bot=ax.scatter(    
                    pN_bot[pXCor],pN_bot[pYCor]                 
                ,s=pSizeFactor*pN_bot[pAttribute]
                ,color=pMCatBottomColor
                ,alpha=pMCatBottomAlpha
                ,edgecolors='face'             
                ,clip_on=pMCatBottomClip)              
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



                # Geometrie
                ,CBFraction=0.05  # fraction of original axes to use for colorbar
                ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
                ,CBLabelPad=0. # Label unmittelbar rechts neben der Colorbar
                ,CBTicklabelsHPad=0.
               
                ,CBAspect=10. # ratio of long to short dimension
                ,CBShrink=1. # Colorbar füllt dann y von ax ganz aus 
                ,CBAnchorHorizontal=0. # horizontaler Fußpunkt der colorbar in Plot-% von ax
                ,CBAnchorVertical=0. # vertikaler Fußpunkt der colorbar in Plot-% von ax       
                
                # Legend 3Classes
                ,pAttribute='Attrib' 
                #,pSizeFactor=1.

                ,pMCategory='MCategory'
                ,pMCatTopTxt='Top'
                ,pMCatMidTxt='Middle'
                ,pMCatBotTxt='Bottom'

                ,pMCatBottomColor='violet'                 
                ,pMCatTopColor='palegreen' 

                ,CBLe3cTopVPad=1+1*1/4                 
                ,CBLe3cMiddleVPad=.5                                                                         
                ,CBLe3cBottomVPad=0-1*1/4  

                ,CBLe3cSySize=1./10. 
                ,CBLe3cSyType='o' 
                                                                    
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



                # Geometrie
                ,CBFraction=CBFraction
                ,CBHpad=CBHpad              
                ,CBLabelPad=CBLabelPad  
                ,CBTicklabelsHPad=CBTicklabelsHPad                              
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
               #,pSizeFactor=pSizeFactor

               ,pMCategory=pMCategory
               ,pMCatTopTxt=pMCatTopTxt
               ,pMCatMidTxt=pMCatMidTxt
               ,pMCatBotTxt=pMCatBotTxt

               ,pMCatBottomColor=pMCatBottomColor                 
               ,pMCatTopColor=pMCatTopColor    
               
               ,CBLe3cTopVPad=CBLe3cTopVPad #1+1*1/4                 
               ,CBLe3cMiddleVPad=CBLe3cMiddleVPad #.5                                                                         
               ,CBLe3cBottomVPad=CBLe3cBottomVPad #0-1*1/4        
               
               ,CBLe3cSySize=CBLe3cSySize
               ,CBLe3cSyType=CBLe3cSyType
               
                                                                                                                            
             )
             if bbTop != None:
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
                
                # Geometrie
                ,CBFraction=0.05  # fraction of original axes to use for colorbar
                ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
                ,CBLabelPad=0. # Label unmittelbar rechts neben der Colorbar        
                ,CBTicklabelsHPad=0                               
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
             #  ,pSizeFactor=1.

               ,pMCategory='MCategory'
               ,pMCatTopTxt='Top'
               ,pMCatMidTxt='Middle'
               ,pMCatBotTxt='Bottom'

               ,pMCatBottomColor='violet' 
               ,pMCatTopColor='palegreen'           
                                  
               ,CBLe3cTopVPad=1+1*1/4                 
               ,CBLe3cMiddleVPad=.5                                                                         
               ,CBLe3cBottomVPad=0-1*1/4          
               
               ,CBLe3cSySize=1./10. 
               ,CBLe3cSyType='o'                               
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

        logger.debug("{:s} pDf_bot_Anz={:d}  pDf_mid_Anz={:d} pDf_top_Anz={:d}".format(logStr,pDf_bot_Anz,pDf_mid_Anz,pDf_top_Anz))

        logger.debug("{:s} pDf[pAttribute].max()={:10.3f}".format(logStr,pDf[pAttribute].max()))
        #legendSymbolSize=pSizeFactor*pDf[pAttribute].max()

        legendSymbolSize=CBLe3cSySize

        logger.debug("{:s} legendSymbolSize={:10.3f} CBLe3cSyType={:s}".format(logStr,legendSymbolSize,CBLe3cSyType))
        
        bbBot=None
        bbMid=None
        bbTop=None

        #print(dir(cax))
        #print(dir(cax.transData))
        #print(cax.get_xlim()) #   (0.0, 1.0)
        #print(cax.get_ylim()) #   (0.0, 1.0)

        if pDf_bot_Anz >= 0:
            po=cax.scatter( CBAnchorHorizontal,CBLe3cBottomVPad                   
                            ,s=legendSymbolSize
                            ,c=pMCatBottomColor
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False
                            ,marker=align_marker(CBLe3cSyType, halign='left')                                     
                            )
            # Text dazu
            o=po.findobj(match=None) 
            p=o[0]           
            bbBot=p.get_datalim(cax.transAxes)      
            logger.debug("{:s} bbBot={!s:s}".format(logStr,bbBot))                         

        #    a=plt.annotate(pMCatBottomText                                     
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cBottomVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'  
        #                    ,color=pMCatBottomColor 
        #                    )
        #    # weiterer Text dazu
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_bot_Anz)                                
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cBottomVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'  
        #                    ,color=pMCatBottomColor 
        #                    )

        if pDf_top_Anz >= 0:
            po=cax.scatter( CBAnchorHorizontal,CBLe3cTopVPad                          
                            ,s=legendSymbolSize
                            ,c=pMCatTopColor
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False     
                            ,marker=align_marker(CBLe3cSyType, halign='left')                                      
                            )
           
            o=po.findobj(match=None) 
            p=o[0]           
            bbTop=p.get_datalim(cax.transAxes)      


        #        #Text dazu
        #    o=po.findobj(match=None) 
        #    p=o[0]           
        #    bb=p.get_datalim(cax.transAxes)     
        #    bbTop=bb      
        #    a=plt.annotate(pMCatTopText                                
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cTopVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'    
        #                    ,color=pMCatTopColor                            
        #                    )

        #        #weiterer Text dazu                  
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_top_Anz)                                       
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad++CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cTopVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'    
        #                    ,color=pMCatTopColor                            
        #                    )


        if pDf_mid_Anz >= 0:           
            po=cax.scatter( CBAnchorHorizontal,CBLe3cMiddleVPad                                    
                            ,s=legendSymbolSize
                            ,c='lightgrey'
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False
                            ,visible=False # es erden nur die Koordinaten benoetigt
                            ,marker=align_marker(CBLe3cSyType, halign='left')             

                            )
           
            o=po.findobj(match=None) 
            p=o[0]           
            bbMid=p.get_datalim(cax.transAxes)  


        #        #Text dazu
        #    o=po.findobj(match=None) 
        #    p=o[0]
        #    bb=p.get_datalim(cax.transAxes)
        #    a=plt.annotate(pMCatMiddleText                                    
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cMiddleVpad)                                                                                 
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'
        #                    ,color=pMCatMiddleColor   
        #                        ,visible=False
        #    )
        #        #weiterer Text dazu                
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_mid_Anz)                                              
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cMiddleVpad)                                                                                 
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'
        #                    ,color=pMCatMiddleColor   
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
        return
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
        
        # plt.figure(dpi=, facecolor=, edgecolor=, linewidth=, frameon=True)
        fig = plt.gcf()  # This will return an existing figure if one is open, or it will make a new one if there is no active figure.

        # https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size

        # Size in pts:
        # the argument markersize in plot    denotes the markersize (i.e. diameter) in points
        # the argument s          in scatter denotes the markersize**2              in points^2
        # so a given plot-marker with markersize=x needs a scatter-marker with s=x**2 if the scatter-marker shall cover the same "area" in points^2
        # the "area" of the scatter-marker is proportional to the s param

        # What are points - pts:
        # the standard size of points in matplotlib is 72 ppi
        # 1 point is hence 1/72 inches (1 inch = 1 Zoll = 2.54 cm)
        # 1 point = 0.352777.... mm

        # points and pixels - px:
        # 1 point = dpi/ppi
        # the standard dpi in matplotlib is 100
        # a scatter-marker whos "area" covers always 10 pixel:
        # s=(10*ppi/dpi)**2       

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
    Args:
        xm: Xm.Xm Object

        mx: Mx.Mx Object
    """
    def __init__(self,xm=None,mx=None): 

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

    def pltNetDHUS(
        self
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
     

        # FWVB ----------------------------------------------------------------------------------------
     
      

        ,pFWVBGCategory=['BLNZ1u5u7'] # ['Süd','Nord','Innenstadt','Nord PWS','NordOst BHW','Ost HWV','Ost PWF/PSE','Nord Rest'] # NAMEn von WBLZ
        ,pFWVBGCategoryUnit='[kW]'
        ,pFWVBGCategoryXStart=.1
        ,pFWVBGCategoryYStart=.9
        ,pFWVBGCategoryYSpace=-.1

        
                   
    #    ,pFWVBMeasureColorMap=plt.cm.autumn 
    #    ,pFWVBMeasureAlpha=0.9 
    #    ,pFWVBMeasureClip=False    
                
    #    ,pMCatTopColor='palegreen'
    #    ,pMCatTopAlpha=0.9 
    #    ,pMCatTopClip=False            
    #    ,pMCatTopText='Top' 
                                                    
     #   ,pMCatBottomColor='violet'
     #   ,pMCatBottomAlpha=0.9 
     #   ,pMCatBottomClip=False    
     #   ,pMCatBottomText='Bottom' 

     #   ,pMCatMiddleColorMap=plt.cm.autumn 
     #   ,pMCatMiddleAlpha=0.9 
     #   ,pMCatMiddleClip=False    
     #   ,pMCatMiddleText='Middle'     
                   
        # CB   -----------------------------------------------------------------------------------------
      #  ,CBFraction=0.05  # fraction of original axes to use for colorbar
      #  ,CBHpad=0.0275 # 0.05 # fraction of original axes between colorbar and new image axes              
      #  ,CBLabelPad=-50         
      #  ,CBTicklabelsHPad=0.      
      #  ,CBAspect=10. # ratio of long to short dimension
      #  ,CBShrink=0.3 # fraction by which to shrink the colorbar
      #  ,CBAnchorHorizontal=0. # horizontaler Fußpunkt der colorbar in Plot-%
      #  ,CBAnchorVertical=0.2 # vertikaler Fußpunkt der colorbar in Plot-%                                

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
                                                   
     
                 
        # TB --------------------------------------------------------------------------------------------
        ,TBVSpace=0.2 
        ,TBHSpace=0.4 

        # FIG -------------------------------------------------------------------------------------------                  
        ,pltTitle='pltNetDHUS' 
        ,figFrameon=True                    
        ,figEdgecolor='black' 
        ,figFacecolor='white' 
                   
       

        ,**kwds
                                                   
        ): 
        """Plot Net: DistrictHeatingUnderSupply. 

        Keyword Args (optional):

            FWVB Attribute (Size)
                * pFWVBAttribute (default: 'W0LFK') 

                    * .astype(float) must be possible
                    * only >0 Values are displayed 

                * pFWVBAttributeAsc (default: False d.h. "kleine auf große")
                * pFWVBAttributeRefSize (default: 10**2)  (Sy-Area in pts^2 of Fwvb with RefSizeValue)
                      
                    * RefSizeValue is Attribute.std()
                    * or Attribute.mean() if Attribute.std() is < 1

            FWVB Measure (Color)
                * pFWVBMeasure (default: 'FWVB~*~*~*~W') 

                    * float() must be possible                

                * pFWVBMeasureInRefPerc (default: True d.h. Measure wird verarbeitet in Prozent T zu Ref) 

                    * 0-1
                    * if refValue is 0 than refPerc is set to 1 

                * pFWVBMeasureAlpha/Colormap/Clip

                * 3Classes

                    * pFWVBMeasure3Classes (default: False d.h. Measure wird nicht in 3 Klassen dargestellt)

                    * CatTexts (werden verwendet wenn 3Classes Wahr gesetzt ist)

                        * für CBLegend (3Classes) als _zusätzliche Beschriftung rechts
                        * als Texte für die Spalte MCategory in return pFWVB

                        * pMCatTopText
                        * pMCatMiddleText
                        * pMCatBottomText

                    * CatAttribs (werden verwendet wenn 3Classes Wahr gesetzt ist)

                        * für die Knotendarstellung                        

                        * pMCatTopAlpha/Color/Clip
                        * pMCatMidAlpha/Colormap/Clip
                        * pMCatBotAlpha/Color/Clip
                                   
                * CBFixedLimits 
                
                    * pFWVBMeasureCBFixedLimits (default: False d.h. Farbskala nach vorh. min./max. Wert)

                        * muss Wahr gesetzt sein, wenn 3Classes Wahr gesetzt ist
                        * in diesem Fall werden zwingend die nachfolgenden Limits für die Klasseneinteilung verwendet

                    * pFWVBMeasureCBFixedLimitLow (default: .10) 
                    * pFWVBMeasureCBFixedLimitHigh (default: .95) 

            CB
                * CBFraction: fraction of original axes to use for colorbar (default: 0.05)
                * CBHpad: fraction of original axes between colorbar and new image axes (default: 0.0275)               
                * CBLabelPad (default: -50)         
                * CBTicklabelsHPad (default: 0.)      
                * CBAspect: ratio of long to short dimension (default: 10.)
                * CBShrink: fraction by which to shrink the colorbar (default: .3)
                * CBAnchorHorizontal: horizontaler Fußpunkt der colorbar in Plot-% (default: 0.)
                * CBAnchorVertical: vertikaler Fußpunkt der colorbar in Plot-% (default: 0.2)     

            CBLegend (3Classes) - Parameterization of the representative Symbols
                * CBLe3cTopVPad (default: 1+1*1/4)
                * CBLe3cMiddleVPad (default: .5)                                                                         
                * CBLe3cBottomVPad (default: 0-1*1/4)
                
                    * 1 is the height of the Colorbar                                                                   
                    * the VPads (the vertical Sy-Positions) are defined in cax.transAxes Coordinates    
                    * cax is the Colorbar Axes               

                * CBLe3cSySize=10**2 (Sy-Area in pts^2)
                * CBLe3cSyType='o' 

            NRCVs - NumeRiCal Values to be displayed
                * pFIGNrcv: List of Sir3sID RegExps to be displayed (i.e. ['KNOT~PKON-Knoten~\S*~\S+~QM'])
                    the 1st Match is used if a RegExp matches more than 1 Channel
                    
                    further Examples for RegExps (and corresponding Texts):
                        * WBLZ~WärmeblnzGes~\S*~\S+~WES (Generation)
                        * WBLZ~WärmeblnzGes~\S*~\S+~WVB (Load)
                        * WBLZ~WärmeblnzGes~\S*~\S+~WVERL (Loss)
                    WBLZ~[\S ]+~\S*~\S+~\S+: Example for a RegExp matching all Channels with OBJTYPE WBLZ  
                * pFIGNrcvTxt: corresponding List of Texts (i.e. ['Kontrollwert DH'])
                * pFIGNrcvFmt (i.e. '{:12s}: {:8.2f} {:4s} {:6.1f}%')
                    * Text (from pFIGNrcvTxt)
                    * Value
                    * UNIT (determined from Channel-Data)
                    * ValueInPercent (use i.e. '{:12s}: {:8.2f} {:4s}' to prevent display)
                * pFIGNrcvXStart (.5 default)
                * pFIGNrcvYStart (.5 default)
                * pFIGNrcvYSpace (-.1 default)
            VICs - VeryImportantCustomers whose Values to be displayed
                * pVICsDf: DataFrame with VeryImportantCustomers (Text & Specification)
                    columns expected:
                        * Kundenname (i.e. 'VIC1') - Text
                        * Knotenname (i.e. 'V-K007') - Specification by Supply-Node
                * pVICsXStart (.8 default)
                * pVICsYStart (.8 default)
                * pVICsYSpace (-.1 default)

            Returns:
                pFWVB
                    columns 
                        * Measure: float 
                        * MCategory: str (meaningfull only if Measure3Classes True):

                            str:
                            * TopText or
                            * MiddleText or
                            * BottomText

                        * GCategory: list (non-empty only if req. GCategories are a subset of the available Categories and FWVB belongs to a req. Category)
                    
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            keys = sorted(kwds.keys())

            # FWVB Attribute (Size)
            if 'pFWVBAttribute' not in keys:
                kwds['pFWVBAttribute']='W0LFK'
            if 'pFWVBAttributeAsc' not in keys:
                kwds['pFWVBAttributeAsc']=False
            if 'pFWVBAttributeRefSize' not in keys:
                kwds['pFWVBAttributeRefSize']=10**2

            # FWVB Measure (Color)
            if 'pFWVBMeasure' not in keys:
                kwds['pFWVBMeasure']='FWVB~*~*~*~W'
            if 'pFWVBMeasureInRefPerc' not in keys:
                kwds['pFWVBMeasureInRefPerc']=True

            if 'pFWVBMeasureAlpha' not in keys:
                kwds['pFWVBMeasureAlpha']=0.9
            if 'pFWVBMeasureColorMap' not in keys:
                kwds['pFWVBMeasureColorMap']=plt.cm.autumn
            if 'pFWVBMeasureClip' not in keys:
                kwds['pFWVBMeasureClip']=False

            # 3Classes
            if 'pFWVBMeasure3Classes' not in keys:
                kwds['pFWVBMeasure3Classes']=False

            # CatTexts (werden verwendet wenn 3Classes Wahr gesetzt ist)
            if 'pMCatTopText' not in keys:
                kwds['pMCatTopText']='Top'
            if 'pMCatMiddleText' not in keys:
                kwds['pMCatMiddleText']='Middle'
            if 'pMCatBottomText' not in keys:
                kwds['pMCatBottomText']='Bottom'

            # CatAttribs (werden verwendet wenn 3Classes Wahr gesetzt ist)
            if 'pMCatTopAlpha' not in keys:
                kwds['pMCatTopAlpha']=0.9
            if 'pMCatTopColor' not in keys:
                kwds['pMCatTopColor']='palegreen'
            if 'pMCatTopClip' not in keys:
                kwds['pMCatTopClip']=False

            if 'pMCatMidAlpha' not in keys:
                kwds['pMCatMidAlpha']=0.9
            if 'pMCatMidColorMap' not in keys:
                kwds['pMCatMidColorMap']=plt.cm.autumn
            if 'pMCatMidClip' not in keys:
                kwds['pMCatMidClip']=False

            if 'pMCatBotAlpha' not in keys:
                kwds['pMCatBotAlpha']=0.9
            if 'pMCatBotColor' not in keys:
                kwds['pMCatBotColor']='violet'
            if 'pMCatBotClip' not in keys:
                kwds['pMCatBotClip']=False

            # CBFixedLimits 
            if 'pFWVBMeasureCBFixedLimits' not in keys:
                kwds['pFWVBMeasureCBFixedLimits']=False
            if 'pFWVBMeasureCBFixedLimitLow' not in keys:
                kwds['pFWVBMeasureCBFixedLimitLow']=.10
            if 'pFWVBMeasureCBFixedLimitHigh' not in keys:
                kwds['pFWVBMeasureCBFixedLimitHigh']=.95

            # CB
            if 'CBFraction' not in keys:
                kwds['CBFraction']=0.05
            if 'CBHpad' not in keys:
                kwds['CBHpad']=0.0275
            if 'CBLabelPad' not in keys:
                kwds['CBLabelPad']=-50
            if 'CBTicklabelsHPad' not in keys:
                kwds['CBTicklabelsHPad']=0
            if 'CBAspect' not in keys:
                kwds['CBAspect']=10.
            if 'CBShrink' not in keys:
                kwds['CBShrink']=0.3
            if 'CBAnchorHorizontal' not in keys:
                kwds['CBAnchorHorizontal']=0.
            if 'CBAnchorVertical' not in keys:
                kwds['CBAnchorVertical']=0.2
                      
            # CBLegend (3Classes) 
            if 'CBLe3cTopVPad' not in keys:
                kwds['CBLe3cTopVPad']=1+1*1/4  
            if 'CBLe3cMiddleVPad' not in keys:
                kwds['CBLe3cMiddleVPad']=.5    
            if 'CBLe3cBottomVPad' not in keys:
                kwds['CBLe3cBottomVPad']=0-1*1/4    
            if 'CBLe3cSySize' not in keys:
                kwds['CBLe3cSySize']=10**2
            if 'CBLe3cSyType' not in keys:
                kwds['CBLe3cSyType']='o'

            # NRCVs
            if 'pFIGNrcv' not in keys:
                kwds['pFIGNrcv']=['KNOT~PKON-Knoten~\S*~\S+~QM']  
            if 'pFIGNrcvTxt' not in keys:
                kwds['pFIGNrcvTxt']=['Kontrollwert DH']
            if 'pFIGNrcvFmt' not in keys:
                kwds['pFIGNrcvFmt']='{:12s}: {:8.2f} {:4s} {:6.1f}%'
            if 'pFIGNrcvXStart' not in keys:
                kwds['pFIGNrcvXStart']=.5
            if 'pFIGNrcvYStart' not in keys:
                kwds['pFIGNrcvYStart']=.5
            if 'pFIGNrcvYSpace' not in keys:
                kwds['pFIGNrcvYSpace']=-.1

            # VICs
            if 'pVICsDf' not in keys:
                kwds['pVICsDf']=pd.DataFrame({'Kundenname': ['VIC1'],'Knotenname': ['V-K007']})
            if 'pVICsXStart' not in keys:
                kwds['pVICsXStart']=.8
            if 'pVICsYStart' not in keys:
                kwds['pVICsYStart']=.8
            if 'pVICsYSpace' not in keys:
                kwds['pVICsYSpace']=-.1

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                     
        
        try: 
            # 2 Szenrariumzeiten ermitteln ===============================================
            firstTime=self.mx.df.index[0]
            if isinstance(timeDeltaToRef,pd.Timedelta):
                timeRef=firstTime+timeDeltaToRef
            else:
                logStrFinal="{:s}{:s} not Type {:s}.".format(logStr,'timeDeltaToRef','pd.Timedelta')
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
            if isinstance(timeDeltaToT,pd.Timedelta):
                timeT=firstTime+timeDeltaToT
            else:
                logStrFinal="{:s}{:s} not Type {:s}.".format(logStr,'timeDeltaToT','pd.Timedelta')
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

            if isinstance(kwds['pVICsDf'],pd.core.frame.DataFrame):
                vFWVB=vFWVB.merge(kwds['pVICsDf'],left_on='NAME_i',right_on='Knotenname',how='left')
                vFWVB.rename(columns={'Kundenname':'VIC'},inplace=True)
                vFWVB.drop('Knotenname',axis=1,inplace=True)
           
            # Einheit der Measures ermitteln (fuer Annotationen)
            pFWVBMeasureCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(kwds['pFWVBMeasure'])]
            pFWVBMeasureUNIT=pFWVBMeasureCh.iloc[0].UNIT
            pFWVBMeasureATTRTYPE=pFWVBMeasureCh.iloc[0].ATTRTYPE

            pROHRMeasureCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(pROHRMeasure)]
            pROHRMeasureUNIT=pROHRMeasureCh.iloc[0].UNIT
            pROHRMeasureATTRTYPE=pROHRMeasureCh.iloc[0].ATTRTYPE

            # Sachdaten annotieren mit Spalte Measure >pXXXX ===============================================

            # FWVB            
            pFWVBMeasureValue=plotTimeDfs[timeTIdx][kwds['pFWVBMeasure']].iloc[0] 
            pFWVBMeasureValueRef=plotTimeDfs[timeRefIdx][kwds['pFWVBMeasure']].iloc[0] 
            if kwds['pFWVBMeasureInRefPerc']:  # auch in diesem Fall trägt die Spalte Measure das Ergebnis                               
                pFWVBMeasureValuePerc=[float(m)/float(mRef) if float(mRef) >0 else 1 for m,mRef in zip(pFWVBMeasureValue,pFWVBMeasureValueRef)]
                pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValuePerc)) #!                                
            else:
                pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValue)) #!                              

            pFWVB=pFWVB.assign(MeasureOrig=pd.Series(pFWVBMeasureValue)) 
            pFWVB=pFWVB.assign(MeasureRef=pd.Series(pFWVBMeasureValueRef)) 

            # Sachdaten annotieren mit Spalte MCategory           
            if  not kwds['pFWVBMeasureCBFixedLimits'] and kwds['pFWVBMeasure3Classes']:
                logger.error("Bei 3-Klassendarstellung Wahr muss FixedLimits Wahr sein.")

            pFWVBCat=[]
            for index, row in pFWVB.iterrows():
                if row.Measure >= kwds['pFWVBMeasureCBFixedLimitHigh']:
                    pFWVBCat.append(kwds['pMCatTopText'])
                elif row.Measure <= kwds['pFWVBMeasureCBFixedLimitLow']:
                    pFWVBCat.append(kwds['pMCatBottomText'])
                else:
                    pFWVBCat.append(kwds['pMCatMiddleText'])
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

            # ========================================
            # Return pFWVB enthält die ungefilterte und unselektierte menge
            # ========================================

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
            pltFWVB[ kwds['pFWVBAttribute']]=pltFWVB[ kwds['pFWVBAttribute']].astype(float)
            pltROHR[pROHRAttribute]=pltROHR[pROHRAttribute].astype(float)
            
            # Selektionen ===============================================
            pltFWVB=pltFWVB[pltFWVB[kwds['pFWVBAttribute']]>0] 
            pltROHR=pltROHR[pltROHR[pROHRAttribute]>0] 
            
            pltFWVB=pltFWVB[(pltFWVB[kwds['pFWVBAttribute']]<=pltFWVB[kwds['pFWVBAttribute']].quantile(quantil_pFWVBAttributeHigh))
                            &
                            (pltFWVB[kwds['pFWVBAttribute']]>=pltFWVB[kwds['pFWVBAttribute']].quantile(quantil_pFWVBAttributeLow))
                           ]

            pltROHR=pltROHR[(pltROHR[pROHRAttribute]<=pltROHR[pROHRAttribute].quantile(quantil_pROHRAttributeHigh))
                            &
                            (pltROHR[pROHRAttribute]>=pltROHR[pROHRAttribute].quantile(quantil_pROHRAttributeLow))
                           ]

            row,col=pltROHR.shape
            logger.debug("{:s}pltROHR nach selektieren: {:d}".format(logStr,row))     

            # Grundsortierung z-Order
            pltFWVB=pltFWVB.sort_values(by=[kwds['pFWVBAttribute']],ascending=kwds['pFWVBAttributeAsc']) 
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

               ,CBFraction=kwds['CBFraction'] 
               ,CBHpad=kwds['CBHpad']              

               ,pltTitle=pltTitle
               ,figFrameon=figFrameon
               #,figLinewidth=1.
               ,figEdgecolor=figEdgecolor 
               ,figFacecolor=figFacecolor                                                                                            
            )
            fig = plt.gcf()  
            ax=plt.gca()

            pFWVBrefSizeValue=pltFWVB[kwds['pFWVBAttribute']].std()
            if pFWVBrefSizeValue < 1:
                pFWVBrefSizeValue=pltFWVB[kwds['pFWVBAttribute']].mean()
            logger.debug("{:s}pFWVBrefSizeValue (Attributwert): {:6.2f}".format(logStr,pFWVBrefSizeValue)) 
            pFWVBSizeFactor=kwds['pFWVBAttributeRefSize']/pFWVBrefSizeValue
            
            pcFWVB, CBLimitLow, CBLimitHigh = pltNetNodes(
                # ALLG
                 pDf=pltFWVB   
                ,pMeasure3Classes=kwds['pFWVBMeasure3Classes'] 

                ,CBFixedLimits=kwds['pFWVBMeasureCBFixedLimits']
                ,CBFixedLimitLow=kwds['pFWVBMeasureCBFixedLimitLow'] 
                ,CBFixedLimitHigh=kwds['pFWVBMeasureCBFixedLimitHigh'] 
                # FWVB
                ,pMeasure='Measure' 
                ,pAttribute=kwds['pFWVBAttribute']
                                             
                ,pSizeFactor=pFWVBSizeFactor
                   
                ,pMeasureColorMap=kwds['pFWVBMeasureColorMap'] 
                ,pMeasureAlpha=kwds['pFWVBMeasureAlpha']
                ,pMeasureClip=kwds['pFWVBMeasureClip']    
   
                ,pMCategory='MCategory' 
                ,pMCatTopTxt=kwds['pMCatTopText'] # 'Top'     
                ,pMCatBotTxt=kwds['pMCatBottomText'] # 'Bottom'    
                ,pMCatMidTxt=kwds['pMCatMiddleText'] # 'Middle'             
               
                ,pMCatTopColor=kwds['pMCatTopColor']
                ,pMCatTopAlpha=kwds['pMCatTopAlpha']
                ,pMCatTopClip=kwds['pMCatTopClip']   
                                                                        
                ,pMCatBottomColor=kwds['pMCatBotColor'] 
                ,pMCatBottomAlpha=kwds['pMCatBotAlpha']
                ,pMCatBottomClip=kwds['pMCatBotClip']
                  
                ,pMCatMiddleColorMap=kwds['pMCatMidColorMap']
                ,pMCatMiddleAlpha=kwds['pMCatMidAlpha']
                ,pMCatMiddleClip=kwds['pMCatMidClip']
            )

            cax,TBAnchorVertical=pltNetColorbar(
                # ALLG
                 pc=pcFWVB # PathCollection aus pltNetNodes                                        
                ,pDf=pltFWVB 
                ,pMeasureInPerc=kwds['pFWVBMeasureInRefPerc'] 
                ,pMeasure3Classes=kwds['pFWVBMeasure3Classes']      
                
                # Ticks (TickLabels und TickValues)
                ,CBFixedLimits=kwds['pFWVBMeasureCBFixedLimits']
                ,CBFixedLimitLow=kwds['pFWVBMeasureCBFixedLimitLow']
                ,CBFixedLimitHigh=kwds['pFWVBMeasureCBFixedLimitHigh']                       

                #
                ,pMeasure='Measure'           
         
                # Label
                ,pMeasureUNIT=pFWVBMeasureUNIT
                ,pMeasureTYPE=pFWVBMeasureATTRTYPE

                # Geometrie
                ,CBFraction=kwds['CBFraction']  
                ,CBHpad=kwds['CBHpad']          
                ,CBLabelPad=kwds['CBLabelPad']    
                ,CBTicklabelsHPad=kwds['CBTicklabelsHPad']                          
                ,CBAspect=kwds['CBAspect'] 
                ,CBShrink=kwds['CBShrink'] 
                ,CBAnchorHorizontal=kwds['CBAnchorHorizontal'] 
                ,CBAnchorVertical=kwds['CBAnchorVertical'] 

                # Legend 3 Classes
                ,pAttribute=kwds['pFWVBAttribute'] 
                #,pSizeFactor=pFWVBSizeFactor                   
                ,pMCategory='MCategory' 
                ,pMCatTopTxt=kwds['pMCatTopText']     
                ,pMCatBotTxt=kwds['pMCatBottomText']       
                ,pMCatMidTxt=kwds['pMCatMiddleText']     

                ,pMCatBottomColor=kwds['pMCatBotColor'] 
                ,pMCatTopColor=kwds['pMCatTopColor'] 

                ,CBLe3cTopVPad=kwds['CBLe3cTopVPad'] #1+1*1/4                 
                ,CBLe3cMiddleVPad=kwds['CBLe3cMiddleVPad'] #.5                                                                         
                ,CBLe3cBottomVPad=kwds['CBLe3cBottomVPad'] #0-1*1/4  
                ,CBLe3cSySize=kwds['CBLe3cSySize'] 
                ,CBLe3cSyType=kwds['CBLe3cSyType'] 


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
            # Bilanzwerte
            fig.sca(ax)

            # Gesamtbilanz-----------------------------------------------------------------------
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

            txt="{:12s}: {:6.1f} {:4s} {:6.1f}%".format(sCh.NAME1,v,pFWVBGCategoryUnit,vp)
            #a=plt.annotate(txt
            #                ,xy=(x,y)
            #                ,family='monospace'
            #                ,size='smaller'                   
            #                ,xycoords=ax.transAxes #'data'  
            #                ,rotation='horizontal'
            #                ,va='bottom'
            #                ,ha='left'   
            #                ,clip_on=False
            #)     


            # Userbilanzen-----------------------------------------------------------------------
            #vKNOT=xm.dataFrames['vKNOT']
            vWBLZ=self.xm.dataFrames['vWBLZ']
            vWBLZ_vKNOT=pd.merge(vWBLZ,vKNOT,left_on='OBJID',right_on='pk')
            vWBLZ_vKNOT_pFWVB=pd.merge(vWBLZ_vKNOT,pFWVB,left_on='NAME_y',right_on='NAME_i')

            vWBLZ_vKNOT_pFWVB=vWBLZ_vKNOT_pFWVB[['NAME_x','NAME_i','pk','W','pk_x','WBLZ', 'Measure', 'MeasureRef','MeasureOrig','MCategory', 'GCategory']]
            vWBLZ_vKNOT_pFWVB.rename(columns={'NAME_x':'NAME','pk_x':'pkWBLZ'},inplace=True)

            vNRCV_Mx1=self.xm.dataFrames['vNRCV_Mx1']
            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1=pd.merge(vWBLZ_vKNOT_pFWVB,vNRCV_Mx1,left_on='pkWBLZ',right_on='fkOBJTYPE',how='left')
            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1['Sir3sID']=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1['Sir3sID'].fillna(value='')
            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1['cRefLfdNr']=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1['cRefLfdNr'].fillna(value=1)
            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.rename(columns={'pk_x':'pkFWVB'},inplace=True)

            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1[['NAME','NAME_i','pkFWVB','W','WBLZ','Sir3sID'
                                                         , 'Measure', 'MeasureRef','MeasureOrig','MCategory', 'GCategory','cRefLfdNr']]
            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1[vWBLZ_vKNOT_pFWVB_vNRCV_Mx1['cRefLfdNr']==1]
            vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.drop('cRefLfdNr',axis=1,inplace=True)
            
            #vWBLZ_vKNOT_pFWVB_vNRCV_Mx1['WIst']=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.apply(lambda row: row.Measure    * row.MeasureRef   , axis=1)

            vAggNumAnz=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.groupby(['NAME','Sir3sID']).size()
            #vAggNumAnz.loc['BLNZ1u5u7'].index[0] liefert Sir3sID


            vAggWblzMCat=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.groupby(['NAME','MCategory']).agg(
            {
                 'W': ['size','min', 'max', 'sum']
                ,'Measure': ['size','min', 'max', 'sum']
                ,'MeasureOrig': ['size','min', 'max', 'sum']
                ,'MeasureRef': ['size','min', 'max', 'sum']
            })

            vAggWblz=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.groupby(['NAME']).agg(
            {
                'W': ['size','min', 'max', 'sum']
               ,'Measure': ['size','min', 'max', 'sum']
               ,'MeasureOrig': ['size','min', 'max', 'sum']
               ,'MeasureRef': ['size','min', 'max', 'sum']
            })

            if isinstance(pFWVBGCategory,list):    
                idx=1
                for NAME in pFWVBGCategory: # verlangte Wärmebilanzen       
                    try: 
                        vSoll=vAggWblz.loc[NAME]['MeasureRef']['sum']
                        vIst=vAggWblz.loc[NAME]['MeasureOrig']['sum']                                     
                        vpAgg=vIst/vSoll*100                                                                                                             
                    except:
                        logger.debug("{:s} verlangte Wärmebilanz (aus pFWVBGCategory)={:s} ist nicht definiert.".format(logStr,NAME))    
                        continue

                    try:                                       
                        topAnz=int(vAggWblzMCat.loc[NAME,kwds['pMCatTopText']]['Measure']['size'])                                                                                
                    except:
                        topAnz=0
                   
                    try:                                                          
                        midAnz=int(vAggWblzMCat.loc[NAME,kwds['pMCatMiddleText']]['Measure']['size'])                                                                             
                    except:                 
                        midAnz=0
                  
                    try:                                                         
                        botAnz=int(vAggWblzMCat.loc[NAME,kwds['pMCatBottomText']]['Measure']['size'])                                                                 
                    except:                   
                        botAnz=0                   

                    try: 
                        Sir3sID=vAggNumAnz.loc[NAME].index[0]   
                        sCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(Sir3sID)].iloc[0]
                        s=self.mx.df[Sir3sID]    
                        v=s[timeT]                
                        v0=s[timeRef]
                        vp=v/v0*100     
                    
                        if math.fabs(vpAgg-vp) > 0.1:
                            logger.error("{:s} für verlangte Wärmebilanz (aus pFWVBGCategory)={:s} ist das NumAnz Ergebnis verschieden vom Agg Ergebnis!".format(logStr,NAME))  
                                                                                                                                        
                    except:
                        logger.debug("{:s} für verlangte Wärmebilanz (aus pFWVBGCategory)={:s} ist keine NumAnz definiert.".format(logStr,NAME))                        
                                                                                    
                    x,y=pFWVBGCategoryXStart,pFWVBGCategoryYStart+pFWVBGCategoryYSpace*idx
                    idx=idx+1

                    #  txt="{:12s}: {:6.1f} {:4s} {:6.1f}%".format(sCh.NAME1,v,pFWVBGCategoryUnit,vp)

                    vpIstZuvSoll=vIst/vSoll
                    if pFWVBGCategoryUnit=='[MW]':
                        vIst=vIst/1000.

                    if kwds['pFWVBMeasure3Classes']:
                        txt="{:12s}: {:6.1f} {:4s} {:6.1f}% {:5d}/{:5d}/{:5d}".format(NAME,vIst,pFWVBGCategoryUnit,vpIstZuvSoll*100,topAnz,midAnz,botAnz)
                    else:
                        txt="{:12s}: {:6.1f} {:4s} {:6.1f}%".format(NAME,vIst,pFWVBGCategoryUnit,vpIstZuvSoll*100)
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
                                  
            # ---------------------------------------------------------------------
            # NRCVs
            fig.sca(ax)

            if isinstance(kwds['pFIGNrcv'],list) and isinstance(kwds['pFIGNrcvTxt'],list):
                if len(kwds['pFIGNrcv']) == len(kwds['pFIGNrcvTxt']):
                    idxTxt=0
                    for idx,Sir3sIDRexp in  enumerate(kwds['pFIGNrcv']):                           
                        try:
                            sCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.contains(Sir3sIDRexp)].iloc[0]
                        except:
                            logger.debug("{:s} Sir3sIDRexp {:s} nicht in .MX1".format(logStr,Sir3sIDRexp))
                            continue

                        x,y=kwds['pFIGNrcvXStart'],kwds['pFIGNrcvYStart']+kwds['pFIGNrcvYSpace']*idxTxt
                        idxTxt=idxTxt+1
                
                        s=self.mx.df[sCh.Sir3sID]                
                        v=s[timeT]  
                        vp=v/v0*100     
                                              
                        # '{:12s}: {:8.2f} {:4s} {:6.1f}%'
                        txt=kwds['pFIGNrcvFmt'].format(kwds['pFIGNrcvTxt'][idx],v,sCh.UNIT,vp) 
                       
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

            if isinstance(kwds['pVICsDf'],pd.core.frame.DataFrame):
                fig.sca(ax)
                xStart=kwds['pVICsXStart']
                yStart=kwds['pVICsYStart']
                fontsize=8
                distance=50
                idx=0
                for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():      
                        kunde=row.VIC                         
                        v=row.Measure
                        if kwds['pFWVBMeasureInRefPerc']:
                            txt="{:30s} {:3.0f}%".format(kunde,v*100)      
                        else:                           
                            txt="{:30s} {:6.2f} {:s}".format(kunde,v,pFWVBMeasureUNIT)    
                        x,y=kwds['pVICsXStart'],kwds['pVICsYStart']+kwds['pVICsYSpace']*idx                  
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
