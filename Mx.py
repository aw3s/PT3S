"""
SIR 3S MX-Interface (short: MX)

    MX is a file based, channel-oriented interface for SIR 3S' calculation results.
    
    This module contains stuff to utilize SIR 3S' MX calculation results in pure Python.  

    SIR 3S MX calculation results:

        * Binary .MXS-Files contain the SIR 3S calculations results. 
        * A Model calculation run creates at least one .MXS-File.
        * There is one .MX1-File (an XML-File) for each SIR 3S Model calculation run.    
        * This .MX1-File defines (in XML) a sequence of MX-Channels. 
        * And - as a result - the Byte-Layout of a single MX3-Record in .MXS-File(s).
        * A MX3-Record contains calculation results for one TIMESTAMP.
        * A .MXS-File contains at least one MX3-Record.

    A MX-Channel can be:
     
        * a single Value 
        * or a Vector: Sequence of Values of the same Type:

            * for all Objects of a certain Type or (called Vectorchannels)
            * number of interior Points for all Pipes (special Vectorchannels: Pipevectorchannels)
            * Vectors with ATTRTYPE in: {'SVEC', 'PVECMIN_INST', 'PVECMAX_INST'}

    For Vectorchannels (including Pipevectorchannels) the sequence of Objects is defined in the .MX2-File.

>>> # ---
>>> # SETUP
>>> # ---
>>> import os
>>> import time
>>> import logging
>>> logger = logging.getLogger('PT3S.Mx')  
>>> # ---
>>> # path
>>> # ---
>>> if __name__ == "__main__":
...    try:
...       dummy=__file__
...       logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ','path = os.path.dirname(__file__)'," .")) 
...       path = os.path.dirname(__file__)
...    except NameError:    
...       logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ',"path = '.' because __file__ not defined"," from Mx import Mx.")) 
...       path = '.'
...       from Mx import Mx
... else:
...    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('DOCTEST: Not __main__ Context: ','__name__: ',__name__,"path = '.'")) 
...    path = '.'
>>> # ---
>>> # testDir
>>> # ---
>>> # globs={'testDir':'testdata'}
>>> try:
...     dummy= testDir
... except NameError:
...     testDir='testdata' 
>>> import zipfile
>>> import pandas as pd
>>> # ---
>>> # Init
>>> # ---
>>> h5File=os.path.join(path,os.path.join(testDir,'OneLPipe.h5')) 
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDOneLPipe\B1\V0\BZ1\M-1-0-1.MX1')) 
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> isinstance(mx.mx1Df,pd.core.frame.DataFrame) # MX1-Content
True
>>> isinstance(mx.df,type(None)) # MXS-Content
True
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> metadataFile=mx.h5File+'.metadata'
>>> if os.path.exists(metadataFile):                        
...    os.remove(metadataFile)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> # ---
>>> # 1st Read MXS
>>> # ---
>>> logger.debug("{0:s}: 1st Read MXS".format('DOCTEST')) 
>>> mx.setResultsToMxsFile() # looks for M-1-0-1.MXS in same Dir 
4
>>> isinstance(mx.df,pd.core.frame.DataFrame) # MXS-Content
True
>>> rowsDf,colsDf = mx.df.shape
>>> (firstTime,lastTime,rows)=mx._checkMxsVecsFile()
>>> rowsDf==rows
True
>>> mx.df.index[0]==firstTime
True
>>> # ---
>>> # Write H5
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...      os.remove(mx.h5File)
>>> mx.ToH5() # M-1-0-1.h5 in same Dir 
>>> os.path.exists(mx.h5File)
True
>>> # ---
>>> # Init with H5
>>> # ---
>>> mx=Mx(mx1File=mx1File) # looks for M-1-0-1.h5 in same Dir 
>>> # and reads the .h5 if newer than .MX1 and newer than an existing .MXS 
>>> isinstance(mx.mx1Df,pd.core.frame.DataFrame) # MX1-Content
True
>>> isinstance(mx.df,pd.core.frame.DataFrame) # MXS-Content
True
>>> # ---
>>> # 1st Read MXS Zip
>>> # ---
>>> # create the Zip first
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
>>> logger.debug("{0:s}: 1st Read MXS Zip".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile() # looks for M-1-0-1.ZIP in same Dir
4
>>> isinstance(mx.df,pd.core.frame.DataFrame) # MXS-Content
True
>>> rowsMxs,colsMxs = mx.df.shape
>>> mx.df.index.is_unique # all setResultsTo... will ensure this uniqueness under all circumstances
True
>>> # uniqueness under all circumstances: also when add=True (setResultsTo... shall add the MXS-Content) is used
>>> # ---
>>> # 1st Add same MXS (for testing ensuring uniqueness) 
>>> # ---
>>> oldShape=mx.df.shape
>>> logger.debug("{0:s}: 1st Add same MXS (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
0
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # 1st Add same Zip (for testing ensuring uniqueness) 
>>> # ---
>>> logger.debug("{0:s}: 1st Add same Zip (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile(add=True) # looks for M-1-0-1.ZIP in same Dir 
0
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # 1st Read MXS Zip with overlapping Timestamps (for testing ensuring uniqueness) 
>>> # ---
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...      myzip.write(mx.mxsFile)  
...      myzip.write(mx.mxsFile,arcname=mx.mxsFile+'.2')  
>>> logger.debug("{0:s}: 1st Read MXS Zip with overlapping Timestamps (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile() # looks for M-1-0-1.ZIP in same Dir 
4
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # shift to younger Timestamps (for testing purposes) 
>>> # ---
>>> lastTimestamp=mx.df.index[-1]
>>> firstTimestamp=mx.df.index[0]
>>> timeSpan=lastTimestamp-firstTimestamp
>>> if len(mx.df.index)>1:
...      timeStep=mx.df.index[-1]-mx.df.index[-2]
... else:
...      timeStep=pd.to_timedelta('1 second')
>>> mx.df.index=mx.df.index-(timeSpan+timeStep)
>>> # ---
>>> # 1st Read MXS (with the original Timestamps)
>>> # ---
>>> logger.debug("{0:s}: 1st Read MXS (with the original Timestamps)".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
4
>>> rowsNew,colsNew=mx.df.shape
>>> rowsOld,colsOld=oldShape
>>> rowsNew==2*rowsOld
True
>>> colsNew==colsOld
True
>>> # ---
>>> # shift to older Timestamps (for testing purposes) 
>>> # ---
>>> lastTimestamp=mx.df.index[-1]
>>> firstTimestamp=mx.df.index[0]
>>> timeSpan=lastTimestamp-firstTimestamp
>>> if len(mx.df.index)>1:
...      timeStep=mx.df.index[-1]-mx.df.index[-2]
... else:
...      timeStep=pd.to_timedelta('1 second')
>>> mx.df.index=mx.df.index+(timeSpan+timeStep)
>>> # ---
>>> # 2nd Read MXS (with the original Timestamps)
>>> # ---
>>> logger.debug("{0:s}: 2nd Read MXS (with the original Timestamps)".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(add=True) # looks for M-1-0-1.MXS in same Dir 
4
>>> rowsNew,colsNew=mx.df.shape
>>> rowsNew==3*rowsOld
True
>>> colsNew==colsOld
True
>>> # ---
>>> # Write Dump
>>> # ---
>>> mx.dumpInMxsFormat() # dumps to .MXS.dump-File in same Dir
>>> # ---
>>> # Read Dump
>>> # ---
>>> logger.debug("{0:s}: Read Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(mxsFile=mxsDumpFile)
8
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
...     myzip.write(mxsDumpFile)  
>>> # ---
>>> # Read Zip with Orig and Dump
>>> # ---
>>> logger.debug("{0:s}: Read Zip with Orig and Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile()
8
>>> mx.df.shape
(8, 41)
>>> mx.ToH5()
>>> # ---
>>> # Without MX1, MXS
>>> # ---
>>> os.rename(mx.mx1File,mx.mx1File+'.blind')
>>> os.rename(mx.mxsFile,mx.mxsFile+'.blind')
>>> mx=Mx(mx1File=mx1File)  
>>> os.rename(mx.mx1File+'.blind',mx.mx1File)
>>> os.rename(mx.mxsFile+'.blind',mx.mxsFile)
>>> # ---
>>> mx.mx1Df['Sir3sID'][mx.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].index[0]   
0
>>> mx.mx1Df['unpackIdx'][mx.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].iloc[0]
0
>>> mx.df.shape
(8, 41)
>>> isinstance(mx.df.index[0],pd.tslib.Timestamp)
True
>>> str(mx.df.index[0])
'2018-03-03 00:00:00+00:00'
>>> ts=mx.df['KNOT~I~~5642914844465475844~QM']
>>> isinstance(ts,pd.core.series.Series)
True
>>> "{:06.2f}".format(round(ts.iloc[0],2))
'176.71'
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.31',1,'New','_checkMxsVecsFile: (...,fullCheck=False,...)')) 
>>> mx._checkMxsVecsFile()
(Timestamp('2018-03-03 00:00:00+0000', tz='UTC'), Timestamp('2018-03-03 00:00:07+0000', tz='UTC'), 8)
>>> mx._checkMxsVecsFile(fullCheck=True)
(Timestamp('2018-03-03 00:00:00+0000', tz='UTC'), Timestamp('2018-03-03 00:00:07+0000', tz='UTC'), 8)
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',1,'Change','setResultsToMxsFile: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',2,'Change','setResultsToMxsZipFile: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',3,'Change','ToH5: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',4,'Change','FromH5: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',5,'Change','*: except Exception as e')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',6,'Change','setResultsToMxsFile: finally: NewH5Vec=False')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',7,'Change','__init__(...,NoH5Read=True,...)')) 
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> mx=Mx(mx1File=mx1File,NoH5Read=True) 
>>> os.path.exists(mx.h5FileVecs) # h5 was written (h5 did not exist)
True
>>> h5VecsFileTime=os.path.getmtime(mx.h5FileVecs) 
>>> mx=Mx(mx1File=mx1File,NoH5Read=True) # h5 will be written again (h5 exists)
>>> h5VecsFileTimeNow=os.path.getmtime(mx.h5FileVecs)
>>> logger.debug("1 h5VecsFileTime:{:s} < h5VecsFileTimeNow:{:s}".format(time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTime)),time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTimeNow))))
>>> h5VecsFileTime<h5VecsFileTimeNow # 1 h5 was written again (h5 did exist before)
True
>>> h5VecsFileTime=os.path.getmtime(mx.h5FileVecs) 
>>> mx=Mx(mx1File=mx1File) # h5 is read - not written
>>> h5VecsFileTimeNow=os.path.getmtime(mx.h5FileVecs)
>>> logger.debug("2 h5VecsFileTime:{:s} == h5VecsFileTimeNow:{:s}".format(time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTime)),time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTimeNow))))
>>> mx.setResultsToMxsFile() # h5 will not be updated
0
>>> h5VecsFileTimeNow=os.path.getmtime(mx.h5FileVecs)
>>> logger.debug("3 h5VecsFileTime:{:s} == h5VecsFileTimeNow:{:s}".format(time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTime)),time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTimeNow))))
>>> mx.setResultsToMxsFile(NewH5Vec=True) # h5 is written
4
>>> h5VecsFileTimeNow=os.path.getmtime(mx.h5FileVecs)
>>> logger.debug("h5VecsFileTime:{:s} == h5VecsFileTimeNow:{:s}".format(time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTime)),time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTimeNow))))
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',8,'Change','setResultsToMxsZipFile: finally: NewH5Vec=False')) 
>>> mx.ToH5()
>>> mx=Mx(mx1File=mx1File,NoH5Read=True)
>>> os.path.exists(mx.h5File)
False
>>> pd.set_option('display.max_columns',None)
>>> pd.set_option('display.max_rows',None)
>>> pd.set_option('display.max_colwidth',666666)   
>>> pd.set_option('display.width',666666666)
>>> print("'''{:s}'''".format(repr(mx.mx1Df).replace('\\n','\\n   ')))      
'''   ADDEND      ATTRTYPE CLIENT_FLAGS CLIENT_ID  DATALENGTH  DATAOFFSET DATATYPE  DATATYPELENGTH DEVIATION FACTOR  FLAGS LINKED_CHANNEL LOWER_LIMIT NAME1 NAME2 NAME3 OBJTYPE           OBJTYPE_PK OPCITEM_ID                                     TITLE       UNIT UPPER_LIMIT                         Sir3sID  NOfItems  isVectorChannel  isVectorChannelMx2  isVectorChannelMx2Rvec  unpackIdx
   0       0     TIMESTAMP            0                    32           0     CHAR              32         0      1    241             -1      -1E+20                      ALLG                   -1                            Zeitstempel nach ISO 8601     [text]       1E+20             ALLG~~~-1~TIMESTAMP         1            False               False                   False          0
   1       0  SNAPSHOTTYPE            0                     4          32     CHAR               4         0      1    241             -1      -1E+20                      ALLG                   -1               Typ des Zeitpunktes/Ausgabedatensatzes     [text]       1E+20          ALLG~~~-1~SNAPSHOTTYPE         1            False               False                   False          1
   2       0        CVERSO            0                    80          36     CHAR              80         0      1    241             -1      -1E+20                      ALLG                   -1                                      Versionskennung     [text]       1E+20                ALLG~~~-1~CVERSO         1            False               False                   False          2
   3       0        EXSTAT            0                     4         116     INT4               4         0      1   1265             -1      -1E+20                      ALLG                   -1                           Exit-Status der Berechnung         []       1E+20                ALLG~~~-1~EXSTAT         1            False               False                   False          3
   4       0         NFEHL            0                     4         120     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1                Anzahl Fehler im Berechnungsabschnitt         []       1E+20                 ALLG~~~-1~NFEHL         1            False               False                   False          4
   5       0         NWARN            0                     4         124     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1             Anzahl Warnungen im Berechnungsabschnitt         []       1E+20                 ALLG~~~-1~NWARN         1            False               False                   False          5
   6       0         NMELD            0                     4         128     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1             Anzahl Meldungen im Berechnungsabschnitt         []       1E+20                 ALLG~~~-1~NMELD         1            False               False                   False          6
   7       0       CPUTIME            0                     4         132     REAL               4         0      1    241             -1      -1E+20                      ALLG                   -1                                  CPU-Zeit seit Start        [s]       1E+20               ALLG~~~-1~CPUTIME         1            False               False                   False          7
   8       0       USRTIME            0                     4         136     REAL               4         0      1    241             -1      -1E+20                      ALLG                   -1                                  USR-Zeit seit Start        [s]       1E+20               ALLG~~~-1~USRTIME         1            False               False                   False          8
   9       0       NPGREST            0                     4         140     INT4               4         0      1     49             -1      -1E+20                      ALLG                   -1                   Anzahl aktiver PGRP in Restriktion         []       1E+20               ALLG~~~-1~NPGREST         1            False               False                   False          9
   10      0       NETZABN            0                     4         144     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                                          Netzabnahme     [m3/h]       1E+20               ALLG~~~-1~NETZABN         1            False               False                   False         10
   11      0         NKNUV            0                     4         148     INT4               4         0      1   1233             -1      -1E+20                      ALLG                   -1                      Anzahl KNOT mit Unterversorgung         []       1E+20                 ALLG~~~-1~NKNUV         1            False               False                   False         11
   12      0         MKNUV            0                     4         152     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                   Fehlmenge KNOT aus Unterversorgung     [m3/h]       1E+20                 ALLG~~~-1~MKNUV         1            False               False                   False         12
   13      0       NFVHYUV            0                     4         156     INT4               4         0      1   1057             -1      -1E+20                      ALLG                   -1                Anzahl FWVB mit hydr. Unterversorgung         []       1E+20               ALLG~~~-1~NFVHYUV         1            False               False                   False         13
   14      0       NFVTHUV            0                     4         160     INT4               4         0      1   1057             -1      -1E+20                      ALLG                   -1                Anzahl FWVB mit ther. Unterversorgung         []       1E+20               ALLG~~~-1~NFVTHUV         1            False               False                   False         14
   15      0       MFVHYUV            0                     4         164     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1             Fehlmenge FWVB aus hydr. Unterversorgung     [m3/h]       1E+20               ALLG~~~-1~MFVHYUV         1            False               False                   False         15
   16      0       MFVTHUV            0                     4         168     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1             Fehlmenge FWVB aus ther. Unterversorgung     [m3/h]       1E+20               ALLG~~~-1~MFVTHUV         1            False               False                   False         16
   17      0      TVMINMAX            0                     4         172     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1                  Maximum der erf. min. VL-Temperatur       [°C]       1E+20              ALLG~~~-1~TVMINMAX         1            False               False                   False         17
   18      0        ITERHY            0                     4         176     INT4               4         0      1   1265             -1      -1E+20                      ALLG                   -1                Anzahl benötigter (hydr.) Iterationen         []       1E+20                ALLG~~~-1~ITERHY         1            False               False                   False         18
   19      0         LFQSV            0                     4         180     REAL               4         0      1   1041             -1      -1E+20                      ALLG                   -1                       Lastfaktor für Strangentnahmen         []       1E+20                 ALLG~~~-1~LFQSV         1            False               False                   False         19
   20      0         JWARN            0                     4         184     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1                                            Warnstufe         []       1E+20                 ALLG~~~-1~JWARN         1            False               False                   False         20
   21      0  NETZABNEXITS            0                     4         188     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                         Netzabnahme ohne Druckränder     [m3/h]       1E+20          ALLG~~~-1~NETZABNEXITS         1            False               False                   False         21
   22      0  LINEPACKRATE            0                     4         192     REAL               4         0      1     65             -1      -1E+20                      ALLG                   -1                                 Gesamt-Linepack-Rate  [(N)m3/h]       1E+20          ALLG~~~-1~LINEPACKRATE         1            False               False                   False         22
   23      0   LINEPACKGES            0                     4         196     REAL               4         0      1     65             -1      -1E+20                      ALLG                   -1                                      Gesamt-Linepack    [(N)m3]       1E+20           ALLG~~~-1~LINEPACKGES         1            False               False                   False         23
   24      0  LINEPACKGEOM            0                     4         200     REAL               4         0      1     65             -1      -1E+20                      ALLG                   -1                           Gesamt-Linepack Rohrinhalt    [(N)m3]       1E+20          ALLG~~~-1~LINEPACKGEOM         1            False               False                   False         24
   25      0         RHOAV            0                     4         204     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                                      Mittlere Dichte    [kg/m3]       1E+20                 ALLG~~~-1~RHOAV         1            False               False                   False         25
   26      0           TAV            0                     4         208     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                                  Mittlere Temperatur       [°C]       1E+20                   ALLG~~~-1~TAV         1            False               False                   False         26
   27      0           PAV            0                     4         212     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                                      Mittlerer Druck    [bar,a]       1E+20                   ALLG~~~-1~PAV         1            False               False                   False         27
   28      0   FWVB_DPHMIN            0                     4         216     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1                Min. Differenzdruck aller Verbraucher      [bar]       1E+20           ALLG~~~-1~FWVB_DPHMIN         1            False               False                   False         28
   29      0    KNOT_PHMAX            0                     4         220     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                             Max. Knotendruck im Netz      [bar]       1E+20            ALLG~~~-1~KNOT_PHMAX         1            False               False                   False         29
   30      0    KNOT_PHMIN            0                     4         224     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                             Min. Knotendruck im Netz      [bar]       1E+20            ALLG~~~-1~KNOT_PHMIN         1            False               False                   False         30
   31      0   FWVB_TVLMIN            0                     4         228     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1                 Min. VL-Temperatur aller Verbraucher       [°C]       1E+20           ALLG~~~-1~FWVB_TVLMIN         1            False               False                   False         31
   32      0       NETZBEZ            0                     4         232     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                                            Netzbezug     [m3/h]       1E+20               ALLG~~~-1~NETZBEZ         1            False               False                   False         32
   33      0            PH            0                     4         236     REAL               4         0      1   1265             -1      -1E+20     I                KNOT  5642914844465475844                                                Druck      [bar]       1E+20  KNOT~I~~5642914844465475844~PH         1            False               False                   False         33
   34      0            QM            0                     4         240     REAL               4         0      1   1265             -1      -1E+20     I                KNOT  5642914844465475844                                  Externer Durchfluss     [m3/h]       1E+20  KNOT~I~~5642914844465475844~QM         1            False               False                   False         34
   35      0            PH            0                     4         244     REAL               4         0      1   1265             -1      -1E+20     K                KNOT  5289899964753656852                                                Druck      [bar]       1E+20  KNOT~K~~5289899964753656852~PH         1            False               False                   False         35
   36      0            QM            0                     4         248     REAL               4         0      1   1265             -1      -1E+20     K                KNOT  5289899964753656852                                  Externer Durchfluss     [m3/h]       1E+20  KNOT~K~~5289899964753656852~QM         1            False               False                   False         36
   37      0          MVEC            0                   404         252     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                          [kg/s]       1E+20                 ROHR~*~*~*~MVEC       101             True                True                    True         37
   38      0        RHOVEC            0                   404         656     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                         [kg/m3]       1E+20               ROHR~*~*~*~RHOVEC       101             True                True                    True        138
   39      0          ZVEC            0                   404        1060     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                             [m]       1E+20                 ROHR~*~*~*~ZVEC       101             True                True                    True        239
   40      0           PHR            0                     4        1464     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                          [IDPH]       1E+20                  ROHR~*~*~*~PHR         1            False               False                   False        340
   41      0          PVEC            0                   404        1468     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                         [bar,a]       1E+20                 ROHR~*~*~*~PVEC       101             True                True                    True        341
   42      0            QM            0                     8        1872     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                          [IDQM]       1E+20                    KNOT~*~~*~QM         2             True                True                   False        442
   43      0            PH            0                     8        1880     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                        [IDPH,4]       1E+20                    KNOT~*~~*~PH         2             True                True                   False        444
   44      0             H            0                     8        1888     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                        [IDPH,6]       1E+20                     KNOT~*~~*~H         2             True                True                   False        446
   45      0          QMAV            0                     4        1896     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                          [IDQM]       1E+20                 ROHR~*~*~*~QMAV         1            False               False                   False        448
   46      0           VAV            0                     4        1900     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                           [m/s]       1E+20                  ROHR~*~*~*~VAV         1            False               False                   False        449
   47      0      LFAKTAKT            0                     8        1904     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                              []       1E+20              KNOT~*~~*~LFAKTAKT         2             True                True                   False        450
   48      0             P            0                     8        1912     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                         [bar,a]       1E+20                     KNOT~*~~*~P         2             True                True                   False        452
   49      0        PH_EIN            0                     8        1920     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                          [IDPH]       1E+20                KNOT~*~~*~PH_EIN         2             True                True                   False        454
   50      0           RHO            0                     8        1928     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                         [kg/m3]       1E+20                   KNOT~*~~*~RHO         2             True                True                   False        456
   51      0             T            0                     8        1936     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                            [°C]       1E+20                     KNOT~*~~*~T         2             True                True                   False        458
   52      0            EH            0                     8        1944     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                           [mNN]       1E+20                    KNOT~*~~*~EH         2             True                True                   False        460
   53      0             A            0                     4        1952     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                           [m/s]       1E+20                    ROHR~*~*~*~A         1            False               False                   False        462
   54      0       IRTRENN            0                     4        1956     INT4               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                              []       1E+20              ROHR~*~*~*~IRTRENN         1            False               False                   False        463'''
>>> print("'''{:s}'''".format(repr(mx.mx2Df).replace('\\n','\\n   ')))
'''       AttrType                                        Data  DataLength DataType  DataTypeLength  NOfItems       ObjType
   0  tk            [5642914844465475844, 5289899964753656852]          40     CHAR              20         2  KNOT        
   1  pk                                 [5252810657060947333]          20     CHAR              20         1  LFKT        
   2  pk                                 [5502689500012692689]          20     CHAR              20         1  PHI1        
   3  pk                                 [5732781659713982525]          20     CHAR              20         1  PUMD        
   4  pk                                 [5163733225086798083]          20     CHAR              20         1  PVAR        
   5  pk                                 [4742976321174242828]          20     CHAR              20         1  QVAR        
   6  tk                                 [4737064599036143765]          20     CHAR              20         1  ROHR        
   7  N_OF_POINTS                                       (101,)           4     INT4               4         1  ROHR        
   8  pk                                 [5396761270498593493]          20     CHAR              20         1  SWVT        '''
>>> print("'''{:s}'''".format(repr(mx.df.drop(['ALLG~~~-1~CPUTIME','ALLG~~~-1~USRTIME','ALLG~~~-1~CVERSO'],axis=1)).replace('\\n','\\n   ')))
'''                          ALLG~~~-1~SNAPSHOTTYPE  ALLG~~~-1~EXSTAT  ALLG~~~-1~NFEHL  ALLG~~~-1~NWARN  ALLG~~~-1~NMELD  ALLG~~~-1~NPGREST  ALLG~~~-1~NETZABN  ALLG~~~-1~NKNUV  ALLG~~~-1~MKNUV  ALLG~~~-1~NFVHYUV  ALLG~~~-1~NFVTHUV  ALLG~~~-1~MFVHYUV  ALLG~~~-1~MFVTHUV  ALLG~~~-1~TVMINMAX  ALLG~~~-1~ITERHY  ALLG~~~-1~LFQSV  ALLG~~~-1~JWARN  ALLG~~~-1~NETZABNEXITS  ALLG~~~-1~LINEPACKRATE  ALLG~~~-1~LINEPACKGES  ALLG~~~-1~LINEPACKGEOM  ALLG~~~-1~RHOAV  ALLG~~~-1~TAV  ALLG~~~-1~PAV  ALLG~~~-1~FWVB_DPHMIN  ALLG~~~-1~KNOT_PHMAX  ALLG~~~-1~KNOT_PHMIN  ALLG~~~-1~FWVB_TVLMIN  ALLG~~~-1~NETZBEZ  KNOT~I~~5642914844465475844~PH  KNOT~I~~5642914844465475844~QM  KNOT~K~~5289899964753656852~PH  KNOT~K~~5289899964753656852~QM  ROHR~*~*~*~PHR  ROHR~*~*~*~QMAV  ROHR~*~*~*~VAV  ROHR~*~*~*~A  ROHR~*~*~*~IRTRENN
   2018-03-03 00:00:00+00:00                b'STAT'                 0                0                0               13                  0         176.714600                0              0.0                  0                  0                0.0                0.0         -273.149994                11              1.0               30                     0.0                0.000000           0.000000e+00              490.873871      1000.299988     556.299988       3.108535           3.402823e+38              4.217070                   0.0           3.402823e+38           176.7146                        4.217070                        176.7146                             0.0                     -176.714600        4.217033       176.714600        1.000000        1000.0                   0
   2018-03-03 00:00:01+00:00                b'TIME'                 0                0                0                0                  0         176.714737                0              0.0                  0                  0                0.0                0.0         -273.149994                 1              1.0               30                     0.0               -0.000137          -2.042460e-08              490.873871      1000.299988     556.299988       3.108534           3.402823e+38              4.217062                   0.0           3.402823e+38           176.7146                        4.217062                        176.7146                             0.0                     -176.714737        4.217032       176.714722        1.000001        1000.0                   0
   2018-03-03 00:00:02+00:00                b'TIME'                 0                0                0                0                  0         176.714798                0              0.0                  0                  0                0.0                0.0         -273.149994                 1              1.0               30                     0.0               -0.000198          -5.934779e-08              490.873871      1000.299988     556.299988       3.108533           3.402823e+38              4.217058                   0.0           3.402823e+38           176.7146                        4.217058                        176.7146                             0.0                     -176.714798        4.217035       176.714767        1.000001        1000.0                   0
   2018-03-03 00:00:03+00:00                b'TIME'                 0                0                0                0                  0         176.714859                0              0.0                  0                  0                0.0                0.0         -273.149994                 1              1.0               30                     0.0               -0.000259          -1.153421e-07              490.873871      1000.299988     556.299988       3.108532           3.402823e+38              4.217054                   0.0           3.402823e+38           176.7146                        4.217054                        176.7146                             0.0                     -176.714859        4.217036       176.714813        1.000001        1000.0                   0'''
>>> # ---
>>> # Clean Up OneLPipe
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...     os.remove(mx.h5File)
>>> metadataFile=mx.h5File+'.metadata'
>>> if os.path.exists(metadataFile):                        
...     os.remove(metadataFile)
>>> if os.path.exists(mx.mxsZipFile):                        
...     os.remove(mx.mxsZipFile)
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1.MX1')) # 'testdata\WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1.MX1')
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> # ---
>>> # Clean Up LocalHeatingNetwork
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> mx.setResultsToMxsFile(maxRecords=1)
1
>>> print("'''{:s}'''".format(repr(mx.df.drop(['ALLG~~~-1~CPUTIME','ALLG~~~-1~USRTIME','ALLG~~~-1~CVERSO'],axis=1)).replace('\\n','\\n   ')))
'''                          ALLG~~~-1~SNAPSHOTTYPE  ALLG~~~-1~EXSTAT  ALLG~~~-1~NFEHL  ALLG~~~-1~NWARN  ALLG~~~-1~NMELD  ALLG~~~-1~NPGREST  ALLG~~~-1~NETZABN  ALLG~~~-1~NKNUV  ALLG~~~-1~MKNUV  ALLG~~~-1~NFVHYUV  ALLG~~~-1~NFVTHUV  ALLG~~~-1~MFVHYUV  ALLG~~~-1~MFVTHUV  ALLG~~~-1~TVMINMAX  ALLG~~~-1~ITERHY  ALLG~~~-1~LFQSV  ALLG~~~-1~JWARN  ALLG~~~-1~NETZABNEXITS  ALLG~~~-1~LINEPACKRATE  ALLG~~~-1~LINEPACKGES  ALLG~~~-1~LINEPACKGEOM  ALLG~~~-1~RHOAV  ALLG~~~-1~TAV  ALLG~~~-1~PAV  ALLG~~~-1~FWVB_DPHMIN  ALLG~~~-1~KNOT_PHMAX  ALLG~~~-1~KNOT_PHMIN  ALLG~~~-1~FWVB_TVLMIN  ALLG~~~-1~NETZBEZ  KNOT~V-L~~5736262931552588702~PH  FWES~R3~V-1~5638756766880678918~W  KNOT~V-K007~~5741235692335544560~DP  WBLZ~WärmeblnzGes~~5262603207038486299~WSPEI  KNOT~R-L~~5356267303828212700~PH  PUMP~R-1~R2~5481331875203087055~N  KNOT~V-1~~5049461676240771430~T  WBLZ~WärmeblnzGes~~5262603207038486299~WES  WBLZ~WärmeblnzGes~~5262603207038486299~WVB  VENT~V-1~V-L~4678923650983295610~QM  WBLZ~WärmeblnzGes~~5262603207038486299~WVERL  KNOT~R3~~5219230031772497417~T  PUMP~R-1~R2~5481331875203087055~BK  PUMP~R-1~R2~5481331875203087055~PE  FWES~R3~V-1~5638756766880678918~TI  FWES~R3~V-1~5638756766880678918~TK  WBLZ~BLNZ1u5u7~~4694700216019268978~WVB  KNOT~PKON-Knoten~~5397990465339071638~QM  FWVB~V-K002~R-K002~4643800032883366034~DP  FWVB~V-K002~R-K002~4643800032883366034~INDUV  FWVB~V-K002~R-K002~4643800032883366034~LFH  FWVB~V-K002~R-K002~4643800032883366034~LFT  FWVB~V-K002~R-K002~4643800032883366034~W  FWVB~V-K002~R-K002~4643800032883366034~WSOLL  FWVB~V-K007~R-K007~5400405917816384862~DP  FWVB~V-K007~R-K007~5400405917816384862~INDUV  FWVB~V-K007~R-K007~5400405917816384862~LFH  FWVB~V-K007~R-K007~5400405917816384862~LFT  FWVB~V-K007~R-K007~5400405917816384862~W  FWVB~V-K007~R-K007~5400405917816384862~WSOLL  FWVB~V-K003~R-K003~5695730293103267172~DP  FWVB~V-K003~R-K003~5695730293103267172~INDUV  FWVB~V-K003~R-K003~5695730293103267172~LFH  FWVB~V-K003~R-K003~5695730293103267172~LFT  FWVB~V-K003~R-K003~5695730293103267172~W  FWVB~V-K003~R-K003~5695730293103267172~WSOLL  FWVB~V-K004~R-K004~4704603947372595298~DP  FWVB~V-K004~R-K004~4704603947372595298~INDUV  FWVB~V-K004~R-K004~4704603947372595298~LFH  FWVB~V-K004~R-K004~4704603947372595298~LFT  FWVB~V-K004~R-K004~4704603947372595298~W  FWVB~V-K004~R-K004~4704603947372595298~WSOLL  FWVB~V-K005~R-K005~5121101823283893406~INDUV  FWVB~V-K005~R-K005~5121101823283893406~LFH  FWVB~V-K005~R-K005~5121101823283893406~LFT  FWVB~V-K005~R-K005~5121101823283893406~W  FWVB~V-K005~R-K005~5121101823283893406~WSOLL  FWVB~V-K007~R-K007~5400405917816384862~QM  FWVB~V-K002~R-K002~4643800032883366034~QM  FWVB~V-K004~R-K004~4704603947372595298~TI  FWVB~V-K004~R-K004~4704603947372595298~TK  FWVB~V-K004~R-K004~4704603947372595298~TVMIN  FWVB~V-K002~R-K002~4643800032883366034~TI  FWVB~V-K002~R-K002~4643800032883366034~TK  FWVB~V-K002~R-K002~4643800032883366034~TVMIN  KNOT~V-L~~5736262931552588702~RHO  KNOT~V-L~~5736262931552588702~P  KNOT~V-L~~5736262931552588702~H  KNOT~V-L~~5736262931552588702~HMAX_INST  KNOT~V-L~~5736262931552588702~HMIN_INST  KNOT~V-L~~5736262931552588702~PMAX_INST  KNOT~V-L~~5736262931552588702~PMIN_INST  KNOT~V-L~~5736262931552588702~PDAMPF  KNOT~V-K000~~4766681917240867943~RHO  KNOT~V-K000~~4766681917240867943~P  KNOT~V-K000~~4766681917240867943~H  KNOT~V-K000~~4766681917240867943~HMAX_INST  KNOT~V-K000~~4766681917240867943~HMIN_INST  KNOT~V-K000~~4766681917240867943~PMAX_INST  KNOT~V-K000~~4766681917240867943~PMIN_INST  KNOT~V-K000~~4766681917240867943~PDAMPF  KNOT~V-K001~~4756962427318766791~RHO  KNOT~V-K001~~4756962427318766791~P  KNOT~V-K001~~4756962427318766791~H  KNOT~V-K001~~4756962427318766791~HMAX_INST  KNOT~V-K001~~4756962427318766791~HMIN_INST  KNOT~V-K001~~4756962427318766791~PMAX_INST  KNOT~V-K001~~4756962427318766791~PMIN_INST  KNOT~V-K001~~4756962427318766791~PDAMPF  KNOT~V-K002~~4731792362611615619~RHO  KNOT~V-K002~~4731792362611615619~P  KNOT~V-K002~~4731792362611615619~H  KNOT~V-K002~~4731792362611615619~HMAX_INST  KNOT~V-K002~~4731792362611615619~HMIN_INST  KNOT~V-K002~~4731792362611615619~PMAX_INST  KNOT~V-K002~~4731792362611615619~PMIN_INST  KNOT~V-K002~~4731792362611615619~PDAMPF  KNOT~V-K003~~5646671866542823796~RHO  KNOT~V-K003~~5646671866542823796~P  KNOT~V-K003~~5646671866542823796~H  KNOT~V-K003~~5646671866542823796~HMAX_INST  KNOT~V-K003~~5646671866542823796~HMIN_INST  KNOT~V-K003~~5646671866542823796~PMAX_INST  KNOT~V-K003~~5646671866542823796~PMIN_INST  KNOT~V-K003~~5646671866542823796~PDAMPF  KNOT~V-K004~~5370423799772591808~RHO  KNOT~V-K004~~5370423799772591808~P  KNOT~V-K004~~5370423799772591808~H  KNOT~V-K004~~5370423799772591808~HMAX_INST  KNOT~V-K004~~5370423799772591808~HMIN_INST  KNOT~V-K004~~5370423799772591808~PMAX_INST  KNOT~V-K004~~5370423799772591808~PMIN_INST  KNOT~V-K004~~5370423799772591808~PDAMPF  KNOT~V-K005~~5444644492819213978~RHO  KNOT~V-K005~~5444644492819213978~P  KNOT~V-K005~~5444644492819213978~H  KNOT~V-K005~~5444644492819213978~HMAX_INST  KNOT~V-K005~~5444644492819213978~HMIN_INST  KNOT~V-K005~~5444644492819213978~PMAX_INST  KNOT~V-K005~~5444644492819213978~PMIN_INST  KNOT~V-K005~~5444644492819213978~PDAMPF  KNOT~V-K006~~5515313800585145571~RHO  KNOT~V-K006~~5515313800585145571~P  KNOT~V-K006~~5515313800585145571~H  KNOT~V-K006~~5515313800585145571~HMAX_INST  KNOT~V-K006~~5515313800585145571~HMIN_INST  KNOT~V-K006~~5515313800585145571~PMAX_INST  KNOT~V-K006~~5515313800585145571~PMIN_INST  KNOT~V-K006~~5515313800585145571~PDAMPF  KNOT~V-K007~~5741235692335544560~RHO  KNOT~V-K007~~5741235692335544560~P  KNOT~V-K007~~5741235692335544560~H  KNOT~V-K007~~5741235692335544560~HMAX_INST  KNOT~V-K007~~5741235692335544560~HMIN_INST  KNOT~V-K007~~5741235692335544560~PMAX_INST  KNOT~V-K007~~5741235692335544560~PMIN_INST  KNOT~V-K007~~5741235692335544560~PDAMPF  KNOT~R-L~~5356267303828212700~RHO  KNOT~R-L~~5356267303828212700~P  KNOT~R-L~~5356267303828212700~H  KNOT~R-L~~5356267303828212700~HMAX_INST  KNOT~R-L~~5356267303828212700~HMIN_INST  KNOT~R-L~~5356267303828212700~PMAX_INST  KNOT~R-L~~5356267303828212700~PMIN_INST  KNOT~R-L~~5356267303828212700~PDAMPF  KNOT~R-K000~~4979785838440534851~RHO  KNOT~R-K000~~4979785838440534851~P  KNOT~R-K000~~4979785838440534851~H  KNOT~R-K000~~4979785838440534851~HMAX_INST  KNOT~R-K000~~4979785838440534851~HMIN_INST  KNOT~R-K000~~4979785838440534851~PMAX_INST  KNOT~R-K000~~4979785838440534851~PMIN_INST  KNOT~R-K000~~4979785838440534851~PDAMPF  KNOT~R-K001~~4807712987325933680~RHO  KNOT~R-K001~~4807712987325933680~P  KNOT~R-K001~~4807712987325933680~H  KNOT~R-K001~~4807712987325933680~HMAX_INST  KNOT~R-K001~~4807712987325933680~HMIN_INST  KNOT~R-K001~~4807712987325933680~PMAX_INST  KNOT~R-K001~~4807712987325933680~PMIN_INST  KNOT~R-K001~~4807712987325933680~PDAMPF  KNOT~R-K002~~5364712333175450942~RHO  KNOT~R-K002~~5364712333175450942~P  KNOT~R-K002~~5364712333175450942~H  KNOT~R-K002~~5364712333175450942~HMAX_INST  KNOT~R-K002~~5364712333175450942~HMIN_INST  KNOT~R-K002~~5364712333175450942~PMAX_INST  KNOT~R-K002~~5364712333175450942~PMIN_INST  KNOT~R-K002~~5364712333175450942~PDAMPF  KNOT~R-K003~~4891048046264179170~RHO  KNOT~R-K003~~4891048046264179170~P  KNOT~R-K003~~4891048046264179170~H  KNOT~R-K003~~4891048046264179170~HMAX_INST  KNOT~R-K003~~4891048046264179170~HMIN_INST  KNOT~R-K003~~4891048046264179170~PMAX_INST  KNOT~R-K003~~4891048046264179170~PMIN_INST  KNOT~R-K003~~4891048046264179170~PDAMPF  KNOT~R-K004~~4638663808856251977~RHO  KNOT~R-K004~~4638663808856251977~P  KNOT~R-K004~~4638663808856251977~H  KNOT~R-K004~~4638663808856251977~HMAX_INST  KNOT~R-K004~~4638663808856251977~HMIN_INST  KNOT~R-K004~~4638663808856251977~PMAX_INST  KNOT~R-K004~~4638663808856251977~PMIN_INST  KNOT~R-K004~~4638663808856251977~PDAMPF  KNOT~R-K005~~5183147862966701025~RHO  KNOT~R-K005~~5183147862966701025~P  KNOT~R-K005~~5183147862966701025~H  KNOT~R-K005~~5183147862966701025~HMAX_INST  KNOT~R-K005~~5183147862966701025~HMIN_INST  KNOT~R-K005~~5183147862966701025~PMAX_INST  KNOT~R-K005~~5183147862966701025~PMIN_INST  KNOT~R-K005~~5183147862966701025~PDAMPF  KNOT~R-K006~~5543326527366090679~RHO  KNOT~R-K006~~5543326527366090679~P  KNOT~R-K006~~5543326527366090679~H  KNOT~R-K006~~5543326527366090679~HMAX_INST  KNOT~R-K006~~5543326527366090679~HMIN_INST  KNOT~R-K006~~5543326527366090679~PMAX_INST  KNOT~R-K006~~5543326527366090679~PMIN_INST  KNOT~R-K006~~5543326527366090679~PDAMPF  KNOT~R-K007~~5508992300317633799~RHO  KNOT~R-K007~~5508992300317633799~P  KNOT~R-K007~~5508992300317633799~H  KNOT~R-K007~~5508992300317633799~HMAX_INST  KNOT~R-K007~~5508992300317633799~HMIN_INST  KNOT~R-K007~~5508992300317633799~PMAX_INST  KNOT~R-K007~~5508992300317633799~PMIN_INST  KNOT~R-K007~~5508992300317633799~PDAMPF  ROHR~V-L~V-K000~4939422678063487923~VI  ROHR~V-L~V-K000~4939422678063487923~VK  ROHR~V-L~V-K000~4939422678063487923~QMI  ROHR~V-L~V-K000~4939422678063487923~QMK  ROHR~V-K000~V-K001~4984202422877610920~VI  ROHR~V-K000~V-K001~4984202422877610920~VK  ROHR~V-K000~V-K001~4984202422877610920~QMI  ROHR~V-K000~V-K001~4984202422877610920~QMK  ROHR~V-K001~V-K002~4789218195240364437~VI  ROHR~V-K001~V-K002~4789218195240364437~VK  ROHR~V-K001~V-K002~4789218195240364437~QMI  ROHR~V-K001~V-K002~4789218195240364437~QMK  ROHR~V-K002~V-K003~4614949065966596185~VI  ROHR~V-K002~V-K003~4614949065966596185~VK  ROHR~V-K002~V-K003~4614949065966596185~QMI  ROHR~V-K002~V-K003~4614949065966596185~QMK  ROHR~V-K003~V-K004~5037777106796980248~VI  ROHR~V-K003~V-K004~5037777106796980248~VK  ROHR~V-K003~V-K004~5037777106796980248~QMI  ROHR~V-K003~V-K004~5037777106796980248~QMK  ROHR~V-K004~V-K005~4713733238627697042~VI  ROHR~V-K004~V-K005~4713733238627697042~VK  ROHR~V-K004~V-K005~4713733238627697042~QMI  ROHR~V-K004~V-K005~4713733238627697042~QMK  ROHR~V-K005~V-K006~5123819811204259837~VI  ROHR~V-K005~V-K006~5123819811204259837~VK  ROHR~V-K005~V-K006~5123819811204259837~QMI  ROHR~V-K005~V-K006~5123819811204259837~QMK  ROHR~V-K006~V-K007~5620197984230756681~VI  ROHR~V-K006~V-K007~5620197984230756681~VK  ROHR~V-K006~V-K007~5620197984230756681~QMI  ROHR~V-K006~V-K007~5620197984230756681~QMK  ROHR~R-L~R-K000~4769996343148550485~VI  ROHR~R-L~R-K000~4769996343148550485~VK  ROHR~R-L~R-K000~4769996343148550485~QMI  ROHR~R-L~R-K000~4769996343148550485~QMK  ROHR~R-K000~R-K001~5647213228462830353~VI  ROHR~R-K000~R-K001~5647213228462830353~VK  ROHR~R-K000~R-K001~5647213228462830353~QMI  ROHR~R-K000~R-K001~5647213228462830353~QMK  ROHR~R-K001~R-K002~5266224553324203132~VI  ROHR~R-K001~R-K002~5266224553324203132~VK  ROHR~R-K001~R-K002~5266224553324203132~QMI  ROHR~R-K001~R-K002~5266224553324203132~QMK  ROHR~R-K002~R-K003~5379365049009065623~VI  ROHR~R-K002~R-K003~5379365049009065623~VK  ROHR~R-K002~R-K003~5379365049009065623~QMI  ROHR~R-K002~R-K003~5379365049009065623~QMK  ROHR~R-K003~R-K004~4637102239750163477~VI  ROHR~R-K003~R-K004~4637102239750163477~VK  ROHR~R-K003~R-K004~4637102239750163477~QMI  ROHR~R-K003~R-K004~4637102239750163477~QMK  ROHR~R-K004~R-K005~4613782368750024999~VI  ROHR~R-K004~R-K005~4613782368750024999~VK  ROHR~R-K004~R-K005~4613782368750024999~QMI  ROHR~R-K004~R-K005~4613782368750024999~QMK  ROHR~R-K005~R-K006~5611703699850694889~VI  ROHR~R-K005~R-K006~5611703699850694889~VK  ROHR~R-K005~R-K006~5611703699850694889~QMI  ROHR~R-K005~R-K006~5611703699850694889~QMK  ROHR~R-K006~R-K007~4945727430885351042~VI  ROHR~R-K006~R-K007~4945727430885351042~VK  ROHR~R-K006~R-K007~4945727430885351042~QMI  ROHR~R-K006~R-K007~4945727430885351042~QMK  PUMP~R-1~R2~5481331875203087055~RHO  PUMP~R-1~R2~5481331875203087055~M  PUMP~R-1~R2~5481331875203087055~ETA  PUMP~R-1~R2~5481331875203087055~ETAW  PUMP~R-1~R2~5481331875203087055~DP  FWES~*~*~*~IAKTIV  KLAP~*~*~*~IAKTIV  PUMP~*~*~*~IAKTIV
   2004-09-22 08:30:00+00:00                b'STAT'                 0                0                0               21                  0           0.000002                0              0.0                  0                  0                0.0                0.0           89.511505                 8              1.0               50                     0.0                     0.0                    0.0                23.12059       975.700012     619.633301        4.11655               1.500571              4.311969                   2.0                   90.0           0.000002                          4.126546                         802.719727                             1.500571                                      2.719672                          2.000133                        1142.490845                             90.0                                  802.719727                                       800.0                             22.98794                                           0.0                            60.0                            0.330514                            2.754284                                60.0                                90.0                                    480.0                                  0.000002                                   1.845007                                             0                                    0.914001                                         0.8                                160.000031                                         160.0                                   1.500571                                             0                                         0.8                                         0.8                                     160.0                                         160.0                                   1.562085                                             0                                    0.642765                                         0.6                                120.000008                                    120.000008                                   1.523539                                             0                                         1.0                                         1.0                                200.000015                                         200.0                                             0                                         0.8                                         0.8                                     160.0                                         160.0                                   3.928163                                   3.928163                                       90.0                                       65.0                                     89.511505                                       90.0                                       55.0                                     86.514343                         965.700012                         5.126546                         4.126546                                 4.126546                                 4.126546                                 5.126546                                 5.126546                                0.7011                            965.700012                            5.122155                            4.122155                                    4.122155                                    4.122155                                    5.122155                                    5.122155                                   0.7011                            965.700012                            5.084035                            4.084035                                    4.084035                                    4.084035                                    5.084035                                    5.084035                                   0.7011                            965.700012                            4.986475                            3.986475                                    3.986475                                    3.986475                                    4.986475                                    4.986475                                   0.7011                            965.700012                            4.845703                            3.845703                                    3.845703                                    3.845703                                    4.845703                                    4.845703                                   0.7011                            965.700012                            4.826566                            3.826566                                    3.826566                                    3.826566                                    4.826566                                    4.826566                                   0.7011                            965.700012                            4.820062                            3.820062                                    3.820062                                    3.820062                                    4.820062                                    4.820062                                   0.7011                            965.700012                            4.817194                            3.817194                                    3.817194                                    3.817194                                    4.817194                                    4.817194                                   0.7011                            965.700012                            4.815285                            3.815285                                    3.815285                                    3.815285                                    4.815285                                    4.815285                                   0.7011                         983.700012                         3.000133                         2.000133                                 2.000133                                 2.000133                                 3.000133                                 3.000133                                0.1992                            983.700012                            3.004938                            2.004938                                    2.004938                                    2.004938                                    3.004938                                    3.004938                                   0.1992                            983.700012                            3.043297                            2.043297                                    2.043297                                    2.043297                                    3.043297                                    3.043297                                   0.1992                            983.700012                            3.141468                            2.141468                                    2.141468                                    2.141468                                    3.141468                                    3.141468                                   0.1992                            983.700012                            3.283618                            2.283618                                    2.283618                                    2.283618                                    3.283618                                    3.283618                                   0.1992                            983.700012                            3.303027                            2.303027                                    2.303027                                    2.303027                                    3.303027                                    3.303027                                   0.1992                            983.700012                            3.309712                            2.309712                                    2.309712                                    2.309712                                    3.309712                                    3.309712                                   0.1992                            983.700012                            3.312715                            2.312715                                    2.312715                                    2.312715                                    3.312715                                    3.312715                                   0.1992                            983.700012                            3.314715                            2.314715                                    2.314715                                    2.314715                                    3.314715                                    3.314715                                   0.1992                                0.327641                                0.327641                                 22.98794                                 22.98794                                   0.733984                                   0.733984                                    22.98794                                    22.98794                                   0.733984                                   0.733984                                    22.98794                                    22.98794                                   0.608561                                   0.608561                                   19.059776                                   19.059776                                   0.491034                                   0.491034                                   15.378898                                   15.378898                                     0.2717                                     0.2717                                    8.509472                                    8.509472                                   0.125423                                   0.125423                                    3.928163                                    3.928163                                   0.125423                                   0.125423                                    3.928163                                    3.928163                               -0.321646                               -0.321646                               -22.987938                               -22.987938                                  -0.720553                                  -0.720553                                  -22.987938                                  -22.987938                                  -0.720553                                  -0.720553                                  -22.987938                                  -22.987938                                  -0.597426                                  -0.597426                                  -19.059776                                  -19.059776                                  -0.482049                                  -0.482049                                  -15.378897                                  -15.378897                                  -0.266728                                  -0.266728                                   -8.509471                                   -8.509471                                  -0.123128                                  -0.123128                                   -3.928163                                   -3.928163                                  -0.123128                                  -0.123128                                   -3.928163                                   -3.928163                           983.700012                           6.385539                             0.544889                              0.625568                            2.311969                  0                  0                  0'''
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.41',1,'New',"getMxsVecsFileData")) 
>>> timesReq=[]
>>> timesReq.append(mx.df.index[0])
>>> plotTimeDfs=mx.getMxsVecsFileData(timesReq=timesReq)
>>> len(plotTimeDfs)
1
>>> isinstance(plotTimeDfs[0],pd.core.frame.DataFrame)
True
>>> print("'''{:s}'''".format(repr(plotTimeDfs[0]).replace('\\n','\\n   ')))
'''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ROHR~*~*~*~MVEC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ROHR~*~*~*~RHOVEC                                                                                                                                                                                   ROHR~*~*~*~ZVEC                                                                                                                                                                                                                                                                                                                                             ROHR~*~*~*~PHR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ROHR~*~*~*~PVEC                                                                                                                                                                                                                                                                                                                                                                                                     KNOT~*~~*~DP                                                                                                                                                                                   ROHR~*~*~*~TVEC                                                                                                                                                                                                                                                                                                        ROHR~*~*~*~WALTERI                                                                                                                                                                                                                                                                                                         ROHR~*~*~*~WALTERK                                                                                                                                 KNOT~*~~*~T                                                                                                                                                                                                                                                                                                                                                                                                                      KNOT~*~~*~PH                                                                FWVB~*~*~*~W                                                                                        FWVB~*~*~*~QM                                                                                                                                                                                                                                                                                                                        ROHR~*~*~*~QMAV                                                                                                                                                                                                                                                                                                                              ROHR~*~*~*~VAV ROHR~V-L~V-K000~4939422678063487923~SVEC ROHR~V-L~V-K000~4939422678063487923~PVECMAX_INST ROHR~V-L~V-K000~4939422678063487923~PVECMIN_INST ROHR~V-K000~V-K001~4984202422877610920~SVEC ROHR~V-K000~V-K001~4984202422877610920~PVECMAX_INST ROHR~V-K000~V-K001~4984202422877610920~PVECMIN_INST ROHR~V-K001~V-K002~4789218195240364437~SVEC ROHR~V-K001~V-K002~4789218195240364437~PVECMAX_INST ROHR~V-K001~V-K002~4789218195240364437~PVECMIN_INST ROHR~V-K002~V-K003~4614949065966596185~SVEC ROHR~V-K002~V-K003~4614949065966596185~PVECMAX_INST ROHR~V-K002~V-K003~4614949065966596185~PVECMIN_INST ROHR~V-K003~V-K004~5037777106796980248~SVEC ROHR~V-K003~V-K004~5037777106796980248~PVECMAX_INST ROHR~V-K003~V-K004~5037777106796980248~PVECMIN_INST ROHR~V-K004~V-K005~4713733238627697042~SVEC ROHR~V-K004~V-K005~4713733238627697042~PVECMAX_INST ROHR~V-K004~V-K005~4713733238627697042~PVECMIN_INST ROHR~V-K005~V-K006~5123819811204259837~SVEC ROHR~V-K005~V-K006~5123819811204259837~PVECMAX_INST ROHR~V-K005~V-K006~5123819811204259837~PVECMIN_INST ROHR~V-K006~V-K007~5620197984230756681~SVEC ROHR~V-K006~V-K007~5620197984230756681~PVECMAX_INST ROHR~V-K006~V-K007~5620197984230756681~PVECMIN_INST ROHR~R-L~R-K000~4769996343148550485~SVEC ROHR~R-L~R-K000~4769996343148550485~PVECMAX_INST ROHR~R-L~R-K000~4769996343148550485~PVECMIN_INST ROHR~R-K000~R-K001~5647213228462830353~SVEC ROHR~R-K000~R-K001~5647213228462830353~PVECMAX_INST ROHR~R-K000~R-K001~5647213228462830353~PVECMIN_INST ROHR~R-K001~R-K002~5266224553324203132~SVEC ROHR~R-K001~R-K002~5266224553324203132~PVECMAX_INST ROHR~R-K001~R-K002~5266224553324203132~PVECMIN_INST ROHR~R-K002~R-K003~5379365049009065623~SVEC ROHR~R-K002~R-K003~5379365049009065623~PVECMAX_INST ROHR~R-K002~R-K003~5379365049009065623~PVECMIN_INST ROHR~R-K003~R-K004~4637102239750163477~SVEC ROHR~R-K003~R-K004~4637102239750163477~PVECMAX_INST ROHR~R-K003~R-K004~4637102239750163477~PVECMIN_INST ROHR~R-K004~R-K005~4613782368750024999~SVEC ROHR~R-K004~R-K005~4613782368750024999~PVECMAX_INST ROHR~R-K004~R-K005~4613782368750024999~PVECMIN_INST ROHR~R-K005~R-K006~5611703699850694889~SVEC ROHR~R-K005~R-K006~5611703699850694889~PVECMAX_INST ROHR~R-K005~R-K006~5611703699850694889~PVECMIN_INST ROHR~R-K006~R-K007~4945727430885351042~SVEC ROHR~R-K006~R-K007~4945727430885351042~PVECMAX_INST ROHR~R-K006~R-K007~4945727430885351042~PVECMIN_INST                                                       KNOT~*~~*~IAKTIV                                 ROHR~*~*~*~IAKTIV FWVB~*~*~*~IAKTIV VENT~*~*~*~IAKTIV                                                                                                                                                                                                                                                                                                                                                                                                       KNOT~*~~*~WALTER
   2004-09-22 08:30:00+00:00  (-2.3637421131134033, -2.3637421131134033, 5.294382572174072, 5.294382572174072, -4.271915912628174, -4.271915912628174, 2.3637421131134033, 2.3637421131134033, -6.385538578033447, -6.385538578033447, 6.3855390548706055, 6.3855390548706055, 6.3855390548706055, 6.3855390548706055, -1.0911563634872437, -1.0911563634872437, 6.3855390548706055, 6.3855390548706055, 4.271915912628174, 4.271915912628174, 1.0911564826965332, 1.0911564826965332, -6.385538578033447, -6.385538578033447, -5.294382095336914, -5.294382095336914, -1.0911563634872437, -1.0911563634872437, 1.0911564826965332, 1.0911564826965332, -6.385538578033447, -6.385538578033447)  (983.7000122070312, 983.7000122070312, 965.7000122070312, 965.7000122070312, 983.7000122070312, 983.7000122070312, 965.7000122070312, 965.7000122070312, 983.7000122070312, 983.7000122070312, 965.7000122070312, 965.7000122070312, 965.7000122070312, 965.7000122070312, 983.7000122070312, 983.7000122070312, 965.7000122070312, 965.7000122070312, 965.7000122070312, 965.7000122070312, 965.7000122070312, 965.7000122070312, 983.7000122070312, 983.7000122070312, 983.7000122070312, 983.7000122070312, 983.7000122070312, 983.7000122070312, 965.7000122070312, 965.7000122070312, 983.7000122070312, 983.7000122070312)  (20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0)  (0.006684500724077225, 0.14074617624282837, 0.01940573751926422, 0.006503125187009573, 0.004804093856364489, 0.097540944814682, 0.004389858338981867, 0.001999376341700554, 0.03811245411634445, 0.019133789464831352, 0.0028679801616817713, 0.09815507382154465, 0.1421286016702652, 0.0030037090182304382, 0.0019090300193056464, 0.03835241496562958)  (3.3030266761779785, 3.3097116947174072, 4.986474990844727, 4.845702648162842, 3.283618688583374, 3.3030266761779785, 4.826566219329834, 4.820062160491943, 3.0001330375671387, 3.0049381256103516, 5.084035396575928, 4.986474990844727, 5.126544952392578, 5.122154712677002, 3.312715530395508, 3.3147149085998535, 5.122154712677002, 5.084035396575928, 4.845702648162842, 4.826566219329834, 4.820062160491943, 4.817193984985352, 3.0432968139648438, 3.141468048095703, 3.141468048095703, 3.283618688583374, 3.3097116947174072, 3.312715530395508, 4.817193984985352, 4.8152852058410645, 3.0049381256103516, 3.0432968139648438)  (1.523539423942566, 1.8450068235397339, 2.040738344192505, 2.1172170639038086, 2.040738344192505, 1.562084674835205, 2.1172170639038086, 0.0, 2.126680850982666, 1.5103505849838257, 0.0, 2.126412868499756, 1.8450068235397339, 1.523539423942566, 0.0, 1.5103505849838257, 1.50057053565979, 1.504478931427002, 1.504478931427002, 2.126680850982666, 1.562084674835205, 2.126412868499756, 1.50057053565979)  (60.0, 60.0, 90.0, 90.0, 60.0, 60.0, 90.0, 90.0, 60.0, 60.0, 90.0, 90.0, 90.0, 90.0, 60.0, 60.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 90.0, 90.0, 60.0, 60.0)  (0.37772566080093384, 0.16107234358787537, 0.257148802280426, 0.3936369717121124, 0.49676957726478577, 0.08707359433174133, 0.0, 0.24764277040958405, 0.05815984681248665, 0.3463727831840515, 0.4836260676383972, 0.4039103388786316, 0.39624181389808655, 0.6196821928024292, 0.8488578200340271, 0.43336305022239685)  (0.2860592305660248, 0.3463727831840515, 0.20900364220142365, 0.4836260676383972, 0.43336305022239685, 0.16107235848903656, 0.05815984681248665, 0.0, 0.08707359433174133, 0.3936369717121124, 0.8488578200340271, 0.32853230834007263, 0.20748749375343323, 0.24764277040958405, 1.0919691324234009, 0.4039103388786316)  (60.0, 90.0, 90.0, 90.0, 60.0, 60.0, 60.0, 60.0, 90.0, 60.0, 60.0, 60.0, 60.0, 90.0, 60.0, 90.0, 60.0, 90.0, 60.0, 60.0, 90.0, 90.0, 90.0)  (2.3030266761779785, 3.9864749908447266, 4.0840349197387695, 4.122154712677002, 2.0432965755462646, 2.283618450164795, 2.0049376487731934, 4.311968803405762, 4.126680850982666, 2.3097116947174072, 4.292252063751221, 2.0001327991485596, 2.141468048095703, 3.826566219329834, 2.0, 3.8200621604919434, 2.3147146701812744, 3.8171942234039307, 2.3127152919769287, 2.0, 3.845703125, 4.1265459060668945, 3.8152852058410645)  (160.00003051757812, 200.00001525878906, 160.0, 160.0, 120.00000762939453)  (3.9281632900238037, 6.8694257736206055, 4.581308364868164, 3.9281630516052246, 3.6808788776397705)  (-8.50947093963623, 19.059776306152344, -15.378896713256836, 8.509471893310547, -22.987937927246094, 22.987939834594727, 22.987939834594727, -3.9281630516052246, 22.987939834594727, 15.378897666931152, 3.9281632900238037, -22.987937927246094, -19.059776306152344, -3.9281628131866455, 3.9281630516052246, -22.987937927246094)  (-0.2667279839515686, 0.6085611581802368, -0.48204901814460754, 0.2716996371746063, -0.3216457962989807, 0.7339838147163391, 0.327641099691391, -0.12312762439250946, 0.7339838743209839, 0.4910340905189514, 0.1254226565361023, -0.7205531597137451, -0.5974255204200745, -0.12312762439250946, 0.1254226416349411, -0.7205531597137451)                  (0.0, 68.5999984741211)           (5.126544952392578, 5.122154712677002)           (5.126544952392578, 5.122154712677002)                     (0.0, 76.4000015258789)              (5.122154712677002, 5.084035396575928)              (5.122154712677002, 5.084035396575928)                   (0.0, 195.52999877929688)              (5.084035396575928, 4.986474990844727)              (5.084035396575928, 4.986474990844727)                    (0.0, 405.9599914550781)              (4.986474990844727, 4.845702648162842)              (4.986474990844727, 4.845702648162842)                    (0.0, 83.55000305175781)              (4.845702648162842, 4.826566219329834)              (4.845702648162842, 4.826566219329834)                     (0.0, 88.0199966430664)              (4.826566219329834, 4.820062160491943)              (4.826566219329834, 4.820062160491943)                   (0.0, 164.91000366210938)              (4.820062160491943, 4.817193984985352)              (4.820062160491943, 4.817193984985352)                    (0.0, 109.7699966430664)             (4.817193984985352, 4.8152852058410645)             (4.817193984985352, 4.8152852058410645)                 (0.0, 73.41999816894531)         (3.0001330375671387, 3.0049381256103516)         (3.0001330375671387, 3.0049381256103516)                     (0.0, 76.4000015258789)            (3.0049381256103516, 3.0432968139648438)            (3.0049381256103516, 3.0432968139648438)                   (0.0, 195.52999877929688)             (3.0432968139648438, 3.141468048095703)             (3.0432968139648438, 3.141468048095703)                    (0.0, 405.9599914550781)              (3.141468048095703, 3.283618688583374)              (3.141468048095703, 3.283618688583374)                    (0.0, 83.55000305175781)             (3.283618688583374, 3.3030266761779785)             (3.283618688583374, 3.3030266761779785)                     (0.0, 88.0199966430664)            (3.3030266761779785, 3.3097116947174072)            (3.3030266761779785, 3.3097116947174072)                   (0.0, 164.91000366210938)             (3.3097116947174072, 3.312715530395508)             (3.3097116947174072, 3.312715530395508)                    (0.0, 109.7699966430664)             (3.312715530395508, 3.3147149085998535)             (3.312715530395508, 3.3147149085998535)  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)   (0, 0, 0, 0, 0)         (0, 0, 0)  (0.20900364220142365, 0.16107234358787537, 0.08707359433174133, 0.05815984681248665, 0.4039103388786316, 0.20748749375343323, 0.43336305022239685, 0.496769517660141, 0.0, 0.2860592305660248, 0.496769517660141, 0.4967695474624634, 0.32853230834007263, 0.3936369717121124, 0.0, 0.4836260676383972, 0.0, 0.8488578200340271, 0.24764277040958405, 0.496769517660141, 0.3463727831840515, 0.0, 1.0919691324234009)'''
>>> l=plotTimeDfs[0]['FWVB~*~*~*~W'].iloc[0]
>>> list(map(lambda x: round(x,2),l))
[160.0, 200.0, 160.0, 160.0, 120.0]
>>> timesReq[0]=timesReq[0]-pd.to_timedelta('1 second')
>>> plotTimeDfs=mx.getMxsVecsFileData(timesReq=timesReq)
>>> len(plotTimeDfs)
0
>>> # ---
>>> # Clean Up LocalHeatingNetwork
>>> # ---
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> # ---
>>> # TinyWDN
>>> # ---
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDTinyWDN\B1\V0\BZ1\M-1-0-1.MX1'))
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> print("'''{:s}'''".format(repr(mx.mx1Df).replace('\\n','\\n   ')))
'''    ADDEND      ATTRTYPE CLIENT_FLAGS CLIENT_ID  DATALENGTH  DATAOFFSET DATATYPE  DATATYPELENGTH DEVIATION FACTOR  FLAGS LINKED_CHANNEL LOWER_LIMIT    NAME1    NAME2 NAME3 OBJTYPE           OBJTYPE_PK OPCITEM_ID                                     TITLE       UNIT UPPER_LIMIT                                          Sir3sID  NOfItems  isVectorChannel  isVectorChannelMx2  isVectorChannelMx2Rvec  unpackIdx
   0        0     TIMESTAMP            0                    32           0     CHAR              32         0      1    241             -1      -1E+20                            ALLG                   -1                            Zeitstempel nach ISO 8601     [text]       1E+20                              ALLG~~~-1~TIMESTAMP         1            False               False                   False          0
   1        0  SNAPSHOTTYPE            0                     4          32     CHAR               4         0      1    241             -1      -1E+20                            ALLG                   -1               Typ des Zeitpunktes/Ausgabedatensatzes     [text]       1E+20                           ALLG~~~-1~SNAPSHOTTYPE         1            False               False                   False          1
   2        0        CVERSO            0                    80          36     CHAR              80         0      1    241             -1      -1E+20                            ALLG                   -1                                      Versionskennung     [text]       1E+20                                 ALLG~~~-1~CVERSO         1            False               False                   False          2
   3        0        EXSTAT            0                     4         116     INT4               4         0      1   1265             -1      -1E+20                            ALLG                   -1                           Exit-Status der Berechnung         []       1E+20                                 ALLG~~~-1~EXSTAT         1            False               False                   False          3
   4        0         NFEHL            0                     4         120     INT4               4         0      1    241             -1      -1E+20                            ALLG                   -1                Anzahl Fehler im Berechnungsabschnitt         []       1E+20                                  ALLG~~~-1~NFEHL         1            False               False                   False          4
   5        0         NWARN            0                     4         124     INT4               4         0      1    241             -1      -1E+20                            ALLG                   -1             Anzahl Warnungen im Berechnungsabschnitt         []       1E+20                                  ALLG~~~-1~NWARN         1            False               False                   False          5
   6        0         NMELD            0                     4         128     INT4               4         0      1    241             -1      -1E+20                            ALLG                   -1             Anzahl Meldungen im Berechnungsabschnitt         []       1E+20                                  ALLG~~~-1~NMELD         1            False               False                   False          6
   7        0       CPUTIME            0                     4         132     REAL               4         0      1    241             -1      -1E+20                            ALLG                   -1                                  CPU-Zeit seit Start        [s]       1E+20                                ALLG~~~-1~CPUTIME         1            False               False                   False          7
   8        0       USRTIME            0                     4         136     REAL               4         0      1    241             -1      -1E+20                            ALLG                   -1                                  USR-Zeit seit Start        [s]       1E+20                                ALLG~~~-1~USRTIME         1            False               False                   False          8
   9        0       NPGREST            0                     4         140     INT4               4         0      1     49             -1      -1E+20                            ALLG                   -1                   Anzahl aktiver PGRP in Restriktion         []       1E+20                                ALLG~~~-1~NPGREST         1            False               False                   False          9
   10       0       NETZABN            0                     4         144     REAL               4         0      1   1233             -1      -1E+20                            ALLG                   -1                                          Netzabnahme     [m3/h]       1E+20                                ALLG~~~-1~NETZABN         1            False               False                   False         10
   11       0         NKNUV            0                     4         148     INT4               4         0      1   1233             -1      -1E+20                            ALLG                   -1                      Anzahl KNOT mit Unterversorgung         []       1E+20                                  ALLG~~~-1~NKNUV         1            False               False                   False         11
   12       0         MKNUV            0                     4         152     REAL               4         0      1   1233             -1      -1E+20                            ALLG                   -1                   Fehlmenge KNOT aus Unterversorgung     [m3/h]       1E+20                                  ALLG~~~-1~MKNUV         1            False               False                   False         12
   13       0       NFVHYUV            0                     4         156     INT4               4         0      1   1057             -1      -1E+20                            ALLG                   -1                Anzahl FWVB mit hydr. Unterversorgung         []       1E+20                                ALLG~~~-1~NFVHYUV         1            False               False                   False         13
   14       0       NFVTHUV            0                     4         160     INT4               4         0      1   1057             -1      -1E+20                            ALLG                   -1                Anzahl FWVB mit ther. Unterversorgung         []       1E+20                                ALLG~~~-1~NFVTHUV         1            False               False                   False         14
   15       0       MFVHYUV            0                     4         164     REAL               4         0      1   1057             -1      -1E+20                            ALLG                   -1             Fehlmenge FWVB aus hydr. Unterversorgung     [m3/h]       1E+20                                ALLG~~~-1~MFVHYUV         1            False               False                   False         15
   16       0       MFVTHUV            0                     4         168     REAL               4         0      1   1057             -1      -1E+20                            ALLG                   -1             Fehlmenge FWVB aus ther. Unterversorgung     [m3/h]       1E+20                                ALLG~~~-1~MFVTHUV         1            False               False                   False         16
   17       0      TVMINMAX            0                     4         172     REAL               4         0      1   1057             -1      -1E+20                            ALLG                   -1                  Maximum der erf. min. VL-Temperatur       [°C]       1E+20                               ALLG~~~-1~TVMINMAX         1            False               False                   False         17
   18       0        ITERHY            0                     4         176     INT4               4         0      1   1265             -1      -1E+20                            ALLG                   -1                Anzahl benötigter (hydr.) Iterationen         []       1E+20                                 ALLG~~~-1~ITERHY         1            False               False                   False         18
   19       0         LFQSV            0                     4         180     REAL               4         0      1   1041             -1      -1E+20                            ALLG                   -1                       Lastfaktor für Strangentnahmen         []       1E+20                                  ALLG~~~-1~LFQSV         1            False               False                   False         19
   20       0         JWARN            0                     4         184     INT4               4         0      1    241             -1      -1E+20                            ALLG                   -1                                            Warnstufe         []       1E+20                                  ALLG~~~-1~JWARN         1            False               False                   False         20
   21       0  NETZABNEXITS            0                     4         188     REAL               4         0      1   1233             -1      -1E+20                            ALLG                   -1                         Netzabnahme ohne Druckränder     [m3/h]       1E+20                           ALLG~~~-1~NETZABNEXITS         1            False               False                   False         21
   22       0  LINEPACKRATE            0                     4         192     REAL               4         0      1     65             -1      -1E+20                            ALLG                   -1                                 Gesamt-Linepack-Rate  [(N)m3/h]       1E+20                           ALLG~~~-1~LINEPACKRATE         1            False               False                   False         22
   23       0   LINEPACKGES            0                     4         196     REAL               4         0      1     65             -1      -1E+20                            ALLG                   -1                                      Gesamt-Linepack    [(N)m3]       1E+20                            ALLG~~~-1~LINEPACKGES         1            False               False                   False         23
   24       0  LINEPACKGEOM            0                     4         200     REAL               4         0      1     65             -1      -1E+20                            ALLG                   -1                           Gesamt-Linepack Rohrinhalt    [(N)m3]       1E+20                           ALLG~~~-1~LINEPACKGEOM         1            False               False                   False         24
   25       0         RHOAV            0                     4         204     REAL               4         0      1   1265             -1      -1E+20                            ALLG                   -1                                      Mittlere Dichte    [kg/m3]       1E+20                                  ALLG~~~-1~RHOAV         1            False               False                   False         25
   26       0           TAV            0                     4         208     REAL               4         0      1   1265             -1      -1E+20                            ALLG                   -1                                  Mittlere Temperatur       [°C]       1E+20                                    ALLG~~~-1~TAV         1            False               False                   False         26
   27       0           PAV            0                     4         212     REAL               4         0      1   1265             -1      -1E+20                            ALLG                   -1                                      Mittlerer Druck    [bar,a]       1E+20                                    ALLG~~~-1~PAV         1            False               False                   False         27
   28       0   FWVB_DPHMIN            0                     4         216     REAL               4         0      1   1057             -1      -1E+20                            ALLG                   -1                Min. Differenzdruck aller Verbraucher      [mNN]       1E+20                            ALLG~~~-1~FWVB_DPHMIN         1            False               False                   False         28
   29       0    KNOT_PHMAX            0                     4         220     REAL               4         0      1   1265             -1      -1E+20                            ALLG                   -1                             Max. Knotendruck im Netz      [bar]       1E+20                             ALLG~~~-1~KNOT_PHMAX         1            False               False                   False         29
   30       0    KNOT_PHMIN            0                     4         224     REAL               4         0      1   1265             -1      -1E+20                            ALLG                   -1                             Min. Knotendruck im Netz      [bar]       1E+20                             ALLG~~~-1~KNOT_PHMIN         1            False               False                   False         30
   31       0   FWVB_TVLMIN            0                     4         228     REAL               4         0      1   1057             -1      -1E+20                            ALLG                   -1                 Min. VL-Temperatur aller Verbraucher       [°C]       1E+20                            ALLG~~~-1~FWVB_TVLMIN         1            False               False                   False         31
   32       0       NETZBEZ            0                     4         232     REAL               4         0      1   1233             -1      -1E+20                            ALLG                   -1                                            Netzbezug     [m3/h]       1E+20                                ALLG~~~-1~NETZBEZ         1            False               False                   False         32
   33       0            PH            0                     4         236     REAL               4         0      1      1             -1      -1E+20        3                   KNOT  4711309381204507891                                                           [bar]       1E+20                   KNOT~3~~4711309381204507891~PH         1            False               False                   False         33
   34       0             H            0                     4         240     REAL               4         0      1      1             -1      -1E+20        3                   KNOT  4711309381204507891                                                           [mNN]       1E+20                    KNOT~3~~4711309381204507891~H         1            False               False                   False         34
   35       0            QM            0                     4         244     REAL               4         0      1      1             -1      -1E+20       WW                   KNOT  5179406559406617933                                                          [m3/h]       1E+20                  KNOT~WW~~5179406559406617933~QM         1            False               False                   False         35
   36       0            PH            0                     4         248     REAL               4         0      1      1             -1      -1E+20       WW                   KNOT  5179406559406617933                                                           [bar]       1E+20                  KNOT~WW~~5179406559406617933~PH         1            False               False                   False         36
   37       0             H            0                     4         252     REAL               4         0      1      1             -1      -1E+20       WW                   KNOT  5179406559406617933                                                           [mNN]       1E+20                   KNOT~WW~~5179406559406617933~H         1            False               False                   False         37
   38       0           WST            0                     4         256     REAL               4         0      1      1             -1      -1E+20       HB                   OBEH  4914542339545953765                                                             [m]       1E+20                 OBEH~HB~~4914542339545953765~WST         1            False               False                   False         38
   39       0             H            0                     4         260     REAL               4         0      1      1             -1      -1E+20       HB                   KNOT  4832703654265095420                                                           [mNN]       1E+20                   KNOT~HB~~4832703654265095420~H         1            False               False                   False         39
   40       0            QM            0                     4         264     REAL               4         0      1      1             -1      -1E+20  Absperr       HB          VENT  5466655470152247657                                                          [m3/h]       1E+20           VENT~Absperr~HB~5466655470152247657~QM         1            False               False                   False         40
   41       0          MVEC            0                   300         268     RVEC               4         0      1    245             -1      -1E+20        *        *          ROHR                    *                                                          [kg/s]       1E+20                                  ROHR~*~*~*~MVEC        75             True                True                    True         41
   42       0        RHOVEC            0                   300         568     RVEC               4         0      1    245             -1      -1E+20        *        *          ROHR                    *                                                         [kg/m3]       1E+20                                ROHR~*~*~*~RHOVEC        75             True                True                    True        116
   43       0          ZVEC            0                   300         868     RVEC               4         0      1    245             -1      -1E+20        *        *          ROHR                    *                                                             [m]       1E+20                                  ROHR~*~*~*~ZVEC        75             True                True                    True        191
   44       0           PHR            0                    88        1168     REAL               4         0      1   1269             -1      -1E+20        *        *          ROHR                    *                                                          [IDPH]       1E+20                                   ROHR~*~*~*~PHR        22             True                True                   False        266
   45       0          PVEC            0                   300        1256     RVEC               4         0      1    245             -1      -1E+20        *        *          ROHR                    *                                                         [bar,a]       1E+20                                  ROHR~*~*~*~PVEC        75             True                True                    True        288
   46       0       WALTERI            0                    88        1556     REAL               4         0      1     53             -1      -1E+20        *        *          ROHR                    *                                                             [h]       1E+20                               ROHR~*~*~*~WALTERI        22             True                True                   False        363
   47       0       WALTERK            0                    88        1644     REAL               4         0      1     53             -1      -1E+20        *        *          ROHR                    *                                                             [h]       1E+20                               ROHR~*~*~*~WALTERK        22             True                True                   False        385
   48       0            QM            0                    68        1732     REAL               4         0      1   1269             -1      -1E+20        *                   KNOT                    *                                                          [IDQM]       1E+20                                     KNOT~*~~*~QM        17             True                True                   False        407
   49       0            PH            0                    68        1800     REAL               4         0      1   1269             -1      -1E+20        *                   KNOT                    *                                                        [IDPH,4]       1E+20                                     KNOT~*~~*~PH        17             True                True                   False        424
   50       0             H            0                    68        1868     REAL               4         0      1   1269             -1      -1E+20        *                   KNOT                    *                                                        [IDPH,6]       1E+20                                      KNOT~*~~*~H        17             True                True                   False        441
   51       0          QMAV            0                    88        1936     REAL               4         0      1   1269             -1      -1E+20        *        *          ROHR                    *                                                          [IDQM]       1E+20                                  ROHR~*~*~*~QMAV        22             True                True                   False        458
   52       0           VAV            0                    88        2024     REAL               4         0      1   1269             -1      -1E+20        *        *          ROHR                    *                                                           [m/s]       1E+20                                   ROHR~*~*~*~VAV        22             True                True                   False        480
   53       0           RHO            0                     4        2112     REAL               4         0      1   1265             -1      -1E+20       WW                   KNOT  5179406559406617933                                                         [kg/m3]       1E+20                 KNOT~WW~~5179406559406617933~RHO         1            False               False                   False        502
   54       0             P            0                     4        2116     REAL               4         0      1   1265             -1      -1E+20       WW                   KNOT  5179406559406617933                                                         [bar,a]       1E+20                   KNOT~WW~~5179406559406617933~P         1            False               False                   False        503
   55       0     HMAX_INST            0                     4        2120     REAL               4         0      1   2161             -1      -1E+20       WW                   KNOT  5179406559406617933                                                        [IDPH,6]       1E+20           KNOT~WW~~5179406559406617933~HMAX_INST         1            False               False                   False        504
   56       0     HMIN_INST            0                     4        2124     REAL               4         0      1   2161             -1      -1E+20       WW                   KNOT  5179406559406617933                                                        [IDPH,6]       1E+20           KNOT~WW~~5179406559406617933~HMIN_INST         1            False               False                   False        505
   57       0     PMAX_INST            0                     4        2128     REAL               4         0      1   2161             -1      -1E+20       WW                   KNOT  5179406559406617933                                                          [IDPH]       1E+20           KNOT~WW~~5179406559406617933~PMAX_INST         1            False               False                   False        506
   58       0     PMIN_INST            0                     4        2132     REAL               4         0      1   2161             -1      -1E+20       WW                   KNOT  5179406559406617933                                                          [IDPH]       1E+20           KNOT~WW~~5179406559406617933~PMIN_INST         1            False               False                   False        507
   59       0        PDAMPF            0                     4        2136     REAL               4         0      1     49             -1      -1E+20       WW                   KNOT  5179406559406617933                                                         [bar,a]       1E+20              KNOT~WW~~5179406559406617933~PDAMPF         1            False               False                   False        508
   60       0             T            0                     4        2140     REAL               4         0      1   1265             -1      -1E+20       WW                   KNOT  5179406559406617933                                                            [°C]       1E+20                   KNOT~WW~~5179406559406617933~T         1            False               False                   False        509
   61       0           RHO            0                     4        2144     REAL               4         0      1   1265             -1      -1E+20        1                   KNOT  5028754475676510796                                                         [kg/m3]       1E+20                  KNOT~1~~5028754475676510796~RHO         1            False               False                   False        510
   62       0             P            0                     4        2148     REAL               4         0      1   1265             -1      -1E+20        1                   KNOT  5028754475676510796                                                         [bar,a]       1E+20                    KNOT~1~~5028754475676510796~P         1            False               False                   False        511
   63       0     HMAX_INST            0                     4        2152     REAL               4         0      1   2161             -1      -1E+20        1                   KNOT  5028754475676510796                                                        [IDPH,6]       1E+20            KNOT~1~~5028754475676510796~HMAX_INST         1            False               False                   False        512
   64       0     HMIN_INST            0                     4        2156     REAL               4         0      1   2161             -1      -1E+20        1                   KNOT  5028754475676510796                                                        [IDPH,6]       1E+20            KNOT~1~~5028754475676510796~HMIN_INST         1            False               False                   False        513
   65       0     PMAX_INST            0                     4        2160     REAL               4         0      1   2161             -1      -1E+20        1                   KNOT  5028754475676510796                                                          [IDPH]       1E+20            KNOT~1~~5028754475676510796~PMAX_INST         1            False               False                   False        514
   66       0     PMIN_INST            0                     4        2164     REAL               4         0      1   2161             -1      -1E+20        1                   KNOT  5028754475676510796                                                          [IDPH]       1E+20            KNOT~1~~5028754475676510796~PMIN_INST         1            False               False                   False        515
   67       0        PDAMPF            0                     4        2168     REAL               4         0      1     49             -1      -1E+20        1                   KNOT  5028754475676510796                                                         [bar,a]       1E+20               KNOT~1~~5028754475676510796~PDAMPF         1            False               False                   False        516
   68       0             T            0                     4        2172     REAL               4         0      1   1265             -1      -1E+20        1                   KNOT  5028754475676510796                                                            [°C]       1E+20                    KNOT~1~~5028754475676510796~T         1            False               False                   False        517
   69       0           RHO            0                     4        2176     REAL               4         0      1   1265             -1      -1E+20        2                   KNOT  4880261452311588026                                                         [kg/m3]       1E+20                  KNOT~2~~4880261452311588026~RHO         1            False               False                   False        518
   70       0             P            0                     4        2180     REAL               4         0      1   1265             -1      -1E+20        2                   KNOT  4880261452311588026                                                         [bar,a]       1E+20                    KNOT~2~~4880261452311588026~P         1            False               False                   False        519
   71       0     HMAX_INST            0                     4        2184     REAL               4         0      1   2161             -1      -1E+20        2                   KNOT  4880261452311588026                                                        [IDPH,6]       1E+20            KNOT~2~~4880261452311588026~HMAX_INST         1            False               False                   False        520
   72       0     HMIN_INST            0                     4        2188     REAL               4         0      1   2161             -1      -1E+20        2                   KNOT  4880261452311588026                                                        [IDPH,6]       1E+20            KNOT~2~~4880261452311588026~HMIN_INST         1            False               False                   False        521
   73       0     PMAX_INST            0                     4        2192     REAL               4         0      1   2161             -1      -1E+20        2                   KNOT  4880261452311588026                                                          [IDPH]       1E+20            KNOT~2~~4880261452311588026~PMAX_INST         1            False               False                   False        522
   74       0     PMIN_INST            0                     4        2196     REAL               4         0      1   2161             -1      -1E+20        2                   KNOT  4880261452311588026                                                          [IDPH]       1E+20            KNOT~2~~4880261452311588026~PMIN_INST         1            False               False                   False        523
   75       0        PDAMPF            0                     4        2200     REAL               4         0      1     49             -1      -1E+20        2                   KNOT  4880261452311588026                                                         [bar,a]       1E+20               KNOT~2~~4880261452311588026~PDAMPF         1            False               False                   False        524
   76       0             T            0                     4        2204     REAL               4         0      1   1265             -1      -1E+20        2                   KNOT  4880261452311588026                                                            [°C]       1E+20                    KNOT~2~~4880261452311588026~T         1            False               False                   False        525
   77       0           RHO            0                     4        2208     REAL               4         0      1   1265             -1      -1E+20        3                   KNOT  4711309381204507891                                                         [kg/m3]       1E+20                  KNOT~3~~4711309381204507891~RHO         1            False               False                   False        526
   78       0             P            0                     4        2212     REAL               4         0      1   1265             -1      -1E+20        3                   KNOT  4711309381204507891                                                         [bar,a]       1E+20                    KNOT~3~~4711309381204507891~P         1            False               False                   False        527
   79       0     HMAX_INST            0                     4        2216     REAL               4         0      1   2161             -1      -1E+20        3                   KNOT  4711309381204507891                                                        [IDPH,6]       1E+20            KNOT~3~~4711309381204507891~HMAX_INST         1            False               False                   False        528
   80       0     HMIN_INST            0                     4        2220     REAL               4         0      1   2161             -1      -1E+20        3                   KNOT  4711309381204507891                                                        [IDPH,6]       1E+20            KNOT~3~~4711309381204507891~HMIN_INST         1            False               False                   False        529
   81       0     PMAX_INST            0                     4        2224     REAL               4         0      1   2161             -1      -1E+20        3                   KNOT  4711309381204507891                                                          [IDPH]       1E+20            KNOT~3~~4711309381204507891~PMAX_INST         1            False               False                   False        530
   82       0     PMIN_INST            0                     4        2228     REAL               4         0      1   2161             -1      -1E+20        3                   KNOT  4711309381204507891                                                          [IDPH]       1E+20            KNOT~3~~4711309381204507891~PMIN_INST         1            False               False                   False        531
   83       0        PDAMPF            0                     4        2232     REAL               4         0      1     49             -1      -1E+20        3                   KNOT  4711309381204507891                                                         [bar,a]       1E+20               KNOT~3~~4711309381204507891~PDAMPF         1            False               False                   False        532
   84       0             T            0                     4        2236     REAL               4         0      1   1265             -1      -1E+20        3                   KNOT  4711309381204507891                                                            [°C]       1E+20                    KNOT~3~~4711309381204507891~T         1            False               False                   False        533
   85       0           RHO            0                     4        2240     REAL               4         0      1   1265             -1      -1E+20        4                   KNOT  5697271655044179265                                                         [kg/m3]       1E+20                  KNOT~4~~5697271655044179265~RHO         1            False               False                   False        534
   86       0             P            0                     4        2244     REAL               4         0      1   1265             -1      -1E+20        4                   KNOT  5697271655044179265                                                         [bar,a]       1E+20                    KNOT~4~~5697271655044179265~P         1            False               False                   False        535
   87       0     HMAX_INST            0                     4        2248     REAL               4         0      1   2161             -1      -1E+20        4                   KNOT  5697271655044179265                                                        [IDPH,6]       1E+20            KNOT~4~~5697271655044179265~HMAX_INST         1            False               False                   False        536
   88       0     HMIN_INST            0                     4        2252     REAL               4         0      1   2161             -1      -1E+20        4                   KNOT  5697271655044179265                                                        [IDPH,6]       1E+20            KNOT~4~~5697271655044179265~HMIN_INST         1            False               False                   False        537
   89       0     PMAX_INST            0                     4        2256     REAL               4         0      1   2161             -1      -1E+20        4                   KNOT  5697271655044179265                                                          [IDPH]       1E+20            KNOT~4~~5697271655044179265~PMAX_INST         1            False               False                   False        538
   90       0     PMIN_INST            0                     4        2260     REAL               4         0      1   2161             -1      -1E+20        4                   KNOT  5697271655044179265                                                          [IDPH]       1E+20            KNOT~4~~5697271655044179265~PMIN_INST         1            False               False                   False        539
   91       0        PDAMPF            0                     4        2264     REAL               4         0      1     49             -1      -1E+20        4                   KNOT  5697271655044179265                                                         [bar,a]       1E+20               KNOT~4~~5697271655044179265~PDAMPF         1            False               False                   False        540
   92       0             T            0                     4        2268     REAL               4         0      1   1265             -1      -1E+20        4                   KNOT  5697271655044179265                                                            [°C]       1E+20                    KNOT~4~~5697271655044179265~T         1            False               False                   False        541
   93       0           RHO            0                     4        2272     REAL               4         0      1   1265             -1      -1E+20       P4                   KNOT  5042575626021291052                                                         [kg/m3]       1E+20                 KNOT~P4~~5042575626021291052~RHO         1            False               False                   False        542
   94       0             P            0                     4        2276     REAL               4         0      1   1265             -1      -1E+20       P4                   KNOT  5042575626021291052                                                         [bar,a]       1E+20                   KNOT~P4~~5042575626021291052~P         1            False               False                   False        543
   95       0     HMAX_INST            0                     4        2280     REAL               4         0      1   2161             -1      -1E+20       P4                   KNOT  5042575626021291052                                                        [IDPH,6]       1E+20           KNOT~P4~~5042575626021291052~HMAX_INST         1            False               False                   False        544
   96       0     HMIN_INST            0                     4        2284     REAL               4         0      1   2161             -1      -1E+20       P4                   KNOT  5042575626021291052                                                        [IDPH,6]       1E+20           KNOT~P4~~5042575626021291052~HMIN_INST         1            False               False                   False        545
   97       0     PMAX_INST            0                     4        2288     REAL               4         0      1   2161             -1      -1E+20       P4                   KNOT  5042575626021291052                                                          [IDPH]       1E+20           KNOT~P4~~5042575626021291052~PMAX_INST         1            False               False                   False        546
   98       0     PMIN_INST            0                     4        2292     REAL               4         0      1   2161             -1      -1E+20       P4                   KNOT  5042575626021291052                                                          [IDPH]       1E+20           KNOT~P4~~5042575626021291052~PMIN_INST         1            False               False                   False        547
   99       0        PDAMPF            0                     4        2296     REAL               4         0      1     49             -1      -1E+20       P4                   KNOT  5042575626021291052                                                         [bar,a]       1E+20              KNOT~P4~~5042575626021291052~PDAMPF         1            False               False                   False        548
   100      0             T            0                     4        2300     REAL               4         0      1   1265             -1      -1E+20       P4                   KNOT  5042575626021291052                                                            [°C]       1E+20                   KNOT~P4~~5042575626021291052~T         1            False               False                   False        549
   101      0           RHO            0                     4        2304     REAL               4         0      1   1265             -1      -1E+20       S2                   KNOT  5388350113283448399                                                         [kg/m3]       1E+20                 KNOT~S2~~5388350113283448399~RHO         1            False               False                   False        550
   102      0             P            0                     4        2308     REAL               4         0      1   1265             -1      -1E+20       S2                   KNOT  5388350113283448399                                                         [bar,a]       1E+20                   KNOT~S2~~5388350113283448399~P         1            False               False                   False        551
   103      0     HMAX_INST            0                     4        2312     REAL               4         0      1   2161             -1      -1E+20       S2                   KNOT  5388350113283448399                                                        [IDPH,6]       1E+20           KNOT~S2~~5388350113283448399~HMAX_INST         1            False               False                   False        552
   104      0     HMIN_INST            0                     4        2316     REAL               4         0      1   2161             -1      -1E+20       S2                   KNOT  5388350113283448399                                                        [IDPH,6]       1E+20           KNOT~S2~~5388350113283448399~HMIN_INST         1            False               False                   False        553
   105      0     PMAX_INST            0                     4        2320     REAL               4         0      1   2161             -1      -1E+20       S2                   KNOT  5388350113283448399                                                          [IDPH]       1E+20           KNOT~S2~~5388350113283448399~PMAX_INST         1            False               False                   False        554
   106      0     PMIN_INST            0                     4        2324     REAL               4         0      1   2161             -1      -1E+20       S2                   KNOT  5388350113283448399                                                          [IDPH]       1E+20           KNOT~S2~~5388350113283448399~PMIN_INST         1            False               False                   False        555
   107      0        PDAMPF            0                     4        2328     REAL               4         0      1     49             -1      -1E+20       S2                   KNOT  5388350113283448399                                                         [bar,a]       1E+20              KNOT~S2~~5388350113283448399~PDAMPF         1            False               False                   False        556
   108      0             T            0                     4        2332     REAL               4         0      1   1265             -1      -1E+20       S2                   KNOT  5388350113283448399                                                            [°C]       1E+20                   KNOT~S2~~5388350113283448399~T         1            False               False                   False        557
   109      0           RHO            0                     4        2336     REAL               4         0      1   1265             -1      -1E+20       P5                   KNOT  4780213881308610359                                                         [kg/m3]       1E+20                 KNOT~P5~~4780213881308610359~RHO         1            False               False                   False        558
   110      0             P            0                     4        2340     REAL               4         0      1   1265             -1      -1E+20       P5                   KNOT  4780213881308610359                                                         [bar,a]       1E+20                   KNOT~P5~~4780213881308610359~P         1            False               False                   False        559
   111      0     HMAX_INST            0                     4        2344     REAL               4         0      1   2161             -1      -1E+20       P5                   KNOT  4780213881308610359                                                        [IDPH,6]       1E+20           KNOT~P5~~4780213881308610359~HMAX_INST         1            False               False                   False        560
   112      0     HMIN_INST            0                     4        2348     REAL               4         0      1   2161             -1      -1E+20       P5                   KNOT  4780213881308610359                                                        [IDPH,6]       1E+20           KNOT~P5~~4780213881308610359~HMIN_INST         1            False               False                   False        561
   113      0     PMAX_INST            0                     4        2352     REAL               4         0      1   2161             -1      -1E+20       P5                   KNOT  4780213881308610359                                                          [IDPH]       1E+20           KNOT~P5~~4780213881308610359~PMAX_INST         1            False               False                   False        562
   114      0     PMIN_INST            0                     4        2356     REAL               4         0      1   2161             -1      -1E+20       P5                   KNOT  4780213881308610359                                                          [IDPH]       1E+20           KNOT~P5~~4780213881308610359~PMIN_INST         1            False               False                   False        563
   115      0        PDAMPF            0                     4        2360     REAL               4         0      1     49             -1      -1E+20       P5                   KNOT  4780213881308610359                                                         [bar,a]       1E+20              KNOT~P5~~4780213881308610359~PDAMPF         1            False               False                   False        564
   116      0             T            0                     4        2364     REAL               4         0      1   1265             -1      -1E+20       P5                   KNOT  4780213881308610359                                                            [°C]       1E+20                   KNOT~P5~~4780213881308610359~T         1            False               False                   False        565
   117      0           RHO            0                     4        2368     REAL               4         0      1   1265             -1      -1E+20        5                   KNOT  5706345341889312301                                                         [kg/m3]       1E+20                  KNOT~5~~5706345341889312301~RHO         1            False               False                   False        566
   118      0             P            0                     4        2372     REAL               4         0      1   1265             -1      -1E+20        5                   KNOT  5706345341889312301                                                         [bar,a]       1E+20                    KNOT~5~~5706345341889312301~P         1            False               False                   False        567
   119      0     HMAX_INST            0                     4        2376     REAL               4         0      1   2161             -1      -1E+20        5                   KNOT  5706345341889312301                                                        [IDPH,6]       1E+20            KNOT~5~~5706345341889312301~HMAX_INST         1            False               False                   False        568
   120      0     HMIN_INST            0                     4        2380     REAL               4         0      1   2161             -1      -1E+20        5                   KNOT  5706345341889312301                                                        [IDPH,6]       1E+20            KNOT~5~~5706345341889312301~HMIN_INST         1            False               False                   False        569
   121      0     PMAX_INST            0                     4        2384     REAL               4         0      1   2161             -1      -1E+20        5                   KNOT  5706345341889312301                                                          [IDPH]       1E+20            KNOT~5~~5706345341889312301~PMAX_INST         1            False               False                   False        570
   122      0     PMIN_INST            0                     4        2388     REAL               4         0      1   2161             -1      -1E+20        5                   KNOT  5706345341889312301                                                          [IDPH]       1E+20            KNOT~5~~5706345341889312301~PMIN_INST         1            False               False                   False        571
   123      0        PDAMPF            0                     4        2392     REAL               4         0      1     49             -1      -1E+20        5                   KNOT  5706345341889312301                                                         [bar,a]       1E+20               KNOT~5~~5706345341889312301~PDAMPF         1            False               False                   False        572
   124      0             T            0                     4        2396     REAL               4         0      1   1265             -1      -1E+20        5                   KNOT  5706345341889312301                                                            [°C]       1E+20                    KNOT~5~~5706345341889312301~T         1            False               False                   False        573
   125      0           RHO            0                     4        2400     REAL               4         0      1   1265             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                         [kg/m3]       1E+20            KNOT~Absperr~~5498009282312522569~RHO         1            False               False                   False        574
   126      0             P            0                     4        2404     REAL               4         0      1   1265             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                         [bar,a]       1E+20              KNOT~Absperr~~5498009282312522569~P         1            False               False                   False        575
   127      0     HMAX_INST            0                     4        2408     REAL               4         0      1   2161             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                        [IDPH,6]       1E+20      KNOT~Absperr~~5498009282312522569~HMAX_INST         1            False               False                   False        576
   128      0     HMIN_INST            0                     4        2412     REAL               4         0      1   2161             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                        [IDPH,6]       1E+20      KNOT~Absperr~~5498009282312522569~HMIN_INST         1            False               False                   False        577
   129      0     PMAX_INST            0                     4        2416     REAL               4         0      1   2161             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                          [IDPH]       1E+20      KNOT~Absperr~~5498009282312522569~PMAX_INST         1            False               False                   False        578
   130      0     PMIN_INST            0                     4        2420     REAL               4         0      1   2161             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                          [IDPH]       1E+20      KNOT~Absperr~~5498009282312522569~PMIN_INST         1            False               False                   False        579
   131      0        PDAMPF            0                     4        2424     REAL               4         0      1     49             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                         [bar,a]       1E+20         KNOT~Absperr~~5498009282312522569~PDAMPF         1            False               False                   False        580
   132      0             T            0                     4        2428     REAL               4         0      1   1265             -1      -1E+20  Absperr                   KNOT  5498009282312522569                                                            [°C]       1E+20              KNOT~Absperr~~5498009282312522569~T         1            False               False                   False        581
   133      0           RHO            0                     4        2432     REAL               4         0      1   1265             -1      -1E+20       HB                   KNOT  4832703654265095420                                                         [kg/m3]       1E+20                 KNOT~HB~~4832703654265095420~RHO         1            False               False                   False        582
   134      0             P            0                     4        2436     REAL               4         0      1   1265             -1      -1E+20       HB                   KNOT  4832703654265095420                                                         [bar,a]       1E+20                   KNOT~HB~~4832703654265095420~P         1            False               False                   False        583
   135      0     HMAX_INST            0                     4        2440     REAL               4         0      1   2161             -1      -1E+20       HB                   KNOT  4832703654265095420                                                        [IDPH,6]       1E+20           KNOT~HB~~4832703654265095420~HMAX_INST         1            False               False                   False        584
   136      0     HMIN_INST            0                     4        2444     REAL               4         0      1   2161             -1      -1E+20       HB                   KNOT  4832703654265095420                                                        [IDPH,6]       1E+20           KNOT~HB~~4832703654265095420~HMIN_INST         1            False               False                   False        585
   137      0     PMAX_INST            0                     4        2448     REAL               4         0      1   2161             -1      -1E+20       HB                   KNOT  4832703654265095420                                                          [IDPH]       1E+20           KNOT~HB~~4832703654265095420~PMAX_INST         1            False               False                   False        586
   138      0     PMIN_INST            0                     4        2452     REAL               4         0      1   2161             -1      -1E+20       HB                   KNOT  4832703654265095420                                                          [IDPH]       1E+20           KNOT~HB~~4832703654265095420~PMIN_INST         1            False               False                   False        587
   139      0        PDAMPF            0                     4        2456     REAL               4         0      1     49             -1      -1E+20       HB                   KNOT  4832703654265095420                                                         [bar,a]       1E+20              KNOT~HB~~4832703654265095420~PDAMPF         1            False               False                   False        588
   140      0             T            0                     4        2460     REAL               4         0      1   1265             -1      -1E+20       HB                   KNOT  4832703654265095420                                                            [°C]       1E+20                   KNOT~HB~~4832703654265095420~T         1            False               False                   False        589
   141      0            VI            0                     4        2464     REAL               4         0      1   4337             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                           [m/s]       1E+20                 ROHR~WW~1~5076321356874807093~VI         1            False               False                   False        590
   142      0            VK            0                     4        2468     REAL               4         0      1   4337             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                           [m/s]       1E+20                 ROHR~WW~1~5076321356874807093~VK         1            False               False                   False        591
   143      0           QMI            0                     4        2472     REAL               4         0      1   4337             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                          [IDQM]       1E+20                ROHR~WW~1~5076321356874807093~QMI         1            False               False                   False        592
   144      0           QMK            0                     4        2476     REAL               4         0      1   4337             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                          [IDQM]       1E+20                ROHR~WW~1~5076321356874807093~QMK         1            False               False                   False        593
   145      0          SVEC            0                     8        2480     RVEC               4         0      1    241             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                             [m]       1E+20               ROHR~WW~1~5076321356874807093~SVEC         2             True               False                   False        594
   146      0          TVEC            0                     8        2488     RVEC               4         0      1    241             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                            [°C]       1E+20               ROHR~WW~1~5076321356874807093~TVEC         2             True               False                   False        596
   147      0  PVECMAX_INST            0                     8        2496     RVEC               4         0      1    113             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                         [bar,a]       1E+20       ROHR~WW~1~5076321356874807093~PVECMAX_INST         2             True               False                   False        598
   148      0  PVECMIN_INST            0                     8        2504     RVEC               4         0      1    113             -1      -1E+20       WW        1          ROHR  5076321356874807093                                                         [bar,a]       1E+20       ROHR~WW~1~5076321356874807093~PVECMIN_INST         2             True               False                   False        600
   149      0            VI            0                     4        2512     REAL               4         0      1   4337             -1      -1E+20        1        2          ROHR  5497762617222653432                                                           [m/s]       1E+20                  ROHR~1~2~5497762617222653432~VI         1            False               False                   False        602
   150      0            VK            0                     4        2516     REAL               4         0      1   4337             -1      -1E+20        1        2          ROHR  5497762617222653432                                                           [m/s]       1E+20                  ROHR~1~2~5497762617222653432~VK         1            False               False                   False        603
   151      0           QMI            0                     4        2520     REAL               4         0      1   4337             -1      -1E+20        1        2          ROHR  5497762617222653432                                                          [IDQM]       1E+20                 ROHR~1~2~5497762617222653432~QMI         1            False               False                   False        604
   152      0           QMK            0                     4        2524     REAL               4         0      1   4337             -1      -1E+20        1        2          ROHR  5497762617222653432                                                          [IDQM]       1E+20                 ROHR~1~2~5497762617222653432~QMK         1            False               False                   False        605
   153      0          SVEC            0                     8        2528     RVEC               4         0      1    241             -1      -1E+20        1        2          ROHR  5497762617222653432                                                             [m]       1E+20                ROHR~1~2~5497762617222653432~SVEC         2             True               False                   False        606
   154      0          TVEC            0                     8        2536     RVEC               4         0      1    241             -1      -1E+20        1        2          ROHR  5497762617222653432                                                            [°C]       1E+20                ROHR~1~2~5497762617222653432~TVEC         2             True               False                   False        608
   155      0  PVECMAX_INST            0                     8        2544     RVEC               4         0      1    113             -1      -1E+20        1        2          ROHR  5497762617222653432                                                         [bar,a]       1E+20        ROHR~1~2~5497762617222653432~PVECMAX_INST         2             True               False                   False        610
   156      0  PVECMIN_INST            0                     8        2552     RVEC               4         0      1    113             -1      -1E+20        1        2          ROHR  5497762617222653432                                                         [bar,a]       1E+20        ROHR~1~2~5497762617222653432~PVECMIN_INST         2             True               False                   False        612
   157      0            VI            0                     4        2560     REAL               4         0      1   4337             -1      -1E+20        2        3          ROHR  4978978527327130204                                                           [m/s]       1E+20                  ROHR~2~3~4978978527327130204~VI         1            False               False                   False        614
   158      0            VK            0                     4        2564     REAL               4         0      1   4337             -1      -1E+20        2        3          ROHR  4978978527327130204                                                           [m/s]       1E+20                  ROHR~2~3~4978978527327130204~VK         1            False               False                   False        615
   159      0           QMI            0                     4        2568     REAL               4         0      1   4337             -1      -1E+20        2        3          ROHR  4978978527327130204                                                          [IDQM]       1E+20                 ROHR~2~3~4978978527327130204~QMI         1            False               False                   False        616
   160      0           QMK            0                     4        2572     REAL               4         0      1   4337             -1      -1E+20        2        3          ROHR  4978978527327130204                                                          [IDQM]       1E+20                 ROHR~2~3~4978978527327130204~QMK         1            False               False                   False        617
   161      0          SVEC            0                    12        2576     RVEC               4         0      1    241             -1      -1E+20        2        3          ROHR  4978978527327130204                                                             [m]       1E+20                ROHR~2~3~4978978527327130204~SVEC         3             True               False                   False        618
   162      0          TVEC            0                    12        2588     RVEC               4         0      1    241             -1      -1E+20        2        3          ROHR  4978978527327130204                                                            [°C]       1E+20                ROHR~2~3~4978978527327130204~TVEC         3             True               False                   False        621
   163      0  PVECMAX_INST            0                    12        2600     RVEC               4         0      1    113             -1      -1E+20        2        3          ROHR  4978978527327130204                                                         [bar,a]       1E+20        ROHR~2~3~4978978527327130204~PVECMAX_INST         3             True               False                   False        624
   164      0  PVECMIN_INST            0                    12        2612     RVEC               4         0      1    113             -1      -1E+20        2        3          ROHR  4978978527327130204                                                         [bar,a]       1E+20        ROHR~2~3~4978978527327130204~PVECMIN_INST         3             True               False                   False        627
   165      0            VI            0                     4        2624     REAL               4         0      1   4337             -1      -1E+20        3        4          ROHR  5461179577260327606                                                           [m/s]       1E+20                  ROHR~3~4~5461179577260327606~VI         1            False               False                   False        630
   166      0            VK            0                     4        2628     REAL               4         0      1   4337             -1      -1E+20        3        4          ROHR  5461179577260327606                                                           [m/s]       1E+20                  ROHR~3~4~5461179577260327606~VK         1            False               False                   False        631
   167      0           QMI            0                     4        2632     REAL               4         0      1   4337             -1      -1E+20        3        4          ROHR  5461179577260327606                                                          [IDQM]       1E+20                 ROHR~3~4~5461179577260327606~QMI         1            False               False                   False        632
   168      0           QMK            0                     4        2636     REAL               4         0      1   4337             -1      -1E+20        3        4          ROHR  5461179577260327606                                                          [IDQM]       1E+20                 ROHR~3~4~5461179577260327606~QMK         1            False               False                   False        633
   169      0          SVEC            0                    16        2640     RVEC               4         0      1    241             -1      -1E+20        3        4          ROHR  5461179577260327606                                                             [m]       1E+20                ROHR~3~4~5461179577260327606~SVEC         4             True               False                   False        634
   170      0          TVEC            0                    16        2656     RVEC               4         0      1    241             -1      -1E+20        3        4          ROHR  5461179577260327606                                                            [°C]       1E+20                ROHR~3~4~5461179577260327606~TVEC         4             True               False                   False        638
   171      0  PVECMAX_INST            0                    16        2672     RVEC               4         0      1    113             -1      -1E+20        3        4          ROHR  5461179577260327606                                                         [bar,a]       1E+20        ROHR~3~4~5461179577260327606~PVECMAX_INST         4             True               False                   False        642
   172      0  PVECMIN_INST            0                    16        2688     RVEC               4         0      1    113             -1      -1E+20        3        4          ROHR  5461179577260327606                                                         [bar,a]       1E+20        ROHR~3~4~5461179577260327606~PVECMIN_INST         4             True               False                   False        646
   173      0            VI            0                     4        2704     REAL               4         0      1   4337             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                           [m/s]       1E+20                 ROHR~4~P4~5148090523913666712~VI         1            False               False                   False        650
   174      0            VK            0                     4        2708     REAL               4         0      1   4337             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                           [m/s]       1E+20                 ROHR~4~P4~5148090523913666712~VK         1            False               False                   False        651
   175      0           QMI            0                     4        2712     REAL               4         0      1   4337             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                          [IDQM]       1E+20                ROHR~4~P4~5148090523913666712~QMI         1            False               False                   False        652
   176      0           QMK            0                     4        2716     REAL               4         0      1   4337             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                          [IDQM]       1E+20                ROHR~4~P4~5148090523913666712~QMK         1            False               False                   False        653
   177      0          SVEC            0                    12        2720     RVEC               4         0      1    241             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                             [m]       1E+20               ROHR~4~P4~5148090523913666712~SVEC         3             True               False                   False        654
   178      0          TVEC            0                    12        2732     RVEC               4         0      1    241             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                            [°C]       1E+20               ROHR~4~P4~5148090523913666712~TVEC         3             True               False                   False        657
   179      0  PVECMAX_INST            0                    12        2744     RVEC               4         0      1    113             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                         [bar,a]       1E+20       ROHR~4~P4~5148090523913666712~PVECMAX_INST         3             True               False                   False        660
   180      0  PVECMIN_INST            0                    12        2756     RVEC               4         0      1    113             -1      -1E+20        4       P4          ROHR  5148090523913666712                                                         [bar,a]       1E+20       ROHR~4~P4~5148090523913666712~PVECMIN_INST         3             True               False                   False        663
   181      0            VI            0                     4        2768     REAL               4         0      1   4337             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                           [m/s]       1E+20                ROHR~P4~S2~5644872080928983958~VI         1            False               False                   False        666
   182      0            VK            0                     4        2772     REAL               4         0      1   4337             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                           [m/s]       1E+20                ROHR~P4~S2~5644872080928983958~VK         1            False               False                   False        667
   183      0           QMI            0                     4        2776     REAL               4         0      1   4337             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                          [IDQM]       1E+20               ROHR~P4~S2~5644872080928983958~QMI         1            False               False                   False        668
   184      0           QMK            0                     4        2780     REAL               4         0      1   4337             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                          [IDQM]       1E+20               ROHR~P4~S2~5644872080928983958~QMK         1            False               False                   False        669
   185      0          SVEC            0                    12        2784     RVEC               4         0      1    241             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                             [m]       1E+20              ROHR~P4~S2~5644872080928983958~SVEC         3             True               False                   False        670
   186      0          TVEC            0                    12        2796     RVEC               4         0      1    241             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                            [°C]       1E+20              ROHR~P4~S2~5644872080928983958~TVEC         3             True               False                   False        673
   187      0  PVECMAX_INST            0                    12        2808     RVEC               4         0      1    113             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                         [bar,a]       1E+20      ROHR~P4~S2~5644872080928983958~PVECMAX_INST         3             True               False                   False        676
   188      0  PVECMIN_INST            0                    12        2820     RVEC               4         0      1    113             -1      -1E+20       P4       S2          ROHR  5644872080928983958                                                         [bar,a]       1E+20      ROHR~P4~S2~5644872080928983958~PVECMIN_INST         3             True               False                   False        679
   189      0            VI            0                     4        2832     REAL               4         0      1   4337             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                           [m/s]       1E+20                ROHR~S2~P5~4984438795139137900~VI         1            False               False                   False        682
   190      0            VK            0                     4        2836     REAL               4         0      1   4337             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                           [m/s]       1E+20                ROHR~S2~P5~4984438795139137900~VK         1            False               False                   False        683
   191      0           QMI            0                     4        2840     REAL               4         0      1   4337             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                          [IDQM]       1E+20               ROHR~S2~P5~4984438795139137900~QMI         1            False               False                   False        684
   192      0           QMK            0                     4        2844     REAL               4         0      1   4337             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                          [IDQM]       1E+20               ROHR~S2~P5~4984438795139137900~QMK         1            False               False                   False        685
   193      0          SVEC            0                    16        2848     RVEC               4         0      1    241             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                             [m]       1E+20              ROHR~S2~P5~4984438795139137900~SVEC         4             True               False                   False        686
   194      0          TVEC            0                    16        2864     RVEC               4         0      1    241             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                            [°C]       1E+20              ROHR~S2~P5~4984438795139137900~TVEC         4             True               False                   False        690
   195      0  PVECMAX_INST            0                    16        2880     RVEC               4         0      1    113             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                         [bar,a]       1E+20      ROHR~S2~P5~4984438795139137900~PVECMAX_INST         4             True               False                   False        694
   196      0  PVECMIN_INST            0                    16        2896     RVEC               4         0      1    113             -1      -1E+20       S2       P5          ROHR  4984438795139137900                                                         [bar,a]       1E+20      ROHR~S2~P5~4984438795139137900~PVECMIN_INST         4             True               False                   False        698
   197      0            VI            0                     4        2912     REAL               4         0      1   4337             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                           [m/s]       1E+20                 ROHR~P5~5~4648047345314768819~VI         1            False               False                   False        702
   198      0            VK            0                     4        2916     REAL               4         0      1   4337             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                           [m/s]       1E+20                 ROHR~P5~5~4648047345314768819~VK         1            False               False                   False        703
   199      0           QMI            0                     4        2920     REAL               4         0      1   4337             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                          [IDQM]       1E+20                ROHR~P5~5~4648047345314768819~QMI         1            False               False                   False        704
   200      0           QMK            0                     4        2924     REAL               4         0      1   4337             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                          [IDQM]       1E+20                ROHR~P5~5~4648047345314768819~QMK         1            False               False                   False        705
   201      0          SVEC            0                    20        2928     RVEC               4         0      1    241             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                             [m]       1E+20               ROHR~P5~5~4648047345314768819~SVEC         5             True               False                   False        706
   202      0          TVEC            0                    20        2948     RVEC               4         0      1    241             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                            [°C]       1E+20               ROHR~P5~5~4648047345314768819~TVEC         5             True               False                   False        711
   203      0  PVECMAX_INST            0                    20        2968     RVEC               4         0      1    113             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                         [bar,a]       1E+20       ROHR~P5~5~4648047345314768819~PVECMAX_INST         5             True               False                   False        716
   204      0  PVECMIN_INST            0                    20        2988     RVEC               4         0      1    113             -1      -1E+20       P5        5          ROHR  4648047345314768819                                                         [bar,a]       1E+20       ROHR~P5~5~4648047345314768819~PVECMIN_INST         5             True               False                   False        721
   205      0            VI            0                     4        3008     REAL               4         0      1   4337             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                           [m/s]       1E+20            ROHR~5~Absperr~5433880705192526755~VI         1            False               False                   False        726
   206      0            VK            0                     4        3012     REAL               4         0      1   4337             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                           [m/s]       1E+20            ROHR~5~Absperr~5433880705192526755~VK         1            False               False                   False        727
   207      0           QMI            0                     4        3016     REAL               4         0      1   4337             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                          [IDQM]       1E+20           ROHR~5~Absperr~5433880705192526755~QMI         1            False               False                   False        728
   208      0           QMK            0                     4        3020     REAL               4         0      1   4337             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                          [IDQM]       1E+20           ROHR~5~Absperr~5433880705192526755~QMK         1            False               False                   False        729
   209      0          SVEC            0                     8        3024     RVEC               4         0      1    241             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                             [m]       1E+20          ROHR~5~Absperr~5433880705192526755~SVEC         2             True               False                   False        730
   210      0          TVEC            0                     8        3032     RVEC               4         0      1    241             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                            [°C]       1E+20          ROHR~5~Absperr~5433880705192526755~TVEC         2             True               False                   False        732
   211      0  PVECMAX_INST            0                     8        3040     RVEC               4         0      1    113             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                         [bar,a]       1E+20  ROHR~5~Absperr~5433880705192526755~PVECMAX_INST         2             True               False                   False        734
   212      0  PVECMIN_INST            0                     8        3048     RVEC               4         0      1    113             -1      -1E+20        5  Absperr          ROHR  5433880705192526755                                                         [bar,a]       1E+20  ROHR~5~Absperr~5433880705192526755~PVECMIN_INST         2             True               False                   False        736
   213      0             V            0                     4        3056     REAL               4         0      1   1137             -1      -1E+20  Absperr       HB          VENT  5466655470152247657                                                           [m/s]       1E+20            VENT~Absperr~HB~5466655470152247657~V         1            False               False                   False        738
   214      0        WALTER            0                    68        3060     REAL               4         0      1   8245             -1      -1E+20        *                   KNOT                    *                                                             [h]       1E+20                                 KNOT~*~~*~WALTER        17             True                True                   False        739
   215      0        WALTER            0                     4        3128     REAL               4         0      1     53             -1      -1E+20        *        *          OBEH                    *                                                             [h]       1E+20                                OBEH~*~*~*~WALTER         1            False               False                   False        756'''
>>> print("'''{:s}'''".format(repr(mx.mx2Df).replace('\\n','\\n   ')))
'''        AttrType                                                                                                                                                                                                                                                                                                                                                                                                                                                                            Data  DataLength DataType  DataTypeLength  NOfItems       ObjType
   0   tk                                                                                                                     [5179406559406617933, 5706345341889312301, 5028754475676510796, 4880261452311588026, 4711309381204507891, 5697271655044179265, 5165939128645634755, 4790715298669926433, 5629305599838467353, 5388350113283448399, 4702108116010765829, 5095105260880965618, 5113971272348625691, 5042575626021291052, 4780213881308610359, 4832703654265095420, 5498009282312522569]         340     CHAR              20        17  KNOT        
   1   pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [4673068329861421062]          20     CHAR              20         1  LFKT        
   2   tk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [4914542339545953765]          20     CHAR              20         1  OBEH        
   3   pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [5295290952622367198]          20     CHAR              20         1  PHI1        
   4   pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [5623478865255556069]          20     CHAR              20         1  PUMD        
   5   pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [4728046487162557851]          20     CHAR              20         1  PVAR        
   6   pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [5377391575499483345]          20     CHAR              20         1  QVAR        
   7   tk            [4820249423461369400, 5508607066407516090, 5095827458323717990, 5700891034663173564, 5729543164571807746, 5067763789937102564, 4799443678518131207, 5605831797210762998, 5126294008398890918, 5419686039699182683, 5312551747276023841, 5296152509037292880, 5670035893444309530, 5433880705192526755, 4648047345314768819, 4984438795139137900, 5644872080928983958, 5148090523913666712, 5461179577260327606, 4978978527327130204, 5497762617222653432, 5076321356874807093]         440     CHAR              20        22  ROHR        
   8   N_OF_POINTS                                                                                                                                                                                                                                                                                                                                                                                                               (5, 6, 5, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 5, 4, 3, 3, 4, 3, 2, 2)          88     INT4               4        22  ROHR        
   9   pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [4955975670134047353]          20     CHAR              20         1  SWVT        
   10  pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [4821755615165519990]          20     CHAR              20         1  TEVT        
   11  tk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [5466655470152247657]          20     CHAR              20         1  VENT        
   12  pk                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [5736734929574151957]          20     CHAR              20         1  WEVT        '''
>>> mx.setResultsToMxsFile(maxRecords=1)
1
>>> print("'''{:s}'''".format(repr(mx.df.drop(['ALLG~~~-1~CPUTIME','ALLG~~~-1~USRTIME','ALLG~~~-1~CVERSO'],axis=1)).replace('\\n','\\n   ')))
'''                          ALLG~~~-1~SNAPSHOTTYPE  ALLG~~~-1~EXSTAT  ALLG~~~-1~NFEHL  ALLG~~~-1~NWARN  ALLG~~~-1~NMELD  ALLG~~~-1~NPGREST  ALLG~~~-1~NETZABN  ALLG~~~-1~NKNUV  ALLG~~~-1~MKNUV  ALLG~~~-1~NFVHYUV  ALLG~~~-1~NFVTHUV  ALLG~~~-1~MFVHYUV  ALLG~~~-1~MFVTHUV  ALLG~~~-1~TVMINMAX  ALLG~~~-1~ITERHY  ALLG~~~-1~LFQSV  ALLG~~~-1~JWARN  ALLG~~~-1~NETZABNEXITS  ALLG~~~-1~LINEPACKRATE  ALLG~~~-1~LINEPACKGES  ALLG~~~-1~LINEPACKGEOM  ALLG~~~-1~RHOAV  ALLG~~~-1~TAV  ALLG~~~-1~PAV  ALLG~~~-1~FWVB_DPHMIN  ALLG~~~-1~KNOT_PHMAX  ALLG~~~-1~KNOT_PHMIN  ALLG~~~-1~FWVB_TVLMIN  ALLG~~~-1~NETZBEZ  KNOT~3~~4711309381204507891~PH  KNOT~3~~4711309381204507891~H  KNOT~WW~~5179406559406617933~QM  KNOT~WW~~5179406559406617933~PH  KNOT~WW~~5179406559406617933~H  OBEH~HB~~4914542339545953765~WST  KNOT~HB~~4832703654265095420~H  VENT~Absperr~HB~5466655470152247657~QM  KNOT~WW~~5179406559406617933~RHO  KNOT~WW~~5179406559406617933~P  KNOT~WW~~5179406559406617933~HMAX_INST  KNOT~WW~~5179406559406617933~HMIN_INST  KNOT~WW~~5179406559406617933~PMAX_INST  KNOT~WW~~5179406559406617933~PMIN_INST  KNOT~WW~~5179406559406617933~PDAMPF  KNOT~WW~~5179406559406617933~T  KNOT~1~~5028754475676510796~RHO  KNOT~1~~5028754475676510796~P  KNOT~1~~5028754475676510796~HMAX_INST  KNOT~1~~5028754475676510796~HMIN_INST  KNOT~1~~5028754475676510796~PMAX_INST  KNOT~1~~5028754475676510796~PMIN_INST  KNOT~1~~5028754475676510796~PDAMPF  KNOT~1~~5028754475676510796~T  KNOT~2~~4880261452311588026~RHO  KNOT~2~~4880261452311588026~P  KNOT~2~~4880261452311588026~HMAX_INST  KNOT~2~~4880261452311588026~HMIN_INST  KNOT~2~~4880261452311588026~PMAX_INST  KNOT~2~~4880261452311588026~PMIN_INST  KNOT~2~~4880261452311588026~PDAMPF  KNOT~2~~4880261452311588026~T  KNOT~3~~4711309381204507891~RHO  KNOT~3~~4711309381204507891~P  KNOT~3~~4711309381204507891~HMAX_INST  KNOT~3~~4711309381204507891~HMIN_INST  KNOT~3~~4711309381204507891~PMAX_INST  KNOT~3~~4711309381204507891~PMIN_INST  KNOT~3~~4711309381204507891~PDAMPF  KNOT~3~~4711309381204507891~T  KNOT~4~~5697271655044179265~RHO  KNOT~4~~5697271655044179265~P  KNOT~4~~5697271655044179265~HMAX_INST  KNOT~4~~5697271655044179265~HMIN_INST  KNOT~4~~5697271655044179265~PMAX_INST  KNOT~4~~5697271655044179265~PMIN_INST  KNOT~4~~5697271655044179265~PDAMPF  KNOT~4~~5697271655044179265~T  KNOT~P4~~5042575626021291052~RHO  KNOT~P4~~5042575626021291052~P  KNOT~P4~~5042575626021291052~HMAX_INST  KNOT~P4~~5042575626021291052~HMIN_INST  KNOT~P4~~5042575626021291052~PMAX_INST  KNOT~P4~~5042575626021291052~PMIN_INST  KNOT~P4~~5042575626021291052~PDAMPF  KNOT~P4~~5042575626021291052~T  KNOT~S2~~5388350113283448399~RHO  KNOT~S2~~5388350113283448399~P  KNOT~S2~~5388350113283448399~HMAX_INST  KNOT~S2~~5388350113283448399~HMIN_INST  KNOT~S2~~5388350113283448399~PMAX_INST  KNOT~S2~~5388350113283448399~PMIN_INST  KNOT~S2~~5388350113283448399~PDAMPF  KNOT~S2~~5388350113283448399~T  KNOT~P5~~4780213881308610359~RHO  KNOT~P5~~4780213881308610359~P  KNOT~P5~~4780213881308610359~HMAX_INST  KNOT~P5~~4780213881308610359~HMIN_INST  KNOT~P5~~4780213881308610359~PMAX_INST  KNOT~P5~~4780213881308610359~PMIN_INST  KNOT~P5~~4780213881308610359~PDAMPF  KNOT~P5~~4780213881308610359~T  KNOT~5~~5706345341889312301~RHO  KNOT~5~~5706345341889312301~P  KNOT~5~~5706345341889312301~HMAX_INST  KNOT~5~~5706345341889312301~HMIN_INST  KNOT~5~~5706345341889312301~PMAX_INST  KNOT~5~~5706345341889312301~PMIN_INST  KNOT~5~~5706345341889312301~PDAMPF  KNOT~5~~5706345341889312301~T  KNOT~Absperr~~5498009282312522569~RHO  KNOT~Absperr~~5498009282312522569~P  KNOT~Absperr~~5498009282312522569~HMAX_INST  KNOT~Absperr~~5498009282312522569~HMIN_INST  KNOT~Absperr~~5498009282312522569~PMAX_INST  KNOT~Absperr~~5498009282312522569~PMIN_INST  KNOT~Absperr~~5498009282312522569~PDAMPF  KNOT~Absperr~~5498009282312522569~T  KNOT~HB~~4832703654265095420~RHO  KNOT~HB~~4832703654265095420~P  KNOT~HB~~4832703654265095420~HMAX_INST  KNOT~HB~~4832703654265095420~HMIN_INST  KNOT~HB~~4832703654265095420~PMAX_INST  KNOT~HB~~4832703654265095420~PMIN_INST  KNOT~HB~~4832703654265095420~PDAMPF  KNOT~HB~~4832703654265095420~T  ROHR~WW~1~5076321356874807093~VI  ROHR~WW~1~5076321356874807093~VK  ROHR~WW~1~5076321356874807093~QMI  ROHR~WW~1~5076321356874807093~QMK  ROHR~1~2~5497762617222653432~VI  ROHR~1~2~5497762617222653432~VK  ROHR~1~2~5497762617222653432~QMI  ROHR~1~2~5497762617222653432~QMK  ROHR~2~3~4978978527327130204~VI  ROHR~2~3~4978978527327130204~VK  ROHR~2~3~4978978527327130204~QMI  ROHR~2~3~4978978527327130204~QMK  ROHR~3~4~5461179577260327606~VI  ROHR~3~4~5461179577260327606~VK  ROHR~3~4~5461179577260327606~QMI  ROHR~3~4~5461179577260327606~QMK  ROHR~4~P4~5148090523913666712~VI  ROHR~4~P4~5148090523913666712~VK  ROHR~4~P4~5148090523913666712~QMI  ROHR~4~P4~5148090523913666712~QMK  ROHR~P4~S2~5644872080928983958~VI  ROHR~P4~S2~5644872080928983958~VK  ROHR~P4~S2~5644872080928983958~QMI  ROHR~P4~S2~5644872080928983958~QMK  ROHR~S2~P5~4984438795139137900~VI  ROHR~S2~P5~4984438795139137900~VK  ROHR~S2~P5~4984438795139137900~QMI  ROHR~S2~P5~4984438795139137900~QMK  ROHR~P5~5~4648047345314768819~VI  ROHR~P5~5~4648047345314768819~VK  ROHR~P5~5~4648047345314768819~QMI  ROHR~P5~5~4648047345314768819~QMK  ROHR~5~Absperr~5433880705192526755~VI  ROHR~5~Absperr~5433880705192526755~VK  ROHR~5~Absperr~5433880705192526755~QMI  ROHR~5~Absperr~5433880705192526755~QMK  VENT~Absperr~HB~5466655470152247657~V  OBEH~*~*~*~WALTER
   2002-05-22 16:16:16+00:00                b'STAT'                 0                0                0               11                  0              160.0                0              0.0                  0                  0                0.0                0.0         -273.149994                 9              1.0               30                   160.0                     0.0                    0.0                86.01461      1000.299988     556.299988       3.736424           3.402823e+38              3.986973              0.980928           3.402823e+38              140.0                        1.006286                      40.258186                            140.0                         3.016954                       40.755142                              10.0                       39.999683                              -20.000008                       1000.299988                        4.016954                               40.755142                               40.755142                                4.016954                                4.016954                               0.0123                            10.0                      1000.299988                       4.986973                              40.643616                              40.643616                               4.986973                               4.986973                              0.0123                           10.0                      1000.299988                       3.507876                              40.565548                              40.565548                               3.507876                               3.507876                              0.0123                           10.0                      1000.299988                       2.006286                              40.258186                              40.258186                               2.006286                               2.006286                              0.0123                           10.0                      1000.299988                       3.936131                              39.931221                              39.931221                               3.936131                               3.936131                              0.0123                           10.0                       1000.299988                        4.416402                               39.827152                               39.827152                                4.416402                                4.416402                               0.0123                            10.0                       1000.299988                        4.920524                               39.966225                               39.966225                                4.920524                                4.920524                               0.0123                            10.0                       1000.299988                        3.937013                               39.940212                               39.940212                                3.937013                                3.937013                               0.0123                            10.0                      1000.299988                        3.45231                                39.9991                                39.9991                                3.45231                                3.45231                              0.0123                           10.0                            1000.299988                             3.452336                                    39.999367                                    39.999367                                     3.452336                                     3.452336                                    0.0123                                 10.0                       1000.299988                        1.980928                               39.999683                               39.999683                                1.980928                                1.980928                               0.0123                            10.0                          0.499333                          0.499333                              140.0                              140.0                         0.499333                         0.499333                             140.0                             140.0                         0.510817                         0.510817                         64.851456                         64.851456                         0.292091                         0.292091                          9.615081                          9.615081                          0.196514                          0.196514                           6.468875                           6.468875                          -0.228407                          -0.228407                           -7.518734                           -7.518734                           0.102688                           0.102688                            7.535347                            7.535347                         -0.126186                         -0.126186                          -9.259682                          -9.259682                              -0.071333                              -0.071333                              -20.000008                              -20.000008                              -0.176839                2.0'''
>>> # ---
>>> # Clean Up Tiny WDN
>>> # ---
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
"""

