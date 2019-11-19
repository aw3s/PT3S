"""
>>> # ---
>>> # SETUP
>>> # ---
>>> import os
>>> import logging
>>> logger = logging.getLogger('PT3S.Rm')
>>> # ---
>>> # path
>>> # ---
>>> if __name__ == "__main__":
...   try:
...      dummy=__file__
...      logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ','path = os.path.dirname(__file__)'," .")) 
...      path = os.path.dirname(__file__)
...   except NameError:    
...      logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ',"path = '.' because __file__ not defined and: "," from Rm import Rm")) 
...      path = '.'
...      from Rm import Rm 
... else:
...    path = '.'
...    logger.debug("{0:s}{1:s}".format('Not __main__ Context: ',"path = '.' .")) 
>>> try:
...    from PT3S import Mx
... except ImportError:
...    logger.debug("{0:s}{1:s}".format("DOCTEST: from PT3S import Mx: ImportError: ","trying import Mx instead ... maybe pip install -e . is active ..."))  
...    import Mx
>>> try:
...    from PT3S import Xm
... except ImportError:
...    logger.debug("{0:s}{1:s}".format("DOCTEST: from PT3S import Xm: ImportError: ","trying import Xm instead ... maybe pip install -e . is active ..."))  
...    import Xm
>>> # ---
>>> # testDir
>>> # ---
>>> # globs={'testDir':'testdata'}
>>> try:
...    dummy= testDir
... except NameError:
...    testDir='testdata' 
>>> # ---
>>> # dotResolution
>>> # ---
>>> # globs={'dotResolution':''}
>>> try:
...     dummy= dotResolution
... except NameError:
...     dotResolution='' 
>>> import pandas as pd
>>> import matplotlib.pyplot as plt
>>> pd.set_option('display.max_columns',None)
>>> pd.set_option('display.width',666666666)
>>> # ---
>>> # LocalHeatingNetwork SETUP
>>> # ---
>>> xmlFile=os.path.join(os.path.join(path,testDir),'LocalHeatingNetwork.XML')
>>> xm=Xm.Xm(xmlFile=xmlFile)
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1'+dotResolution+'.MX1')) 
>>> mx=Mx.Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> mx.setResultsToMxsFile(NewH5Vec=True)
5
>>> xm.MxSync(mx=mx)
>>> rm=Rm(xm=xm,mx=mx)
>>> # ---
>>> # Plot 3Classes False
>>> # ---
>>> plt.close('all')
>>> ppi=72 # matplotlib default
>>> dpi_screen=2*ppi
>>> fig=plt.figure(dpi=dpi_screen,linewidth=1.)
>>> timeDeltaToT=mx.df.index[2]-mx.df.index[0]
>>> # 3Classes und FixedLimits sind standardmaessig Falsch; RefPerc ist standardmaessig Wahr
>>> # die Belegung von MCategory gemaess FixedLimitsHigh/Low erfolgt immer ... 
>>> pFWVB=rm.pltNetDHUS(timeDeltaToT=timeDeltaToT,pFWVBMeasureCBFixedLimitHigh=0.80,pFWVBMeasureCBFixedLimitLow=0.66,pFWVBGCategory=['BLNZ1u5u7'],pVICsDf=pd.DataFrame({'Kundenname': ['VIC1'],'Knotenname': ['V-K007']}))
>>> # ---
>>> # Check pFWVB Return
>>> # ---
>>> f=lambda x: "{0:8.5f}".format(x) 
>>> print(pFWVB[['Measure','MCategory','GCategory','VIC']].to_string(formatters={'Measure':f}))
   Measure MCategory  GCategory   VIC
0  0.80971       Top  BLNZ1u5u7   NaN
1  0.66692    Middle              NaN
2  0.66043    Middle  BLNZ1u5u7   NaN
3  0.65551    Bottom  BLNZ1u5u7  VIC1
4  0.68548    Middle              NaN
>>> # ---
>>> # Print 
>>> # ---
>>> (wD,fileName)=os.path.split(xm.xmlFile)
>>> (base,ext)=os.path.splitext(fileName)
>>> plotFileName=wD+os.path.sep+base+'.'+'pdf'
>>> if os.path.exists(plotFileName):                        
...    os.remove(plotFileName)
>>> plt.savefig(plotFileName,dpi=2*dpi_screen)
>>> os.path.exists(plotFileName)
True
>>> # ---
>>> # Plot 3Classes True
>>> # ---
>>> plt.close('all')
>>> # FixedLimits wird automatisch auf Wahr gesetzt wenn 3Classes Wahr ... 
>>> pFWVB=rm.pltNetDHUS(timeDeltaToT=timeDeltaToT,pFWVBMeasure3Classes=True,pFWVBMeasureCBFixedLimitHigh=0.80,pFWVBMeasureCBFixedLimitLow=0.66)
>>> # ---
>>> # LocalHeatingNetwork Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> if os.path.exists(plotFileName):                        
...    os.remove(plotFileName)
"""

import warnings # 3.6
#...\Anaconda3\lib\site-packages\h5py\__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
#   from ._conv import register_converters as _register_converters
warnings.simplefilter(action='ignore', category=FutureWarning)

#C:\Users\Wolters\Anaconda3\lib\site-packages\matplotlib\cbook\deprecation.py:107: MatplotlibDeprecationWarning: Adding an axes using the same arguments as a previous axes currently reuses the earlier instance.  In a future version, a new instance will always be created and returned.  Meanwhile, this warning can be suppressed, and the future behavior ensured, by passing a unique label to each axes instance.
#  warnings.warn(message, mplDeprecation, stacklevel=1)
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

import os
import sys

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


import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import scipy
import networkx as nx
from itertools import chain
import math
import sys


import logging
# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S.Rm')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

try:
    from PT3S import Mx
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Mx - trying import Mx instead ... maybe pip install -e . is active ...')) 
    import Mx

try:
    from PT3S import Xm
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Xm - trying import Xm instead ... maybe pip install -e . is active ...')) 
    import Xm

# ---
# --- main Imports
# ---
import argparse
import unittest
import doctest

import math

# DIN A6 105 x 148 mm	4,13 x 5,83 in
# DIN A5 148 x 210 mm	5,83 x 8,27 in
# DIN A4 210 x 297 mm	8,27 x 11,69 in
# DIN A3 297 x 420 mm	11,69 x 16,54 in
# DIN A0 841 x 1189 mm	33,11 x 46,81 in

DINA4_x=8.2677165354
DINA4_y=11.6929133858

DINA3_x=DINA4_x*math.sqrt(2)
DINA3_y=DINA4_y*math.sqrt(2)

class RmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

from matplotlib import markers
from matplotlib.path import Path

import numpy as np

def pltMakeCategoricalCmap(catagoryCmap="tab10",catagoryColors=None,nOfSubCatsReq=3,reversedSubCatOrder=False):
    """
    Returns a cmap with nOfCatsReq * nOfSubCatsReq discrete colors.

    Parameter:
        catagoryCmap:    a (discrete) cmap with different "base"colors
                         default: tab10
        catagoryColors:  a list of "base"colors indices for this cmap
                         the length of the list is the number of Categories requested: nOfCatsReq
                         apparently cmap's nOfColors must be ge than nOfCatsReq
                         default: None (==> nOfCatsReq = cmap's nOfColors)
                         i.e. [2,8,3] for tab10 is green, yellow (ocher), red
        nOfSubCatsReq:   number of Subcategories requested
        
    Returns:
        cmap with nOfCatsReq * nOfSubCatsReq discrete colors; None if an error occurs
        one "base"color per category
        nOfSubCatsReq "sub"colors per category
        so each category consists of nOfSubCatsReq colors
        the 1st color of a category is from catagoryCmap - the "base"color of the category
        the other colors of a category are derived from the "base"color 
        if reversedSubCatOrder, the last color of a category is from catagoryCmap

    Raises:
        RmError

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> import Rm    
    >>> Rm.pltMakeCategoricalCmap().N
    30
    >>> Rm.pltMakeCategoricalCmap(catagoryColors=[2,8,3]).N
    9
    >>> catagoryCmap="tab10"
    >>> catagoryColors=[2,8,3]
    >>> nOfSubCatsReq=4
    >>> cm=Rm.pltMakeCategoricalCmap(catagoryCmap=catagoryCmap,catagoryColors=catagoryColors,nOfSubCatsReq=nOfSubCatsReq,reversedSubCatOrder=True)
    >>> nCat=len(catagoryColors)
    >>> nCatSub=nOfSubCatsReq
    >>> colorsY=np.ones(nCat*nCatSub) #1
    >>> colorsX=np.ones(nCat*nCatSub) #1
    >>> for idxC in range(nCat):
    ...        for idxCatSub in range (nCatSub):
    ...            colorsY[idxC*nCatSub+idxCatSub]=idxC
    ...            colorsX[idxC*nCatSub+idxCatSub]=idxC*nCatSub+idxCatSub*nCatSub
    >>> plt.close()
    >>> size_DINA6quer=(5.8,4.1) 
    >>> fig=plt.figure(figsize=size_DINA6quer)
    >>> pco=plt.scatter(colorsX,colorsY, c=np.arange(nCat*nCatSub), s=180, cmap=cm)
    >>> #plt.show()
    """

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    cmap=None

    try:  
        # Farben, "base"colors, welche die cmap hat
        nOfColors=plt.get_cmap(catagoryCmap).N

        if catagoryColors==None:            
            catagoryColors=np.arange(nOfColors,dtype=int)

        # verlangte Kategorien
        nOfCatsReq=len(catagoryColors)
        
        if nOfCatsReq > nOfColors:
            logStrFinal="{0:s}: nOfCatsReq: {1:d} > cmap's nOfColors: {2:d}!".format(logStr,nOfCatsReq,nOfColors)                                 
            raise RmError(logStrFinal)          
                        
        if max(catagoryColors) > nOfColors-1:
            logStrFinal="{0:s}: max. Idx of catsReq: {1:d} > cmap's nOfColors-1: {2:d}!".format(logStr,max(catagoryColors),nOfColors-1)                                 
            raise RmError(logStrFinal)      

        # alle Farben holen, welche die cmap hat
        ccolors = plt.get_cmap(catagoryCmap)(np.arange(nOfColors,dtype=int))
        # die gewuenschten Kategoriefarben extrahieren
        #ccolors=[color for idx,color in enumerate(ccolors) if idx in catagoryColors] # waere in Reihenfolge der cmap und nicht in der gewünschten Reihenfolge 
        ccolors=[ccolors[idx] for idx in catagoryColors]
    
        # Farben bauen

        # resultierende Farben vorbelegen
        cols = np.zeros((nOfCatsReq*nOfSubCatsReq, 3))

        # ueber alle Kategoriefarben
        for i, c in enumerate(ccolors):
            chsv = matplotlib.colors.rgb_to_hsv(c[:3])
            arhsv = np.tile(chsv,nOfSubCatsReq).reshape(nOfSubCatsReq,3)
            arhsv[:,1] = np.linspace(chsv[1],0.25,nOfSubCatsReq)
            arhsv[:,2] = np.linspace(chsv[2],1,nOfSubCatsReq)
            rgb = matplotlib.colors.hsv_to_rgb(arhsv)
            if reversedSubCatOrder:
                rgb=list(reversed(rgb))                
            cols[i*nOfSubCatsReq:(i+1)*nOfSubCatsReq,:] = rgb
            

        cmap = matplotlib.colors.ListedColormap(cols)                

                                                                                          
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:       
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))         
        return cmap

def pltMakePatchSpinesInvisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def pltHlpAlignMarker(marker,halign='center',valign='middle'):
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

