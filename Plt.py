"""

---------------------------
DOCTEST
---------------------------
>>> # ---
>>> # Imports
>>> # ---
>>> import logging
>>> logger = logging.getLogger('PT3S.Mx')  
>>> import os
>>> import zipfile
>>> import pandas as pd
>>> path = os.path.dirname(__file__)
>>> # ---
>>> # Init
>>> # ---

"""


import os
import sys
import logging
logger = logging.getLogger('PT3S.Plt')  
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

class PltError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Plt():
    """
      
    """
    def __init__(self): 
        """
          
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            pass

            
                             
        except PltError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     


# stationaer / n-1 ohne / n-1 mit
plotTimesUsed=[]
firstTime=mx.df.index[0] # in df stehen nur die Nicht-Vektorergebnisse
print(firstTime)

time1=firstTime+pd.to_timedelta('8 minutes 5 seconds')
time2=firstTime+pd.to_timedelta('9 minutes')

plotTimesUsed.append(Mx.getMicrosecondsFromRefTime(refTime=firstTime,time=firstTime))
plotTimesUsed.append(Mx.getMicrosecondsFromRefTime(refTime=firstTime,time=time1))
plotTimesUsed.append(Mx.getMicrosecondsFromRefTime(refTime=firstTime,time=time2))
print(plotTimesUsed)

# die Vektorergebnisse alle in den Arbeitsspeicher zu lesen funktioniert i.d.R. nicht
plotTimesUsedH5Keys=['/'+str(key) for key in plotTimesUsed]
print(plotTimesUsedH5Keys)

plotTimeDfs=[]
with pd.HDFStore(mx.h5FileMxsVecs) as h5Store: 
    for h5Key in plotTimesUsedH5Keys:
        plotTimeDfs.append(h5Store[h5Key])

        timeIdx=1 # n-1
timeIdx2=2 # n-1 + SpitzenHW

vROHR=xm.dataFrames['vROHR']
vKNOT=xm.dataFrames['vKNOT']
vFWVB=xm.dataFrames['vFWVB']

###########################

sensibleKunden=pd.read_excel('20180301_FW-HA-Zähler_sensible Kunden.xlsx')
sensibleKunden=sensibleKunden[pd.isnull(sensibleKunden['Knotenname'])== False]

#In diesem Zuge habe ich den Kunden Bombardier dem richtigen Knoten zugeordnet (von K58099 nach K58139, 
#der HA-Zähler war fälschlicherweise als Netto Markt in STANET hinterlegt).
# Knoten wieder auf den alten Namen ändern (SIR 3S Modell hat den alten Namen):
zeilenNummer=sensibleKunden[sensibleKunden['Knotenname']=='K58139'].index.values[0]
sensibleKunden.loc[zeilenNummer,'Knotenname']='K58099'

# Kundenanlagen filtern die nur wg. >1 Zaehler mehrfach auftauchen

# lfdNr Knotennamen
sensibleKunden=sensibleKunden.assign(KnotennameLfdNr
                      =sensibleKunden.sort_values(['Knotenname','Zähler Nr.']).groupby(['Knotenname']).cumcount()+1)
# Anz Knotennamen
sensibleKunden=sensibleKunden.merge(sensibleKunden.groupby(['Knotenname']).size().reset_index(name='Knotenname_Anz'),left_on='Knotenname',right_on='Knotenname')

# Kundennamen mit mehrfach Knotennamen markieren
for index,row in sensibleKunden.iterrows():
    if (row.Knotenname_Anz>1):
        sensibleKunden.loc[index,'Kundenname']=row.Kundenname+' (ZAE:'+ str(row.Knotenname_Anz) + ')'

# Mehrfachnennungen von Knotennnamen wegfiltern
sensibleKunden=sensibleKunden[sensibleKunden['KnotennameLfdNr']==1]

# an Kundennamen kennzeichnen, wenn derselbe Kundenname mehrere HA besitzt
sensibleKunden=sensibleKunden.assign(KundennameLfdNr
                      =sensibleKunden.sort_values(['Kundenname','Knotenname','Zähler Nr.']).groupby(['Kundenname']).cumcount()+1)
for index,row in sensibleKunden.iterrows():
    if (row.KundennameLfdNr>1):
        sensibleKunden.loc[index,'Kundenname']=row.Kundenname+' (HA Nr.:'+ str(row.KundennameLfdNr) + ')'
        
sensibleKunden=sensibleKunden[['Kundenname','Knotenname']]

df=vFWVB.merge(sensibleKunden,left_on='NAME_i',right_on='Knotenname')

vFWVB=vFWVB.assign(VIC=df['Kundenname'])

vFWVB[pd.isnull(vFWVB['VIC'])==False]


###########################

###########################

timeIdx=1 # diese Zeit ~ Measure
# stat. ~ MeasureS

measure=plotTimeDfs[timeIdx]['FWVB~*~*~*~DP'].iloc[0] 
pFWVB=vFWVB.assign(Measure=pd.Series(measure))

measure=plotTimeDfs[0]['FWVB~*~*~*~DP'].iloc[0] 
pFWVB=pFWVB.assign(MeasureS=pd.Series(measure))

measure=plotTimeDfs[timeIdx2]['FWVB~*~*~*~DP'].iloc[0] 
pFWVB=pFWVB.assign(MeasureT2=pd.Series(measure))

WIst=plotTimeDfs[timeIdx]['FWVB~*~*~*~W'].iloc[0] 
WSoll=pFWVB['W0']

WProz=[ WIst/WSoll if WSoll >0 else 1. for WIst,WSoll in zip(WIst,WSoll)]
pFWVB=pFWVB.assign(MeasureWProz=pd.Series(WProz))

measure=plotTimeDfs[timeIdx]['ROHR~*~*~*~QMAV'].iloc[0] 
measureMapped=[None for m in measure]
for idx in range(len(measure)):
    mx2Idx=vROHR['mx2Idx'].iloc[idx]
    measureMapped[idx]=math.fabs(measure[mx2Idx])
pPltROHR=vROHR.assign(Measure=pd.Series(measureMapped))

measure=plotTimeDfs[0]['ROHR~*~*~*~QMAV'].iloc[0] 
measureMapped=[None for m in measure]
for idx in range(len(measure)):
    mx2Idx=vROHR['mx2Idx'].iloc[idx]
    measureMapped[idx]=math.fabs(measure[mx2Idx])
pPltROHR=pPltROHR.assign(MeasureS=pd.Series(measureMapped))

measure=plotTimeDfs[timeIdx2]['ROHR~*~*~*~QMAV'].iloc[0] 
measureMapped=[None for m in measure]
for idx in range(len(measure)):
    mx2Idx=vROHR['mx2Idx'].iloc[idx]
    measureMapped[idx]=math.fabs(measure[mx2Idx])
pPltROHR=pPltROHR.assign(MeasureT2=pd.Series(measureMapped))

#KNOT~*~~*~H
measure=plotTimeDfs[timeIdx]['KNOT~*~~*~H'].iloc[0] 
pKNOT=vKNOT.assign(Measure=pd.Series(measure))
#pKNOT['Measure'].min()
#pKNOT['Measure'].max()

measure=plotTimeDfs[0]['KNOT~*~~*~H'].iloc[0] 
pKNOT=pKNOT.assign(MeasureS=pd.Series(measure))

measure=plotTimeDfs[timeIdx2]['KNOT~*~~*~H'].iloc[0] 
pKNOT=pKNOT.assign(MeasureT2=pd.Series(measure))


##########################



########################################################################################################
########################################################################################################

# Ausdehnung des Plots in Weltkoordinaten
# fuer die Ausdehnung der "Netzfarbdarstellung" sind hier nur die Koordinaten der Netzrohre und die der FWVB massgebend ...
dx=max(vFWVB['pXCor_i'].max(),max(vROHR[(vROHR['CONT_ID'].astype(int).isin([1001]))]['pXCor_i'].max(),vROHR[(vROHR['CONT_ID'].astype(int).isin([1001]))]['pXCor_k'].max()))
dy=max(vFWVB['pYCor_i'].max(),max(vROHR[(vROHR['CONT_ID'].astype(int).isin([1001]))]['pYCor_i'].max(),vROHR[(vROHR['CONT_ID'].astype(int).isin([1001]))]['pYCor_k'].max()))

# erf. Verhältnis bei verzerrungsfreier Darstellung
dydx=dy/dx 

DINA4_x=8.2677165354
DINA4_y=11.6929133858

if(dydx>=1):
    dxInch=DINA4_x # Hochformat
else:
    dxInch=DINA4_y # Querformat
    
print(dx)
print(dy)
print(dxInch)


# === PARAMETER ===

#Zeiten
timeRef=mx.df.index[0]
timeT1=timeRef+pd.to_timedelta('8 minutes 5 seconds')
timeT2=timeRef+pd.to_timedelta('9 minutes')

#colorbar ------------------
# colorbar-Bereich beruecksichtigen
fraction=0.05  # fraction of original axes to use for colorbar
pad=0.05 # fraction of original axes between colorbar and new image axes

labelpad=-20 # negative labelpad values will move closer to the bar, positive away


anchorVertical=0.15 # vertikaler Fußpunkt der colorbar
aspect=10. # ratio of long to short dimension
shrink=0.25 # fraction by which to shrink the colorbar

yUnitCB=(1.-anchorVertical)*shrink
#print(yUnitCB) # 0.225

vPadNOK=-0.30
vPadUV=-0.15
vPadOK=1.15 

#ax ------------------------------------
clip_on=False

#FWVB ------------------

limitOk=0.95
limitNOk=0.10

colorOk='palegreen'
cororNOk='violet' # 'orchid'
cmapNOK_OK=plt.cm.autumn 

refSize=10 # Groesse der FWVB-Symbole bei Referenzwert
# der Referenzwert ist factorRef x std()
factorRef=2.
refColName='W0'
alpha=0.9

ascendingZColName='W0'
ascendingZOrder=False # ascendingZColName wird für die Sortierung benutzt; bei False werden "kleine" auf "große" geplottet

filterColName='W0'
filterColValue=0
# es werden nur die FWVB geplottet für die der Wert des Kriteriums > filterColValue ist

plotColName='MeasureWProz'

faktorSchriftabstandZuKuller=0.75

#Pipes ------------------

#Vorauswahl
KVRisIn=[2]
CONT_IDisIn=[1001]
quantilDI=0#75./80. # es werden nur Rohre geplottet bei denen refColNamePipe >= ist
quantilMarker=75./80. # oder bei denen plotColNamePipeMarker >= ist
quantilMarkerRef=75./80. # oder bei denen der plotColNamePipeMarkerRef >= ist

quantilselColNamePipe=75./80. # oder bei denen plotColNamePipeMarker >= ist
quantilselColNamePipe2=75./80. # oder bei denen der plotColNamePipeMarkerRef >= ist
quantilselColNamePipeN1Hoch=9.75/10.
quantilselColNamePipeN1Niedrig=1.0

#Auswahl n-1
# Rohre die in der Bezugsspalte einen sehr hohen Wert haben
quantilN1Hoch=9.5/10.
# und im BZ einen niedrigen
N1Niedrig=1.0

selColNamePipe='Measure'
selColNamePipe2='MeasureS'

#Breite und Farbe der Rohre
refSizePipeDI=1.0 # Breite bei Referenzwert
refColNamePipe='DI'
reColMapPipes=plt.cm.binary
pipeUnit='mm'
#Skalierung auf min/max von refColNamePipe


#Marker  der Rohre
pipeMarkerFactor=1.1
refSizePipeMarker=pipeMarkerFactor*refSizePipeDI
plotColNamePipeMarker=refColNamePipe     #'Measure'
colorMapPipeMarker=reColMapPipes               #plt.cm.autumn
markerUnit=pipeUnit #'t/h' 

#Marker Bezugsspalte 
plotColNamePipeMarkerRef='MeasureS'

# NumAnz ------------
#patWBLZ='(WBLZ)~(\S+)~(\S*)~(\S+)~(\S+)'
patWBLZ='WBLZ~[\S ]+~\S*~\S+~\S+'
patDH='KNOT~K0001~\S*~\S+~QM'

reSir3SID='(\S+)~([\S ]+)~(\S*)~(\S+)~(\S+)'
reSir3SIDcompiled=re.compile(reSir3SID)

# Legend
vPadL=0.6 #Legend
hSpaceL=0.6 #Pts

#Rechenlauf
Event='TL Nord 2'
Massnahme='ohne HW'
RechnungsNrProjekt=666

#fig -----------------------------------
frameon=True
linewidth=1.
edgecolor='k'

#weitere Auswahl
pROHR=pPltROHR

pROHR=pROHR[(pROHR['CONT_ID'].astype(int).isin(CONT_IDisIn))]
pROHR=pROHR[(pROHR['KVR'].astype(int).isin(KVRisIn))]


pROHR=pROHR[(pROHR[refColNamePipe].astype(float)>=pROHR[refColNamePipe].astype(float).quantile(quantilDI))
           | 
           (pROHR[selColNamePipe].astype(float)>=pROHR[selColNamePipe].astype(float).quantile(quantilselColNamePipe)) 
           | 
           (pROHR[selColNamePipe2].astype(float)>=pROHR[selColNamePipe2].astype(float).quantile(quantilselColNamePipe2))  
           ]


n_1ROHRe=pROHR[ 
           (pROHR[selColNamePipe2].astype(float)>=pROHR[selColNamePipe2].astype(float).quantile(quantilselColNamePipeN1Hoch)) 
           & 
           (pROHR[selColNamePipe].astype(float)<=quantilselColNamePipeN1Niedrig)  
    ]

# fig-Abmessungen für verzerrungsfreie Darstellung berechnen

#f = gcf()  
#f.set_figwidth(figwidth)
#f.set_figheight(figheight)



figwidth=dxInch

#verzerrungsfrei: Blattkoordinatenverhaeltnis = Weltkoordinatenverhaeltnis
factor=1-(fraction+pad)
# verzerrungsfreie Darstellung sicherstellen
figheight=figwidth*dydx*factor


# Weltkoordinatenbereich
xlimLeft=0
ylimBottom=0
xlimRight=dx
ylimTop=dy

plt.close('all')
fig=plt.figure(
     frameon=frameon
    ,linewidth=linewidth
    ,edgecolor=edgecolor
)
fig.set_figwidth(figwidth)
fig.set_figheight(figheight)
#f = gcf()  
#f.set_size_inches(11.69,8.27) A4
#f.set_size_inches(16.53,11.69) A3

ax=plt.subplot()
ax.set_xlim(left=xlimLeft)
ax.set_ylim(bottom=ylimBottom)
ax.set_xlim(right=xlimRight)
ax.set_ylim(top=ylimTop)



# Normierung Symbolfarbe
minDp=0.0
maxDp=1.4
markDp=0.7

minUV=0.0
maxUV=1.0
#markUV=0.7


# Vorfilter
pFWVB=pFWVB[pFWVB[filterColName]>filterColValue] 

#Sortierung z-Order
pFWVB=pFWVB.sort_values(by=[ascendingZColName],ascending=ascendingZOrder) 

pFWVBOk=pFWVB[
    (pFWVB[plotColName]>=limitOk)
    ] 
pColDummy=ax.scatter(    
                 pFWVBOk['pXCor_i'],pFWVBOk['pYCor_i']                 
                ,s=refSize*pFWVBOk[refColName]/(factorRef*pFWVB[refColName].std())   
                ,color=colorOk 
                ,alpha=alpha
                ,edgecolors='face'             
                ,clip_on=clip_on
               )

pFWVBI=pFWVB[
    (pFWVB[plotColName]<limitOk)
    &
     (pFWVB[plotColName]>limitNOk)
    ] 
pCol=ax.scatter(    
                 pFWVBI['pXCor_i'],pFWVBI['pYCor_i']            
                ,s=refSize*pFWVBI[refColName]/(factorRef*pFWVB[refColName].std())   
                # Farbskala
                ,cmap=cmapNOK_OK
                # Normierung Farbe
                ,vmin=limitNOk 
                ,vmax=limitOk
                # Measure
                ,c=pFWVBI[plotColName] 
                ,alpha=alpha
                ,edgecolors='face'
                ,clip_on=clip_on
               )


pFWVBNOk=pFWVB[
    (pFWVB[plotColName]<=limitNOk)
     &
     (pFWVB[plotColName]>=0)
    ] 
pColDummy=ax.scatter(    
                pFWVBNOk['pXCor_i'],pFWVBNOk['pYCor_i']                
                ,s=refSize*pFWVBNOk[refColName]/(factorRef*pFWVB[refColName].std())   
                ,color=cororNOk 
                ,alpha=alpha
                ,edgecolors='face'              
                ,clip_on=clip_on
               )

minMeasure=pROHR[refColNamePipe].astype(float).min()
maxMeasure=pROHR[refColNamePipe].astype(float).max()
normR = colors.Normalize(minMeasure,maxMeasure)

#Sortierung z-Order
pROHR=pROHR.sort_values(by=[plotColNamePipeMarker],ascending=False) # kleine auf große

minMarkerMeasure=pROHR[plotColNamePipeMarker].astype(float).min()
maxMarkerMeasure=pROHR[plotColNamePipeMarker].astype(float).max()
normMarker = colors.Normalize(minMarkerMeasure,maxMarkerMeasure)
  
for xs,ys,measureV,measureMarker in zip(pROHR['pWAYPXCors'],pROHR['pWAYPYCors'],pROHR[refColNamePipe].astype(float),pROHR[plotColNamePipeMarker].astype(float)):        
    colorR = reColMapPipes(normR(measureV))
    colorMarker = colorMapPipeMarker(normMarker(measureMarker))
    lines = ax.plot(xs,ys
                    ,color=colorR
                    ,linewidth=refSizePipeDI*measureV/maxMeasure
                    , ls='-'
                    ,marker='.'
                    ,mfc=colorMarker #'b'#colorR
                    ,ms=refSizePipeMarker*measureMarker/maxMarkerMeasure
                    ,mew=0.
                    ,markevery=[0,len(xs)-1]
                    ,aa=True
                   )

row,col=n_1ROHRe.shape
if row >= 1:
    for xs,ys,measureV,measureMarker in zip(n_1ROHRe['pWAYPXCors'],n_1ROHRe['pWAYPYCors'],n_1ROHRe['DI'].astype(float),n_1ROHRe['Measure']):   
        colorMarker = plt.cm.autumn(normMarker(measureMarker))
        lines = ax.plot(xs,ys
                        ,color='r'#colorR
                        ,linewidth=refSizePipeDI*measureV/maxMeasure
                        , ls='-'
                        ,marker='.'
                        ,mfc=colorMarker #'b'#colorR
                        ,ms=refSizePipeMarker*measureMarker/maxMarkerMeasure
                        ,mew=0.
                        ,markevery=[0,len(xs)-1]
                        ,aa=True
                       )

    x = n_1ROHRe['pXCor_i'].mean()     
    y = n_1ROHRe['pYCor_i'].mean()

    a=plt.annotate(Event
                   , xy=(x,y),xycoords='data'
                   , xytext=(14000,18000),textcoords='data'
                   ,arrowprops=dict(arrowstyle="->",connectionstyle="arc3",facecolor='black',lw=1.)#, shrink=0.05)
                   #,bbox=dict(boxstyle="round", fc="w")
                   ,zorder=0
    )

    vNRCV_Mx1=xm.dataFrames['vNRCV_Mx1']

    for index, row in vNRCV_Mx1[
     (vNRCV_Mx1['Sir3sID'].str.contains(patWBLZ) )  
    &
     (vNRCV_Mx1['CONT_ID'].astype(int) == 1001)  
    ].iterrows():
    s=mx.df[row.Sir3sID]
    v=s[timeT1]
    #print(v)
    v0=s[timeRef]
    vp=v/v0*100
    #print(vp)
    x,y = row.pXYLB
    #print(x,y)
    if x<0:
        x=0
    if y<0:
        continue

    m=re.match(reSir3SIDcompiled,row.Sir3sID)
    if m == None:
        continue
    
    #print(m.group(2))
    #print(row.Sir3sID)
    a=plt.annotate("{:s}: {:6.1f} MW {:6.1f}%".format(m.group(2),v,vp), xy=(round(x,0),round(y,0)), xycoords='data'
             #,rotation='vertical'
             ,va='bottom'
             ,ha='center' 
            ,clip_on=clip_on
                  )

for index, row in vNRCV_Mx1[
     (vNRCV_Mx1['Sir3sID'].str.contains(patDH) )  
    &
     (vNRCV_Mx1['CONT_ID'].astype(int) == 1001)  
    ].iterrows():
    s=mx.df[row.Sir3sID]
    v=s[timeT1]
    #print(v)
    v0=s[timeRef]
    vp=v/v0*100
    #print(vp)
    x,y = row.pXYLB
    #print(x,y)
    if x<0:
        x=0
    if y<0:
        continue

    m=re.match(reSir3SIDcompiled,row.Sir3sID)
    if m == None:
        continue
    
    #print(m.group(2))
    #print(row.Sir3sID)
    a=plt.annotate("DH-Kontrollwert: {:6.1f} t/h".format(v), xy=(round(x,0),round(y,0)), xycoords='data'
             #,rotation='vertical'
             ,va='bottom'
             ,ha='center' 
            ,clip_on=clip_on
                  )

    xStart=9000.
yStart=1000.
fontsize=8
distance=50
idx=0
for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():      
      kunde=row.VIC     
      #print(len(kunde))
      a=plt.annotate("{:s}".format(kunde), xy=(xStart,yStart+fontsize*distance*idx), xycoords='data'
                 #,rotation='vertical'
                 ,fontsize=fontsize    
                 ,va='bottom'
                 ,ha='left' 
                ,clip_on=clip_on
                   )
      idx=idx+1

idx=0
for index, row in pFWVB[pd.isnull(pFWVB['VIC'])==False].sort_values(['VIC'],ascending=False).iterrows():
      v=pFWVB[plotColName].loc[index]
      a=plt.annotate("{:6.2f} %".format(v*100), xy=(xStart+6000,yStart+fontsize*distance*idx), xycoords='data'
                 #,rotation='vertical'
                 ,fontsize=fontsize    
                 ,va='bottom'
                 ,ha='left' 
                ,clip_on=clip_on
                      )
      idx=idx+1  

      cax,kw=make_axes(ax
                 ,location='right'
                 ,fraction=fraction # fraction of original axes to use for colorbar
                 ,pad=pad # fraction of original axes between colorbar and new image axes
                 ,anchor=(0.,anchorVertical) # the anchor point of the colorbar axes
                 ,aspect=aspect # ratio of long to short dimension
                 ,shrink=shrink # fraction by which to shrink the colorbar
                )
#print(str(kw)) # {'ticklocation': 'right', 'orientation': 'vertical'}
cB=fig.colorbar(pCol
                ,cax=cax
                ,**kw
               )
cB.set_ticks([limitNOk,limitOk])
cB.set_ticklabels([">{:3.0f}%".format(limitNOk*100),"<{:3.0f}%".format(limitOk*100)])
cB.set_label('Versorgung in %',labelpad=-1)

#dir(cB)



Projekt=xm.dataFrames['MODELL']['PROJEKT'].iloc[0]
Planer=xm.dataFrames['MODELL']['PLANER'].iloc[0]
Inst=xm.dataFrames['MODELL']['INST'].iloc[0]




a=plt.annotate(Projekt, xy=(0,1+vPadL), xycoords=cax.transAxes 
             ,rotation='vertical'
             ,va='bottom'
             ,ha='left'
)

a=plt.annotate(Planer, xy=(0+hSpaceL,1+vPadL), xycoords=cax.transAxes 
             ,rotation='vertical'
             ,va='bottom'
             ,ha='left'   
)

a=plt.annotate(Inst, xy=(0+2*hSpaceL,1+vPadL), xycoords=cax.transAxes 
             ,rotation='vertical'
             ,va='bottom'
             ,ha='left'   
)

xmFileName,ext = os.path.splitext(os.path.basename(xm.xmlFile))
a=plt.annotate("Modelldatei: {:s}".format(xmFileName), xy=(0+3*hSpaceL,1+vPadL), xycoords=cax.transAxes 
             ,rotation='vertical'
             ,va='bottom'
             ,ha='left'   
)

RechnungsNrImModell=str(timeT1-timeRef)
RechnungsNrImModell=RechnungsNrImModell[9:]
a=plt.annotate("RechnungsNr. im Modell: {!s:s} Bemerkung: {:s}".format(RechnungsNrImModell, Massnahme), xy=(0+4*hSpaceL,1+vPadL), xycoords=cax.transAxes 
             ,rotation='vertical'
             ,va='bottom'
             ,ha='left'   
)

a=plt.annotate("RechnungsNr. Projekt: {!s:s}".format(RechnungsNrProjekt), xy=(0+5*hSpaceL,1+vPadL), xycoords=cax.transAxes 
             ,rotation='vertical'
             ,va='bottom'
             ,ha='left'   
)

thisSizeValue=pFWVBNOk[refColName].max()
po=cax.scatter(     pad
                ,vPadNOK 
                # Skalierung Symbolgroesse
                ,s=refSize*thisSizeValue/(factorRef*pFWVB[refColName].std())                  
                ,c=cororNOk
                ,alpha=0.9
                ,edgecolors='face'             
                ,clip_on=False
               )


o=po.findobj(match=None) 
px=o[0]
#print(px.get_datalim(cax.transData))
#print(px.get_datalim(cax.transAxes))
bb=px.get_datalim(cax.transAxes)
#print(bb.x1-bb.x0)



a=plt.annotate("{:6.1f} MW".format(thisSizeValue/1000.), xy=(pad+faktorSchriftabstandZuKuller*(bb.x1-bb.x0)                                                            
                                                             ,vPadNOK), xycoords=cax.transAxes 
             ,va='center'
             ,ha='left'   
)


normUV = colors.Normalize(limitNOk,limitOk)


colorUV = cmapNOK_OK(normUV(pFWVBI[plotColName].loc[pFWVBI[refColName].idxmax()]))

thisSizeValue=pFWVBI[refColName].max()
po=cax.scatter(     pad
                ,vPadUV 
                # Skalierung Symbolgroesse
                ,s=refSize*thisSizeValue/(factorRef*pFWVB[refColName].std())                  
                ,c=colorUV
                ,alpha=0.9
                ,edgecolors='face'             
                ,clip_on=False
               )

o=po.findobj(match=None) 
px=o[0]
#print(px.get_datalim(cax.transData))
#print(px.get_datalim(cax.transAxes))
bb=px.get_datalim(cax.transAxes)
#print(bb.x1-bb.x0)



a=plt.annotate("{:6.1f} MW".format(thisSizeValue/1000.), xy=(pad+faktorSchriftabstandZuKuller*(bb.x1-bb.x0)                                                                     
                                                             ,vPadUV), xycoords=cax.transAxes 
             ,va='center'
             ,ha='left'   
)



thisSizeValue=pFWVBOk[refColName].max()
po=cax.scatter(     pad
                ,vPadOK 
                # Skalierung Symbolgroesse
                ,s=refSize*thisSizeValue/(factorRef*pFWVB[refColName].std())                  
                ,c=colorOk
                ,alpha=0.9
                ,edgecolors='face'             
                ,clip_on=False
               )

o=po.findobj(match=None) 
px=o[0]
#print(px.get_datalim(cax.transData))
#print(px.get_datalim(cax.transAxes))
bb=px.get_datalim(cax.transAxes)
#print(bb.x1-bb.x0)

a=plt.annotate("{:6.1f} MW".format(thisSizeValue/1000.), xy=(pad+faktorSchriftabstandZuKuller*(bb.x1-bb.x0)        
                                            
                                                             ,vPadOK), xycoords=cax.transAxes 
             ,va='center'
             ,ha='left'   
)

#bb
dyOkCircle=bb.y1-bb.y0
yLine=bb.y1+0.5*dyOkCircle
print(yLine)
print(dyOkCircle)




lines = cax.plot([0,1*hSpaceL],[yLine,yLine]
                    ,color=reColMapPipes(normR(maxMeasure))
                    ,linewidth=refSizePipeDI
                    , ls='-'
                    ,marker=''

                    ,aa=True
                  ,clip_on=False
                   )
a=plt.annotate("{:d} {:s}".format(int(maxMeasure),pipeUnit), xy=(1.5*hSpaceL,yLine), xycoords=cax.transAxes 
          #   ,rotation='vertical'
             ,va='center'
             ,ha='left'   
)

yLine2=yLine+0.1 

lines = cax.plot([0,1*hSpaceL],[yLine2,yLine2]
                    ,color='r'#plt.cm.binary(normR(maxMeasure))
                    ,linewidth=refSizePipeDI*n_1ROHRe['DI'].astype(float).mean()/maxMeasure
                    , ls='-'
                    ,marker=''

                    ,aa=True
                  ,clip_on=False
                   )
a=plt.annotate("gesperrt".format(), xy=(1.5*hSpaceL,yLine2), xycoords=cax.transAxes 
          #   ,rotation='vertical'
             ,va='center'
             ,ha='left'   
)

xTicks=ax.get_xticks()
dxTick = xTicks[1]-xTicks[0]
#[idx*dxTick for idx in range(math.floor(dy/dxTick))]
yTicks=ax.set_yticks([idx*dxTick for idx in range(math.floor(dy/dxTick)+1)])

plotFileName=xmFileName+'_Plot1'+'.pdf'
plt.savefig(plotFileName 
,dpi=300
)
plt.show()




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