import warnings # 3.6
#...\Anaconda3\lib\site-packages\h5py\__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
#   from ._conv import register_converters as _register_converters
#...\PT3S\Mx.py:1: FutureWarning: pandas.tslib is deprecated and will be removed in a future version.
#   You can access Timestamp as pandas.Timestamp
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import sys

import xml.etree.ElementTree as ET
import re
import struct
import zipfile
import pandas as pd
import h5py
import tables
import math

import logging
# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S.Mx')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context: ',' .')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

# ---
# --- main Imports
# ---
import argparse
import unittest
import doctest

# Sir3sID regExp
reSir3sID='(\S+)~([\S ]+)~(\S*)~(\S+)~(\S+)'
reSir3sIDcompiled=re.compile(reSir3sID) 
  
def getMicrosecondsFromRefTime(refTime,time):
    """Returns time in microseconds since refTime.

    Args:
        * refTime
        * time

    Raises:
        MxError
    """
    try:
        timeH5=time-refTime
        h5Key=int(math.floor(timeH5.total_seconds())*1000+timeH5.microseconds)
    except Exception as e:
        logStrFinal="{:s}: Exception: Line: {:d}: {!s:s}: {:s}".format('getMicrosecondsFromRefTime',sys.exc_info()[-1].tb_lineno,type(e),str(e)) 
        raise MxError(logStrFinal)              
    finally:
        return h5Key