def pltNetFigAx(pDf,**kwds):
    """
    Erzeugt eine für die Netzdarstellung verzerrungsfreie Axes-Instanz.

        * verwendet gcf() (will return an existing figure if one is open, or it will make a new one if there is no active figure)
        * an already existing figure might be created this way: fig=plt.figure(dpi=2*72,linewidth=1.) 
        * errechnet die verzerrungsfreie Darstellung unter Berücksichtigung einer zukünftigen horizontalen Farblegende
        * erzeugt eine Axes-Instanz
        * setzt Attribute der Axes-Instanz
        * setzt Attribute der Figure-Instanz

    Args:
        pDf: dataFrame

        Coordinates:
            * pXCor_i: colName in pDf (default: 'pXCor_i'): x-Start Coordinate of all Edges to be plotted  
            * pYCor_i: colName in pDf (default: 'pYCor_i'): y-Start Coordinate of all Edges to be plotted  
            * pXCor_k: colName in pDf (default: 'pXCor_k'): x-End   Coordinate of all Edges to be plotted  
            * pYCor_k: colName in pDf (default: 'pYCor_k'): y-End   Coordinate of all Edges to be plotted  

        Colorlegend:
            * CBFraction: fraction of original axes to use for colorbar (default: 0.05)
            * CBHpad: fraction of original axes between colorbar and new image axes (default: 0.0275)

        Figure:
            * pltTitle: title [not suptitle] (default: 'pltNetFigAx') 
            * figFrameon: figure frame (background): displayed or invisible (default: True)
            * figEdgecolor: edge color of the Figure rectangle (default: 'black')
            * figFacecolor: face color of the Figure rectangle (default: 'white')
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
        keys = sorted(kwds.keys())

        # Coordinates
        if 'pXCor_i' not in keys:
            kwds['pXCor_i']='pXCor_i'
        if 'pYCor_i' not in keys:
            kwds['pYCor_i']='pYCor_i'
        if 'pXCor_k' not in keys:
            kwds['pXCor_k']='pXCor_k'
        if 'pYCor_k' not in keys:
            kwds['pYCor_k']='pYCor_k'

        # Colorlegend
        if 'CBFraction' not in keys:
            kwds['CBFraction']=0.05
        if 'CBHpad' not in keys:
            kwds['CBHpad']=0.0275

        # Figure
        if 'pltTitle' not in keys:
            kwds['pltTitle']='pltNetFigAx'
        if 'figFrameon' not in keys:
            kwds['figFrameon']=True
        if 'figEdgecolor' not in keys:
            kwds['figEdgecolor']='black'
        if 'figFacecolor' not in keys:
            kwds['figFacecolor']='white'

    except:
        pass
    
    try:         
        dx=max(pDf[kwds['pXCor_i']].max(),pDf[kwds['pXCor_k']].max())
        dy=max(pDf[kwds['pYCor_i']].max(),pDf[kwds['pYCor_k']].max())

        # erf. Verhältnis bei verzerrungsfreier Darstellung
        dydx=dy/dx 

        if(dydx>=1):
            dxInch=DINA4_x # Hochformat
        else:
            dxInch=DINA4_y # Querformat
    
        figwidth=dxInch

        #verzerrungsfrei: Blattkoordinatenverhaeltnis = Weltkoordinatenverhaeltnis
        factor=1-(kwds['CBFraction']+kwds['CBHpad'])
        # verzerrungsfreie Darstellung sicherstellen
        figheight=figwidth*dydx*factor

        # Weltkoordinatenbereich
        xlimLeft=0
        ylimBottom=0
        xlimRight=dx
        ylimTop=dy
        
        # plt.figure(dpi=, facecolor=, edgecolor=, linewidth=, frameon=True)
        fig = plt.gcf()  # This will return an existing figure if one is open, or it will make a new one if there is no active figure.



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

        plt.title(kwds['pltTitle'])              
        fig.set_frameon(kwds['figFrameon']) 
        fig.set_edgecolor(kwds['figEdgecolor'])
        fig.set_facecolor(kwds['figFacecolor'])


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
                                                                                          
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:       
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))               

def pltNetNodes(pDf,**kwds):
    """
    Scatters NODEs on gca().

    Args:
            pDf: dataFrame

            NODE: Size (Attribute)
                * pAttribute: colName (default: 'Attribute') in pDf  
                * pSizeFactor: (deafault: 1.)
                * scatter Sy-Area in pts^2 = pSizeFactor * Attribute   

            NODE: Color (Measure)
                * pMeasure: colName (default: 'Measure') in pDf  
                * pMeasureColorMap (default: plt.cm.autumn)
                * pMeasureAlpha (default: 0.9)
                * pMeasureClip (default: False)

                * CBFixedLimits (default: True)
                * CBFixedLimitLow (default: 0.) 
                * CBFixedLimitHigh (default: 1.) 

            NODE: 3Classes
                * pMeasure3Classes (default: True) 

                * pMCategory: colName (default: 'MCategory') in pDf                    
                * pMCatTopTxt (default: 'Top')     
                * pMCatMidTxt (default: 'Middle')             
                * pMCatBotTxt (default: 'Bottom')    

                * pMCatTopColor (default: 'palegreen')
                * pMCatTopAlpha (default: 0.9) 
                * pMCatTopClip (default: False)            

                * pMCatMidColorMap (default: plt.cm.autumn) 
                * pMCatMidAlpha (default: 0.9) 
                * pMCatMidClip (default: False)  
                                                                        
                * pMCatBotColor (default: 'violet') 
                * pMCatBotAlpha (default: 0.9) 
                * pMCatBotClip (default: False)     
            
            NODE:
                * pXCor: colName (default: 'pXCor_i') in pDf 
                * pYCor: colName (default: 'pYCor_i') in pDf 

    Returns:
            (pcN, vmin, vmax)

                * pcN: die mit Farbskala gezeichneten Symbole
                * vmin/vmax: die für die Farbskala verwendeten Extremalwerte
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
            keys = sorted(kwds.keys())

            # NODE: Size (Attribute)
            if 'pAttribute' not in keys:
                kwds['pAttribute']='Attribute'
            if 'pSizeFactor' not in keys:
                kwds['pSizeFactor']=1.

            # NODE: Color (Measure)
            if 'pMeasure' not in keys:
                kwds['pMeasure']='Measure'
            if 'pMeasureColorMap' not in keys:
                kwds['pMeasureColorMap']=plt.cm.autumn
            if 'pMeasureAlpha' not in keys:
                kwds['pMeasureAlpha']=0.9
            if 'pMeasureClip' not in keys:
                kwds['pMeasureClip']=False

            if 'CBFixedLimits' not in keys:
                kwds['CBFixedLimits']=True
            if 'CBFixedLimitLow' not in keys:
                kwds['CBFixedLimitLow']=0.
            if 'CBFixedLimitHigh' not in keys:
                kwds['CBFixedLimitHigh']=1.

            # NODE: 3Classes
            if 'pMeasure3Classes' not in keys:
                kwds['pMeasure3Classes']=True

            if 'pMCategory' not in keys:
                kwds['pMCategory']='MCategory'
            if 'pMCatTopTxt' not in keys:
                kwds['pMCatTopTxt']='Top'
            if 'pMCatMidTxt' not in keys:
                kwds['pMCatMidTxt']='Middle'
            if 'pMCatBotTxt' not in keys:
                kwds['pMCatBotTxt']='Bottom'

            if 'pMCatTopColor' not in keys:
                kwds['pMCatTopColor']='palegreen'
            if 'pMCatTopAlpha' not in keys:
                kwds['pMCatTopAlpha']=0.9
            if 'pMCatTopClip' not in keys:
                kwds['pMCatTopClip']=False

            if 'pMCatMidColorMap' not in keys:
                kwds['pMCatMidColorMap']=plt.cm.autumn
            if 'pMCatMidAlpha' not in keys:
                kwds['pMCatMidAlpha']=0.9
            if 'pMCatMidClip' not in keys:
                kwds['pMCatMidClip']=False

            if 'pMCatBotColor' not in keys:
                kwds['pMCatBotColor']='violet'
            if 'pMCatBotAlpha' not in keys:
                kwds['pMCatBotAlpha']=0.9
            if 'pMCatBotClip' not in keys:
                kwds['pMCatBotClip']=False

            # NODE:
            if 'pXCor' not in keys:
                kwds['pXCor']='pXCor_i'
            if 'pYCor' not in keys:
                kwds['pYCor']='pYCor_i'

    except:
        pass 
        
    try: 


 
        ax=plt.gca()
                     
        if kwds['pMeasure3Classes']:

            pN_top=pDf[(pDf[kwds['pMCategory']]==kwds['pMCatTopTxt'])] 
            pN_mid=pDf[(pDf[kwds['pMCategory']]==kwds['pMCatMidTxt'])]     
            pN_bot=pDf[(pDf[kwds['pMCategory']]==kwds['pMCatBotTxt'])] 

            pN_top_Anz,col=pN_top.shape
            pN_mid_Anz,col=pN_mid.shape
            pN_bot_Anz,col=pN_bot.shape

            pcN_top=ax.scatter(    
                    pN_top[kwds['pXCor']],pN_top[kwds['pYCor']]                 
                ,s=kwds['pSizeFactor']*pN_top[kwds['pAttribute']]
                ,color=kwds['pMCatTopColor']
                ,alpha=kwds['pMCatTopAlpha']
                ,edgecolors='face'             
                ,clip_on=kwds['pMCatTopClip'])        
            logger.debug("{:s}Anzahl mit fester Farbe Top gezeichneter Symbole={:d}".format(logStr,pN_top_Anz))                        

            if not kwds['CBFixedLimits']:
                vmin=pN_mid[kwds['pMeasure']].min()
                vmax=pN_mid[kwds['pMeasure']].max()
            else:
                vmin=kwds['CBFixedLimitLow']
                vmax=kwds['CBFixedLimitHigh']

            pcN=ax.scatter(    
                    pN_mid[kwds['pXCor']],pN_mid[kwds['pYCor']]       
                ,s=kwds['pSizeFactor']*pN_mid[kwds['pAttribute']]
                # Farbskala
                ,cmap=kwds['pMCatMidColorMap']
                # Normierung Farbe
                ,vmin=vmin
                ,vmax=vmax
                # Farbwert
                ,c=pN_mid[kwds['pMeasure']] 
                ,alpha=kwds['pMCatMidAlpha']
                ,edgecolors='face'
                ,clip_on=kwds['pMCatMidClip']
                )
            logger.debug("{:s}Anzahl mit Farbskala gezeichneter Symbole={:d}".format(logStr,pN_mid_Anz))    

            pcN_bot=ax.scatter(    
                    pN_bot[kwds['pXCor']],pN_bot[kwds['pYCor']]                 
                ,s=kwds['pSizeFactor']*pN_bot[kwds['pAttribute']]
                ,color=kwds['pMCatBotColor']
                ,alpha=kwds['pMCatBotAlpha']
                ,edgecolors='face'             
                ,clip_on=kwds['pMCatBotClip'])              
            logger.debug("{:s}Anzahl mit fester Farbe Bot gezeichneter Symbole={:d}".format(logStr,pN_bot_Anz))     
                          
        else:

            pN_Anz,col=pDf.shape

            if not kwds['CBFixedLimits']:
                vmin=pDf[kwds['pMeasure']].min()
                vmax=pDf[kwds['pMeasure']].max()
            else:
                vmin=kwds['CBFixedLimitLow']
                vmax=kwds['CBFixedLimitHigh']
                                         
            pcN=ax.scatter(    
                    pDf[kwds['pXCor']],pDf[kwds['pYCor']]       
                ,s=kwds['pSizeFactor']*pDf[kwds['pAttribute']]
                # Farbskala
                ,cmap=kwds['pMeasureColorMap']
                # Normierung Farbe
                ,vmin=vmin
                ,vmax=vmax
                # Farbwert
                ,c=pDf[kwds['pMeasure']] 
                ,alpha=kwds['pMeasureAlpha']
                ,edgecolors='face'
                ,clip_on=kwds['pMeasureClip']
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

def pltNetPipes(pDf,**kwds):
    """
    Plots Lines with Marker on gca().

    Args:
            pDf: dataFrame

            PIPE-Line:
                * pAttribute: column in pDf (default: 'Attribute')                                                       
                * pAttributeLs (default: '-')
                * pAttributeSizeFactor: plot linewidth in pts = pAttributeSizeFactor (default: 1.0) * Attribute       
                * pAttributeColorMap (default: plt.cm.binary)    
                * pAttributeColorMapUsageStart (default: 1./3; Wertebereich: [0,1])   
                     
                    * Farbskala nach vorh. min./max. Wert
                    * die Farbskala wird nur ab UsageStart genutzt
                    * d.h. Werte die eine "kleinere" Farbe hätten, bekommen die Farbe von UsageStart

            PIPE-Marker:
                * pMeasure: column in pDf  (default: 'Measure')                                  
                * pMeasureMarker (default: '.')
                * pMeasureSizeFactor: plot markersize in pts = pMeasureSizeFactor (default: 1.0) * Measure       
                * pMeasureColorMap (default: plt.cm.cool) 
                * pMeasureColorMapUsageStart (default: 0.; Wertebereich: [0,1])        

                    * Farbskala nach vorh. min./max. Wert
                    * die Farbskala wird nur ab UsageStart genutzt
                    * d.h. Werte die eine "kleinere" Farbe hätten, bekommen die Farbe von UsageStart

            PIPE:
                * pWAYPXCors: column in pDf (default: 'pWAYPXCors')     
                * pWAYPYCors: column in pDf (default: 'pWAYPYCors')     
                * pClip (default: False)
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
            keys = sorted(kwds.keys())

            # PIPE-Line
            if 'pAttribute' not in keys:
                kwds['pAttribute']='Attribute'
            if 'pAttributeSizeFactor' not in keys:
                kwds['pAttributeSizeFactor']=1.           
            if 'pAttributeLs' not in keys:
                kwds['pAttributeLs']='-'           
            if 'pAttributeColorMap' not in keys:
                kwds['pAttributeColorMap']=plt.cm.binary
            if 'pAttributeColorMapUsageStart' not in keys:
                kwds['pAttributeColorMapUsageStart']=1./3.                  

            # PIPE-Marker
            if 'pMeasure' not in keys:
                kwds['pMeasure']='Measure'
            if 'pMeasureSizeFactor' not in keys:
                kwds['pMeasureSizeFactor']=1.
            if 'pMeasureMarker' not in keys:
                kwds['pMeasureMarker']='.'
            if 'pMeasureColorMap' not in keys:
                kwds['pMeasureColorMap']=plt.cm.cool
            if 'pMeasureColorMapUsageStart' not in keys:
                kwds['pMeasureColorMapUsageStart']=0.

            # PIPE
            if 'pWAYPXCors' not in keys:
                kwds['pWAYPXCors']='pWAYPXCors'
            if 'pWAYPYCors' not in keys:
                kwds['pWAYPYCors']='pWAYPYCors'
            if 'pClip' not in keys:
                kwds['pClip']=False

    except:
        pass 
        
    try: 
       
        # Line
        minLine=pDf[kwds['pAttribute']].min()
        maxLine=pDf[kwds['pAttribute']].max()
        logger.debug("{:s}minLine (Attribute): {:6.2f}".format(logStr,minLine))
        logger.debug("{:s}maxLine (Attribute): {:6.2f}".format(logStr,maxLine))
        normLine=colors.Normalize(minLine,maxLine)
        usageLineValue=minLine+kwds['pAttributeColorMapUsageStart']*(maxLine-minLine)
        usageLineColor=kwds['pAttributeColorMap'](normLine(usageLineValue)) 

        # Marker
        minMarker=pDf[kwds['pMeasure']].min()
        maxMarker=pDf[kwds['pMeasure']].max()
        logger.debug("{:s}minMarker (Measure): {:6.2f}".format(logStr,minMarker))
        logger.debug("{:s}maxMarker (Measure): {:6.2f}".format(logStr,maxMarker))
        normMarker=colors.Normalize(minMarker,maxMarker)
        usageMarkerValue=minMarker+kwds['pMeasureColorMapUsageStart']*(maxMarker-minMarker)
        usageMarkerColor=kwds['pMeasureColorMap'](normMarker(usageMarkerValue)) 

        ax=plt.gca()
        for xs,ys,vLine,vMarker in zip(pDf[kwds['pWAYPXCors']],pDf[kwds['pWAYPYCors']],pDf[kwds['pAttribute']],pDf[kwds['pMeasure']]):        

            if vLine >= usageLineValue:
                colorLine=kwds['pAttributeColorMap'](normLine(vLine)) 
            else:
                colorLine=usageLineColor

            if vMarker >= usageMarkerValue:
                colorMarker=kwds['pMeasureColorMap'](normMarker(vMarker))
            else:
                colorMarker=usageMarkerColor

            pcLines=ax.plot(xs,ys
                            ,color=colorLine
                            ,linewidth=kwds['pAttributeSizeFactor']*vLine 
                            ,ls=kwds['pAttributeLs']
                            ,marker=kwds['pMeasureMarker']
                            ,mfc=colorMarker 
                            ,mec=colorMarker  
                            ,mfcalt=colorMarker  
                            ,mew=0
                            ,ms=kwds['pMeasureSizeFactor']*vMarker                                                    
                            ,markevery=[0,len(xs)-1]
                            ,aa=True
                            ,clip_on=kwds['pClip']
                           )            
                                                        
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:       
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                   

def pltNetLegendColorbar(pc,pDf,**kwds): 
    """
    Erzeugt eine Axes cax für den Legendenbereich aus ax (=gca()) und zeichnet auf cax die Farblegende (die Farbskala mit allen Eigenschaften).

        Args:
            pc: (eingefaerbte) PathCollection (aus pltNetNodes); wird für die Erzeugung der Farbskala zwingend benoetigt  
            pDf: dataFrame (default: None)

            Measure:
                * pMeasure: colName in pDf (default: 'Measure') 
                * pMeasureInPerc: Measure wird interpretiert in Prozent [0-1] (default: True)
                * pMeasure3Classes (default: False d.h. Measure wird nicht in 3 Klassen dargestellt)

            CBFixedLimits (Ticks):
                * CBFixedLimits (default: False d.h. Farbskala nach vorh. min./max. Wert)
                * CBFixedLimitLow (default: .10) 
                * CBFixedLimitHigh (default: .95) 

            Label:
                * pMeasureUNIT (default: '[]')
                * pMeasureTYPE (default: '')

            CB
                * CBFraction: fraction of original axes to use for colorbar (default: 0.05)
                * CBHpad: fraction of original axes between colorbar and new image axes (default: 0.0275)               
                * CBLabelPad (default: -50)         
                * CBTicklabelsHPad (default: 0.)      
                * CBAspect: ratio of long to short dimension (default: 10.)
                * CBShrink: fraction by which to shrink the colorbar (default: 0.3)
                * CBAnchorHorizontal: horizontaler Fußpunkt der colorbar in Plot-% (default: 0.)
                * CBAnchorVertical: vertikaler Fußpunkt der colorbar in Plot-% (default: 0.2)     

        Return:
            cax
                  
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
            keys = sorted(kwds.keys())

            # Measure
            if 'pMeasure' not in keys:
                kwds['pMeasure']='Measure'
            if 'pMeasureInPerc' not in keys:
                kwds['pMeasureInPerc']=True
            if 'pMeasure3Classes' not in keys:
                kwds['pMeasure3Classes']=False

            # Label
            if 'pMeasureUNIT' not in keys:
                kwds['pMeasureUNIT']='[]'
            if 'pMeasureTYPE' not in keys:
                kwds['pMeasureTYPE']=''

            # CBFixedLimits 
            if 'CBFixedLimits' not in keys:
                kwds['CBFixedLimits']=False
            if 'CBFixedLimitLow' not in keys:
                kwds['CBFixedLimitLow']=.10
            if 'CBFixedLimitHigh' not in keys:
                kwds['CBFixedLimitHigh']=.95

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


    except:
            pass

        
    try: 
          
        ax=plt.gca()
        fig=plt.gcf()   

        # cax   
        cax=None           
        cax,kw=make_axes(ax
                        ,location='right'
                        ,fraction=kwds['CBFraction'] # fraction of original axes to use for colorbar
                        ,pad=kwds['CBHpad'] # fraction of original axes between colorbar and new image axes
                        ,anchor=(kwds['CBAnchorHorizontal'],kwds['CBAnchorVertical']) # the anchor point of the colorbar axes
                        ,aspect=kwds['CBAspect'] # ratio of long to short dimension
                        ,shrink=kwds['CBShrink'] # fraction by which to shrink the colorbar
                        )         

        # colorbar
        colorBar=fig.colorbar(pc
                    ,cax=cax
                    ,**kw
                    )        

        # tick Values  
        if kwds['pMeasure3Classes']: # FixedLimits should be True and FixedLimitHigh/Low should be set ...
            minCBtickValue=kwds['CBFixedLimitLow']
            maxCBtickValue=kwds['CBFixedLimitHigh']             
        else:
            if kwds['CBFixedLimits'] and isinstance(kwds['CBFixedLimitHigh'],float) and isinstance(kwds['CBFixedLimitLow'],float):
                minCBtickValue=kwds['CBFixedLimitLow']
                maxCBtickValue=kwds['CBFixedLimitHigh']                      
            else:
                minCBtickValue=pDf[kwds['pMeasure']].min()
                maxCBtickValue=pDf[kwds['pMeasure']].max()           
        colorBar.set_ticks([minCBtickValue,minCBtickValue+.5*(maxCBtickValue-minCBtickValue),maxCBtickValue])  

        # tick Labels
        if kwds['pMeasureInPerc']:
            if kwds['pMeasure3Classes']:
                minCBtickLabel=">{:3.0f}%".format(minCBtickValue*100)
                maxCBtickLabel="<{:3.0f}%".format(maxCBtickValue*100)                             
            else:
                minCBtickLabel="{:6.2f}%".format(minCBtickValue*100)
                maxCBtickLabel="{:6.2f}%".format(maxCBtickValue*100) 
        else:
            if kwds['pMeasure3Classes']:
                minCBtickLabel=">{:6.2f}".format(minCBtickValue)
                maxCBtickLabel="<{:6.2f}".format(maxCBtickValue)    
            else:
                minCBtickLabel="{:6.2f}".format(minCBtickValue)
                maxCBtickLabel="{:6.2f}".format(maxCBtickValue)    
        logger.debug("{:s}minCBtickLabel={:s} maxCBtickLabel={:s}".format(logStr,minCBtickLabel,maxCBtickLabel))    
        colorBar.set_ticklabels([minCBtickLabel,'',maxCBtickLabel])        
        colorBar.ax.yaxis.set_tick_params(pad=kwds['CBTicklabelsHPad'])     
                                 
        # Label
        if kwds['pMeasureInPerc']:
                CBLabelText="{:s} in [%]".format(kwds['pMeasureTYPE'])                                                                
        else:
                CBLabelText="{:s} in {:s}".format(kwds['pMeasureTYPE'],kwds['pMeasureUNIT'])
         
        colorBar.set_label(CBLabelText,labelpad=kwds['CBLabelPad'])
                                                                                                                
    except RmError:
        raise            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal) 
        raise RmError(logStrFinal)                       
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
        return cax

def pltNetLegendColorbar3Classes(pDf,**kwds):               
    """
    Zeichnet auf gca() die ergaenzenden Legendeninformationen bei 3 Klassen.  

    * scatters the Top-Symbol
    * scatters the Bot-Symbol
    * the "Mid-Symbol" is the (already existing) colorbar with (already existing) ticks and ticklabels 

    Args:

            pDf: dataFrame

            Category:
                * pMCategory: colName in pDf (default: 'MCategory')
                * pMCatTopText
                * pMCatMidText
                * pMCatBotText

            CBLegend (3Classes) - Parameterization of the representative Symbols
                * CBLe3cTopVPad (default: 1+1*1/4)
                * CBLe3cMidVPad (default: .5)                                                                         
                * CBLe3cBotVPad (default: 0-1*1/4)
                
                    * 1 is the height of the Colorbar                                                                   
                    * the VPads (the vertical Sy-Positions) are defined in cax.transAxes Coordinates    
                    * cax is the Colorbar Axes               

                * CBLe3cSySize=10**2 (Sy-Area in pts^2)
                * CBLe3cSyType='o' 

            Color:
                * pMCatBotColor='violet' 
                * pMCatTopColor='palegreen'    

    Returns:
            (bbTop, bbMid, bbBot): the boundingBoxes of the 3Classes-Symbols  

    """

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
            keys = sorted(kwds.keys())

            # Cats
            if 'pMCategory' not in keys:
                kwds['pMCategory']='MCategory'

            if 'pMCatTopText' not in keys:
                kwds['pMCatTopText']='Top'
            if 'pMCatMidText' not in keys:
                kwds['pMCatMidText']='Middle'
            if 'pMCatBotText' not in keys:
                kwds['pMCatBotText']='Bottom'

            # CBLegend3Cats 
            if 'CBLe3cTopVPad' not in keys:
                kwds['CBLe3cTopVPad']=1+1*1/4  
            if 'CBLe3cMidVPad' not in keys:
                kwds['CBLe3cMidVPad']=.5    
            if 'CBLe3cBotVPad' not in keys:
                kwds['CBLe3cBotVPad']=0-1*1/4    
            if 'CBLe3cSySize' not in keys:
                kwds['CBLe3cSySize']=10**2
            if 'CBLe3cSyType' not in keys:
                kwds['CBLe3cSyType']='o'

            # CatAttribs 
            if 'pMCatTopColor' not in keys:
                kwds['pMCatTopColor']='palegreen'
            if 'pMCatBotColor' not in keys:
                kwds['pMCatBotColor']='violet'

    except:
            pass
        
    try: 
        cax=plt.gca()
        
        pDf_top=pDf[(pDf[kwds['pMCategory']]==kwds['pMCatTopTxt'])] 
        pDf_mid=pDf[(pDf[kwds['pMCategory']]==kwds['pMCatMidTxt'])]     
        pDf_bot=pDf[(pDf[kwds['pMCategory']]==kwds['pMCatBotTxt'])] 

        pDf_top_Anz,col=pDf_top.shape
        pDf_mid_Anz,col=pDf_mid.shape
        pDf_bot_Anz,col=pDf_bot.shape

        logger.debug("{:s} pDf_bot_Anz={:d}  pDf_mid_Anz={:d} pDf_top_Anz={:d}".format(logStr,pDf_bot_Anz,pDf_mid_Anz,pDf_top_Anz))
        logger.debug("{:s} CBLe3cBotVPad={:f}  CBLe3cMidVPad={:f} CBLe3cTopVPad={:f}".format(logStr,kwds['CBLe3cBotVPad'],kwds['CBLe3cMidVPad'],kwds['CBLe3cTopVPad']))

        bbBot=None
        bbMid=None
        bbTop=None

        if pDf_bot_Anz >= 0:
            po=cax.scatter( 0.,kwds['CBLe3cBotVPad']                   
                            ,s=kwds['CBLe3cSySize']
                            ,c=kwds['pMCatBotColor']
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False
                            ,marker=pltHlpAlignMarker(kwds['CBLe3cSyType'], halign='left')                                     
                            )
            # Text dazu
            o=po.findobj(match=None) 
            p=o[0]           
            bbBot=p.get_datalim(cax.transAxes)      
            logger.debug("{:s} bbBot={!s:s}".format(logStr,bbBot))                         

        #    a=plt.annotate(pMCatBotText                                     
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cBotVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'  
        #                    ,color=pMCatBotColor 
        #                    )
        #    # weiterer Text dazu
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_bot_Anz)                                
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cBotVpad)
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'  
        #                    ,color=pMCatBotColor 
        #                    )

        if pDf_top_Anz >= 0:
            po=cax.scatter( 0.,kwds['CBLe3cTopVPad']                          
                            ,s=kwds['CBLe3cSySize']
                            ,c=kwds['pMCatTopColor']
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False     
                            ,marker=pltHlpAlignMarker(kwds['CBLe3cSyType'], halign='left')                                      
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
            po=cax.scatter( 0.,kwds['CBLe3cMidVPad']                                    
                            ,s=kwds['CBLe3cSySize']
                            ,c='lightgrey'
                            ,alpha=0.9
                            ,edgecolors='face'             
                            ,clip_on=False
                            ,visible=False # es erden nur die Koordinaten benoetigt
                            ,marker=pltHlpAlignMarker(kwds['CBLe3cSyType'], halign='left')             

                            )
           
            o=po.findobj(match=None) 
            p=o[0]           
            bbMid=p.get_datalim(cax.transAxes)  


        #        #Text dazu
        #    o=po.findobj(match=None) 
        #    p=o[0]
        #    bb=p.get_datalim(cax.transAxes)
        #    a=plt.annotate(pMCatMidText                                    
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0),CBLe3cMidVpad)                                                                                 
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'
        #                    ,color=pMCatMidColor   
        #                        ,visible=False
        #    )
        #        #weiterer Text dazu                
        #    a=plt.annotate("Anz HA: {:6d}".format(pDf_mid_Anz)                                              
        #                    ,xy=(CBHpad+CBLe3cHpadSymbol+CBLe3cHpad+CBLe3cTextSpaceFactor*(bb.x1-bb.x0)+.5,CBLe3cMidVpad)                                                                                 
        #                    ,xycoords=cax.transAxes 
        #                    ,rotation='vertical' #90
        #                    ,va='center'
        #                    ,ha='center'
        #                    ,color=pMCatMidColor   
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