class MxError(Exception):
    """MxError.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """Reading SIR 3S' MX-Files. 

    Summry:
        * (mx1File): use this to profit from previous reads finalized with ToH5()
        * (mx1File,NoH5Read=True): use this for a fresh start with implicit .MXS-File read; finalize with ToH5()
        * (mx1File,NoH5Read=True,NoMxsRead=True): use this for a fresh start; call setResultsTo...() explicit; finalize with ToH5()
        * note that base.h5-File has to be dunped explicitely with ToH5()
        * and .vec.h5-File is written implicitely while (implicit or explicit calls to) setResultsTo...() 
        * and is deleted explicitely (mx1File,NoH5Read=True) or implicitely (because too old or because 

    Args:
        * mx1File (str): base.MX1-File (an XML-File) (base.1.MX1-File for 90-10)

        * NoH5Read (bool): 
            False (default - use this to profit from previous reads finalized with ToH5()): 
                * If a base.h5-File 
                    * exists 
                    * and is newer (>) than an .MX1-File (base.1.Mx1-File for 90-10) 
                    * and is newer (>) than an .MXS-File (base.1.MXS-File for 90-10):

                        * The base.h5-File is read instead of the .MX1-File.                        

            True (use this for a fresh start):             
                * An base.h5-File is deleted if existing.  
                * The .MX1-File is read.
                * The .vec.h5-File is newly created in case of an .MXS-File read.       

        * NoMxsRead (bool):
            True:
                * a .MXS-File is not read
                * a .vec.h5-File is not touched

            False (default):
                * If a .MXS-File 
                    * exists
                    * and is newer (>=) than .MX1-File 
                    * and base.h5-File is not read:

                        * The .MXS-File is read.          
                        * NoH5Read=True will delete .vec.h5-File.

    Attributes:
        * fileNames
            * .mx1File: .MX1-File 

            derived from mx1File
                * .mx2File: .MX2-File 
                * .mxsFile: .MXS-File 
                * .mxsZipFile
                * .h5File: .h5-File
                * .h5FileVecs: .vec.h5-File

        * .mxRecordStructFmtString

        * dataFrames
            * .mx1Df  
            * .mx2Df 
            * .df
                * the .MXS-File(s) Content
                * non Vectordata only
                * index:   TIMESTAMP (scenario time)
                * columns: Values  
                    * The following (String-)ID - called Sir3sID - is used as Columnlabel:                    
                    * this Sir3sID consists of ~ separated .MX1-File terms:
                    * OBJTYPE~NAME1~NAME2~OBJTYPE_PK~ATTRTYPE  
                    * Sir3sID regExp: '(\S+)~([\S ]+)~(\S*)~(\S+)~(\S+)'
    
    Raises:
        MxError
    """
    def __init__(self,mx1File,NoH5Read=False,NoMxsRead=False): 
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            if type(mx1File) == str:
                    self.mx1File=mx1File  
            else:
                    logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,mx1File)                                 
                    raise MxError(logStrFinal)     

            #Determine corresponding .MX2 Filename
            (wD,fileName)=os.path.split(self.mx1File)
            (base,ext)=os.path.splitext(fileName)

            # wenn 90-10, dann ist base im Sinne des folgenden Codes um .1 zu strippen
            # bei MXS allerdings ist .1 wieder zu ergaenzen

            self.mx2File=wD+os.path.sep+base+'.'+'MX2'   
                                                     
            #Determine corresponding .h5 Filename(s)
            self.h5File=wD+os.path.sep+base+'.'+'h5'    # mx1Df, mx2Df, df (non Vectordata only)
            self.h5FileVecs=wD+os.path.sep+base+'.'+'vec'+'.'+'h5' # (Vectordata)           
            
            #Determine corresponding .MXS Filename
            self.mxsFile=wD+os.path.sep+base+'.'+'MXS'  
          
            #Determine corresponding .MXS Zip-Filename
            self.mxsZipFile=wD+os.path.sep+base+'.'+'ZIP'   

            #check if mx1File exists ...
            if os.path.exists(self.mx1File):
                mx1FileThere=True
                mx1FileTime=os.path.getmtime(self.mx1File) 
            else:
                mx1FileThere=False
                mx1FileTime=0
                logger.debug("{0:s}{1:s}: Not existing!".format(logStr,mx1File))     

            if NoH5Read: 
                if os.path.exists(self.h5File):  
                    logger.debug("{0:s}{1:s}: Delete ...".format(logStr,self.h5File))     
                    os.remove(self.h5File)
             
            #check if h5File exists 
            if os.path.exists(self.h5File):  
                #check if h5File is newer               
                h5FileTime=os.path.getmtime(self.h5File)
                if(h5FileTime>mx1FileTime):
                    if os.path.exists(self.mxsFile):  
                        mxsFileTime=os.path.getmtime(self.mxsFile)
                        if(h5FileTime>mxsFileTime and not NoH5Read):
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an mx1File {2:s} _and is newer than an (existing) mxsFile {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an mx1File (mxsFile exists).".format(logStr))   
                            h5Read=True
                        else:                                                             
                            h5Read=False  
                    else:
                        if not NoH5Read:
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an mx1File {2:s} _and there is no mxsFile like {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an mx1File.".format(logStr))   
                            h5Read=True  
                        else:
                            h5Read=False  
                else:                    
                    h5Read=False
            else:
                h5Read=False

            self.df=None   
            self.mx1Df=None

            if not h5Read:
                if not mx1FileThere:
                   logStrFinal="{0:s}{1:s}: Not existing! Error.".format(logStr,mx1File)                                 
                   raise MxError(logStrFinal)                 
                self._initWithMx1()                    
                if os.path.exists(self.mxsFile):  
                    mx1FileTime=os.path.getmtime(self.mx1File) 
                    mxsFileTime=os.path.getmtime(self.mxsFile)
                    if(mxsFileTime>=mx1FileTime) and not NoMxsRead: # inplace nach pip install tragen die Dateien denselben Zeitstempel; deswegen >= statt nur >
                        logger.debug("{:s}mxsFile {:s} exists _and is newer than mx1File {:s} _and NoMxsRead False:".format(logStr,self.mxsFile,self.mx1File))     
                        logger.debug("{:s}The mxsFile is read.".format(logStr))   
                        self.setResultsToMxsFile(NewH5Vec = NoH5Read)  # wenn kein H5 gelesen werden soll, dann soll auch das H5Vec neu angelegt werden
            else:                
                self.FromH5(h5File=self.h5File)
                             
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _initWithMx1(self):
        """(Re-)initialize .mx1Df, .mx2Df, .mxRecordStructFmtString and related stuff with .mx1File.

        Calls:
            * ._parseMx1()     
            * ._parseMx2()     
            * ._buildMxRecordStructUnpackFmtString()      
            * ._buildMxRecordStructUnpackFmtStringPost()   

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:             
            self._parseMx1()     
            self._parseMx2()     
            self._buildMxRecordStructUnpackFmtString()      
            self._buildMxRecordStructUnpackFmtStringPost()      
                            
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}mx1File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,self.mx1File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                    
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _parseMx1(self):
        """Parses .mx1File.

        Sets
            * .mx1Df

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:             
            logger.debug("{0:s}mx1File: {1:s} reading ...".format(logStr,self.mx1File))    
            # read mx1File To Dataframe
            Mx1Tree = ET.parse(self.mx1File)
            Mx1Root = Mx1Tree.getroot()

            logger.debug("{0:s}mx1File: {1:s} parsing ...".format(logStr,self.mx1File))    
            all_records = []
            for mxChannel in Mx1Root.findall('XL1'): # returns a list containing all matching elements in document order
                record = {}
                for attrName in sorted(mxChannel.keys()):
                    attrValue=mxChannel.get(attrName)
                    record[attrName]=attrValue 
                all_records.append(record)
            self.mx1Df=pd.DataFrame(all_records) 
            logger.debug("{0:s}mx1File: {1:s} mx1Df read. Shape: {2!s}.".format(logStr,self.mx1File,self.mx1Df.shape))    

            #Conversions
            self.mx1Df['DATALENGTH']=self.mx1Df['DATALENGTH'].astype('int64')
            self.mx1Df['DATATYPELENGTH']=self.mx1Df['DATATYPELENGTH'].astype('int64')
            self.mx1Df['DATAOFFSET']=self.mx1Df['DATAOFFSET'].astype('int64')
            self.mx1Df['FLAGS']=self.mx1Df['FLAGS'].astype('int64')

            #XPath-Example:
            #tsElement=MxRoot.find('./XL1[@OBJTYPE="ALLG"]/.[@ATTRTYPE="TIMESTAMP"]')
            #dfTsIdx = self.mx1Df.index[(self.mx1Df['OBJTYPE']=='ALLG') & (self.mx1Df['ATTRTYPE']=='TIMESTAMP')] 
            #self.channelTsIdx=dfTsIdx.tolist()[0] #channelNumber of the TimeStamp
            #logger.debug("{0:s}mx1File: {1:s}: channelNumber of the TimeStamp: {2:d}.".format(logStr,self.mx1File,self.channelTsIdx))    
            
            #Sir3sID
            sep='~'
            self.mx1Df['Sir3sID']=self.mx1Df['OBJTYPE']+sep+self.mx1Df['NAME1']+sep+self.mx1Df['NAME2']+sep+self.mx1Df['OBJTYPE_PK']+sep+self.mx1Df['ATTRTYPE']
            self.mx1Df['Sir3sID']=self.mx1Df['Sir3sID'].astype(str)

            #markVectorChannels (vectorChannel-Definition here := more than 1 Item)
            self.mx1Df['NOfItems']=[int(cDLength/cDTypeLength) for cDLength,cDTypeLength in zip(self.mx1Df['DATALENGTH'],self.mx1Df['DATATYPELENGTH'])] 
            #self.mx1Df['isVectorChannel']=[True if int(cDLength/cDTypeLength)>1 else False for cDLength,cDTypeLength in zip(self.mx1Df['DATALENGTH'],self.mx1Df['DATATYPELENGTH'])] 
            self.mx1Df['isVectorChannel']=[True if nItems>1 else False for nItems in self.mx1Df['NOfItems']] 
           
            #set(mx.mx1Df['DATATYPE'])
            #{'RVEC', 'CHAR', 'INT4', 'REAL'}
          
            #markMx2DefinedVectorChannels
            #True for all Mx2-defined-Types
            self.mx1Df['isVectorChannelMx2']=[True if isVectorChannel and bit3rd and flagStr[-3]=='1' else False for isVectorChannel,flagStr,bit3rd in zip(self.mx1Df['isVectorChannel'],self.mx1Df['FLAGS'].apply(bin),self.mx1Df['FLAGS'].apply(lambda x: True if x >=4 else False))] 
            #True for a special Mx2-defined-Type (Mx2 AttrType = N_OF_POINTS) 
            self.mx1Df['isVectorChannelMx2Rvec']=[True if isVectorChannelMx2 and dataType=='RVEC' else False for isVectorChannelMx2,dataType in zip(self.mx1Df['isVectorChannelMx2'],self.mx1Df['DATATYPE'])] 

            logger.debug("{0:s}mx1Df after some generated Columns: Shape: {1!s}.".format(logStr,self.mx1Df.shape))    
                                                                       
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}mx2File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,self.mx2File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)             
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _parseMx2(self):
        """Parses .mx2File.

        Sets
            * .mx2Df

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            logger.debug("{0:s}mx2File: {1:s} parsing ...".format(logStr,self.mx2File))    

            headerFmtString='12s12s4si28xi'
            with open(self.mx2File,'rb') as f:               
                offsetToNextHeader=0
                all_records = []
                while True:
                    header=f.read(64)
                    headerLength=len(header)

                    if headerLength!=64:
                        if headerLength != 0:
                            logger.error("{:s}:headerLength: {:d} != 0?".format(logStr,headeLength))      
                        self.mx2Df=pd.DataFrame(all_records)                       
                        break

                    record = {}
                    headerData = struct.unpack(headerFmtString,header)  

                    ObjType=headerData[0].decode('utf-8')
                    AttrType=headerData[1].decode('utf-8')
                    DataType=headerData[2].decode('utf-8')
                    DataTypeLength=headerData[3]
                    DataLength=headerData[4]                   
                    
                    record['ObjType']=ObjType
                    record['AttrType']=AttrType
                    record['DataType']=DataType
                    record['DataTypeLength']=DataTypeLength
                    record['DataLength']=DataLength
                    NOfItems=int(DataLength/DataTypeLength)
                    record['NOfItems']=NOfItems

                    if DataType=='CHAR':
                        fmtItem=str(DataTypeLength)+'s'
                        dataFmtString=fmtItem*NOfItems 
                    elif DataType=='INT4':
                        fmtItem='i'
                        dataFmtString=fmtItem*NOfItems 
                    else:
                        fmtItem='x'
                        dataFmtString=str(DataLength)+fmtItem

                    dataBytes=f.read(DataLength)
                    Data = struct.unpack(dataFmtString,dataBytes)  

                    if DataType=='CHAR':
                        Data=list(map(lambda x: x.decode('utf-8').rstrip(),Data)) #20 vs. 19?!

                    record['Data']=Data

                    all_records.append(record)
                                                           
                    offsetToNextHeader=offsetToNextHeader+64+DataLength
                    if f.tell() != offsetToNextHeader:
                        logger.error("{:s}:offsetToNextHeader: {:d} != {:d}?".format(logStr,offsetToNextHeader,f.tell()))     
                        f.seek(offsetToNextHeader)                    

                    logger.debug("{:s}ObjType:{:s} AttrType:{:s} DataType:{:s} DataTypeLength:{:>3d} DataLength:{:>8d} Data[0]:{!s:>20s} Data[-1]:{!s:>20s} offsetToNextHeader:{:>11d}".format(logStr
                           ,ObjType #headerData[0]
                           ,AttrType #headerData[1]
                           ,DataType #headerData[2]
                           ,DataTypeLength #headerData[3]
                           ,DataLength #headerData[4]
                           ,Data[0]
                           ,Data[-1]
                           ,offsetToNextHeader
                           )
                                 )    
                                                            
  
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}mx2File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,self.mx2File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)             
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _buildMxRecordStructUnpackFmtString(self):
        """(Re-)builds .mxRecordStructFmtString and releated stuff.
            
        Sets
            * .mxRecordStructFmtString                   
            * .mx1Df['unpackIdx']        

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            self.mxRecordStructFmtString=''
            unpackIdx=[]
            idxUnpack=0
            bytesSkipped=0

            for row in self.mx1Df.itertuples():

                idxChannel=int(row.Index)

                fmtItem='' # End of Loop: self.mxRecordStructUnpackFmtString+=fmtItem

                sir3sID=row.Sir3sID

                isVectorChannel=row.isVectorChannel

                #if isVectorChannel:
                #    toBeUnpacked=False
                #else:
                #    toBeUnpacked=True

                toBeUnpacked=True
                                                                                   
                cDType=row.DATATYPE 
                cDTypeLength=row.DATATYPELENGTH 
                cDLength=row.DATALENGTH 
                nItems=row.NOfItems                
                
                if cDType=='CHAR':
                    if toBeUnpacked:   
                        unpackIdx.append(idxUnpack)    
                        if isVectorChannel:                                                                                  
                            for idx in range(nItems):
                                fmtItem+=(str(cDTypeLength)+'s') 
                            idxUnpack+=nItems                            
                        else:                            
                            fmtItem=str(cDLength)+'s'                         
                            idxUnpack+=1 
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'  
                        unpackIdx.append(-1)
                                                    
                elif cDType=='INT4':    
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)     
                        unpackIdx.append(idxUnpack)        
                        if isVectorChannel:                                                                                                                                                                                                                                                                                            
                            fmtItem=str(nItems)+'i'                    
                            idxUnpack+=nItems                           
                        else:                            
                            fmtItem='i'                         
                            idxUnpack+=1    
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x' 
                        unpackIdx.append(-1)                                     
                            
                elif cDType=='REAL':
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)    
                        unpackIdx.append(idxUnpack)        
                        if isVectorChannel:                                                                                                                                                                                                                                                                                            
                            fmtItem=str(nItems)+'f'                    
                            idxUnpack+=nItems                           
                        else:                            
                            fmtItem='f'                         
                            idxUnpack+=1    
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'
                        unpackIdx.append(-1)
                                                                                     
                elif cDType=='RVEC':
                    if toBeUnpacked:
                        if cDTypeLength != 4:    
                            logStrFinal="{0:s}sir3sID: {1:s}: DATATYPE={2:s} and DATATYPELENGTH<>4 ({3:d})?! Error.".format(logStr,sir3sID,cDType,cDTypeLength)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        unpackIdx.append(idxUnpack)                                                                                                                                                                                                                                                                                                                            
                        fmtItem=str(nItems)+'f'                    
                        idxUnpack+=nItems                             
                    else:
                        bytesSkipped+=cDLength
                        fmtItem=str(cDLength)+'x'
                        unpackIdx.append(-1)
                else:                       
                    if toBeUnpacked:
                         logStrFinal="{0:s}sir3sID: {1:s}: UNKNOWN DATATYPE={2:s}. Error.".format(logStr,sir3sID,cDType)     
                         logger.error(logStrFinal) 
                         raise MxError(logStrFinal)                                                
                    else:
                         logStrFinal="{0:s}sir3sID: {1:s}: UNKNOWN DATATYPE={2:s}. Skipped!".format(logStr,sir3sID,cDType)     
                         logger.debug(logStrFinal)                                               
                    bytesSkipped+=cDLength
                    fmtItem=str(cDLength)+'x'
                    unpackIdx.append(-1)
                    
                self.mxRecordStructFmtString+=fmtItem

            MxRecordLengthMx1=self.mx1Df['DATAOFFSET'].iloc[-1]+self.mx1Df['DATALENGTH'].iloc[-1]     
            MxRecordLengthFmt=struct.calcsize(self.mxRecordStructFmtString)            
            if MxRecordLengthMx1 != MxRecordLengthFmt:
                logStrFinal="{0:s}Bytes per MX-Record from MX-Channels={1:d} <> Bytes from struct fmt-String for MX-Records={2:d}?! Error.".format(logStr,MxRecordLengthMx1,MxRecordLengthFmt)
                raise MxError(logStrFinal)    

            bytesUnpacked = MxRecordLengthFmt - bytesSkipped
            logger.debug("{0:s}Bytes per MX-Record={1:d}. Bytes Unpacked={2:d} (making up {3:06.2f} Bytes-%).".format(logStr,MxRecordLengthMx1,bytesUnpacked,bytesUnpacked/MxRecordLengthFmt*100))                                                  

            self.mx1Df['unpackIdx']=pd.Series(unpackIdx)
            self.mx1Df['unpackIdx']=self.mx1Df['unpackIdx'].astype('int64')      
            logger.debug("{0:s}mx1Df after generated Column: Shape: {1!s}.".format(logStr,self.mx1Df.shape))        
                                                                                                 
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _buildMxRecordStructUnpackFmtStringPost(self):
        """Stuff todo after buildMxRecordStructUnpackFmtString.
           
        Sets                 
            * .idxTIMESTAMP (idx of TIMESTAMP in MX1)
            * .unpackIdxTIMESTAMP (idx of TIMESTAMP in recordData)
            * .mxColumnNames=[] (of non Vectordata without TIMESTAMP in MX1-Sequence)
            * .mxColumnNamesVecs=[] (of Vectordata without TIMESTAMP in MX1-Sequence)
            * .idxUnpackNonVectorChannels[] (idx in recordData)
            * .idxUnpackVectorChannels[] (idx in recordData of the 1st ([0]) Element of the Vector)
            * .idxOfNonVectorChannels[] (idx in MX1 without TIMESTAMP)
            * .idxVectorChannels[] (idx in MX1)

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            
            # idxTIMESTAMP
            self.idxTIMESTAMP=self.mx1Df['Sir3sID'][self.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].index[0]
            # unpackIdxTIMESTAMP
            self.unpackIdxTIMESTAMP=self.mx1Df['unpackIdx'][self.mx1Df['Sir3sID']=='ALLG~~~-1~TIMESTAMP'].iloc[0]    
            logger.debug("{:s}idxTIMESTAMP={:d} (idx in MX1) unpackIdxTIMESTAMP={:d} (idx in recordData).".format(logStr,self.idxTIMESTAMP,self.unpackIdxTIMESTAMP))                    
            
            # columnNames used in Pandas        
            self.mxColumnNames=[]  
            self.mxColumnNamesVecs=[]  
            for idxChannel,idxUnpack in [(idxChannel,idxUnpack)  for idxChannel,idxUnpack in enumerate(self.mx1Df['unpackIdx']) if idxUnpack >=0]:                 
                sir3sID=self.mx1Df['Sir3sID'].iloc[idxChannel]        
                isVectorChannel=self.mx1Df['isVectorChannel'].iloc[idxChannel]        
                if not isVectorChannel:                   
                    self.mxColumnNames.append(sir3sID)
                else:
                    self.mxColumnNamesVecs.append(sir3sID)

            # remove Timestamp in mxColumnNamesVecs (index not value)
            idxTIMESTAMP=self.mxColumnNames.index('ALLG~~~-1~TIMESTAMP')
            del self.mxColumnNames[idxTIMESTAMP] 
            columns=len(self.mxColumnNames)
            logger.debug("{0:s}NOfColumns (without TIMESTAMP): {1:d}.".format(logStr,columns))                
            logger.debug("{0:s}NOfColumnsVecs: {1:d}.".format(logStr,len(self.mxColumnNamesVecs)))                  

            # unpack Idx of Non Vector Channels (without unpack Idx of TIMESTAMP)
            self.idxUnpackNonVectorChannels=[self.mx1Df['unpackIdx'].iloc[idx] for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if not isVectorChannel]
            self.idxUnpackNonVectorChannels.remove(self.unpackIdxTIMESTAMP) 
            idxUnpackNonVectorChannelsLen=len(self.idxUnpackNonVectorChannels)
            logger.debug("{:s}idxUnpackNonVectorChannelsLen: {:d}.".format(logStr,idxUnpackNonVectorChannelsLen))

            # check NonVectorChannels
            if idxUnpackNonVectorChannelsLen != columns:
                logger.error("{:s}idxUnpackNonVectorChannelsLen: {:d} != NOfColumns (without Timestamp): {:d}?!".format(logStr,idxUnpackNonVectorChannelsLen,columns))               

            # unpack Idx of Vector Channels
            self.idxUnpackVectorChannels=[self.mx1Df['unpackIdx'].iloc[idx] for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if isVectorChannel]
            idxUnpackVectorChannelsLen=len(self.idxUnpackVectorChannels)
            logger.debug("{:s}idxUnpackVectorChannelsLen: {:d}.".format(logStr,idxUnpackVectorChannelsLen))

            # check AllValueChannels
            rows,cols=self.mx1Df.shape
            valueChannels=idxUnpackVectorChannelsLen+idxUnpackNonVectorChannelsLen
            if (valueChannels != rows-1):
                logger.error("{:s}valueChannels: {:d} != mx1Df rows -1 {:d}?!".format(logStr,valueChannels,rows-1))               

            # Idx of Non Vector Channels
            self.idxOfNonVectorChannels=[idx for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if not isVectorChannel]
            self.idxOfNonVectorChannels.remove(self.idxTIMESTAMP) 
            logger.debug("{:s}idxOfNonVectorChannels: Len: {:d}.".format(logStr,len(self.idxOfNonVectorChannels)))

            # Idx of Vector Channels
            self.idxOfVectorChannels=[idx for idx,isVectorChannel in enumerate(self.mx1Df['isVectorChannel']) if isVectorChannel]
            logger.debug("{:s}idxOfVectorChannels:    Len: {:d}.".format(logStr,len(self.idxOfVectorChannels)))

            # check AllChannels
            allChannels=len(self.idxOfNonVectorChannels)+len(self.idxOfVectorChannels)
            if allChannels != rows-1:
                logger.error("{:s}allChannels: {:d} != mx1Df rows-1 {:d}?!".format(logStr,allChannels,rows-1))   
                
            ## list all Channels with their relevant attributes         
            #for idxChannel,idxUnpack in [(idxChannel,idxUnpack)  for idxChannel,idxUnpack in enumerate(self.mx1Df['unpackIdx']) if idxUnpack >=0]:                 
            #    sir3sID=self.mx1Df['Sir3sID'].iloc[idxChannel]
            #    idxUnpack=self.mx1Df['unpackIdx'].iloc[idxChannel]
            #    isVectorChannel=self.mx1Df['isVectorChannel'].iloc[idxChannel]
            #    isVectorChannelMx2=self.mx1Df['isVectorChannelMx2'].iloc[idxChannel]             
            #    isVectorChannelMx2Rvec=self.mx1Df['isVectorChannelMx2Rvec'].iloc[idxChannel]
            #    logger.debug("{:s}Channel-Nr. {:>6d} Sir3sID {:>60s} idxUnpack {:>6d}  isVectorChannel {!s:>6s} isVectorChannelMx2 {!s:>6s} isVectorChannelMx2Rvec {!s:>6s}.".format(logStr
            #             ,idxChannel
            #             ,sir3sID
            #             ,idxUnpack
            #             ,isVectorChannel
            #             ,isVectorChannelMx2
            #             ,isVectorChannelMx2Rvec))  
                                                                                     
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _readMxsFile(self,mxsFilePtr,mxsVecsH5StorePtr,firstTime=None,maxRecords=None):

        """
        Args:
            * mxsFilePtr: .MXS-File
            * mxsVecsH5StorePtr: .vec.h5-File
            * firstTime: used to calculate h5Key for mxsVecsH5Store
                * None (default): firstTime is set to 1st TIMESTAMP in .MXS-File 

            * maxRecords

        Returns:
            df: the mxsFile (non Vectordata only) as DataFrame

                * index: TIMESTAMP
                * df.index.is_unique 
                    
                    * might be False 
                    * because of SIR 3S'
                    * 1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  

            timesWrittenToMxsVecs: the times written to the mxsVecsH5Store
        
        mxsVecsH5StorePtr

            * is used to update the mxsVecsH5Store with mxsFile-Content

                * Key: microseconds from firstTime 
                * dfVecs
                    * index: TIMESTAMP 
                    * values: Vectordata for the TIMESTAMP
            
            * the Vectordata for a TIMESTAMP is only written when the Key does _not already exist 

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:   
            df = None 
                                                       
            mxTimes=[]
            mxTimesVecs=[]
            mxValues=[]      
            mxValuesVecs=[]           
            
            MxRecordLength=struct.calcsize(self.mxRecordStructFmtString)    
            if isinstance(maxRecords,int):
                maxRecordsLimit=True
            else:
                maxRecordsLimit=False   
                      
            recsReadFromFile=0     
            timesWrittenToMxsVecs=0
            
            if mxsVecsH5StorePtr != None:
                keysAtStart=mxsVecsH5StorePtr.keys()
                                                                     
            with mxsFilePtr: 
                try:                    
                    while True:   # while f.tell() != os.fstat(f.fileno()).st_size does NOT work with Zip's file objects ...    
                            
                        # read record 
                        try: 
                            record=mxsFilePtr.read(MxRecordLength)
                            recordData = struct.unpack(self.mxRecordStructFmtString,record)  
                        except:
                            logger.debug("{0:s}record=f.read(MxRecordLength) failed (EOF probably).".format(logStr))  
                            raise EOFError
                        else:
                            timeISO8601=None

                        # process record time
                        try:
                            timeISO8601 = recordData[self.unpackIdxTIMESTAMP] #b'2017-10-20 00:00:00.000000+01:00' for scenTime 2017-10-20 00:00:00
                            time = pd.to_datetime(timeISO8601.decode(),utc=True) # 3.6
                            time_read_after_to_datetime=time.strftime("%Y-%m-%d %H:%M:%S.%f%z") #%z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive)        
                            time = time + pd.to_timedelta('1 hour')   
                            time_read_finally=time.strftime("%Y-%m-%d %H:%M:%S.%f%z")       
                            if recsReadFromFile==0 and firstTime==None:
                                firstTime=time                                                                                                                                                                                                                                                                             
                        except Exception as e:
                            logStrFinal="{0:s}process record time failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                    
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                
                        
                        # process record
                        try:                                                                                                                 
                            # Values (without TIMESTAMP)
                            values=[recordData[idx] for idx in self.idxUnpackNonVectorChannels]                          
                            
                            # Vecs
                            valuesVecs=[] 
                            for idxOf,idxUnpack in zip(self.idxOfVectorChannels,self.idxUnpackVectorChannels):                                                            
                                valueVec=recordData[idxUnpack:idxUnpack+self.mx1Df['NOfItems'].iloc[idxOf]] # one Vector For One Timestep
                                valuesVecs.append(valueVec)                                                                                                                   
                        except:
                            logStrFinal="{0:s}process record failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                                                                                                          
                                                  
                        # store values in memory
                        try:                            
                            mxTimes.append(time)                         
                            mxValues.append(values)                           
                        except:
                            logStrFinal="{0:s}store record in memory failed at Time={1!s}. Error.".format(logStr,time_read_finally)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        
                        # store vecs in H5
                        if mxsVecsH5StorePtr != None:                            
                            try:      
                                 h5DumpLog="{:s} NO.".format('H5Dump:')
                                 h5Key=getMicrosecondsFromRefTime(refTime=firstTime,time=time)   
                                 
                                 if '/'+str(h5Key) not in keysAtStart:                                                                                                      
                                     keys=mxsVecsH5StorePtr.keys()
                                 
                                     if '/'+str(h5Key) not in keys:      
                                        mxTimesVecs=[]            
                                        mxValuesVecs=[]                                                            
                                        mxTimesVecs.append(time)     
                                        mxValuesVecs.append(valuesVecs)
                                        dfVecs = pd.DataFrame.from_records(mxValuesVecs,index=mxTimesVecs,columns=self.mxColumnNamesVecs)                                                                                                      
                                        # write H5
                                        warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
                                        warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)                          
                                        mxsVecsH5StorePtr.put(str(h5Key),dfVecs)   
                                        timesWrittenToMxsVecs+=1
                                        h5DumpLog="{:s} Written DataFrame {:s} (Nr. {:d}) with h5Key=/{!s:>20s}".format('H5Dump:','dfVecs',timesWrittenToMxsVecs,h5Key) 
                                     else:
                                        h5DumpLog="{:s} NO: key already written.".format('H5Dump:')
                                 else:
                                     h5DumpLog="{:s} NO: key in keysAtStart.".format('H5Dump:')
                                                              
                            except Exception as e:
                                logger.error("{0:s}store record as df in H5 failed at Time={1!s}. Error.".format(logStr,time_read_finally))
                                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                                logger.error(logStrFinal) 
                                raise MxError(logStrFinal)   
                                                     
                        logger.debug("{:s}TimeNr. {:>6d} read and processed finally={!s:s} Time read after to_datetime: {!s:s} timeISO8601 read: {!s:s} Values (without TIMESTAMP): {:d} - {:s}.".format(logStr
                                        ,recsReadFromFile+1
                                        ,time_read_finally
                                        ,time_read_after_to_datetime
                                        ,timeISO8601
                                        ,len(values)
                                        ,h5DumpLog))  

                        # next record                            
                        recsReadFromFile+=1                               
                        if maxRecordsLimit:
                            if recsReadFromFile == maxRecords:
                                logger.debug("{0:s}maxRecords={1:d} read.".format(logStr,maxRecords))  
                                raise EOFError   
                                                   
                except EOFError:                    
                    logger.debug("{0:s}Last Time read={1!s}. File finished.".format(logStr,time_read_finally))                                                                                             
                
                except Exception as e:
                    logger.error("{0:s}Last Time read={1!s}. Error.".format(logStr,time_read_finally))
                    logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.error(logStrFinal) 
                    raise MxError(logStrFinal) 
                                     
            logger.debug("{0:s}File finished: Records read={1:d}. Last Time read={2!s}. MB read={3:07.2f}.".format(logStr                                                                                                                                         
                                                                                    ,recsReadFromFile
                                                                                    ,time_read_finally
                                                                                    ,recsReadFromFile*MxRecordLength/pow(10,6)                                                                                                                                                               
                                                                                                                                                 )
                        )                                                                     

            df = pd.DataFrame.from_records(mxValues,index=mxTimes,columns=self.mxColumnNames)                
            logger.debug("{0:s}df.shape(): {1!s}.".format(logStr,df.shape))   
                                                                                  
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return df,timesWrittenToMxsVecs

    def _checkMxsVecsFile(self,fullCheck=False):
        """Returns (firstTime,lastTime,NOfTimes).

        Args:
            * fullCheck (bool)
                * False (default): only 1st and last h5Keys are read
                * True: all h5Keys are read

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:         
            with pd.HDFStore(self.h5FileVecs) as mxsVecsH5Store: 
                                                                                                                                               
                keys=sorted([int(key.replace('/','')) for key in mxsVecsH5Store.keys()])
                keysH5=['/'+str(key) for key in keys]
                if fullCheck:
                    for idx,key in enumerate(keysH5):                
                        dfVecs=mxsVecsH5Store[key]  
                        time=dfVecs.index[0]
                        if idx==0:
                            firstTime=time
                        logger.debug("{:s}TimeNr. {:>6d} with key {!s:>20s} and TIMESTAMP {!s:s}.".format(logStr,idx+1,key,time))         
                    lastTime=time
                else:
                    #1st Time
                    key=keysH5[0]
                    dfVecs=mxsVecsH5Store[key] 
                    firstTime=dfVecs.index[0]
                    #last Time
                    key=keysH5[-1]
                    dfVecs=mxsVecsH5Store[key] 
                    lastTime=dfVecs.index[0]
                                                                                                                
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                      
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return (firstTime,lastTime,len(keysH5))   
        
    def _handleMxsVecsFileDeletion(self,mxsFile,newMxsVecsFile=False):
        """Handles the deletion of mxsVecsFile.

        Args:
            * mxsFile
            * newMxsVecsFile

        mxsVecsFile is DELETED! if: 
            * existing and older than mxsFile
            * or newMxsVecsFile                  
            
        Raises:
            MxError                         
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
        
            # .vec.h5 Handling 
            if os.path.exists(self.h5FileVecs):      

                if newMxsVecsFile:
                    logger.debug("{:s}Delete H5VecDump because NewH5Vec ...".format(logStr,self.h5FileVecs)) 
                    os.remove(self.h5FileVecs)   
                else:
                    if os.path.exists(mxsFile):                         
                        mxsFileTime=os.path.getmtime(mxsFile) 
                    else:
                        mxsFileTime=0
                    mxsH5FileTime=os.path.getmtime(self.h5FileVecs)

                    if mxsFileTime>mxsH5FileTime:
                        # die zu lesende Mxs ist neuer als der Dump: Dump loeschen              
                        logger.debug("{:s}Delete H5VecDump because Mxs {:s} To Read is newer than H5VecDump {:s} ...".format(logStr,mxsFile,self.h5FileVecs))                             
                        os.remove(self.h5FileVecs)      
                        
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                      
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                                       
            
    def setResultsToMxsFile(self,mxsFile=None,add=False,NewH5Vec=False,maxRecords=None):
        """Sets (default) or adds mxsFile-Content to .df.
        
        Args:
            * mxsFile (str)
                * None (default): .mxsFile is used  
            * add (bool): default: False: sets df to mxsFile-Content 
            * NewH5Vec
            * maxRecords

        Returns:
            * timesWrittenToMxsVecs
             
        .df
            * index: TIMESTAMP
            
            * self.df.index.is_unique will be True 

            * because in SIR 3S'
            * 1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  

                * +TIME       is dropped                                
                * +TMIN/TMAX are dropped
                   
            * and because resulting overlapping TIMESTAMPs due to intersections (add=True) are also dropped      

        .h5FileVecs

            * is updated with mxsFile-Content

            * is DELETED! before if existing and 
                * older than mxsFile
                * or newMxsVecsFile        
                
        Raises:
            MxError                                                 
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 

            # Mxs specification 
            if mxsFile == None:
                logger.debug("{0:s}Mxs: Implicit specified.".format(logStr))                                
                mxsFile=self.mxsFile
            
            # .vec.h5 Handling 
            self._handleMxsVecsFileDeletion(mxsFile=mxsFile,newMxsVecsFile=NewH5Vec)
            
            mxsVecH5Store=pd.HDFStore(self.h5FileVecs) 
            #
            #h5VecsFileTimeBefore=os.path.getmtime(self.h5FileVecs)
                                                                                      
            if isinstance(self.df,pd.core.frame.DataFrame):   
                firstTime=self.df.index[0]
            else:
                firstTime=None
            
            #Mxs reading ...           
            logger.debug("{0:s}Mxs: {1:s} opening ...".format(logStr,mxsFile))                
            with open(mxsFile,'rb') as f:
                 # Mxs exists ...
                logger.debug("{0:s}Mxs: {1:s} reading ...".format(logStr,mxsFile))                
                # Mxs reading ...
                dfMxs,timesWrittenToMxsVecs=self._readMxsFile(f,mxsVecsH5StorePtr=mxsVecH5Store,firstTime=firstTime,maxRecords=maxRecords)                                     
                           
            if isinstance(dfMxs,pd.core.frame.DataFrame):                                     
                # Unique index ...
                if not dfMxs.index.is_unique:                        
                     logger.debug("{0:s}Mxs: {1:s}: NOT unique TIMESTAMPS: Their dfMxs Shape: {2!s}.".format(logStr,mxsFile,dfMxs[dfMxs.index.duplicated()].shape))    
                     dfMxs=dfMxs[dfMxs.index.duplicated() == False]     
                     logger.debug("{0:s}Mxs: {1:s}: New unique                   dfMxs Shape: {2!s}.".format(logStr,mxsFile,dfMxs.shape))   
                if not add or not isinstance(self.df,pd.core.frame.DataFrame): 
                    self.df=dfMxs
                    logger.debug("{0:s}Mxs: {1:s}: Assigned.     df Shape: {2!s}.".format(logStr,mxsFile,self.df.shape))    
                else:
                    self.df=pd.concat([self.df,dfMxs])
                    logger.debug("{0:s}Mxs: {1:s}: Added.    New df Shape: {2!s}.".format(logStr,mxsFile,self.df.shape))    
                    if not self.df.index.is_unique:                        
                        logger.debug("{0:s}Mxs: {1:s}: NOT unique TIMESTAMPS added (intersection): Their df Shape: {2!s}.".format(logStr,mxsFile,self.df[self.df.index.duplicated()].shape))    
                        self.df=self.df[self.df.index.duplicated() == False] 
                        logger.debug("{0:s}Mxs: {1:s}: New unique                                        df Shape: {2!s}.".format(logStr,mxsFile,self.df.shape))       
                # sort
                if add:
                    self.df.sort_index(inplace=True)    
                logger.debug("{0:s}RESULT after {1:s}: df Shape: {2!s} First Time: {3!s} Last Time: {4!s}.".format(logStr,mxsFile,self.df.shape,self.df.index[0],self.df.index[-1]))                                             
            else:
                logger.error("{0:s}Mxs: {1:s}: Reading failed.".format(logStr,mxsFile))    
            
            #import time
            #h5VecsFileTimeAfter=os.path.getmtime(self.h5FileVecs)
            #logger.debug("{:s}: h5FileVecs: Before: {:s}: After:  {:s}.".format(logStr
            #,time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTimeBefore))
            #,time.strftime("%Y-%m-%d %H:%M:%S %z",time.gmtime(h5VecsFileTimeAfter))
            #))                                             

        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}mxsFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                       
        finally:
            mxsVecH5Store.close()
            return timesWrittenToMxsVecs
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def setResultsToMxsZipFile(self,mxsZipFile=None,add=False,NewH5Vec=False,maxRecords=None):
        """Sets (default) or adds mxsZipFile-Content to .df.

        Args:
            * mxsZipFile (str)
                * None (default): .mxsFile is used  
            * add (bool): default: False: sets df to mxsZipFile-Content 
            * NewH5Vec
            * maxRecords

        Returns:
            * timesWrittenToMxsVecsFromZip

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            # Zip specification ...
            if mxsZipFile == None:
                mxsZipFile=self.mxsZipFile
            
            # Zip existence ... 
            logger.debug("{0:s}Zip: {1:s} ...".format(logStr,mxsZipFile))                               
            with open(mxsZipFile,'rb') as f:   
                pass     

            # Zip opening ...
            logger.debug("{0:s}Zip: {1:s} opening ...".format(logStr,mxsZipFile)) 
            try:
                z = zipfile.ZipFile(mxsZipFile,'r')
            except:
                logStrFinal="{0:s}{1:s}: opening the Zip failed. Error.".format(logStr,mxsZipFile)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)   

            # maxRecords-Check
            if isinstance(maxRecords,int):
                maxRecordsLimit=True
            else:
                maxRecordsLimit=False   

            # .vec.h5 Handling 
            self._handleMxsVecsFileDeletion(mxsFile=mxsZipFile,newMxsVecsFile=NewH5Vec)
                
            mxsVecH5Store=pd.HDFStore(self.h5FileVecs) 
                                                                                      
            if isinstance(self.df,pd.core.frame.DataFrame):   
                firstTime=self.df.index[0]
            else:
                firstTime=None
          
            # Zip reading ...              
            recsReadFromZip=0         
            timesWrittenToMxsVecsFromZip=0
            dfZip=None
            for mxsFileName in sorted(z.namelist()):  
                # Mxs reading ...                        
                with z.open(mxsFileName,'r') as f: 
                    logger.debug("{0:s}Zip: {1:s}: {2:s} reading ...".format(logStr,mxsZipFile,mxsFileName))       
                    dfMxs,timesWrittenToMxsVecs=self._readMxsFile(f,mxsVecsH5StorePtr=mxsVecH5Store,firstTime=firstTime,maxRecords=maxRecords) 
                    timesWrittenToMxsVecsFromZip+=timesWrittenToMxsVecs

                if isinstance(dfMxs,pd.core.frame.DataFrame):                                                                                      
                    # Unique index ...
                    if not dfMxs.index.is_unique:                        
                         logger.debug("{0:s}Mxs: {1:s}: NOT unique TIMESTAMPS: Their dfMxs Shape: {2!s}.".format(logStr,mxsFileName,dfMxs[dfMxs.index.duplicated()].shape))    
                         dfMxs=dfMxs[dfMxs.index.duplicated() == False]     
                         logger.debug("{0:s}Mxs: {1:s}: New unique                   dfMxs Shape: {2!s}.".format(logStr,mxsFileName,dfMxs.shape))                                                                            
                    recsReadFromZip+=len(dfMxs.index)
                else:
                    logger.warning("{0:s}Zip: {1:s}: {2:s}: Reading failed.".format(logStr,mxsZipFile,mxsFileName))    
                    continue   

                if not isinstance(dfZip,pd.core.frame.DataFrame):
                    # 1st Mxs
                    dfZip=dfMxs
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: Assigned. Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip.shape))    
                else:                    
                    dfZip=pd.concat([dfZip,dfMxs])
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: Added.    Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip.shape))    
                # Unique index ...
                if not dfZip.index.is_unique:                        
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: NOT unique TIMESTAMPS added (intersection): Their Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip[dfZip.index.duplicated()].shape))    
                    dfZip=dfZip[dfZip.index.duplicated() == False] 
                    logger.debug("{0:s}Zip: {1:s}: {2:s}: New unique Shape: {3!s}.".format(logStr,mxsZipFile,mxsFileName,dfZip.shape))             
                
                if maxRecordsLimit:
                    if recsReadFromZip >= maxRecords:
                        logger.debug("{0:s}>=maxRecords ({1:d}) read.".format(logStr,maxRecords))  
                        break

            if isinstance(dfZip,pd.core.frame.DataFrame):
                logger.debug("{0:s}Zip: {1:s}: Final dfZip Shape: {2!s}.".format(logStr,mxsZipFile,dfZip.shape))  

                if not add or not isinstance(self.df,pd.core.frame.DataFrame): 
                    self.df = dfZip   
                    logger.debug("{0:s}Zip: {1:s}: Assigned dfZip To df. df     Shape: {2!s}.".format(logStr,mxsZipFile,self.df.shape))    
                else:
                    self.df=pd.concat([self.df,dfZip])
                    logger.debug("{0:s}Zip: {1:s}: Added    dfZip To df. New df Shape: {2!s}.".format(logStr,mxsZipFile,self.df.shape))    
                # Unique index ...
                if not self.df.index.is_unique:                        
                    logger.debug("{0:s}Zip: {1:s}: NOT unique TIMESTAMPS added (intersection): Their df Shape: {2!s}.".format(logStr,mxsZipFile,self.df[self.df.index.duplicated()].shape))    
                    self.df=self.df[self.df.index.duplicated() == False] 
                    logger.debug("{0:s}Zip: {1:s}: New unique                                        df Shape: {2!s}.".format(logStr,mxsZipFile,self.df.shape))   
                
                # sort
                self.df.sort_index(inplace=True)  
                logger.debug("{0:s}RESULT after {1:s}: df Shape: {2!s} First Time: {3!s} Last Time: {4!s}.".format(logStr,mxsZipFile,self.df.shape,self.df.index[0],self.df.index[-1]))                

            else:
                logger.error("{0:s}Zip: {1:s}: Reading failed.".format(logStr,mxsZipFile))                                          
                                                                    
                       
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}mxsZipFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsZipFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                  
        finally:
            mxsVecH5Store.close()
            return timesWrittenToMxsVecsFromZip
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def ToH5(self,h5File=None):
        """Stores .mx1Df, .mx2Df, .df to h5File.

        Args:
            h5File(str): default: None: self.h5File is used  

        .h5File
            * is !DELETED! before if existing

        Keys used
            * /MX1
            * /MX2
            * /MXS

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            if h5File == None:
                h5File=self.h5File

            if os.path.exists(h5File):                        
                logger.debug("{0:s}{1:s}: Delete H5 ...".format(logStr,h5File))     
                os.remove(h5File)

            relPath2Mx1FromCurDir=os.path.normpath(os.path.relpath(os.path.normpath(self.mx1File),start=os.path.normpath(os.path.curdir)))
            h5KeySep='/'
            h5KeyCharForDot='_'
            h5KeyCharForMinus='_'
            relPath2Mx1FromCurDirH5BaseKey=re.sub('\.',h5KeyCharForDot,re.sub(r'\\',h5KeySep,re.sub('-',h5KeyCharForMinus,re.sub('.mx1','',relPath2Mx1FromCurDir,flags=re.IGNORECASE))))
                       
            warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
            warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)
                                      
            logger.debug("{0:s}pd.HDFStore({1:s}) ...".format(logStr,h5File))                 
            with pd.HDFStore(h5File) as h5Store:  
                if isinstance(self.mx1Df,pd.core.frame.DataFrame):      
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MX1' 
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'mx1Df',h5Key))           
                    h5Store.put(h5Key,self.mx1Df)

                    recordStructFmtStringFile=self.h5File+'.metadata'
                    recordStructFmtStringFileKey='recordStructFmtStringFileKey'
                    metadata=dict(recordStructFmtStringFileKey=recordStructFmtStringFile)
                    with open(recordStructFmtStringFile,'w') as f:
                        f.write(self.mxRecordStructFmtString)
                    #recordStructFmtStringKey='recordStructFmtStringKey'
                    #metadata=dict(recordStructFmtStringKey=self.mxRecordStructFmtString)
                        #File "C:\aroot\work\hdf5-1.8.15-patch1\src\H5Oalloc.c", line 1142, in H5O_alloc object header message is too large
                    
                    h5Store.get_storer(h5Key).attrs.metadata=metadata
                    #logger.debug("{:s}{:s}: Writing metadata for h5Key={:s} with key={:s}: {:s}".format(
                    #    logStr,h5File,h5Key,recordStructFmtStringKey,self.mxRecordStructFmtString)
                    #             )  
                    logger.debug("{:s}{:s}: Writing metadata for h5Key={:s} with key={:s}: {:s}".format(
                        logStr,h5File,h5Key,recordStructFmtStringFileKey,recordStructFmtStringFile)
                                 )  
     
                if isinstance(self.mx2Df,pd.core.frame.DataFrame):      
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MX2' 
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'mx2Df',h5Key))           
                    h5Store.put(h5Key,self.mx2Df)
                if isinstance(self.df,pd.core.frame.DataFrame):    
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'MXS'  
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'df',h5Key))         
                    h5Store.put(h5Key,self.df)
             
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                      
        finally:
            h5Store.close()
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def FromH5(self,h5File=None):
        """Sets .mx1Df, .mx2Df, .df to h5File-Content.

        Args:
            * h5File(str)
                * None (default): .h5File is used  

        Keys expected
            * /MX1
            * /MX2
            * /MXS

        Raises:
            MxError
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))  
        
        try:

            if h5File == None:
                h5File=self.h5File

            #Check if h5File exists
            if not os.path.exists(h5File):    
                logStrFinal="{0:s}{1:s}: Not Existing!".format(logStr,h5File)                                 
                raise MxError(logStrFinal)           
  
            #Read
            with pd.HDFStore(h5File) as h5Store:
                h5Keys=sorted(h5Store.keys())
                for h5Key in h5Keys:
                    h5KeySep='/'
                    match=re.search('('+h5KeySep+')(\w+$)',h5Key)
                    key=match.group(2)
                    if key == 'MX1':                            
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.mx1Df=h5Store[h5Key]

                        metadataAvailable=False
                        try:
                            metadata=h5Store.get_storer(h5Key).attrs.metadata  
                            #recordStructFmtStringKey='recordStructFmtStringKey'
                            recordStructFmtStringFileKey='recordStructFmtStringFileKey'
                            #if recordStructFmtStringKey in metadata:
                            if recordStructFmtStringFileKey in metadata:
                                #mxRecordStructFmtString=metadata[recordStructFmtStringKey]
                                recordStructFmtStringFile=metadata[recordStructFmtStringFileKey]
                                #logger.debug("{:s}{:s}: Read metadata for h5Key={:s}. key={:s}: {:s}".format(logStr,h5File,h5Key,recordStructFmtStringKey,mxRecordStructFmtString))    
                                logger.debug("{:s}{:s}: Read metadata for h5Key={:s}. key={:s}: {:s}".format(logStr,h5File,h5Key,recordStructFmtStringFileKey,recordStructFmtStringFile))    
                                
                                with open(recordStructFmtStringFile) as f:
                                    mxRecordStructFmtString=f.readline()
                                
                                metadataAvailable=True                      
                        except Exception as e:
                            logger.debug("{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e)))    
                            logger.debug("{:s}{:s}: metadata for h5Key={:s} not existing.".format(logStr,h5File,h5Key))
                        
                        if metadataAvailable:
                            self.mxRecordStructFmtString=mxRecordStructFmtString
                        else:
                            self._buildMxRecordStructUnpackFmtString()                                                                                                                           
                        self._buildMxRecordStructUnpackFmtStringPost()      

                    if key == 'MX2':                            
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.mx2Df=h5Store[h5Key]                         
                    if key == 'MXS':                           
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.df=h5Store[h5Key]
                        # Check if .vec.h5 corresponds
                        firstTime=self.df.index[0]
                        lastTime=self.df.index[-1]
                        rows,cols=self.df.shape
                        tupleDf=(firstTime,lastTime,rows)
                        tupleVecH5=self._checkMxsVecsFile()
                        if tupleDf != tupleVecH5:                            
                            logger.warning("{:s}{:s}: tupleDf {!s:s} != tupleVecH5 {!s:s}.".format(logStr,h5File,tupleDf,tupleVecH5))              
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                           
        finally: 
            h5Store.close()            
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                

    def getMxsVecsFileData(self,timesReq=None):
        """
        Args:
            * timesReq: List of requested TIMESTAMPs

        Returns:
            * List of dfs with mxsVecsFileData
            * one TIMESTAMP per df
            * index: TIMESTAMP

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
           
            mxsVecsDfs=None

            if os.path.exists(self.h5FileVecs):
                pass
            else:
                logStrFinal="{:s}{:s}: Not existing!".format(logStr,self.h5FileVecs)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)         

            #requested
            h5KeysRequested=[]
            firstTime=self.df.index[0]
            for timeReq in timesReq:
                key=getMicrosecondsFromRefTime(refTime=firstTime,time=timeReq)
                h5KeysRequested.append(key)
            h5KeysRequested=['/'+str(key) for key in h5KeysRequested]           
                                 
            mxsVecsDfs=[]
            with pd.HDFStore(self.h5FileVecs) as h5Store:
                #available
                h5KeysAvailable=sorted(h5Store.keys())      
                for idx,h5Key in enumerate(h5KeysRequested):
                    if h5Key in h5KeysAvailable:
                        mxsVecsDfs.append(h5Store[h5Key])
                    else:
                        logger.debug("{:s}{:s}: Key {:s} (Time {:s}) not available.".format(logStr,self.h5FileVecs,h5Key,timesReq[idx]))
                                                        
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                           
        finally:                      
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return mxsVecsDfs

    def dumpInMxsFormat(self,mxsDumpFile=None):
        """Dumps in MXS-Format to mxsDumpFile (for testing purposes). 

        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
            if mxsDumpFile == None:
                mxsDumpFile=self.mxsFile+'.dump'

            with open(mxsDumpFile,'wb') as f:

                # ueber alle Zeiten in self.df ...
                idxDumped=0
                for idx,row in enumerate(self.df.itertuples(index=False)):
                    
                    # TIMESTAMP herrichten
                    try:                        
                        scenTime=self.df.index[idx]                                                                                               
                        #timeISO8601 read:          b'2017-10-20 00:00:00.000000+01:00' - the original timeISO8601 read is marked as UTC +1 written as +01:00
                        #Time read after to_datetime: 2017-10-19 23:00:00.000000+0000   - the result after pd.to_datetime(timeISO8601,utc=True) 
                        #Time read finally            2017-10-20 00:00:00.000000+0000   - the time used - "corrected" manually +1 hour 
                        #+01:00 instead of %z because %z will be +0000 ...  
                        scenTimeStr=scenTime.strftime("%Y-%m-%d %H:%M:%S.%f+01:00") 
                        scenTimeStrBytes=scenTimeStr.encode('utf-8')
                    except:
                        logStrFinal="{0:s}h5File: {1!s}: TIMESTAMP herrichten: Error.".format(logStr,mxsDumpFile)
                        logger.error(logStrFinal) 
                        raise MxError(logStrFinal)    

                    # Values herrichten und Satz schreiben
                    try:    
                        valuesNonVec=list(row)
                        # valuesVec
                        # h5Key aus scenTime
                        firstTime=self.df.index[0]
                        h5Key=getMicrosecondsFromRefTime(refTime=firstTime,time=scenTime)
                        
                        h5Key='/'+str(h5Key)
                        # dfVecs lesen
                        with pd.HDFStore(self.h5FileVecs) as mxsVecsH5Store: 
                            dfVecs=mxsVecsH5Store[h5Key]  
                        for row in dfVecs.itertuples(index=False):
                            # one row
                            valuesVec=list(row)
                        # Gesamt anlegen
                        rows,cols = self.mx1Df.shape
                        values=[]
                        for idx in range(rows):
                            values.append(None)
                        # Gesamt bestuecken
                        for idx,idxOf in enumerate(self.idxOfVectorChannels):
                            values[idxOf]=valuesVec[idx]
                        for idx,idxOf in enumerate(self.idxOfNonVectorChannels):
                            values[idxOf]=valuesNonVec[idx]                        
                        # TIMESTAMP einpflegen
                        values[self.idxTIMESTAMP]=scenTimeStrBytes      
                        # Gesamt Einzelvalues
                        valuesSingle=[]
                        for idx,value in enumerate(values):
                            if idx not in self.idxOfVectorChannels:
                                valuesSingle.append(value)
                            else:
                                for vecItem in value:
                                    valuesSingle.append(vecItem)                                                                                                                                  
                        # Satz schreiben
                        bytes=struct.pack(self.mxRecordStructFmtString,*valuesSingle)
                        f.write(bytes)        
                        logger.debug("{:s}mxsDumpFile: {:s}: TimeNr. {:>6d} with TIMESTAMP: {:s}: Dumped.".format(logStr,mxsDumpFile,idxDumped,scenTimeStr))    
                        idxDumped=idxDumped+1                                                                 
                    except:
                        logger.debug("{:s}mxsDumpFile: {:s}: TIMESTAMP: {:s}: Exception. Continue.".format(logStr,mxsDumpFile,scenTimeStr))                                                     
                        continue                      
                                                                                    
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}mxsDumpFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsDumpFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                  
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

        suite=doctest.DocTestSuite() # globs={'testDir':'testdata'})   
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