def pltNetLegendTitleblock(text='',**kwds):
    """
    Zeichnet auf gca() ergaenzende Schriftfeldinformationen.    

    Args:

        text    
        
        Parametrierung:
            * anchorVertical
    """

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
            keys = sorted(kwds.keys())
            
            if 'anchorVertical' not in keys:
                kwds['anchorVertical']=1.
    except:
            pass

    cax=plt.gca()
    try:         
        a=plt.text( 0.
                   ,kwds['anchorVertical']
                   ,text
                   ,transform=cax.transAxes
                   ,family='monospace'
                   ,size='smaller'                    
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

def pltNetTextblock(text='',**kwds):
    """
    Zeichnet einen Textblock auf gca().      
    """

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
            keys = sorted(kwds.keys())
            
            if 'x' not in keys:
                kwds['x']=0.
            if 'y' not in keys:
                kwds['y']=1.


    except:
            pass

    ax=plt.gca()
    try:         
        a=plt.text( kwds['x']
                   ,kwds['y']
                   ,text
                   ,transform=ax.transAxes
                   ,family='monospace'
                   ,size='smaller'                    
                   ,rotation='horizontal'
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

class Rm():


    @classmethod
    def pltNetPipes(cls,pDf,**kwds):
        """
        Plots colored PIPES.
        
        Args:
                DATA:
                    pDf: dataFrame
                        * query: query to filter pDf; default: None; Exp.: ="CONT_ID == '1001'"
                        * fmask: function to filter pDf; default: None; Exp.: =lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False   
                        * query and fmask are used both (query 1st) if not None
                        * sort_values_by: list of colNames defining the plot order; default: None (d.h. die Plotreihenfolge - und damit die z-Order - ist dann die pDF-Reihenfolge)
                        * sort_values_ascending; default: False (d.h. kleine zuletzt und damit (wenn pAttrLineSize = pAttribute/pAttributeFunc) auch dünne über dicke); nur relevant bei sort_values_by

                AXES:
                    pAx: Axes to be plotted on; if not specified: gca() is used

                Colorlegend:
                        * CBFraction in % (default: 5)
                        * CBHpad (default: 0.05)
                        * CBLabel (default: pAttribute/pAttributeFunc)  
                        * CBBinTicks (default: None, d.h. keine Vorgabe von Außen); Vorgabe N: N yTicks; bei diskreten CM gemeint im Sinne von N-1 diskreten Kategorien

                        * CBBinDiscrete (default: False, d.h. eine gegebene (kontinuierliche) CM wird nicht in eine diskrete gewandelt)
                        * wenn CBBinDiscrete, dann gilt N aus CBBinTicks fuer die Ticks (bzw. Kategorien); ist CBBinTicks undef. gilt 4 (also 3 Kategorien)
                        * bei den vorgenannten Kategorien handelt es sich um eine gleichmäßige Unterteilung des definierten Wertebereiches
                        * CBBinBounds (default: None): wenn die CM eine diskrete ist, dann wird eine vorgegebene BoundaryNorm angewandt; CBBinTicks hat dann keine Bedeutung

                PIPE-Attribute:
                    * pAttribute: column in pDf (default: 'Attribute')     
                    * pAttributeFunc: 
                        * function to be used to construct a new col to be plotted
                        * if pAttributeFunc is not None pAttribute is not used: pAttribute is set to 'pAttributeFunc'
                        * the new constructed col is named 'pAttributeFunc'; this name can be used in sort_values_by        
                        
                PIPE-Color:
                    * pAttributeColorMap (default: plt.cm.cool)   
                    * Farbskalamapping:
                    * ------------------
                    * pAttributeColorMapMin (default: pAttribute.min()); ordnet der kleinsten   Farbe einen Wert zu; CM: wenn angegeben _und unterschritten: <=    
                    * pAttributeColorMapMax (default: pAttribute.max()); ordnet der größten     Farbe einen Wert zu; CM: wenn angegeben _und überschritten:  >=   
                    * Standard: Farbskala wird voll ausgenutzt; d.h. der (ggf. mit Min/Max) eingegrenzte Wertebereich wird den Randfarben der Skala zugeordnet
                    * wenn ein anderer, kleinerer, Wertebereich mit derselben Farbskala geplottet wird, dann sind die Farben in den Plots nicht vergleichbar ...
                    * ... wenn eine Farbvergleichbarkeit erzielt werden soll, darf dieselbe Farbskala nicht voll ausgenutzt werden  

                    * pAttributeColorMapUsageStart (default: 0.; Wertebereich: [0,1[)                          
                        * hier: die Farbskala wird unten nur ab UsageStart genutzt ...
                        * ... d.h. Werte die eine "kleinere" Farbe hätten, bekommen die Farbe von UsageStart; CM: v=
                    * pAttributeColorMapUsageEnd (default: 1.; Wertebereich: ]0,1])                           
                        * hier: die Farbskala wird oben nur bis UsageEnd genutzt ...
                        * ... d.h. Werte die eine "größere" Farbe hätten, bekommen die Farbe von UsageEnd; CM: ^=
                        
                    * etwas anderes ist es, wenn man eine Farbskala an den Rändern nicht voll ausnutzen möchte weil einem die Farben dort nicht gefallen ...
                                     
                PIPE-Color 2nd:
                    * um "unwichtige" Bereiche zu "dimmen": Beispiele:                    
                    * räumlich: nicht-Schnitt Bereiche; Bestand (2nd) vs. Ausbau; Zonen unwichtig (2nd) vs. Zonen wichtig; Ok (2nd) von NOK
                    * es werden erst die 2nd-Color Pipes gezeichnet; die (1st-)Color Pipes werden danach gezeichnet, liegen also "über" den "unwichtigen"

                    * es wird dieselbe Spalte pAttribute/pAttributeFunc für die 2. Farbskala verwendet
                    * es wird derselbe Linienstil (pAttributeLs) für die 2. Farbskala verwendet
                    * es wird dieselbe Dicke pAttrLineSize (pAttribute/pAttributeFunc) für die 2. Farbskala verwendet

                    * nur die Farbskala ist anders sowie ggf. das Farbskalamapping

                    * pAttributeColorMapFmask: function to filter pDf to decide to plot with colorMap; default: =lambda row: True       
                    * pAttributeColorMap2ndFmask: function to filter pDf to decide to plot with colorMap2nd; default: =lambda row: False     
                                        
                    * mit den beiden Funktionsmasken kann eine Filterung zusätzlich zu query und fmask realisiert werden
                    * die Funktionsmasken sollten schnittmengenfrei sein; wenn nicht: 2nd überschreibt 

                    * pAttributeColorMap2nd (default: plt.cm.binary)    
                    * Farbskalamapping:
                    * ------------------
                    * pAttributeColorMap2ndMin (default: pAttributeColorMapMin)    
                    * pAttributeColorMap2ndMax (default: pAttributeColorMapMax)    

                    * die Farbskala wird an den Rändern nicht voll ausgenutzt wenn die Farben dort ggf. nicht gefallen:
                    * pAttributeColorMap2ndUsageStart (default: 0.; Wertebereich: [0,1[)                                                
                    * pAttributeColorMap2ndUsageEnd (default: 1.; Wertebereich: ]0,1])                                              
                
                PIPE-Linestyle:
                    * pAttributeLs (default: '-')
                    * same for all colors if mutliple colors are specified

                PIPE-Linesize:
                    * pAttrLineSize: column in pDf; if not specified: pAttribute/pAttributeFunc                
                    * pAttrLineSizeFactor (>0): plot linewidth in pts = pAttrLineSizeFactor (default: =...) * fabs(pAttrLineSize) 
                    * ...: 1./(pDf[pAttrLineSize].std()*2.)      
                    * same for all colors if mutliple colors are specified

                PIPE-Geometry:
                    * pWAYPXCors: column in pDf (default: 'pWAYPXCors')     
                    * pWAYPYCors: column in pDf (default: 'pWAYPYCors')     
                    * pClip (default: True)

                >>> import pandas as pd
                >>> import matplotlib
                >>> import matplotlib.pyplot as plt
                >>> import matplotlib.gridspec as gridspec
                >>> import math
                >>> # ---
                >>> xm=xms['DHNetwork']
                >>> #mx=mxs['DHNetwork']                  
                >>> # ---
                >>> plt.close()
                >>> size_DINA3quer=(16.5, 11.7) 
                >>> dpiSize=72
                >>> fig=plt.figure(figsize=size_DINA3quer,dpi=dpiSize)         
                >>> gs = gridspec.GridSpec(4, 2)
                >>> # ---
                >>> vROHR=xm.dataFrames['vROHR']                 
                >>> # ---
                >>> import Rm
                >>> # ---
                >>> # Attribute (with neg. Values)
                >>> # --------------------------
                >>> axNfd = fig.add_subplot(gs[0])              
                >>> Rm.Rm.pltNetPipes(vROHR
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttribute='ROHR~*~*~*~QMAV'
                ...     )     
                >>> txt=axNfd.set_title('RL QMAV')
                >>> # ---
                >>> # Function as Attribute
                >>> # --------------------------
                >>> axNfd = fig.add_subplot(gs[1])              
                >>> Rm.Rm.pltNetPipes(vROHR
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])
                ...     )
                >>> txt=axNfd.set_title('RL QMAV Abs')
                >>> # --------------------------
                >>> # ---
                >>> # Mi/MaD zS auf
                >>> # --------------------------
                >>> axNfd = fig.add_subplot(gs[2])              
                >>> Rm.Rm.pltNetPipes(vROHR
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])
                ...     ,pAttributeColorMapMin=0.
                ...     ,pAttributeColorMapMax=1600.
                ...     ,CBLabel='Q [t/h]'            
                ...     ,sort_values_by=['pAttributeFunc'] 
                ...     ,sort_values_ascending=True                 
                ...     )
                >>> txt=axNfd.set_title('Mi/MaD zS auf')
                >>> # --------------------------
                >>> # ---
                >>> # ind. Kategorien 
                >>> # --------------------------
                >>> axNfd = fig.add_subplot(gs[3])           
                >>> cm = matplotlib.colors.ListedColormap(['cyan', 'royalblue', 'magenta', 'coral'])
                >>> cm.set_over('0.25')
                >>> cm.set_under('0.75')
                >>> bounds = [10.,100.,200.,800.,1600.]
                >>> norm = matplotlib.colors.BoundaryNorm(bounds, cm.N)
                >>> Rm.Rm.pltNetPipes(vROHR
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])     
                ...     ,pAttributeColorMap=cm
                ...     ,CBBinBounds=bounds                              
                ...     ,CBLabel='Q [t/h]'    
                ...     ,sort_values_by=['pAttributeFunc'] 
                ...     ,sort_values_ascending=True                   
                ...     )              
                >>> txt=axNfd.set_title('ind. Kategorien')
                >>> # --------------------------
                >>> # ---
                >>> # Unwichtiges ausblenden über 2nd Color
                >>> # --------------------------
                >>> vAGSN=xm.dataFrames['vAGSN']    
                >>> hpRL=vAGSN[(vAGSN['LFDNR']=='1') & (vAGSN['Layer']==2)]               
                >>> pDf=pd.merge(vROHR
                ...     ,hpRL[hpRL.IptIdx=='S'] # wg. Innenpunkte 
                ...     ,how='left'
                ...     ,left_on='pk'
                ...     ,right_on='OBJID'
                ...     ,suffixes=('','_AGSN')).filter(items=vROHR.columns.tolist()+['OBJID'])
                >>> axNfd = fig.add_subplot(gs[4])              
                >>> Rm.Rm.pltNetPipes(pDf
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])
                ...     ,pAttributeColorMapMin=0.
                ...     ,pAttributeColorMapMax=1500.
                ...     ,CBBinTicks=7 
                ...     ,CBLabel='Q [t/h]'    
                ...     ,sort_values_by=['pAttributeFunc'] 
                ...     ,sort_values_ascending=True       
                ...     ,pAttributeColorMapFmask=lambda row: True if not pd.isnull(row.OBJID) else False 
                ...     ,pAttributeColorMap2ndFmask=lambda row: True if pd.isnull(row.OBJID) else False                 
                ...     )
                >>> txt=axNfd.set_title('Unwichtiges ausblenden über 2nd Color')
                >>> # --------------------------
                >>> # ---
                >>> # Farbskalen an den Rändern abschneiden
                >>> # --------------------------              
                >>> axNfd = fig.add_subplot(gs[5])              
                >>> Rm.Rm.pltNetPipes(pDf
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])                
                ...     ,pAttributeColorMapMin=0.
                ...     ,pAttributeColorMapMax=1500.
                ...     ,CBLabel='Q [t/h]'    
                ...     ,sort_values_by=['pAttributeFunc'] 
                ...     ,sort_values_ascending=True       
                ...     ,pAttributeColorMapFmask=lambda row: True if not pd.isnull(row.OBJID) else False 
                ...     ,pAttributeColorMap2ndFmask=lambda row: True if pd.isnull(row.OBJID) else False 
                ...     ,pAttributeColorMap2ndUsageStart=.5/5. # nicht zu weiß 
                ...     ,pAttributeColorMap2ndUsageEnd=2.5/5. # nicht zu schwarz
                ...     ,pAttributeColorMapUsageStart=3/15.
                ...     ,pAttributeColorMapUsageEnd=12/15.                
                ...     )
                >>> txt=axNfd.set_title('Farbskalen an den Rändern abschneiden')
                >>> # --------------------------
                >>> # ---
                >>> # Farbskala diskretisieren
                >>> # --------------------------              
                >>> axNfd = fig.add_subplot(gs[6])              
                >>> Rm.Rm.pltNetPipes(pDf
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])                
                ...     ,pAttributeColorMapMin=0.
                ...     ,pAttributeColorMapMax=1500.
                ...     ,CBBinDiscrete=True 
                ...     ,CBLabel='Q [t/h]'    
                ...     ,sort_values_by=['pAttributeFunc'] 
                ...     ,sort_values_ascending=True       
                ...     ,pAttributeColorMapFmask=lambda row: True if not pd.isnull(row.OBJID) else False 
                ...     ,pAttributeColorMap2ndFmask=lambda row: True if pd.isnull(row.OBJID) else False        
                ...     ,pAttributeColorMap2ndUsageStart=.5/5. # nicht zu weiß 
                ...     ,pAttributeColorMap2ndUsageEnd=2.5/5. # nicht zu schwarz                
                ...     )
                >>> txt=axNfd.set_title('Farbskala diskretisieren')
                >>> # --------------------------
                >>> # ---
                >>> # Unterkategorien
                >>> # --------------------------              
                >>> catagoryCmap="tab10"
                >>> catagoryColors=[9,6,1]
                >>> nOfSubCatsReq=4
                >>> cm=Rm.pltMakeCategoricalCmap(catagoryCmap=catagoryCmap,catagoryColors=catagoryColors,nOfSubCatsReq=nOfSubCatsReq,reversedSubCatOrder=True)
                >>> axNfd = fig.add_subplot(gs[7])              
                >>> Rm.Rm.pltNetPipes(pDf
                ...     ,query="CONT_ID == '1001'"
                ...     ,fmask=lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False 
                ...     ,pAx=axNfd
                ...     ,pAttributeFunc=lambda row: math.fabs(row['ROHR~*~*~*~QMAV'])
                ...     ,pAttributeColorMap=cm
                ...     ,pAttributeColorMapMin=0.
                ...     ,pAttributeColorMapMax=1500.
                ...     ,CBBinTicks=4
                ...     ,CBLabel='Q [t/h]'    
                ...     ,sort_values_by=['pAttributeFunc'] 
                ...     ,sort_values_ascending=True       
                ...     ,pAttributeColorMapFmask=lambda row: True if not pd.isnull(row.OBJID) else False 
                ...     ,pAttributeColorMap2ndFmask=lambda row: True if pd.isnull(row.OBJID) else False     
                ...     ,pAttributeColorMap2ndUsageStart=.5/5. # nicht zu weiß 
                ...     ,pAttributeColorMap2ndUsageEnd=2.5/5. # nicht zu schwarz                
                ...     )
                >>> txt=axNfd.set_title('Unterkategorien')
                >>> # --------------------------
                >>> gs.tight_layout(fig)
                >>> plt.savefig('pltNetPipes.pdf',format='pdf',dpi=dpiSize*2)
        """
        logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
                keys = sorted(kwds.keys())
                
                # AXES
                if 'pAx' not in keys:
                    kwds['pAx']=plt.gca()
                
                # CB
                if 'CBFraction' not in keys:
                    kwds['CBFraction']=5 # in %
                if 'CBHpad' not in keys:
                    kwds['CBHpad']=0.05         
                if 'CBLabel' not in keys:
                    kwds['CBLabel']=None       
                # CB / Farbskala
                if 'CBBinTicks' not in keys:
                    kwds['CBBinTicks']=None         
                if 'CBBinDiscrete' not in keys:
                    kwds['CBBinDiscrete']=False     
                if  kwds['CBBinDiscrete']:
                    if kwds['CBBinTicks']==None:                                           
                        kwds['CBBinTicks']=4 # (d.h. 3 Kategorien)
                if 'CBBinBounds' not in keys:
                    kwds['CBBinBounds']=None
            
                # DATA
                if 'query' not in keys:
                    kwds['query']=None # Exp.: = "KVR_i=='2' & KVR_k=='2'"
                if 'fmask' not in keys:
                    kwds['fmask']=None # Exp.: =lambda row: True if row.KVR_i=='2' and row.KVR_k=='2' else False                    
                if 'sort_values_by' not in keys:
                    kwds['sort_values_by']=None  
                if 'sort_values_ascending' not in keys:
                    kwds['sort_values_ascending']=False                   

                # PIPE-Attribute
                if 'pAttribute' not in keys:                   
                    kwds['pAttribute']='Attribute'
                    if 'pAttributeFunc' not in keys:            
                        logger.debug("{:s}pAttribute: not specified?! 'Attribute' will be used. pAttributeFunc is also not specified?!".format(logStr))                  
                if 'pAttributeFunc' not in keys:                    
                    kwds['pAttributeFunc']=None     
                    
                # PIPE-Color
                if 'pAttributeColorMap' not in keys:
                    kwds['pAttributeColorMap']=plt.cm.cool                        
                if 'pAttributeColorMapMin' not in keys:           
                    kwds['pAttributeColorMapMin']=None
                if 'pAttributeColorMapMax' not in keys:
                    kwds['pAttributeColorMapMax']=None

                # Trunc Cmap
                if 'pAttributeColorMapUsageStart' not in keys and 'pAttributeColorMapUsageEnd' not in keys:
                    kwds['pAttributeColorMapTrunc']=False
                else:
                    kwds['pAttributeColorMapTrunc']=True
                if 'pAttributeColorMapUsageStart' not in keys:
                    kwds['pAttributeColorMapUsageStart']=0.     
                if 'pAttributeColorMapUsageEnd' not in keys:
                    kwds['pAttributeColorMapUsageEnd']=1.     

                # PIPE-Color 1st/2nd - FMasks
                if 'pAttributeColorMapFmask' not in keys:                    
                    kwds['pAttributeColorMapFmask']=lambda row: True           
                else:
                     logger.debug("{:s}Color 1st-PIPEs are filtered with fmask: {:s} ...".format(logStr,str(kwds['pAttributeColorMapFmask'])))   
                if 'pAttributeColorMap2ndFmask' not in keys:
                    kwds['pAttributeColorMap2ndFmask']=lambda row: False    
                else:
                    logger.debug("{:s}Color 2nd-PIPEs are filtered with fmask: {:s} ...".format(logStr,str(kwds['pAttributeColorMap2ndFmask'])))   
                    
                # PIPE-Color 2nd
                if 'pAttributeColorMap2nd' not in keys:
                    kwds['pAttributeColorMap2nd']=plt.cm.binary                        
                if 'pAttributeColorMap2ndMin' not in keys:
                    kwds['pAttributeColorMap2ndMin']=kwds['pAttributeColorMapMin']
                if 'pAttributeColorMap2ndMax' not in keys:
                    kwds['pAttributeColorMap2ndMax']=kwds['pAttributeColorMapMax']

                # Trunc Cmap
                if 'pAttributeColorMap2ndUsageStart' not in keys and 'pAttributeColorMap2ndUsageEnd' not in keys:
                    kwds['pAttributeColorMap2ndTrunc']=False
                else:
                    kwds['pAttributeColorMap2ndTrunc']=True

                if 'pAttributeColorMap2ndUsageStart' not in keys:
                    kwds['pAttributeColorMap2ndUsageStart']=0.  
                if 'pAttributeColorMap2ndUsageEnd' not in keys:
                    kwds['pAttributeColorMap2ndUsageEnd']=1.  

                # PIPE-Linestyle
                if 'pAttributeLs' not in keys:
                    kwds['pAttributeLs']='-'           

                # PIPE-Linesize
                if 'pAttrLineSize' not in keys:                    
                    kwds['pAttrLineSize']=None       
                if 'pAttrLineSizeFactor' not in keys:
                    kwds['pAttrLineSizeFactor']=None  

                # PIPE-Geometry
                if 'pWAYPXCors' not in keys:
                    kwds['pWAYPXCors']='pWAYPXCors'
                if 'pWAYPYCors' not in keys:
                    kwds['pWAYPYCors']='pWAYPYCors'
                if 'pClip' not in keys:
                    kwds['pClip']=True

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                     
        
        try: 
                               
            # ggf. filtern
            if kwds['query'] != None:                    
                logger.debug("{:s}pDf is filtered with query: {:s} ...".format(logStr,str(kwds['query'])))   
                pDf=pd.DataFrame(pDf.query(kwds['query']).values,columns=pDf.columns)
            if kwds['fmask'] != None:
                logger.debug("{:s}pDf is filtered with fmask: {:s} ...".format(logStr,str(kwds['fmask'])))   
                pDf=pd.DataFrame(pDf[pDf.apply(kwds['fmask'],axis=1)].values,columns=pDf.columns)         
                              
            # ggf. zu plottende Spalte(n) neu ausrechnen bzw. Plotreihenfolge ändern: Kopie erstellen
            if kwds['pAttributeFunc'] != None or kwds['sort_values_by'] != None:
                # Kopie!
                logger.debug("{:s}pDf is copied ...".format(logStr))   
                pDf=pDf.copy(deep=True)              
        
            # ggf. zu plottende Spalte(n) neu ausrechnen
            if kwds['pAttributeFunc'] != None:                 
                logger.debug("{:s}pAttribute: col '{:s}' is not used: ...".format(logStr,kwds['pAttribute']))  
                logger.debug("{:s}... pAttributeFunc {:s} is used to calculate a new col named 'pAttributeFunc'".format(logStr,str(kwds['pAttributeFunc'])))               
                pDf['pAttributeFunc']=pDf.apply(kwds['pAttributeFunc'],axis=1)
                kwds['pAttribute']='pAttributeFunc'
            logger.debug("{:s}col '{:s}' is used as Attribute.".format(logStr,kwds['pAttribute']))  
            
            # Label für CB
            if kwds['CBLabel'] == None:
                kwds['CBLabel']=kwds['pAttribute']

            # Spalte für Liniendicke ermitteln
            if kwds['pAttrLineSize'] == None:
                kwds['pAttrLineSize']=kwds['pAttribute']
            logger.debug("{:s}col '{:s}' is used as  LineSize.".format(logStr,kwds['pAttrLineSize']))  
            # Liniendicke skalieren  
            if kwds['pAttrLineSizeFactor']==None:
                kwds['pAttrLineSizeFactor']=1./(pDf[kwds['pAttrLineSize']].std()*2.)    
            logger.debug("{:s}Faktor Liniendicke: {:12.6f} - eine Linie mit Attributwert {:6.2f} wird in {:6.2f} Pts Dicke geplottet.".format(logStr
                                                                                                                                       ,kwds['pAttrLineSizeFactor']
                                                                                                                                       ,pDf[kwds['pAttrLineSize']].std()*2.
                                                                                                                                       ,kwds['pAttrLineSizeFactor']*pDf[kwds['pAttrLineSize']].std()*2.
                                                                                                                                       ))  
            logger.debug("{:s}min. Liniendicke: Attributwert {:9.2f} Pts: {:6.2f}.".format(logStr
                                                                                   ,math.fabs(pDf[kwds['pAttrLineSize']].min())
                                                                                   ,kwds['pAttrLineSizeFactor']*math.fabs(pDf[kwds['pAttrLineSize']].min()))
                                                                                   )
            logger.debug("{:s}max. Liniendicke: Attributwert {:9.2f} Pts: {:6.2f}.".format(logStr
                                                                                   ,math.fabs(pDf[kwds['pAttrLineSize']].max())
                                                                                   ,kwds['pAttrLineSizeFactor']*math.fabs(pDf[kwds['pAttrLineSize']].max()))
                                                                                   )
                                                                               
            # ggf. Plotreihenfolge ändern
            if kwds['sort_values_by'] != None:            
                logger.debug("{:s}pDf is sorted (=Plotreihenfolge) by {:s} ascending={:s}.".format(logStr,str(kwds['sort_values_by']),str(kwds['sort_values_ascending'])))  
                pDf.sort_values(by=kwds['sort_values_by'],ascending=kwds['sort_values_ascending'],inplace=True)
                
            # x,y-Achsen: Lims ermitteln und setzen                                          
            xMin=0          
            yMin=0
            xMax=0          
            yMax=0
            for xs,ys in zip(pDf[kwds['pWAYPXCors']],pDf[kwds['pWAYPYCors']]):
                xMin=min(xMin,min(xs))
                yMin=min(yMin,min(ys))
                xMax=max(xMax,max(xs))
                yMax=max(yMax,max(ys))                                                 
            logger.debug("{:s}pWAYPXCors: {:s} Min: {:6.2f} Max: {:6.2f}".format(logStr,kwds['pWAYPXCors'],xMin,xMax))   
            logger.debug("{:s}pWAYPYCors: {:s} Min: {:6.2f} Max: {:6.2f}".format(logStr,kwds['pWAYPYCors'],yMin,yMax))  
            dx=xMax-xMin
            dy=yMax-yMin
            dxdy=dx/dy
            dydx=1./dxdy
        
            kwds['pAx'].set_xlim(left=xMin)
            kwds['pAx'].set_ylim(bottom=yMin)
            kwds['pAx'].set_xlim(right=xMax)
            kwds['pAx'].set_ylim(top=yMax)    
        
            # x,y-Seitenverhältnisse ermitteln  (derzeit nur zu DEBUG-/INFO-Zwecken)           
            # total figure size
            figW, figH = kwds['pAx'].get_figure().get_size_inches()
            # Axis size on figure
            x0, y0, w, h = kwds['pAx'].get_position().bounds
            # Ratio of display units
            disp_ratio = (figH * h) / (figW * w)
            # Ratio of data units
            data_ratio=kwds['pAx'].get_data_ratio()
            #logger.debug("{:s}figH: {:6.2f} figW: {:6.2f}".format(logStr,figW,figH))  
            #logger.debug("{:s}x0: {:6.2f} y0: {:6.2f} w: {:6.2f} h: {:6.2f}".format(logStr,x0,y0,w,h))  
            #logger.debug("{:s}pWAYPCors: Y/X: {:6.2f}".format(logStr,dydx))  
            #logger.debug("{:s}disp_ratio: {:6.2f} data_ratio: {:6.2f}".format(logStr,disp_ratio,data_ratio))  
      
            # x,y-Achsen: Ticks ermitteln und setzen         
            xTicks=kwds['pAx'].get_xticks()
            dxTick = xTicks[1]-xTicks[0]
            yTicks=kwds['pAx'].set_yticks([idx*dxTick for idx in range(math.floor(dy/dxTick)+1)])   
            kwds['pAx'].grid()
                                 
            # PIPE-Color: Farbskalamapping:
            cMap=plt.cm.get_cmap(kwds['pAttributeColorMap'])
            if kwds['CBBinDiscrete'] and hasattr(cMap,'from_list'): # diskrete Farbskala aus kontinuierlicher erzeugen                                
                N=kwds['CBBinTicks']-1
                color_list = cMap(np.linspace(0, 1, N))
                cmap_name = cMap.name + str(N)
                kwds['pAttributeColorMap']=cMap.from_list(cmap_name, color_list, N)            
            
            minAttr=pDf[kwds['pAttribute']].min()      
            maxAttr=pDf[kwds['pAttribute']].max()  
            if kwds['pAttributeColorMapMin'] != None:
                minLine=kwds['pAttributeColorMapMin']
            else:
                minLine=minAttr
            if kwds['pAttributeColorMapMax'] != None:
                maxLine=kwds['pAttributeColorMapMax']
            else:
                maxLine=maxAttr                  
            logger.debug("{:s}Attribute: minLine (used for CM-Scaling): {:8.2f} min (Data): {:8.2f}".format(logStr,minLine,minAttr))
            logger.debug("{:s}Attribute: maxLine (used for CM-Scaling): {:8.2f} max (Data): {:8.2f}".format(logStr,maxLine,maxAttr))

            # Norm
            normLine=colors.Normalize(minLine,maxLine)

            # kont. Farbskala truncated: Farbskala und Norm anpassen
            cMap=plt.cm.get_cmap(kwds['pAttributeColorMap'])   
            if kwds['pAttributeColorMapTrunc'] and hasattr(cMap,'from_list'):   

                #
                usageStartLineValue=minLine+kwds['pAttributeColorMapUsageStart']*(maxLine-minLine)
                usageStartLineColor=kwds['pAttributeColorMap'](normLine(usageStartLineValue)) 
                logger.debug("{:s}pAttributeColorMapUsageStart: {:6.2f} ==> usageStartLineValue: {:8.2f} (minLine: {:8.2f}) color: {:s}".format(logStr
                                                                                                                                    ,kwds['pAttributeColorMapUsageStart']
                                                                                                                                    ,usageStartLineValue,minLine,str(usageStartLineColor)))
                #
                usageEndLineValue=maxLine-(1.-kwds['pAttributeColorMapUsageEnd'])*(maxLine-minLine)
                usageEndLineColor=kwds['pAttributeColorMap'](normLine(usageEndLineValue)) 
                logger.debug("{:s}pAttributeColorMapUsageEnd:   {:6.2f} ==> usageEndLineValue:   {:8.2f} (maxLine: {:8.2f}) color: {:s}".format(logStr
                                                                                                                                    ,kwds['pAttributeColorMapUsageEnd']                                          
                                                                                                                                    ,usageEndLineValue,maxLine,str(usageEndLineColor)))
            
                nColors=100
                kwds['pAttributeColorMap'] = colors.LinearSegmentedColormap.from_list(
                'trunc({n},{a:.2f},{b:.2f})'.format(n=cMap.name, a=kwds['pAttributeColorMapUsageStart'], b=kwds['pAttributeColorMapUsageEnd'])
                ,cMap(np.linspace(kwds['pAttributeColorMapUsageStart'],kwds['pAttributeColorMapUsageEnd'],nColors)))
                
                normLine=colors.Normalize(max(minLine,usageStartLineValue),min(maxLine,usageEndLineValue))
            
            # diskrete Farbskala mit individuellen Kategorien: Norm anpassen
            
            cMap=plt.cm.get_cmap(kwds['pAttributeColorMap'])   
            if kwds['CBBinBounds'] != None and not hasattr(cMap,'from_list'): # diskrete Farbskala liegt vor und Bounds sind vorgegeben
                normLine = colors.BoundaryNorm(kwds['CBBinBounds'],cMap.N)
                CBPropExtend='both'
            else:
                CBPropExtend='neither'
                
            # PIPE-Color 2nd: Farbskalamapping:        
            if kwds['pAttributeColorMap2ndMin'] != None:
                minLine2nd=kwds['pAttributeColorMap2ndMin']
            else:
                minLine2nd=minAttr
            if kwds['pAttributeColorMap2ndMax'] != None:
                maxLine2nd=kwds['pAttributeColorMap2ndMax']
            else:
                maxLine2nd=maxAttr                  
            logger.debug("{:s}Attribute: minLine2nd (used for CM-Scaling): {:8.2f} min (Data): {:8.2f}".format(logStr,minLine2nd,minAttr))
            logger.debug("{:s}Attribute: maxLine2nd (used for CM-Scaling): {:8.2f} max (Data): {:8.2f}".format(logStr,maxLine2nd,maxAttr))

            # Norm
            normLine2nd=colors.Normalize(minLine2nd,maxLine2nd)

            # kont. Farbskala truncated: Farbskala anpassen
            cMap=plt.cm.get_cmap(kwds['pAttributeColorMap2nd'])   
            if kwds['pAttributeColorMap2ndTrunc'] and hasattr(cMap,'from_list'):   

                #
                usageStartLineValue2nd=minLine2nd+kwds['pAttributeColorMap2ndUsageStart']*(maxLine2nd-minLine2nd)
                logger.debug("{:s}pAttributeColorMap2ndUsageStart: {:8.2f} ==> usageStartLineValue2nd: {:8.2f} (minLine2nd: {:8.2f})".format(logStr,kwds['pAttributeColorMap2ndUsageStart'],usageStartLineValue2nd,minLine2nd))
                usageStartLineColor2nd=kwds['pAttributeColorMap2nd'](normLine2nd(usageStartLineValue2nd))      
                #
                usageEndLineValue2nd=maxLine2nd-(1.-kwds['pAttributeColorMap2ndUsageEnd'])*(maxLine2nd-minLine2nd)
                logger.debug("{:s}pAttributeColorMap2ndUsageEnd:   {:8.2f} ==> usageEndLineValue2nd:   {:8.2f} (maxLine2nd: {:8.2f})".format(logStr,kwds['pAttributeColorMap2ndUsageEnd'],usageEndLineValue2nd,maxLine2nd))
                usageEndLineColor2nd=kwds['pAttributeColorMap2nd'](normLine2nd(usageEndLineValue2nd))      


                nColors=100
                kwds['pAttributeColorMap2nd'] = colors.LinearSegmentedColormap.from_list(
                'trunc({n},{a:.2f},{b:.2f})'.format(n=cMap.name, a=kwds['pAttributeColorMap2ndUsageStart'], b=kwds['pAttributeColorMap2ndUsageEnd'])
                ,cMap(np.linspace(kwds['pAttributeColorMap2ndUsageStart'],kwds['pAttributeColorMap2ndUsageEnd'],nColors)))
          
            # PIPE-Color 2nd: PLOT           
            pDfColorMap2nd=pDf[pDf.apply(kwds['pAttributeColorMap2ndFmask'],axis=1)]
            (rows   ,cols)=pDf.shape
            (rows2nd,cols)=pDfColorMap2nd.shape
            logger.debug("{:s}Color 2nd-PIPEs: {:d} von {:d}".format(logStr,rows2nd,rows))   
            for xs,ys,vLine,tLine in zip(pDfColorMap2nd[kwds['pWAYPXCors']],pDfColorMap2nd[kwds['pWAYPYCors']],pDfColorMap2nd[kwds['pAttribute']],pDfColorMap2nd[kwds['pAttrLineSize']]):        


                #if vLine >= usageStartLineValue2nd and vLine <= usageEndLineValue2nd:
                #    colorLine=kwds['pAttributeColorMap2nd'](normLine2nd(vLine))                     
                #elif vLine > usageEndLineValue2nd:
                #    colorLine=usageEndLineColor2nd                   
                #else:
                #    colorLine=usageStartLineColor2nd        
                    
                colorLine=kwds['pAttributeColorMap2nd'](normLine2nd(vLine))     

                pcLines=kwds['pAx'].plot(xs,ys
                                ,color=colorLine
                                ,linewidth=kwds['pAttrLineSizeFactor']*math.fabs(tLine)#(vLine) 
                                ,ls=kwds['pAttributeLs']
                                ,solid_capstyle='round'                             
                                ,aa=True
                                ,clip_on=kwds['pClip']
                               )  
                  
            # PIPE-Color: PLOT            
            pDfColorMap=pDf[pDf.apply(kwds['pAttributeColorMapFmask'],axis=1)]  
            (rows   ,cols)=pDf.shape
            (rows1st,cols)=pDfColorMap.shape
            colorsCBValues=[]
            logger.debug("{:s}Color 1st-PIPEs: {:d} von {:d}".format(logStr,rows1st,rows))               
            for xs,ys,vLine,tLine in zip(pDfColorMap[kwds['pWAYPXCors']],pDfColorMap[kwds['pWAYPYCors']],pDfColorMap[kwds['pAttribute']],pDfColorMap[kwds['pAttrLineSize']]):        

                #if vLine >= usageStartLineValue and vLine <= usageEndLineValue:
                #    colorLine=kwds['pAttributeColorMap'](normLine(vLine))      
                #    value=vLine
                #elif vLine > usageEndLineValue:
                #    colorLine=usageEndLineColor   
                #    value=usageEndLineValue
                #else:
                #    colorLine=usageStartLineColor   
                #    value=usageStartLineValue
                               
                colorLine=kwds['pAttributeColorMap'](normLine(vLine))                      
                colorsCBValues.append(vLine)           
                
                pcLines=kwds['pAx'].plot(xs,ys
                                ,color=colorLine
                                ,linewidth=kwds['pAttrLineSizeFactor']*math.fabs(tLine)#(vLine) 
                                ,ls=kwds['pAttributeLs']
                                ,solid_capstyle='round'                             
                                ,aa=True
                                ,clip_on=kwds['pClip']
                               )   
            

            # PIPE-Color: PLOT der PIPE-Anfänge um Farbskala konstruieren zu koennen      
            s=kwds['pAttrLineSizeFactor']*pDfColorMap[kwds['pAttrLineSize']].apply(lambda x: math.fabs(x))     
            s=s.apply(lambda x: math.pow(x,2))  # https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size   
            pcN=kwds['pAx'].scatter(pDfColorMap['pXCor_i'],pDfColorMap['pYCor_i']                          
                    ,s=s
                    ,linewidth=0 # the linewidth of the marker edges
                    # Farbskala
                    ,cmap=kwds['pAttributeColorMap']
                    # Normierung Farbe                
                    ,norm=normLine
                    # Werte
                    ,c=colorsCBValues                                       
                    ,edgecolors='none'
                    ,clip_on=kwds['pClip']
                    )        
        
            # CB: Axes         
            divider = make_axes_locatable(kwds['pAx'])
            cax = divider.append_axes('right',size="{:f}%".format(kwds['CBFraction']),pad=kwds['CBHpad'])
            x0, y0, w, h = kwds['pAx'].get_position().bounds
            #logger.debug("{:s}ohne Änderung?!: x0: {:6.2f} y0: {:6.2f} w: {:6.2f} h: {:6.2f}".format(logStr,x0,y0,w,h))  
            kwds['pAx'].set_aspect(1.) #!
            x0, y0, w, h = kwds['pAx'].get_position().bounds
            #logger.debug("{:s}ohne Änderung?!: x0: {:6.2f} y0: {:6.2f} w: {:6.2f} h: {:6.2f}".format(logStr,x0,y0,w,h))  
                      
            # CB
            cB=plt.gcf().colorbar(pcN, cax=cax, orientation='vertical',extend=CBPropExtend,spacing='proportional') 





            cB.set_label(kwds['CBLabel'])

            # CB Ticks
            if kwds['CBBinTicks'] != None:
                cB.set_ticks(np.linspace(minLine,maxLine,kwds['CBBinTicks']))
                
            ticks=cB.get_ticks()     
            try:
                ticks=np.unique(np.append(ticks,[usageStartLineValue,usageEndLineValue]))
            except:
                pass
            cB.set_ticks(ticks)  

            # CB Ticklabels
            labels=cB.ax.get_yticklabels()

            if kwds['pAttributeColorMapUsageStart'] > 0:
                idx=np.where(ticks == usageStartLineValue)
                labels[idx[0][0]].set_text(labels[idx[0][0]].get_text()+" v=")
            if kwds['pAttributeColorMapUsageEnd'] < 1:
                idx=np.where(ticks == usageEndLineValue)
                labels[idx[0][0]].set_text(labels[idx[0][0]].get_text()+" ^=")

           
            if kwds['pAttributeColorMapMax'] != None and maxLine<maxAttr:
                labels[-1].set_text(labels[-1].get_text()+" >=")
            if kwds['pAttributeColorMapMin'] != None and minLine>minAttr:
                labels[0].set_text(labels[0].get_text()+" <=")
            cB.ax.set_yticklabels(labels)  
                                                                    
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                       
        finally:       
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                   

    def __init__(self,xm=None,mx=None): 
        """
        Args:
            xm: Xm.Xm Object
            mx: Mx.Mx Object
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.xm=xm
            self.mx=mx
 
            try:
                vNRCV_Mx1=self.xm.dataFrames['vNRCV_Mx1'] # d.h. Sachdaten bereits annotiert mit MX1-Wissen 
            except:
                logger.debug("{:s}{:s} not in {:s}. Sachdaten mit MX1-Wissen zu annotieren wird nachgeholt ...".format(logStr,'vNRCV_Mx1','dataFrames'))
                self.xm.MxSync(mx=self.mx)                      
                                                       
        except RmError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def pltNetDHUS(self,**kwds):
        """Plot: Net: DistrictHeatingUnderSupply. 

        Args (optional):

            TIMEs (als TIMEDELTA zu Szenariumbeginn):
                * timeDeltaToRef: Reference Scenariotime (for MeasureInRefPerc-Calculations) (default: pd.to_timedelta('0 seconds'))
                * timeDeltaToT: Scenariotime (default: pd.to_timedelta('0 seconds'))

            FWVB
               * pFWVBFilterFunction: Filterfunction to be applied to FWVB to determine the FWVB to be plotted
                    * default: lambda df: (df.CONT_ID.astype(int).isin([1001])) & (df.W0LFK>0)
                        * CONT_IDisIn: [1001]
                            * um zu vermeiden, dass FWVB aus Bloecken gezeichnet werden (unwahrscheinlich, dass es solche gibt)    
                        * W0LFK>0:
                            * um zu vermeiden, dass versucht wird, FWVB mit der Soll-Leistung 0 zu zeichnen (pFWVBAttribute default is 'W0LFK')              

            FWVB Attribute (Size, z-Order)
                * pFWVBAttribute: columnName (default: 'W0LFK') 

                    * the column must be able to be converted to a float
                    * the conversion is done before FilterFunction 
                    * see ApplyFunction and NaNValue for conversion details:
                        * pFWVBAttributeApplyFunction: Function to be applied to column pFWVBAttribute 
                                            * default: lambda x: pd.to_numeric(x,errors='coerce')                                    
                        * pFWVBAttributeApplyFunctionNaNValue: Value for NaN-Values produced by pFWVBAttributeApplyFunction if any  
                                            * default: 0
                                            * .fillna(pFWVBAttributeApplyFunktionNaNValue).astype(float) is called after ApplyFunction

                * pFWVBAttributeAsc: z-Order (default: False d.h. "kleine auf große")
                * pFWVBAttributeRefSize: scatter Sy-Area in pts^2 of for RefSizeValue (default: 10**2)  
                      
                    * corresponding RefSizeValue is Attribute.std() or Attribute.mean() if Attribute.std() is < 1

            FWVB (plot only large (small, medium) FWVB ...)
               * quantil_pFWVBAttributeHigh <= (default: 1.) 
               * quantil_pFWVBAttributeLow >= (default: .0)
               * default: all FWVB are plotted 
               * note that Attribute >0 is a precondition 

            FWVB Measure (Color)
                * pFWVBMeasure (default: 'FWVB~*~*~*~W') 

                    * float() must be possible                

                * pFWVBMeasureInRefPerc (default: True d.h. Measure wird verarbeitet in Prozent T zu Ref) 

                    * 0-1
                    * if refValue is 0 than refPerc-Result is set to 1 

                * pFWVBMeasureAlpha/Colormap/Clip

                * 3Classes

                    * pFWVBMeasure3Classes (default: False)
                        * False:
                            * Measure wird nicht in 3 Klassen dargestellt
                            * die Belegung von MCategory gemaess FixedLimitsHigh/Low erfolgt dennoch

                    * CatTexts (werden verwendet wenn 3Classes Wahr gesetzt ist)

                        * für CBLegend (3Classes) als _zusätzliche Beschriftung rechts
                        * als Texte für die Spalte MCategory in return pFWVB

                        * pMCatTopText
                        * pMCatMidText
                        * pMCatBotText

                    * CatAttribs (werden verwendet wenn 3Classes Wahr gesetzt ist)

                        * für die Knotendarstellung                        

                        * pMCatTopAlpha/Color/Clip
                        * pMCatMidAlpha/Colormap/Clip
                        * pMCatBotAlpha/Color/Clip
                                   
                * CBFixedLimits 
                
                    * pFWVBMeasureCBFixedLimits (default: False d.h. Farbskala nach vorh. min./max. Wert)

                        * wird Wahr gesetzt sein, wenn 3Classes Wahr gesetzt ist
                        * damit die mittlere Farbskala den Klassengrenzen "gehorcht"

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
                * CBLe3cMidVPad (default: .5)                                                                         
                * CBLe3cBotVPad (default: 0-1*1/4)
                
                    * 1 is the height of the Colorbar                                                                   
                    * the VPads (the vertical Sy-Positions) are defined in cax.transAxes Coordinates    
                    * cax is the Colorbar Axes               

                * CBLe3cSySize=10**2 (Sy-Area in pts^2)
                * CBLe3cSyType='o' 

            ROHR
               * pROHRFilterFunction: Filterfunction to be applied to PIPEs to determine the PIPEs to be plotted
                    * default: lambda df: (df.KVR.astype(int).isin([2])) & (df.CONT_ID.astype(int).isin([1001])) & (df.DI>0)
                        * KVRisIn: [2]
                            * 1: supply-line
                            * 2: return-line                                       
                        * CONT_IDisIn: [1001]
                            * um zu vermeiden, dass Rohre aus Bloecken gezeichnet werden (deren Koordinaten nicht zu den Koordinaten von Rohren aus dem Ansichtsblock passen)    
                        * DI>0:
                            * um zu vermeiden, dass versucht wird, Rohre mit dem Innendurchmesser 0 zu zeichnen (pROHRAttribute default is 'DI')              

            ROHR (PIPE-Line: Size and Color, z-Order)   
                * pROHRAttribute: columnName (default: 'DI')
                    * the column must be able to be converted to a float
                    * the conversion is done before FilterFunction 
                    * see ApplyFunction and NaNValue for conversion details:
                        * pROHRAttributeApplyFunction: Function to be applied to column pROHRAttribute 
                                            * default: lambda x: pd.to_numeric(x,errors='coerce')                                    
                        * pROHRAttributeApplyFunctionNaNValue: Value for NaN-Values produced by pROHRAttributeApplyFunction if any  
                                            * default: 0
                                            * .fillna(pROHRAttributeApplyFunktionNaNValue).astype(float) is called after ApplyFunction
      
                * pROHRAttributeAsc: z-Order (default: False d.h. "kleine auf grosse")                                               

                * pROHRAttributeLs (default: '-')
                * pROHRAttributeRefSize: plot linewidth in pts for RefSizeValue (default: 1.0)      

                    * corresponding RefSizeValue is Attribute.std() or Attribute.mean() if Attribute.std() is < 1

                * pROHRAttributeColorMap (default: plt.cm.binary)    
                * pROHRAttributeColorMapUsageStart (default: 1./3; Wertebereich: [0,1])        

                    * Farbskala nach vorh. min./max. Wert
                    * die Farbskala wird nur ab UsageStart genutzt
                    * d.h. Werte die eine "kleinere" Farbe haetten, bekommen die Farbe von UsageStart

            ROHR (plot only large (small, medium) pipes ...)
               * quantil_pROHRAttributeHigh <= (default: 1.) 
               * quantil_pROHRAttributeLow >= (default: .75)
               * default: only the largest 25% are plotted 
               * note that Attribute >0 is a precondition 

            ROHR (PIPE-Marker: Size and Color)
                * pROHRMeasure columnName (default: 'ROHR~*~*~*~QMAV') 
                * pROHRMeasureApplyFunction: Function to be applied to column pROHRMeasure (default: lambda x: math.fabs(x))  
                
                * pROHRMeasureMarker (default: '.')
                * pROHRMeasureRefSize: plot markersize for RefSizeValue in pts (default: 1.0)
                    
                        * corresponding RefSizeValue is Measure.std() or Measure.mean() if Measure.std() is < 1                        
                        * if pROHRMeasureRefSize is None: plot markersize will be plot linewidth

                * pROHRMeasureColorMap (default: plt.cm.cool) 
                * pROHRMeasureColorMapUsageStart (default: 0.; Wertebereich: [0,1])        

                    * Farbskala nach vorh. min./max. Wert
                    * die Farbskala wird nur ab UsageStart genutzt
                    * d.h. Werte die eine "kleinere" Farbe hätten, bekommen die Farbe von UsageStart
               
            NRCVs - NumeRiCal Values to be displayed
                * pFIGNrcv: List of Sir3sID RegExps to be displayed (i.e. ['KNOT~PKON-Knoten~\S*~\S+~QM']) default: None
                    the 1st Match is used if a RegExp matches more than 1 Channel
                    
                    further Examples for RegExps (and corresponding Texts):
                        * WBLZ~WärmeblnzGes~\S*~\S+~WES (Generation)
                        * WBLZ~WärmeblnzGes~\S*~\S+~WVB (Load)
                        * WBLZ~WärmeblnzGes~\S*~\S+~WVERL (Loss)

                    WBLZ~[\S ]+~\S*~\S+~\S+: Example for a RegExp matching all Channels with OBJTYPE WBLZ  

                * pFIGNrcvTxt: corresponding (same length required!) List of Texts (i.e. ['Kontrolle DH']) default: None
                    
                * pFIGNrcvFmt (i.e. '{:12s}: {:8.2f} {:6s}')
                    * Text (from pFIGNrcvTxt)
                    * Value
                    * UNIT (determined from Channel-Data)

                * pFIGNrcvPercFmt (i.e. ' {:6.1f}%')                   
                    * ValueInRefPercent
                    * if refValue==0: 100% 

                * pFIGNrcvXStart (.5 default)
                * pFIGNrcvYStart (.5 default)

            Category - User Heat Balances to be displayed
                * pFWVBGCategory: List of Heat Balances to be displayed (i.e. ['BLNZ1u5u7']) default: None
                * pFWVBGCategoryUnit:  Unit of all these Balances (default: '[kW]'])               
                * pFWVBGCategoryXStart (.1 default)
                * pFWVBGCategoryYStart (.9 default)

                * pFWVBGCategoryCatFmt (i.e. '{:12s}: {:6.1f} {:4s}')
                    * Category NAME
                    * Category Load
                    * pFWVBGCategoryUnit                   

                * pFWVBGCategoryPercFmt (i.e. ' {:6.1f}%')                   
                    * Last Ist/Soll
                    
                * pFWVBGCategory3cFmt (i.e. ' {:5d}/{:5d}/{:5d}')
                    * NOfTops
                    * NOfMids
                    * NOfBots                
                                       
            VICs - VeryImportantCustomers whose Values to be displayed
                * pVICsDf: DataFrame with VeryImportantCustomers (Text & Specification)
                    columns expected:
                        * Kundenname (i.e. 'VIC1') - Text
                        * Knotenname (i.e. 'V-K007') - Specification by Supply-Node

                    i.e.: pd.DataFrame({'Kundenname': ['VIC1'],'Knotenname': ['V-K007']})

                 * pVICsPercFmt (i.e. '{:12s}: {:6.1f}%')
                    * Kundenname
                    * Load in Percent to Reference

                 * pVICsFmt (i.e. '{:12s}: {:6.1f} {:6s}')
                    * Kundenname
                    * Load
                    * pFWVBGCategoryUnit

                * pVICsXStart (.5 default)
                * pVICsYStart (.1 default)              

            Figure:
                * pltTitle: title [not suptitle] (default: 'pltNetFigAx') 
                * figFrameon: figure frame (background): displayed or invisible (default: True)
                * figEdgecolor: edge color of the Figure rectangle (default: 'black')
                * figFacecolor: face color of the Figure rectangle (default: 'white')

            Returns:
                pFWVB
                    * columns changed (compared to vFWVB):
                        * pFWVBAttribute (wg. z.B. pFWVBAttributeApplyFunction und .astype(float))

                    * columns added (compared to vFWVB):
                        * Measure (in % zu Ref wenn pFWVBMeasureInRefPer=True) 
                        * MeasureRef (Wert von Measure im Referenzzustand)
                        * MeasureOrig (Wert von Measure)

                        * MCategory: str (Kategorisierung von Measure mit FixedLimitHigh/Low-Werten):                           
                                * TopText or
                                * MidText or
                                * BotText
                            
                        * GCategory: list (non-empty only if req. GCategories are a subset of the available Categories and object belongs to a req. Category)
                        * VIC (filled with Kundenname from pVICsDf)

                    * rows (compared to vFWVB):
                        * pFWVB enthaelt dieselben Objekte wie vFWVB
                        * aber: die geplotteten Objekte sind ggf. nur eine Teilmenge (wg. z.B. pFWVBFilterFunction) 
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            
            keysDefined=['CBAnchorHorizontal', 'CBAnchorVertical', 'CBAspect', 'CBFraction', 'CBHpad', 'CBLabelPad'
                         ,'CBLe3cBotVPad', 'CBLe3cMidVPad', 'CBLe3cSySize', 'CBLe3cSyType', 'CBLe3cTopVPad'
                         ,'CBShrink', 'CBTicklabelsHPad'

                         ,'figEdgecolor', 'figFacecolor', 'figFrameon'
                         
                         ,'pFIGNrcv','pFIGNrcvFmt', 'pFIGNrcvPercFmt','pFIGNrcvTxt', 'pFIGNrcvXStart', 'pFIGNrcvYStart'
                         
                         ,'pFWVBFilterFunction'
                         ,'pFWVBAttribute'
                         ,'pFWVBAttributeApplyFunction','pFWVBAttributeApplyFunctionNaNValue'
                         ,'pFWVBAttributeAsc'
                         ,'pFWVBAttributeRefSize'
                         
                         ,'pFWVBGCategory', 'pFWVBGCategoryUnit','pFWVBGCategory3cFmt','pFWVBGCategoryCatFmt', 'pFWVBGCategoryPercFmt', 'pFWVBGCategoryXStart', 'pFWVBGCategoryYStart'
                         
                         ,'pFWVBMeasure', 'pFWVBMeasure3Classes', 'pFWVBMeasureAlpha', 'pFWVBMeasureCBFixedLimitHigh', 'pFWVBMeasureCBFixedLimitLow', 'pFWVBMeasureCBFixedLimits', 'pFWVBMeasureClip', 'pFWVBMeasureColorMap', 'pFWVBMeasureInRefPerc'
                         ,'pMCatBotAlpha', 'pMCatBotClip', 'pMCatBotColor', 'pMCatBotText', 'pMCatMidAlpha', 'pMCatMidClip', 'pMCatMidColorMap', 'pMCatMidText', 'pMCatTopAlpha', 'pMCatTopClip', 'pMCatTopColor', 'pMCatTopText'
                         
                         ,'pROHRFilterFunction'                        
                         ,'pROHRAttribute'
                         ,'pROHRAttributeApplyFunction','pROHRAttributeApplyFunctionNaNValue'
                         ,'pROHRAttributeAsc', 'pROHRAttributeColorMap', 'pROHRAttributeColorMapUsageStart', 'pROHRAttributeLs', 'pROHRAttributeRefSize'
                         
                         ,'pROHRMeasure','pROHRMeasureApplyFunction'
                         ,'pROHRMeasureColorMap', 'pROHRMeasureColorMapUsageStart', 'pROHRMeasureMarker', 'pROHRMeasureRefSize'

                         ,'pVICsDf','pVICsPercFmt','pVICsFmt','pVICsXStart', 'pVICsYStart'
                         ,'pltTitle'
                         
                         ,'quantil_pFWVBAttributeHigh', 'quantil_pFWVBAttributeLow'
                         
                         ,'quantil_pROHRAttributeHigh', 'quantil_pROHRAttributeLow'
                         
                         ,'timeDeltaToRef', 'timeDeltaToT']

            keys=sorted(kwds.keys())
            for key in keys:
                if key in keysDefined:
                    value=kwds[key]
                    logger.debug("{0:s}kwd {1:s}: {2:s}".format(logStr,key,str(value))) 
                else:
                    logger.warning("{0:s}kwd {1:s} NOT defined!".format(logStr,key)) 
                    del kwds[key]

            # TIMEs
            if 'timeDeltaToRef' not in keys:
                kwds['timeDeltaToRef']=pd.to_timedelta('0 seconds')
            if 'timeDeltaToT' not in keys:
                kwds['timeDeltaToT']=pd.to_timedelta('0 seconds')

            # FWVB
            if 'pFWVBFilterFunction' not in keys:
                kwds['pFWVBFilterFunction']=lambda df: (df.CONT_ID.astype(int).isin([1001])) & (df.W0LFK.astype(float)>0)

            # FWVB Attribute (Size)
            if 'pFWVBAttribute' not in keys:
                kwds['pFWVBAttribute']='W0LFK'
            if 'pFWVBAttributeApplyFunction' not in keys:
                kwds['pFWVBAttributeApplyFunction']=lambda x: pd.to_numeric(x,errors='coerce') # .apply(kwds['pFWVBAttributeApplyFunktion'])
            if 'pFWVBAttributeApplyFunctionNaNValue' not in keys:
                kwds['pFWVBAttributeApplyFunctionNaNValue']=0 # .fillna(kwds['pFWVBAttributeApplyFunktionNaNValue']).astype(float)

            if 'pFWVBAttributeAsc' not in keys:
                kwds['pFWVBAttributeAsc']=False

            if 'pFWVBAttributeRefSize' not in keys:
                kwds['pFWVBAttributeRefSize']=10**2

            if 'quantil_pFWVBAttributeHigh' not in keys:
                kwds['quantil_pFWVBAttributeHigh']=1.
            if 'quantil_pFWVBAttributeLow' not in keys:
                kwds['quantil_pFWVBAttributeLow']=.0

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
            if 'pMCatMidText' not in keys:
                kwds['pMCatMidText']='Middle'
            if 'pMCatBotText' not in keys:
                kwds['pMCatBotText']='Bottom'

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
            if 'CBLe3cMidVPad' not in keys:
                kwds['CBLe3cMidVPad']=.5    
            if 'CBLe3cBotVPad' not in keys:
                kwds['CBLe3cBotVPad']=0-1*1/4    
            if 'CBLe3cSySize' not in keys:
                kwds['CBLe3cSySize']=10**2
            if 'CBLe3cSyType' not in keys:
                kwds['CBLe3cSyType']='o'

            # ROHR             
            if 'pROHRFilterFunction' not in keys:
                kwds['pROHRFilterFunction']=lambda df: (df.KVR.astype(int).isin([2])) & (df.CONT_ID.astype(int).isin([1001])) & (df.DI>0)

            # pROHR (PIPE-Line: Size and Color)
            if 'pROHRAttribute' not in keys:
                kwds['pROHRAttribute']='DI'
            if 'pROHRAttributeApplyFunction' not in keys:
                kwds['pROHRAttributeApplyFunction']=lambda x: pd.to_numeric(x,errors='coerce') # .apply(kwds['pROHRAttributeApplyFunktion'])
            if 'pROHRAttributeApplyFunctionNaNValue' not in keys:
                kwds['pROHRAttributeApplyFunctionNaNValue']=0 # .fillna(kwds['pROHRAttributeApplyFunktionNaNValue']).astype(float)

            if 'pROHRAttributeAsc' not in keys:
                kwds['pROHRAttributeAsc']=False

            if 'pROHRAttributeLs' not in keys:
                kwds['pROHRAttributeLs']='-'
            if 'pROHRAttributeRefSize' not in keys:
                kwds['pROHRAttributeRefSize']=1.
            if 'pROHRAttributeColorMap' not in keys:
                kwds['pROHRAttributeColorMap']=plt.cm.binary
            if 'pROHRAttributeColorMapUsageStart' not in keys:
                kwds['pROHRAttributeColorMapUsageStart']=1./3.

            if 'quantil_pROHRAttributeHigh' not in keys:
                kwds['quantil_pROHRAttributeHigh']=1.
            if 'quantil_pROHRAttributeLow' not in keys:
                kwds['quantil_pROHRAttributeLow']=.75

            # pROHR (PIPE-Marker: Size and Color)
            if 'pROHRMeasure' not in keys:
                kwds['pROHRMeasure']='ROHR~*~*~*~QMAV'
            if 'pROHRMeasureApplyFunction' not in keys:
                kwds['pROHRMeasureApplyFunction']=lambda x: math.fabs(x)

            if 'pROHRMeasureMarker' not in keys:
                kwds['pROHRMeasureMarker']='.'
            if 'pROHRMeasureRefSize' not in keys:
                kwds['pROHRMeasureRefSize']=1.0
            if 'pROHRMeasureColorMap' not in keys:
                kwds['pROHRMeasureColorMap']=plt.cm.cool
            if 'pROHRMeasureColorMapUsageStart' not in keys:
                kwds['pROHRMeasureColorMapUsageStart']=0.

            # NRCVs to be displayed
            if 'pFIGNrcv' not in keys:
                kwds['pFIGNrcv']=None #['KNOT~PKON-Knoten~\S*~\S+~QM']  
            if 'pFIGNrcvTxt' not in keys:
                kwds['pFIGNrcvTxt']=None #['Kontrolle DH']
            if 'pFIGNrcvFmt' not in keys:
                kwds['pFIGNrcvFmt']='{:12s}: {:8.2f} {:6s}'
            if 'pFIGNrcvPercFmt' not in keys:
                kwds['pFIGNrcvPercFmt']=' {:6.1f}%'
            if 'pFIGNrcvXStart' not in keys:
                kwds['pFIGNrcvXStart']=.5
            if 'pFIGNrcvYStart' not in keys:
                kwds['pFIGNrcvYStart']=.5

            # User Heat Balances to be displayed
            if 'pFWVBGCategory' not in keys:
                kwds['pFWVBGCategory']=None #['BLNZ1u5u7']  
            if 'pFWVBGCategoryUnit' not in keys:
                kwds['pFWVBGCategoryUnit']='[kW]'  

            if 'pFWVBGCategoryCatFmt' not in keys:
                kwds['pFWVBGCategoryCatFmt']='{:12s}: {:6.1f} {:4s}'
            if 'pFWVBGCategoryPercFmt' not in keys:
                kwds['pFWVBGCategoryPercFmt']=' {:6.1f}%'
            if 'pFWVBGCategory3cFmt' not in keys:
                kwds['pFWVBGCategory3cFmt']=' {:5d}/{:5d}/{:5d}'  

            if 'pFWVBGCategoryXStart' not in keys:
                kwds['pFWVBGCategoryXStart']=.1
            if 'pFWVBGCategoryYStart' not in keys:
                kwds['pFWVBGCategoryYStart']=.9

            # VICs
            if 'pVICsDf' not in keys:
                kwds['pVICsDf']=None #pd.DataFrame({'Kundenname': ['VIC1'],'Knotenname': ['V-K007']})
            if 'pVICsPercFmt' not in keys:
                kwds['pVICsPercFmt']='{:12s}: {:6.1f}%'
            if 'pVICsFmt' not in keys:
                kwds['pVICsFmt']='{:12s}: {:6.1f} {:6s}'                
            if 'pVICsXStart' not in keys:
                kwds['pVICsXStart']=.5
            if 'pVICsYStart' not in keys:
                kwds['pVICsYStart']=.1        
                
            # Figure
            if 'pltTitle' not in keys:
                kwds['pltTitle']='pltNetDHUS'
            if 'figFrameon' not in keys:
                kwds['figFrameon']=True
            if 'figEdgecolor' not in keys:
                kwds['figEdgecolor']='black'
            if 'figFacecolor' not in keys:
                kwds['figFacecolor']='white'      
                
            # Plausis
            if kwds['pFWVBMeasure3Classes'] and not kwds['pFWVBMeasureCBFixedLimits']:
                kwds['pFWVBMeasureCBFixedLimits']=True
                logger.debug("{0:s}kwd {1:s} set to {2:s} because kwd {3:s}={4:s}".format(logStr,'pFWVBMeasureCBFixedLimits',str(kwds['pFWVBMeasureCBFixedLimits']),'pFWVBMeasure3Classes',str(kwds['pFWVBMeasure3Classes']))) 
                      
            keys = sorted(kwds.keys())
            logger.debug("{0:s}keys: {1:s}".format(logStr,str(keys))) 
            for key in keys:
                value=kwds[key]
                logger.debug("{0:s}kwd {1:s}: {2:s}".format(logStr,key,str(value))) 

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise RmError(logStrFinal)                     
        
        try: 
            # 2 Szenrariumzeiten ermitteln ===============================================
            firstTime=self.mx.df.index[0]
            if isinstance(kwds['timeDeltaToRef'],pd.Timedelta):
                timeRef=firstTime+kwds['timeDeltaToRef']
            else:
                logStrFinal="{:s}{:s} not Type {:s}.".format(logStr,'timeDeltaToRef','pd.Timedelta')
                logger.error(logStrFinal) 
                raise RmError(logStrFinal)  
            if isinstance(kwds['timeDeltaToT'],pd.Timedelta):
                timeT=firstTime+kwds['timeDeltaToT']
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

            pROHRMeasureCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.startswith(kwds['pROHRMeasure'])]
            pROHRMeasureUNIT=pROHRMeasureCh.iloc[0].UNIT
            pROHRMeasureATTRTYPE=pROHRMeasureCh.iloc[0].ATTRTYPE

            # Sachdaten annotieren mit Spalte Measure 

            # FWVB            
            pFWVBMeasureValueRaw=plotTimeDfs[timeTIdx][kwds['pFWVBMeasure']].iloc[0] 
            pFWVBMeasureValueRefRaw=plotTimeDfs[timeRefIdx][kwds['pFWVBMeasure']].iloc[0] 

            pFWVBMeasureValue=[None for m in pFWVBMeasureValueRaw]
            pFWVBMeasureValueRef=[None for m in pFWVBMeasureValueRefRaw]
            for idx in range(len(pFWVBMeasureValueRaw)):                   
                mx2Idx=vFWVB['mx2Idx'].iloc[idx]
                
                m=pFWVBMeasureValueRaw[mx2Idx]
                pFWVBMeasureValue[idx]=m
                m=pFWVBMeasureValueRefRaw[mx2Idx]
                pFWVBMeasureValueRef[idx]=m
              
            if kwds['pFWVBMeasureInRefPerc']:  # auch in diesem Fall traegt die Spalte Measure das Ergebnis                               
                pFWVBMeasureValuePerc=[float(m)/float(mRef) if float(mRef) >0 else 1 for m,mRef in zip(pFWVBMeasureValue,pFWVBMeasureValueRef)]
                pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValuePerc)) #!                                
            else:
                pFWVB=vFWVB.assign(Measure=pd.Series(pFWVBMeasureValue)) #!                              

            pFWVB=pFWVB.assign(MeasureOrig=pd.Series(pFWVBMeasureValue)) 
            pFWVB=pFWVB.assign(MeasureRef=pd.Series(pFWVBMeasureValueRef)) 

            # Sachdaten annotieren mit Spalte MCategory           
            pFWVBCat=[]
            for index, row in pFWVB.iterrows():
                if row.Measure >= kwds['pFWVBMeasureCBFixedLimitHigh']:
                    pFWVBCat.append(kwds['pMCatTopText'])
                elif row.Measure <= kwds['pFWVBMeasureCBFixedLimitLow']:
                    pFWVBCat.append(kwds['pMCatBotText'])
                else:
                    pFWVBCat.append(kwds['pMCatMidText'])
            pFWVB=pFWVB.assign(MCategory=pd.Series(pFWVBCat)) 

            # Sachdaten annotieren mit Spalte GCategory (mit den verlangten Waermebilanzen zu denen ein FWVB gehoert)     
            if isinstance(kwds['pFWVBGCategory'],list):         
                sCatReq=set(kwds['pFWVBGCategory'])       
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
            pROHRMeasureValueRaw=plotTimeDfs[timeTIdx][kwds['pROHRMeasure']].iloc[0]               
            pROHRMeasureValue=[None for m in pROHRMeasureValueRaw]
            for idx in range(len(pROHRMeasureValueRaw)):                   
                mx2Idx=vROHR['mx2Idx'].iloc[idx]
                m=pROHRMeasureValueRaw[mx2Idx]

                mApplied=kwds['pROHRMeasureApplyFunction'](m)
                pROHRMeasureValue[idx]=mApplied

            pROHR=vROHR.assign(Measure=pd.Series(pROHRMeasureValue)) #!

            # ========================================
            # ROHR Attribute-Behandlung wg. float & Filter
            # ========================================        
            pROHR[kwds['pROHRAttribute']]=pROHR[kwds['pROHRAttribute']].apply(kwds['pROHRAttributeApplyFunction']) 
            pROHR[kwds['pROHRAttribute']]=pROHR[kwds['pROHRAttribute']].fillna(kwds['pROHRAttributeApplyFunctionNaNValue']).astype(float)       
             
            # ROHRe filtern
            row,col=pROHR.shape
            logger.debug("{:s}pROHR vor   filtern: Zeilen: {:d}".format(logStr,row))   
            f=kwds['pROHRFilterFunction']  
            logger.debug("{:s}pltROHR Filterfunktion: {:s}".format(logStr,str(f)))     
            pltROHR=pROHR[f] #!    
            row,col=pltROHR.shape
            logger.debug("{:s}pltROHR nach filtern: Zeilen: {:d}".format(logStr,row))        

            # ========================================
            # FWVB Attribute-Behandlung wg. float & Filter
            # ========================================
            pFWVB[kwds['pFWVBAttribute']]=pFWVB[kwds['pFWVBAttribute']].apply(kwds['pFWVBAttributeApplyFunction'])
            pFWVB[kwds['pFWVBAttribute']]=pFWVB[kwds['pFWVBAttribute']].fillna(kwds['pFWVBAttributeApplyFunctionNaNValue']).astype(float) 
            
            # FWVB filtern
            row,col=pFWVB.shape
            logger.debug("{:s}pFWVB vor   filtern: Zeilen: {:d}".format(logStr,row))   
            f=kwds['pFWVBFilterFunction']  
            logger.debug("{:s}pltFWVB Filterfunktion: {:s}".format(logStr,str(f)))     
            pltFWVB=pFWVB[f] #!          
            row,col=pltFWVB.shape
            logger.debug("{:s}pltFWVB nach filtern: Zeilen: {:d}".format(logStr,row))    

            
            pltFWVB=pltFWVB[(pltFWVB[kwds['pFWVBAttribute']]<=pltFWVB[kwds['pFWVBAttribute']].quantile(kwds['quantil_pFWVBAttributeHigh']))
                            &
                            (pltFWVB[kwds['pFWVBAttribute']]>=pltFWVB[kwds['pFWVBAttribute']].quantile(kwds['quantil_pFWVBAttributeLow']))
                           ]

            logger.debug("{:s}pltROHR: quantil_pROHRAttributeHigh: {:f} f(): {:f}".format(logStr
                                                                                          ,kwds['quantil_pROHRAttributeHigh']
                                                                                          ,pltROHR[kwds['pROHRAttribute']].quantile(kwds['quantil_pROHRAttributeHigh'])
                                                                                          ))
            logger.debug("{:s}pltROHR: quantil_pROHRAttributeLow: {:f} f(): {:f}".format(logStr
                                                                                          ,kwds['quantil_pROHRAttributeLow']
                                                                                          ,pltROHR[kwds['pROHRAttribute']].quantile(kwds['quantil_pROHRAttributeLow'])
                                                                                          ))                              


            pltROHR=pltROHR[(pltROHR[kwds['pROHRAttribute']]<=pltROHR[kwds['pROHRAttribute']].quantile(kwds['quantil_pROHRAttributeHigh']))
                            &
                            (pltROHR[kwds['pROHRAttribute']]>=pltROHR[kwds['pROHRAttribute']].quantile(kwds['quantil_pROHRAttributeLow']))
                           ]

            row,col=pltROHR.shape
            logger.debug("{:s}pltROHR nach selektieren: {:d}".format(logStr,row))     

            # Grundsortierung z-Order
            pltFWVB=pltFWVB.sort_values(by=[kwds['pFWVBAttribute']],ascending=kwds['pFWVBAttributeAsc']) 
            pltROHR=pltROHR.sort_values(by=[kwds['pROHRAttribute']],ascending=kwds['pROHRAttributeAsc']) 
           
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

               ,pltTitle=kwds['pltTitle']
               ,figFrameon=kwds['figFrameon']
               #,figLinewidth=1.
               ,figEdgecolor=kwds['figEdgecolor'] 
               ,figFacecolor=kwds['figFacecolor']                                                                                            
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
                ,pMCatBotTxt=kwds['pMCatBotText'] # 'Bottom'    
                ,pMCatMidTxt=kwds['pMCatMidText'] # 'Middle'             
               
                ,pMCatTopColor=kwds['pMCatTopColor']
                ,pMCatTopAlpha=kwds['pMCatTopAlpha']
                ,pMCatTopClip=kwds['pMCatTopClip']   
                                                                        
                ,pMCatBotColor=kwds['pMCatBotColor'] 
                ,pMCatBotAlpha=kwds['pMCatBotAlpha']
                ,pMCatBotClip=kwds['pMCatBotClip']
                  
                ,pMCatMidColorMap=kwds['pMCatMidColorMap']
                ,pMCatMidAlpha=kwds['pMCatMidAlpha']
                ,pMCatMidClip=kwds['pMCatMidClip']
            )

            #fig.sca(ax)

            pROHRMeasureRefSizeValue=pltROHR['Measure'].std()
            if pROHRMeasureRefSizeValue < 1:
                pROHRMeasureRefSizeValue=pltROHR['Measure'].mean()
            logger.debug("{:s}pROHRMeasureRefSizeValue: {:6.2f}".format(logStr,pROHRMeasureRefSizeValue)) 
            pROHRMeasureSizeFactor=kwds['pROHRMeasureRefSize']/pROHRMeasureRefSizeValue

            pROHRAttributeRefSizeValue=pltROHR[kwds['pROHRAttribute']].std()
            if pROHRAttributeRefSizeValue < 1:
                pROHRAttributeRefSizeValue=pltROHR[kwds['pROHRAttribute']].mean()
            logger.debug("{:s}pROHRAttributeRefSizeValue: {:6.2f}".format(logStr,pROHRAttributeRefSizeValue)) 
            pROHRAttributeSizeFactor=kwds['pROHRAttributeRefSize']/pROHRAttributeRefSizeValue

            pltNetPipes(
                pltROHR
               ,pAttribute=kwds['pROHRAttribute']  # Line
               ,pMeasure='Measure'  # Marker

               ,pClip=False
               ,pAttributeLs=kwds['pROHRAttributeLs'] 
               ,pMeasureMarker=kwds['pROHRMeasureMarker']

               ,pAttributeColorMap=kwds['pROHRAttributeColorMap'] 
               ,pAttributeColorMapUsageStart=kwds['pROHRAttributeColorMapUsageStart'] 
               ,pAttributeSizeFactor=pROHRAttributeSizeFactor            

               ,pMeasureColorMap=kwds['pROHRMeasureColorMap'] 
               ,pMeasureColorMapUsageStart=kwds['pROHRMeasureColorMapUsageStart']             
               ,pMeasureSizeFactor=pROHRMeasureSizeFactor     
            )

            # ============================================================
            # Legend
            # ============================================================

            cax=pltNetLegendColorbar(
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
            )
    
            if kwds['pFWVBMeasure3Classes']:                                                                   
                 bbTop, bbMid, bbBot = pltNetLegendColorbar3Classes(                 
                     pDf=pltFWVB          
                    ,pMCategory='MCategory' 
                    ,pMCatTopTxt=kwds['pMCatTopText']     
                    ,pMCatBotTxt=kwds['pMCatBotText']       
                    ,pMCatMidTxt=kwds['pMCatMidText']     

                    ,pMCatBotColor=kwds['pMCatBotColor'] 
                    ,pMCatTopColor=kwds['pMCatTopColor'] 

                    ,CBLe3cTopVPad=kwds['CBLe3cTopVPad'] 
                    ,CBLe3cMidVPad=kwds['CBLe3cMidVPad']                                                                     
                    ,CBLe3cBotVPad=kwds['CBLe3cBotVPad'] 
                    ,CBLe3cSySize=kwds['CBLe3cSySize'] 
                    ,CBLe3cSyType=kwds['CBLe3cSyType']                                                                                                    
                 )
                 TBAV=1.15*bbTop.y1
            else:
                 TBAV=1.15
            
            xmFileName,ext = os.path.splitext(os.path.basename(self.xm.xmlFile))
            (wDir,modelDir,modelName,mx1File)=self.xm.getWDirModelDirModelName()
            Projekt=self.xm.dataFrames['MODELL']['PROJEKT'].iloc[0]
            Planer=self.xm.dataFrames['MODELL']['PLANER'].iloc[0]
            Inst=self.xm.dataFrames['MODELL']['INST'].iloc[0]       
            Model="M: {:s}".format(xmFileName)   
            Result="E: {:s}".format(mx1File)   
            Times="TRef: {!s:s} T: {!s:s}".format(kwds['timeDeltaToRef'],kwds['timeDeltaToT']).replace('days','Tage')       
            pltNetLegendTitleblock(
               text=Projekt+'\n'+Planer+'\n'+Inst+'\n'+Model+'\n'+Result+'\n'+Times 
              ,anchorVertical=TBAV                    
            )
                   
            # ============================================================
            # NRCVs to be displayed in Net
            # ============================================================
            text=None
            if isinstance(kwds['pFIGNrcv'],list) and isinstance(kwds['pFIGNrcvTxt'],list):
                if len(kwds['pFIGNrcv']) == len(kwds['pFIGNrcvTxt']):                    
                    for idx,Sir3sIDRexp in  enumerate(kwds['pFIGNrcv']):                           
                        try:
                            sCh=self.mx.mx1Df[self.mx.mx1Df['Sir3sID'].str.contains(Sir3sIDRexp)].iloc[0]
                        except:
                            logger.debug("{:s} Sir3sIDRexp {:s} nicht in .MX1".format(logStr,Sir3sIDRexp))
                            continue # NRCV wird ausgelassen
                    
                        s=self.mx.df[sCh.Sir3sID]                
                        v=s[timeT]  
                        v0=s[timeRef]
                        if v0==0:                            
                            vp=100.
                        else:
                            vp=v/v0*100     
                                              
                        fmtStr=kwds['pFIGNrcvFmt']
                        if kwds['pFWVBMeasureInRefPerc']:
                            fmtStr=fmtStr+kwds['pFIGNrcvPercFmt']                                                  
                            txt=fmtStr.format(kwds['pFIGNrcvTxt'][idx],v,sCh.UNIT,vp) 
                        else:
                            txt=fmtStr.format(kwds['pFIGNrcvTxt'][idx],v,sCh.UNIT)                        

                        if text==None:
                            text=txt
                        else:
                            text=text+'\n'+txt
                    
                    fig.sca(ax)            
                    pltNetTextblock(text=text,x=kwds['pFIGNrcvXStart'],y=kwds['pFIGNrcvYStart'])         
                      
            # ============================================================
            # User Heat Balances to be displayed in Net
            # ============================================================            
                                         
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
            
            vAggNumAnz=vWBLZ_vKNOT_pFWVB_vNRCV_Mx1.groupby(['NAME','Sir3sID']).size()            

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

            if isinstance(kwds['pFWVBGCategory'],list):    
                text=None
                for NAME in kwds['pFWVBGCategory']: # verlangte Wärmebilanzen       
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
                        midAnz=int(vAggWblzMCat.loc[NAME,kwds['pMCatMidText']]['Measure']['size'])                                                                             
                    except:                 
                        midAnz=0
                  
                    try:                                                         
                        botAnz=int(vAggWblzMCat.loc[NAME,kwds['pMCatBotText']]['Measure']['size'])                                                                 
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
                        continue                      
                                                                                    
                    vpIstZuvSoll=vIst/vSoll
                    if kwds['pFWVBGCategoryUnit']=='[MW]':
                        vIst=vIst/1000.

                    fmtStr=kwds['pFWVBGCategoryCatFmt']
                    if kwds['pFWVBMeasureInRefPerc'] and kwds['pFWVBMeasure3Classes']:
                        fmtStr=fmtStr+kwds['pFWVBGCategoryPercFmt']+kwds['pFWVBGCategory3cFmt']
                        txt=fmtStr.format(NAME,vIst,kwds['pFWVBGCategoryUnit'],vpIstZuvSoll*100,topAnz,midAnz,botAnz)
                    if kwds['pFWVBMeasureInRefPerc'] and not kwds['pFWVBMeasure3Classes']:
                        fmtStr=fmtStr+kwds['pFWVBGCategoryPercFmt']
                        txt=fmtStr.format(NAME,vIst,kwds['pFWVBGCategoryUnit'],vpIstZuvSoll*100)
                    if not kwds['pFWVBMeasureInRefPerc'] and kwds['pFWVBMeasure3Classes']:
                        fmtStr=fmtStr+kwds['pFWVBGCategory3cFmt']
                        txt=fmtStr.format(NAME,vIst,kwds['pFWVBGCategoryUnit'],topAnz,midAnz,botAnz)

                    if text==None:
                            text=txt
                    else:
                            text=text+'\n'+txt
                
                fig.sca(ax)            
                pltNetTextblock(text=text,x=kwds['pFWVBGCategoryXStart'],y=kwds['pFWVBGCategoryYStart'])         

            # ============================================================
            # VICs to be displayed in Net
            # ============================================================                                    

            if isinstance(kwds['pVICsDf'],pd.core.frame.DataFrame):
                text=None
                for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():      
                        kunde=row.VIC                         
                        v=row.Measure
                        if kwds['pFWVBMeasureInRefPerc']:
                            txt=kwds['pVICsPercFmt'].format(kunde,v*100)      
                        else:                           
                            txt=kwds['pVICsFmt'].format(kunde,v,pFWVBMeasureUNIT)    
                        
                        if text==None:
                            text=txt
                        else:
                            text=text+'\n'+txt
                
                fig.sca(ax)            
                pltNetTextblock(text=text,x=kwds['pVICsXStart'],y=kwds['pVICsYStart'])   
                                                                           
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
    Run Tests.
    """

    try:      
        
        # Arguments      
        parser = argparse.ArgumentParser(description='Run Tests.'
        ,epilog='''
        UsageExamples: 

        Modultest:

        -q -m 1 -t both -w OneLPipe -w LocalHeatingNetwork -w GPipe -w GPipes -w TinyWDN 

        Singletests:
        
        -q -m 0 -s "^Mx\." -t both -y yes -z no -w OneLPipe -w LocalHeatingNetwork -w GPipe -w GPipes -w TinyWDN 

        Singletests: separater MockUp-Lauf:

        -q -m 0 -t before -u yes -w DHNetwork
        
        Singletests (die auf dem vorstehenden MockUp-Lauf basieren):
        -q -m 0 -s "^Mx\." -z no -w DHNetwork

        '''                                 
        )

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")           

        parser.add_argument('--testDir',type=str,default='testdata',help="value for global 'testDir' i.e. testdata")
        parser.add_argument('--dotResolution',type=str,default='.1',help="value for global 'dotResolution' i.e. .1 (default); use NONE for no dotResolution")      
                                 
        parser.add_argument("-m","--moduleTest", help="execute the Module Doctest On/Off: -m 1 (default)", action="store",default='1')      
        parser.add_argument("-s","--singleTest", help='execute single Doctest: Exp.1: -s  "^Rm.": all Doctests in Module Rm are executed - but not the Module Doctest (which is named Rm) Exp.2:  -s "^Xm."  -s "^Mx."  -s "^Rm.": all Doctests in the 3 Modules are executed - but not the Module Doctests'
                            ,action="append"
                            ,default=[])    
        parser.add_argument("-x","--singleTestNO", help='execute NOT single Doctest: Exp.1: -s  "^Rm.": NO Doctests in Module Rm are executed - but not the Module Doctest (which is named Rm) Exp.2:  -s "^Xm."  -s "^Mx."  -s "^Rm.": NO Doctests in the 3 Modules are executed - but not the Module Doctests'
                            ,action="append"
                            ,default=[])               
        parser.add_argument("-t","--delGenFiles", help="Tests: decide if generated Files - i.e. .h5-Files - shall be deleted: Exp.: -t both: generated Files are deleted before and after the Tests"
                            ,choices=['before', 'after', 'both','nothing'],default='nothing')

        parser.add_argument("-y","--mockUpDetail1", help="MockUp Detail1: decide if NoH5 shall be used during MockUps: Exp.: -y yes"
                            ,choices=['no','yes'],default='no')

        parser.add_argument("-z","--mockUpDetail2", help="MockUp Detail2: decide if Sync/Add and ToH5 shall be done during MockUps: Exp.: -z no"
                            ,choices=['no','yes'],default='yes')

        parser.add_argument("-u","--mockUpAtTheEnd", help="Tests: decide if after all Tests and after delGenFiles some mockUp shall be done: Exp.: -u yes"
                            ,choices=['no','yes'],default='no')

        parser.add_argument("-w","--testModel", help='specify a testModel: Exp.: -w DHNetwork'
                            ,action="append"
                            ,default=[])           

        parser.add_argument("-l","--logExternDefined", help="Logging (File etc.) ist extern defined", action="store_true",default=False)      


        args = parser.parse_args()


        class LogStart(Exception):
            pass

        try:
            logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
            if args.logExternDefined:  
                logger = logging.getLogger('PT3S')  
                logStr=logStr+" (Logging extern defined) "
            else:                
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
                          
            raise LogStart
        except LogStart:   
            if args.verbose:  # default         
                logger.setLevel(logging.DEBUG)  
            if args.quiet:    # Debug Messages are turned Off
                logger.setLevel(logging.ERROR)  
                args.verbose=False            
            logger.debug("{0:s}{1:s}".format(logStr,'Start.'))             
        else:
            pass
                                            
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Argumente:',str(sys.argv))) 
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'testDir: ',args.testDir)) 

        if args.dotResolution == 'NONE':
            args.dotResolution=''

        try:
            from PT3S import Mx, Xm
        except ImportError:
            logger.debug("{0:s}{1:s}".format("test: from PT3S import Mx, Xm: ImportError: ","trying import Mx, Xm ..."))  
            import Mx, Xm

        testModels=args.testModel 

        # die Modultests gehen i.d.R. vom Ausgangszustand aus; Relikte aus alten Tests müssen daher i.d.R. gelöscht werden ...
        if args.delGenFiles in ['before','both']:
                for testModel in testModels:   
                    #Xm                    
                    xmlFile=os.path.join(os.path.join('.',args.testDir),testModel+'.XML')                      
                    h5FileXm=os.path.join(os.path.join('.',args.testDir),testModel+'.h5')
                    #Mx
                    mx1File=os.path.join('.',os.path.join(args.testDir,'WD'+testModel+'\B1\V0\BZ1\M-1-0-1'+args.dotResolution+'.MX1'))                     
                    (wD,fileName)=os.path.split(mx1File)
                    (base,ext)=os.path.splitext(fileName)
                    (base,dotResolution)=os.path.splitext(base)                                                                             
                    h5File=wD+os.path.sep+base+'.'+'h5'    
                    h5FileVecs=wD+os.path.sep+base+dotResolution+'.'+'vec'+'.'+'h5' 
                    h5FileMx1FmtString=h5File+'.metadata'
                    #loeschen
                    for file in [h5FileXm,h5File,h5FileVecs,h5FileMx1FmtString]:                    
                        if os.path.exists(file):      
                            logger.debug("{:s}Tests Vorbereitung {:s} Delete {:s} ...".format(logStr,testModel,file)) 
                            os.remove(file)


        if args.moduleTest == '1':
            # as unittests
            logger.info("{0:s}{1:s}{2:s}".format(logStr,'Start unittests (by DocTestSuite...). testDir: ',args.testDir)) 

            dtFinder=doctest.DocTestFinder(recurse=False,verbose=args.verbose) # recurse = False findet nur den Modultest

            suite=doctest.DocTestSuite(test_finder=dtFinder #,setUp=setUpFct
                                   ,globs={'testDir':args.testDir
                                           ,'dotResolution':args.dotResolution
                                           })   
            unittest.TextTestRunner().run(suite)
                      
        if len(args.singleTest)>0:

            #Relikte, die die Modultests oder andere Tests produziert haben ggf. loeschen
            if args.delGenFiles in ['before','both']:
                for testModel in testModels:   
                    #Xm                    
                    xmlFile=os.path.join(os.path.join('.',args.testDir),testModel+'.XML')                      
                    h5FileXm=os.path.join(os.path.join('.',args.testDir),testModel+'.h5')
                    #Mx
                    mx1File=os.path.join('.',os.path.join(args.testDir,'WD'+testModel+'\B1\V0\BZ1\M-1-0-1'+args.dotResolution+'.MX1'))                     
                    (wD,fileName)=os.path.split(mx1File)
                    (base,ext)=os.path.splitext(fileName)
                    (base,dotResolution)=os.path.splitext(base)                                                                             
                    h5File=wD+os.path.sep+base+'.'+'h5'    
                    h5FileVecs=wD+os.path.sep+base+dotResolution+'.'+'vec'+'.'+'h5' 
                    h5FileMx1FmtString=h5File+'.metadata'
                    #loeschen
                    for file in [h5FileXm,h5File,h5FileVecs,h5FileMx1FmtString]:                    
                        if os.path.exists(file):      
                            logger.debug("{:s}singleTests Vorbereitung {:s} Delete {:s} ...".format(logStr,testModel,file)) 
                            os.remove(file)

            #MockUp
            logger.debug("{:s}singleTests Vorbereitung Start ...".format(logStr)) 
            xms={}   
            mxs={} 
            ms={}
                               
            for testModel in testModels:   
                logger.debug("{:s}singleTests Vorbereitung {:s} Start ...".format(logStr,testModel)) 


                #Xm
                xmlFile=os.path.join(os.path.join('.',args.testDir),testModel+'.XML')  
                ms[testModel]=xmlFile
                if args.mockUpDetail1 in ['yes']:   
                    xm=Xm.Xm(xmlFile=xmlFile,NoH5Read=True) 
                else:
                    xm=Xm.Xm(xmlFile=xmlFile)      
                logger.debug("{:s}singleTests Vorbereitung {:s} xm instanziert.".format(logStr,testModel)) 

                #Mx
                mx1File=os.path.join('.',os.path.join(args.testDir,'WD'+testModel+'\B1\V0\BZ1\M-1-0-1'+args.dotResolution+'.MX1'))    
                if args.mockUpDetail1 in ['yes']:   
                     mx=Mx.Mx(mx1File=mx1File,NoH5Read=True) 
                else:
                    mx=Mx.Mx(mx1File=mx1File) 
                logger.debug("{:s}singleTests Vorbereitung {:s} mx instanziert.".format(logStr,testModel)) 

                if args.mockUpDetail2 in ['yes']:                    
                    #Sync                
                    xm.MxSync(mx=mx)
                    xm.MxAdd(mx=mx)
                    logger.debug("{:s}singleTests Vorbereitung {:s} Sync/Add erfolgt.".format(logStr,testModel)) 

                    #H5
                    xm.ToH5()
                    mx.ToH5()
                    logger.debug("{:s}singleTests Vorbereitung {:s} ToH5 erfolgt.".format(logStr,testModel)) 
                
                xms[testModel]=xm
                mxs[testModel]=mx
                logger.debug("{:s}singleTests Vorbereitung {:s} fertig.".format(logStr,testModel)) 
 
            dtFinder=doctest.DocTestFinder(verbose=args.verbose)
                     
            logger.debug("{:s}singleTests suchen in Rm ...".format(logStr)) 
            dTests=dtFinder.find(Rm,globs={'testDir':args.testDir     
                                           ,'dotResolution':args.dotResolution
                                           ,'xms':xms
                                           ,'mxs':mxs})

            dTests.extend(dtFinder.find(pltMakeCategoricalCmap))

            # gefundene Tests mit geforderten Tests abgleichen

            testsToBeExecuted=[]
            for expr in args.singleTest:
                logger.debug("{0:s}singleTests: {1:s}: {2:s} ...".format(logStr,'Searching in Tests found for Expr     TBD',expr.strip("'")))                
                testsToBeExecuted=testsToBeExecuted+[test for test in dTests if re.search(expr.strip("'"),test.name) != None]     
            logger.debug("{0:s}singleTests: {1:s}: {2:s}".format(logStr,'    TBD',str(sorted([test.name for test in testsToBeExecuted]))))                   

            testsNotToBeExecuted=[]
            for expr in args.singleTestNO:
                logger.debug("{0:s}singleTests: {1:s}: {2:s} ...".format(logStr,'Searching in Tests found for Expr NOT TBD',expr.strip("'")))      
                testsNotToBeExecuted=testsNotToBeExecuted+[test for test in testsToBeExecuted if re.search(expr.strip("'"),test.name) != None]       
            logger.debug("{0:s}singleTests: {1:s}: {2:s}".format(logStr,'NOT TBD',str(sorted([test.name for test in testsNotToBeExecuted]))))    

            # effektiv auszuführende Tests 
            testsToBeExecutedEff=sorted(set(testsToBeExecuted)-set(testsNotToBeExecuted),key=lambda test: test.name)      
            
            dtRunner=doctest.DocTestRunner(verbose=args.verbose) 
            for test in testsToBeExecutedEff:                      
                    logger.debug("{0:s}singleTests: {1:s}: {2:s} ...".format(logStr,'Running Test',test.name)) 
                    dtRunner.run(test)    

        if args.delGenFiles in ['after','both']:              
            for testModel in testModels:   
                logger.debug("{:s}Tests Nachbereitung {:s} Delete files ...".format(logStr,testModel)) 
                mx=mxs[testModel]
                mx.delFiles()        
                xm=xms[testModel]
                xm.delFiles()   
                if os.path.exists(mx.mxsZipFile):                        
                    os.remove(mx.mxsZipFile)
                mxsDumpFile=mx.mxsFile+'.dump'
                if os.path.exists(mxsDumpFile):                        
                    os.remove(mxsDumpFile)

        if args.mockUpAtTheEnd in ['yes']:                
            for testModel in testModels:
                logger.debug("{:s}Tests Nachbereitung {:s} mockUpAtTheEnd ...".format(logStr,testModel)) 

                #Mx
                mx1File=os.path.join('.',os.path.join(args.testDir,'WD'+testModel+'\B1\V0\BZ1\M-1-0-1'+args.dotResolution+'.MX1')) 
                if args.mockUpDetail1 in ['yes']:                 
                    mx=Mx.Mx(mx1File=mx1File,NoH5Read=True) # avoid doing anything than just plain Init                         
                else:
                    mx=Mx.Mx(mx1File=mx1File) 
                #Xm                     
                xmlFile=os.path.join(os.path.join('.',args.testDir),testModel+'.XML')
                if args.mockUpDetail1 in ['yes']:    
                    xm=Xm.Xm(xmlFile=xmlFile,NoH5Read=True) # avoid doing anything than just plain Init                                           
                else:
                    xm=Xm.Xm(xmlFile=xmlFile) 
                   
                if args.mockUpDetail2 in ['yes']:                    
                    #Sync                
                    xm.MxSync(mx=mx)
                    xm.MxAdd(mx=mx)
                    logger.debug("{:s}Tests Nachbereitung {:s} Sync/Add erfolgt.".format(logStr,testModel)) 

                    #H5
                    xm.ToH5()
                    mx.ToH5()
                    logger.debug("{:s}Tests Nachbereitung {:s} ToH5 erfolgt.".format(logStr,testModel)) 
                                
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

