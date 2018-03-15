"""
SIR 3S MX-Interface (short: MX):
---------------------------
MX is a file based, channel-oriented interface for SIR 3S' calculation results.
Module Mx contains stuff to utilize SIR 3S' MX calculation results in pure Python.  
SIR 3S MX calculation results:
---------------------------
Binary .MXS-Files contain the SIR 3S calculations results. 
A Model calculation run creates at least one .MXS-File (Result-File).
There is one .MX1-File (an XML-File) for each SIR 3S Model calculation run.    
This .MX1-File defines in XML a sequence of MX-Channels. 
And - as a result - the Byte-Layout of a single MX3-Record in .MXS.
A MX3-Record contains calculation results for one Timestamp.
A .MXS-File contains at least one MX3-Record.
---------------------------
A MX-Channel can be 
a single Value or a
Vector: Sequence of calculation results of the same AType
    of all Objects of a certain OType or (called Vectorchannels)
    of all interior Points for all Pipes (called Pipevectorchannels)
    and Vectors with ATTRTYPE in: {'SVEC', 'PVECMIN_INST', 'PVECMAX_INST'}.
For Vectorchannels and Pipevectorchannels the sequence of Objects is defined in the .MX2-File. 
For Pipevectorchannels the Number of interior Points per Pipe is defined in the .MX2-File. 
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
>>> h5File=os.path.join(path,'testdata\OneLPipe.h5')
>>> mx1File=os.path.join(path,'testdata\WDOneLPipe\B1\V0\BZ1\M-1-0-1.MX1')
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
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...    os.remove(mx.h5FileMxsVecs)
>>> # ---
>>> # 1st Read MXS
>>> # ---
>>> logger.debug("{0:s}: 1st Read MXS".format('DOCTEST')) 
>>> mx.setResultsToMxsFile() # looks for M-1-0-1.MXS in same Dir 
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
>>> newShape=mx.df.shape
>>> newShape==oldShape
True
>>> # ---
>>> # 1st Add same Zip (for testing ensuring uniqueness) 
>>> # ---
>>> logger.debug("{0:s}: 1st Add same Zip (for testing ensuring uniqueness)".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile(add=True) # looks for M-1-0-1.ZIP in same Dir 
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
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
...     myzip.write(mxsDumpFile)  
>>> # ---
>>> # Read Zip with Orig and Dump
>>> # ---
>>> logger.debug("{0:s}: Read Zip with Orig and Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile()
>>> rowsZip,colsZip = mx.df.shape
>>> rowsZip==rowsOld
True
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
(4, 41)
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
(Timestamp('2018-03-03 00:00:00+0000', tz='UTC'), Timestamp('2018-03-03 00:00:03+0000', tz='UTC'), 4)
>>> mx._checkMxsVecsFile(fullCheck=True)
(Timestamp('2018-03-03 00:00:00+0000', tz='UTC'), Timestamp('2018-03-03 00:00:03+0000', tz='UTC'), 4)
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',1,'Change','setResultsToMxsFile: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',2,'Change','setResultsToMxsZipFile: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',3,'Change','ToH5: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',4,'Change','FromH5: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',5,'Change','*: except Exception as e')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',6,'Change','setResultsToMxsFile: finally: NewH5Vec=False')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',7,'Change','__init__(...,NoH5Read=True,...)')) 
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...    os.remove(mx.h5FileMxsVecs)
>>> mx=Mx(mx1File=mx1File,NoH5Read=True)
>>> os.path.exists(mx.h5FileMxsVecs) # exists due to previous test
True
>>> h5VecsFileTime=os.path.getmtime(mx.h5FileMxsVecs) 
>>> mx=Mx(mx1File=mx1File,NoH5Read=True)
>>> h5VecsFileTime<os.path.getmtime(mx.h5FileMxsVecs) 
True
>>> h5VecsFileTime=os.path.getmtime(mx.h5FileMxsVecs) 
>>> mx=Mx(mx1File=mx1File)
>>> h5VecsFileTime==os.path.getmtime(mx.h5FileMxsVecs) 
True
>>> mx.setResultsToMxsFile()
>>> h5VecsFileTime==os.path.getmtime(mx.h5FileMxsVecs) 
True
>>> mx.setResultsToMxsFile(NewH5Vec=True)
>>> h5VecsFileTime<os.path.getmtime(mx.h5FileMxsVecs) 
True
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',8,'Change','setResultsToMxsZipFile: finally: NewH5Vec=False')) 
>>> mx.ToH5()
>>> mx=Mx(mx1File=mx1File,NoH5Read=True)
>>> os.path.exists(mx.h5File)
False
>>> pd.set_option('display.max_columns',None)
>>> pd.set_option('display.width',666666)
>>> print("'''{:s}'''".format(repr(mx.mx1Df).replace('\\n','\\n   ')))
'''   ADDEND      ATTRTYPE CLIENT_FLAGS CLIENT_ID  DATALENGTH  DATAOFFSET DATATYPE  DATATYPELENGTH DEVIATION FACTOR  FLAGS LINKED_CHANNEL LOWER_LIMIT NAME1 NAME2 NAME3 OBJTYPE           OBJTYPE_PK OPCITEM_ID                                     TITLE       UNIT UPPER_LIMIT                         Sir3sID  NOfItems isVectorChannel isVectorChannelMx2 isVectorChannelMx2Rvec  unpackIdx
   0       0     TIMESTAMP            0                    32           0     CHAR              32         0      1    241             -1      -1E+20                      ALLG                   -1                            Zeitstempel nach ISO 8601     [text]       1E+20             ALLG~~~-1~TIMESTAMP         1           False              False                  False          0
   1       0  SNAPSHOTTYPE            0                     4          32     CHAR               4         0      1    241             -1      -1E+20                      ALLG                   -1               Typ des Zeitpunktes/Ausgabedatensatzes     [text]       1E+20          ALLG~~~-1~SNAPSHOTTYPE         1           False              False                  False          1
   2       0        CVERSO            0                    80          36     CHAR              80         0      1    241             -1      -1E+20                      ALLG                   -1                                      Versionskennung     [text]       1E+20                ALLG~~~-1~CVERSO         1           False              False                  False          2
   3       0        EXSTAT            0                     4         116     INT4               4         0      1   1265             -1      -1E+20                      ALLG                   -1                           Exit-Status der Berechnung         []       1E+20                ALLG~~~-1~EXSTAT         1           False              False                  False          3
   4       0         NFEHL            0                     4         120     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1                Anzahl Fehler im Berechnungsabschnitt         []       1E+20                 ALLG~~~-1~NFEHL         1           False              False                  False          4
   5       0         NWARN            0                     4         124     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1             Anzahl Warnungen im Berechnungsabschnitt         []       1E+20                 ALLG~~~-1~NWARN         1           False              False                  False          5
   6       0         NMELD            0                     4         128     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1             Anzahl Meldungen im Berechnungsabschnitt         []       1E+20                 ALLG~~~-1~NMELD         1           False              False                  False          6
   7       0       CPUTIME            0                     4         132     REAL               4         0      1    241             -1      -1E+20                      ALLG                   -1                                  CPU-Zeit seit Start        [s]       1E+20               ALLG~~~-1~CPUTIME         1           False              False                  False          7
   8       0       USRTIME            0                     4         136     REAL               4         0      1    241             -1      -1E+20                      ALLG                   -1                                  USR-Zeit seit Start        [s]       1E+20               ALLG~~~-1~USRTIME         1           False              False                  False          8
   9       0       NPGREST            0                     4         140     INT4               4         0      1     49             -1      -1E+20                      ALLG                   -1                   Anzahl aktiver PGRP in Restriktion         []       1E+20               ALLG~~~-1~NPGREST         1           False              False                  False          9
   10      0       NETZABN            0                     4         144     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                                          Netzabnahme     [m3/h]       1E+20               ALLG~~~-1~NETZABN         1           False              False                  False         10
   11      0         NKNUV            0                     4         148     INT4               4         0      1   1233             -1      -1E+20                      ALLG                   -1                      Anzahl KNOT mit Unterversorgung         []       1E+20                 ALLG~~~-1~NKNUV         1           False              False                  False         11
   12      0         MKNUV            0                     4         152     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                   Fehlmenge KNOT aus Unterversorgung     [m3/h]       1E+20                 ALLG~~~-1~MKNUV         1           False              False                  False         12
   13      0       NFVHYUV            0                     4         156     INT4               4         0      1   1057             -1      -1E+20                      ALLG                   -1                Anzahl FWVB mit hydr. Unterversorgung         []       1E+20               ALLG~~~-1~NFVHYUV         1           False              False                  False         13
   14      0       NFVTHUV            0                     4         160     INT4               4         0      1   1057             -1      -1E+20                      ALLG                   -1                Anzahl FWVB mit ther. Unterversorgung         []       1E+20               ALLG~~~-1~NFVTHUV         1           False              False                  False         14
   15      0       MFVHYUV            0                     4         164     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1             Fehlmenge FWVB aus hydr. Unterversorgung     [m3/h]       1E+20               ALLG~~~-1~MFVHYUV         1           False              False                  False         15
   16      0       MFVTHUV            0                     4         168     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1             Fehlmenge FWVB aus ther. Unterversorgung     [m3/h]       1E+20               ALLG~~~-1~MFVTHUV         1           False              False                  False         16
   17      0      TVMINMAX            0                     4         172     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1                  Maximum der erf. min. VL-Temperatur       [°C]       1E+20              ALLG~~~-1~TVMINMAX         1           False              False                  False         17
   18      0        ITERHY            0                     4         176     INT4               4         0      1   1265             -1      -1E+20                      ALLG                   -1                Anzahl benötigter (hydr.) Iterationen         []       1E+20                ALLG~~~-1~ITERHY         1           False              False                  False         18
   19      0         LFQSV            0                     4         180     REAL               4         0      1   1041             -1      -1E+20                      ALLG                   -1                       Lastfaktor für Strangentnahmen         []       1E+20                 ALLG~~~-1~LFQSV         1           False              False                  False         19
   20      0         JWARN            0                     4         184     INT4               4         0      1    241             -1      -1E+20                      ALLG                   -1                                            Warnstufe         []       1E+20                 ALLG~~~-1~JWARN         1           False              False                  False         20
   21      0  NETZABNEXITS            0                     4         188     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                         Netzabnahme ohne Druckränder     [m3/h]       1E+20          ALLG~~~-1~NETZABNEXITS         1           False              False                  False         21
   22      0  LINEPACKRATE            0                     4         192     REAL               4         0      1     65             -1      -1E+20                      ALLG                   -1                                 Gesamt-Linepack-Rate  [(N)m3/h]       1E+20          ALLG~~~-1~LINEPACKRATE         1           False              False                  False         22
   23      0   LINEPACKGES            0                     4         196     REAL               4         0      1     65             -1      -1E+20                      ALLG                   -1                                      Gesamt-Linepack    [(N)m3]       1E+20           ALLG~~~-1~LINEPACKGES         1           False              False                  False         23
   24      0  LINEPACKGEOM            0                     4         200     REAL               4         0      1     65             -1      -1E+20                      ALLG                   -1                           Gesamt-Linepack Rohrinhalt    [(N)m3]       1E+20          ALLG~~~-1~LINEPACKGEOM         1           False              False                  False         24
   25      0         RHOAV            0                     4         204     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                                      Mittlere Dichte    [kg/m3]       1E+20                 ALLG~~~-1~RHOAV         1           False              False                  False         25
   26      0           TAV            0                     4         208     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                                  Mittlere Temperatur       [°C]       1E+20                   ALLG~~~-1~TAV         1           False              False                  False         26
   27      0           PAV            0                     4         212     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                                      Mittlerer Druck    [bar,a]       1E+20                   ALLG~~~-1~PAV         1           False              False                  False         27
   28      0   FWVB_DPHMIN            0                     4         216     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1                Min. Differenzdruck aller Verbraucher      [bar]       1E+20           ALLG~~~-1~FWVB_DPHMIN         1           False              False                  False         28
   29      0    KNOT_PHMAX            0                     4         220     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                             Max. Knotendruck im Netz      [bar]       1E+20            ALLG~~~-1~KNOT_PHMAX         1           False              False                  False         29
   30      0    KNOT_PHMIN            0                     4         224     REAL               4         0      1   1265             -1      -1E+20                      ALLG                   -1                             Min. Knotendruck im Netz      [bar]       1E+20            ALLG~~~-1~KNOT_PHMIN         1           False              False                  False         30
   31      0   FWVB_TVLMIN            0                     4         228     REAL               4         0      1   1057             -1      -1E+20                      ALLG                   -1                 Min. VL-Temperatur aller Verbraucher       [°C]       1E+20           ALLG~~~-1~FWVB_TVLMIN         1           False              False                  False         31
   32      0       NETZBEZ            0                     4         232     REAL               4         0      1   1233             -1      -1E+20                      ALLG                   -1                                            Netzbezug     [m3/h]       1E+20               ALLG~~~-1~NETZBEZ         1           False              False                  False         32
   33      0            PH            0                     4         236     REAL               4         0      1   1265             -1      -1E+20     I                KNOT  5642914844465475844                                                Druck      [bar]       1E+20  KNOT~I~~5642914844465475844~PH         1           False              False                  False         33
   34      0            QM            0                     4         240     REAL               4         0      1   1265             -1      -1E+20     I                KNOT  5642914844465475844                                  Externer Durchfluss     [m3/h]       1E+20  KNOT~I~~5642914844465475844~QM         1           False              False                  False         34
   35      0            PH            0                     4         244     REAL               4         0      1   1265             -1      -1E+20     K                KNOT  5289899964753656852                                                Druck      [bar]       1E+20  KNOT~K~~5289899964753656852~PH         1           False              False                  False         35
   36      0            QM            0                     4         248     REAL               4         0      1   1265             -1      -1E+20     K                KNOT  5289899964753656852                                  Externer Durchfluss     [m3/h]       1E+20  KNOT~K~~5289899964753656852~QM         1           False              False                  False         36
   37      0          MVEC            0                   404         252     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                          [kg/s]       1E+20                 ROHR~*~*~*~MVEC       101            True               True                   True         37
   38      0        RHOVEC            0                   404         656     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                         [kg/m3]       1E+20               ROHR~*~*~*~RHOVEC       101            True               True                   True        138
   39      0          ZVEC            0                   404        1060     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                             [m]       1E+20                 ROHR~*~*~*~ZVEC       101            True               True                   True        239
   40      0           PHR            0                     4        1464     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                          [IDPH]       1E+20                  ROHR~*~*~*~PHR         1           False              False                  False        340
   41      0          PVEC            0                   404        1468     RVEC               4         0      1    245             -1      -1E+20     *     *          ROHR                    *                                                         [bar,a]       1E+20                 ROHR~*~*~*~PVEC       101            True               True                   True        341
   42      0            QM            0                     8        1872     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                          [IDQM]       1E+20                    KNOT~*~~*~QM         2            True               True                  False        442
   43      0            PH            0                     8        1880     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                        [IDPH,4]       1E+20                    KNOT~*~~*~PH         2            True               True                  False        444
   44      0             H            0                     8        1888     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                        [IDPH,6]       1E+20                     KNOT~*~~*~H         2            True               True                  False        446
   45      0          QMAV            0                     4        1896     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                          [IDQM]       1E+20                 ROHR~*~*~*~QMAV         1           False              False                  False        448
   46      0           VAV            0                     4        1900     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                           [m/s]       1E+20                  ROHR~*~*~*~VAV         1           False              False                  False        449
   47      0      LFAKTAKT            0                     8        1904     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                              []       1E+20              KNOT~*~~*~LFAKTAKT         2            True               True                  False        450
   48      0             P            0                     8        1912     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                         [bar,a]       1E+20                     KNOT~*~~*~P         2            True               True                  False        452
   49      0        PH_EIN            0                     8        1920     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                          [IDPH]       1E+20                KNOT~*~~*~PH_EIN         2            True               True                  False        454
   50      0           RHO            0                     8        1928     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                         [kg/m3]       1E+20                   KNOT~*~~*~RHO         2            True               True                  False        456
   51      0             T            0                     8        1936     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                            [°C]       1E+20                     KNOT~*~~*~T         2            True               True                  False        458
   52      0            EH            0                     8        1944     REAL               4         0      1   1269             -1      -1E+20     *                KNOT                    *                                                           [mNN]       1E+20                    KNOT~*~~*~EH         2            True               True                  False        460
   53      0             A            0                     4        1952     REAL               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                           [m/s]       1E+20                    ROHR~*~*~*~A         1           False              False                  False        462
   54      0       IRTRENN            0                     4        1956     INT4               4         0      1   1269             -1      -1E+20     *     *          ROHR                    *                                                              []       1E+20              ROHR~*~*~*~IRTRENN         1           False              False                  False        463'''
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
>>> if os.path.exists(mx.mxsZipFile):                        
...     os.remove(mx.mxsZipFile)
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...    os.remove(mx.h5FileMxsVecs)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> mx1File=os.path.join(path,'testdata\WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1.MX1')
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> mx.setResultsToMxsFile(maxRecords=1)
>>> print("'''{:s}'''".format(repr(mx.df.drop(['ALLG~~~-1~CPUTIME','ALLG~~~-1~USRTIME','ALLG~~~-1~CVERSO'],axis=1)).replace('\\n','\\n   ')))
'''                          ALLG~~~-1~SNAPSHOTTYPE  ALLG~~~-1~EXSTAT  ALLG~~~-1~NFEHL  ALLG~~~-1~NWARN  ALLG~~~-1~NMELD  ALLG~~~-1~NPGREST  ALLG~~~-1~NETZABN  ALLG~~~-1~NKNUV  ALLG~~~-1~MKNUV  ALLG~~~-1~NFVHYUV  ALLG~~~-1~NFVTHUV  ALLG~~~-1~MFVHYUV  ALLG~~~-1~MFVTHUV  ALLG~~~-1~TVMINMAX  ALLG~~~-1~ITERHY  ALLG~~~-1~LFQSV  ALLG~~~-1~JWARN  ALLG~~~-1~NETZABNEXITS  ALLG~~~-1~LINEPACKRATE  ALLG~~~-1~LINEPACKGES  ALLG~~~-1~LINEPACKGEOM  ALLG~~~-1~RHOAV  ALLG~~~-1~TAV  ALLG~~~-1~PAV  ALLG~~~-1~FWVB_DPHMIN  ALLG~~~-1~KNOT_PHMAX  ALLG~~~-1~KNOT_PHMIN  ALLG~~~-1~FWVB_TVLMIN  ALLG~~~-1~NETZBEZ  KNOT~V-L~~5736262931552588702~PH  FWES~R3~V-1~5638756766880678918~W  KNOT~V-K007~~5741235692335544560~DP  WBLZ~WärmeblnzGes~~5262603207038486299~WSPEI  KNOT~R-L~~5356267303828212700~PH  PUMP~R-1~R2~5481331875203087055~N  KNOT~V-1~~5049461676240771430~T  WBLZ~WärmeblnzGes~~5262603207038486299~WES  WBLZ~WärmeblnzGes~~5262603207038486299~WVB  VENT~V-1~V-L~4678923650983295610~QM  WBLZ~WärmeblnzGes~~5262603207038486299~WVERL  KNOT~R3~~5219230031772497417~T  PUMP~R-1~R2~5481331875203087055~BK  PUMP~R-1~R2~5481331875203087055~PE  FWES~R3~V-1~5638756766880678918~TI  FWES~R3~V-1~5638756766880678918~TK  WBLZ~BLNZ1u5u7~~4694700216019268978~WVB  KNOT~PKON-Knoten~~5397990465339071638~QM  KNOT~V-L~~5736262931552588702~RHO  KNOT~V-L~~5736262931552588702~P  KNOT~V-L~~5736262931552588702~H  KNOT~V-L~~5736262931552588702~HMAX_INST  KNOT~V-L~~5736262931552588702~HMIN_INST  KNOT~V-L~~5736262931552588702~PMAX_INST  KNOT~V-L~~5736262931552588702~PMIN_INST  KNOT~V-L~~5736262931552588702~PDAMPF  KNOT~V-K000~~4766681917240867943~RHO  KNOT~V-K000~~4766681917240867943~P  KNOT~V-K000~~4766681917240867943~H  KNOT~V-K000~~4766681917240867943~HMAX_INST  KNOT~V-K000~~4766681917240867943~HMIN_INST  KNOT~V-K000~~4766681917240867943~PMAX_INST  KNOT~V-K000~~4766681917240867943~PMIN_INST  KNOT~V-K000~~4766681917240867943~PDAMPF  KNOT~V-K001~~4756962427318766791~RHO  KNOT~V-K001~~4756962427318766791~P  KNOT~V-K001~~4756962427318766791~H  KNOT~V-K001~~4756962427318766791~HMAX_INST  KNOT~V-K001~~4756962427318766791~HMIN_INST  KNOT~V-K001~~4756962427318766791~PMAX_INST  KNOT~V-K001~~4756962427318766791~PMIN_INST  KNOT~V-K001~~4756962427318766791~PDAMPF  KNOT~V-K002~~4731792362611615619~RHO  KNOT~V-K002~~4731792362611615619~P  KNOT~V-K002~~4731792362611615619~H  KNOT~V-K002~~4731792362611615619~HMAX_INST  KNOT~V-K002~~4731792362611615619~HMIN_INST  KNOT~V-K002~~4731792362611615619~PMAX_INST  KNOT~V-K002~~4731792362611615619~PMIN_INST  KNOT~V-K002~~4731792362611615619~PDAMPF  KNOT~V-K003~~5646671866542823796~RHO  KNOT~V-K003~~5646671866542823796~P  KNOT~V-K003~~5646671866542823796~H  KNOT~V-K003~~5646671866542823796~HMAX_INST  KNOT~V-K003~~5646671866542823796~HMIN_INST  KNOT~V-K003~~5646671866542823796~PMAX_INST  KNOT~V-K003~~5646671866542823796~PMIN_INST  KNOT~V-K003~~5646671866542823796~PDAMPF  KNOT~V-K004~~5370423799772591808~RHO  KNOT~V-K004~~5370423799772591808~P  KNOT~V-K004~~5370423799772591808~H  KNOT~V-K004~~5370423799772591808~HMAX_INST  KNOT~V-K004~~5370423799772591808~HMIN_INST  KNOT~V-K004~~5370423799772591808~PMAX_INST  KNOT~V-K004~~5370423799772591808~PMIN_INST  KNOT~V-K004~~5370423799772591808~PDAMPF  KNOT~V-K005~~5444644492819213978~RHO  KNOT~V-K005~~5444644492819213978~P  KNOT~V-K005~~5444644492819213978~H  KNOT~V-K005~~5444644492819213978~HMAX_INST  KNOT~V-K005~~5444644492819213978~HMIN_INST  KNOT~V-K005~~5444644492819213978~PMAX_INST  KNOT~V-K005~~5444644492819213978~PMIN_INST  KNOT~V-K005~~5444644492819213978~PDAMPF  KNOT~V-K006~~5515313800585145571~RHO  KNOT~V-K006~~5515313800585145571~P  KNOT~V-K006~~5515313800585145571~H  KNOT~V-K006~~5515313800585145571~HMAX_INST  KNOT~V-K006~~5515313800585145571~HMIN_INST  KNOT~V-K006~~5515313800585145571~PMAX_INST  KNOT~V-K006~~5515313800585145571~PMIN_INST  KNOT~V-K006~~5515313800585145571~PDAMPF  KNOT~V-K007~~5741235692335544560~RHO  KNOT~V-K007~~5741235692335544560~P  KNOT~V-K007~~5741235692335544560~H  KNOT~V-K007~~5741235692335544560~HMAX_INST  KNOT~V-K007~~5741235692335544560~HMIN_INST  KNOT~V-K007~~5741235692335544560~PMAX_INST  KNOT~V-K007~~5741235692335544560~PMIN_INST  KNOT~V-K007~~5741235692335544560~PDAMPF  KNOT~R-L~~5356267303828212700~RHO  KNOT~R-L~~5356267303828212700~P  KNOT~R-L~~5356267303828212700~H  KNOT~R-L~~5356267303828212700~HMAX_INST  KNOT~R-L~~5356267303828212700~HMIN_INST  KNOT~R-L~~5356267303828212700~PMAX_INST  KNOT~R-L~~5356267303828212700~PMIN_INST  KNOT~R-L~~5356267303828212700~PDAMPF  KNOT~R-K000~~4979785838440534851~RHO  KNOT~R-K000~~4979785838440534851~P  KNOT~R-K000~~4979785838440534851~H  KNOT~R-K000~~4979785838440534851~HMAX_INST  KNOT~R-K000~~4979785838440534851~HMIN_INST  KNOT~R-K000~~4979785838440534851~PMAX_INST  KNOT~R-K000~~4979785838440534851~PMIN_INST  KNOT~R-K000~~4979785838440534851~PDAMPF  KNOT~R-K001~~4807712987325933680~RHO  KNOT~R-K001~~4807712987325933680~P  KNOT~R-K001~~4807712987325933680~H  KNOT~R-K001~~4807712987325933680~HMAX_INST  KNOT~R-K001~~4807712987325933680~HMIN_INST  KNOT~R-K001~~4807712987325933680~PMAX_INST  KNOT~R-K001~~4807712987325933680~PMIN_INST  KNOT~R-K001~~4807712987325933680~PDAMPF  KNOT~R-K002~~5364712333175450942~RHO  KNOT~R-K002~~5364712333175450942~P  KNOT~R-K002~~5364712333175450942~H  KNOT~R-K002~~5364712333175450942~HMAX_INST  KNOT~R-K002~~5364712333175450942~HMIN_INST  KNOT~R-K002~~5364712333175450942~PMAX_INST  KNOT~R-K002~~5364712333175450942~PMIN_INST  KNOT~R-K002~~5364712333175450942~PDAMPF  KNOT~R-K003~~4891048046264179170~RHO  KNOT~R-K003~~4891048046264179170~P  KNOT~R-K003~~4891048046264179170~H  KNOT~R-K003~~4891048046264179170~HMAX_INST  KNOT~R-K003~~4891048046264179170~HMIN_INST  KNOT~R-K003~~4891048046264179170~PMAX_INST  KNOT~R-K003~~4891048046264179170~PMIN_INST  KNOT~R-K003~~4891048046264179170~PDAMPF  KNOT~R-K004~~4638663808856251977~RHO  KNOT~R-K004~~4638663808856251977~P  KNOT~R-K004~~4638663808856251977~H  KNOT~R-K004~~4638663808856251977~HMAX_INST  KNOT~R-K004~~4638663808856251977~HMIN_INST  KNOT~R-K004~~4638663808856251977~PMAX_INST  KNOT~R-K004~~4638663808856251977~PMIN_INST  KNOT~R-K004~~4638663808856251977~PDAMPF  KNOT~R-K005~~5183147862966701025~RHO  KNOT~R-K005~~5183147862966701025~P  KNOT~R-K005~~5183147862966701025~H  KNOT~R-K005~~5183147862966701025~HMAX_INST  KNOT~R-K005~~5183147862966701025~HMIN_INST  KNOT~R-K005~~5183147862966701025~PMAX_INST  KNOT~R-K005~~5183147862966701025~PMIN_INST  KNOT~R-K005~~5183147862966701025~PDAMPF  KNOT~R-K006~~5543326527366090679~RHO  KNOT~R-K006~~5543326527366090679~P  KNOT~R-K006~~5543326527366090679~H  KNOT~R-K006~~5543326527366090679~HMAX_INST  KNOT~R-K006~~5543326527366090679~HMIN_INST  KNOT~R-K006~~5543326527366090679~PMAX_INST  KNOT~R-K006~~5543326527366090679~PMIN_INST  KNOT~R-K006~~5543326527366090679~PDAMPF  KNOT~R-K007~~5508992300317633799~RHO  KNOT~R-K007~~5508992300317633799~P  KNOT~R-K007~~5508992300317633799~H  KNOT~R-K007~~5508992300317633799~HMAX_INST  KNOT~R-K007~~5508992300317633799~HMIN_INST  KNOT~R-K007~~5508992300317633799~PMAX_INST  KNOT~R-K007~~5508992300317633799~PMIN_INST  KNOT~R-K007~~5508992300317633799~PDAMPF  ROHR~V-L~V-K000~4939422678063487923~VI  ROHR~V-L~V-K000~4939422678063487923~VK  ROHR~V-L~V-K000~4939422678063487923~QMI  ROHR~V-L~V-K000~4939422678063487923~QMK  ROHR~V-K000~V-K001~4984202422877610920~VI  ROHR~V-K000~V-K001~4984202422877610920~VK  ROHR~V-K000~V-K001~4984202422877610920~QMI  ROHR~V-K000~V-K001~4984202422877610920~QMK  ROHR~V-K001~V-K002~4789218195240364437~VI  ROHR~V-K001~V-K002~4789218195240364437~VK  ROHR~V-K001~V-K002~4789218195240364437~QMI  ROHR~V-K001~V-K002~4789218195240364437~QMK  ROHR~V-K002~V-K003~4614949065966596185~VI  ROHR~V-K002~V-K003~4614949065966596185~VK  ROHR~V-K002~V-K003~4614949065966596185~QMI  ROHR~V-K002~V-K003~4614949065966596185~QMK  ROHR~V-K003~V-K004~5037777106796980248~VI  ROHR~V-K003~V-K004~5037777106796980248~VK  ROHR~V-K003~V-K004~5037777106796980248~QMI  ROHR~V-K003~V-K004~5037777106796980248~QMK  ROHR~V-K004~V-K005~4713733238627697042~VI  ROHR~V-K004~V-K005~4713733238627697042~VK  ROHR~V-K004~V-K005~4713733238627697042~QMI  ROHR~V-K004~V-K005~4713733238627697042~QMK  ROHR~V-K005~V-K006~5123819811204259837~VI  ROHR~V-K005~V-K006~5123819811204259837~VK  ROHR~V-K005~V-K006~5123819811204259837~QMI  ROHR~V-K005~V-K006~5123819811204259837~QMK  ROHR~V-K006~V-K007~5620197984230756681~VI  ROHR~V-K006~V-K007~5620197984230756681~VK  ROHR~V-K006~V-K007~5620197984230756681~QMI  ROHR~V-K006~V-K007~5620197984230756681~QMK  ROHR~R-L~R-K000~4769996343148550485~VI  ROHR~R-L~R-K000~4769996343148550485~VK  ROHR~R-L~R-K000~4769996343148550485~QMI  ROHR~R-L~R-K000~4769996343148550485~QMK  ROHR~R-K000~R-K001~5647213228462830353~VI  ROHR~R-K000~R-K001~5647213228462830353~VK  ROHR~R-K000~R-K001~5647213228462830353~QMI  ROHR~R-K000~R-K001~5647213228462830353~QMK  ROHR~R-K001~R-K002~5266224553324203132~VI  ROHR~R-K001~R-K002~5266224553324203132~VK  ROHR~R-K001~R-K002~5266224553324203132~QMI  ROHR~R-K001~R-K002~5266224553324203132~QMK  ROHR~R-K002~R-K003~5379365049009065623~VI  ROHR~R-K002~R-K003~5379365049009065623~VK  ROHR~R-K002~R-K003~5379365049009065623~QMI  ROHR~R-K002~R-K003~5379365049009065623~QMK  ROHR~R-K003~R-K004~4637102239750163477~VI  ROHR~R-K003~R-K004~4637102239750163477~VK  ROHR~R-K003~R-K004~4637102239750163477~QMI  ROHR~R-K003~R-K004~4637102239750163477~QMK  ROHR~R-K004~R-K005~4613782368750024999~VI  ROHR~R-K004~R-K005~4613782368750024999~VK  ROHR~R-K004~R-K005~4613782368750024999~QMI  ROHR~R-K004~R-K005~4613782368750024999~QMK  ROHR~R-K005~R-K006~5611703699850694889~VI  ROHR~R-K005~R-K006~5611703699850694889~VK  ROHR~R-K005~R-K006~5611703699850694889~QMI  ROHR~R-K005~R-K006~5611703699850694889~QMK  ROHR~R-K006~R-K007~4945727430885351042~VI  ROHR~R-K006~R-K007~4945727430885351042~VK  ROHR~R-K006~R-K007~4945727430885351042~QMI  ROHR~R-K006~R-K007~4945727430885351042~QMK  PUMP~R-1~R2~5481331875203087055~RHO  PUMP~R-1~R2~5481331875203087055~M  PUMP~R-1~R2~5481331875203087055~ETA  PUMP~R-1~R2~5481331875203087055~ETAW  PUMP~R-1~R2~5481331875203087055~DP  FWES~*~*~*~IAKTIV  KLAP~*~*~*~IAKTIV  PUMP~*~*~*~IAKTIV
   2004-09-22 08:30:00+00:00                b'STAT'                 0                0                0              132                  0           0.000002                0              0.0                  0                  0                0.0                0.0           89.511505                34              1.0               50                     0.0                     0.0                    0.0               23.109745       976.283203      618.55719       4.144426                1.49995              4.376726                   2.0              87.466125           0.000002                          4.178078                         850.571106                              1.49995                                     -0.208576                          2.000143                        1158.798218                             90.0                                  850.571045                                  799.991089                            23.879057                                     50.788544                       59.396606                            0.345204                            2.876699                           59.396606                                90.0                                479.99353                                  0.000002                         965.700012                         5.178078                         4.178078                                 4.178078                                 4.178078                                 5.178078                                 5.178078                                0.7011                            965.753174                            5.173357                            4.173357                                    4.173357                                    4.173357                                    5.173357                                    5.173357                                 0.698779                            965.795837                            5.132317                            4.132317                                    4.132317                                    4.132317                                    5.132317                                    5.132317                                 0.696916                            965.904907                            5.027433                            4.027433                                    4.027433                                    4.027433                                    5.027433                                    5.027433                                 0.692152                            966.175476                            4.874779                            3.874779                                    3.874779                                    3.874779                                    4.874779                                    4.874779                                 0.680338                            966.244019                            4.853855                            3.853855                                    3.853855                                    3.853855                                    4.853855                                    4.853855                                 0.677345                            966.385315                            4.846632                            3.846632                                    3.846632                                    3.846632                                    4.846632                                    4.846632                                 0.671804                            966.980835                            4.843333                            3.843333                                    3.843333                                    3.843333                                    4.843333                                    4.843333                                 0.650195                            967.373718                            4.841135                            3.841135                                    3.841135                                    3.841135                                    4.841135                                    4.841135                                 0.636366                         984.001709                         3.000143                         2.000143                                 2.000143                                 2.000143                                 3.000143                                 3.000143                              0.193769                             983.97229                            3.005309                            2.005309                                    2.005309                                    2.005309                                    3.005309                                    3.005309                                 0.194299                            983.950134                            3.046598                            2.046598                                    2.046598                                    2.046598                                    3.046598                                    3.046598                                 0.194698                            983.893372                            3.152257                            2.152257                                    2.152257                                    2.152257                                    3.152257                                    3.152257                                  0.19572                            983.288513                            3.306693                            2.306693                                    2.306693                                    2.306693                                    3.306693                                    3.306693                                 0.206936                            983.390381                            3.327914                            2.327914                                    2.327914                                    2.327914                                    3.327914                                    3.327914                                 0.205021                            985.065979                            3.335367                            2.335367                                    2.335367                                    2.335367                                    3.335367                                    3.335367                                 0.175352                            986.362671                            3.338861                            2.338861                                    2.338861                                    2.338861                                    3.338861                                    3.338861                                 0.154993                            986.200012                            3.341185                            2.341185                                    2.341185                                    2.341185                                    3.341185                                    3.341185                                   0.1574                                0.340342                                0.340342                                23.879057                                23.879057                                   0.762394                                   0.762394                                   23.879057                                   23.879057                                   0.762361                                   0.762361                                   23.879057                                   23.879057                                   0.635639                                   0.635639                                   19.912077                                   19.912077                                   0.514563                                   0.514563                                   16.123739                                   16.123739                                   0.287049                                   0.287049                                    8.995258                                    8.995258                                   0.135141                                   0.135141                                    4.235538                                    4.235538                                   0.135058                                   0.135058                                    4.235538                                    4.235538                               -0.334022                               -0.334022                               -23.879055                               -23.879055                                  -0.748295                                  -0.748295                                  -23.879057                                  -23.879057                                  -0.748338                                  -0.748338                                  -23.879057                                  -23.879057                                  -0.624402                                  -0.624402                                  -19.912075                                  -19.912075                                  -0.505555                                  -0.505555                                  -16.123737                                  -16.123737                                  -0.281564                                  -0.281564                                   -8.995257                                   -8.995257                                  -0.132404                                  -0.132404                                   -4.235537                                   -4.235537                                  -0.132426                                  -0.132426                                   -4.235537                                   -4.235537                           984.001709                           6.633071                             0.556937                              0.636801                            2.376726                  0                  0                  0'''
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.41',1,'New',"getMxsVecsFileData")) 
>>> timesReq=[]
>>> timesReq.append(mx.df.index[0])
>>> plotTimeDfs=mx.getMxsVecsFileData(timesReq=timesReq)
>>> len(plotTimeDfs)
1
>>> isinstance(plotTimeDfs[0],pd.core.frame.DataFrame)
True
>>> print("'''{:s}'''".format(repr(plotTimeDfs[0]).replace('\\n','\\n   ')))
'''                                                             ROHR~*~*~*~MVEC                                  ROHR~*~*~*~RHOVEC                                    ROHR~*~*~*~ZVEC                                     ROHR~*~*~*~PHR                                    ROHR~*~*~*~PVEC                                       KNOT~*~~*~DP                                    ROHR~*~*~*~TVEC                                 ROHR~*~*~*~WALTERI                                 ROHR~*~*~*~WALTERK                                        KNOT~*~~*~T                                       KNOT~*~~*~PH                                       FWVB~*~*~*~W                                      FWVB~*~*~*~QM                                    ROHR~*~*~*~QMAV                                     ROHR~*~*~*~VAV ROHR~V-L~V-K000~4939422678063487923~SVEC ROHR~V-L~V-K000~4939422678063487923~PVECMAX_INST ROHR~V-L~V-K000~4939422678063487923~PVECMIN_INST ROHR~V-K000~V-K001~4984202422877610920~SVEC ROHR~V-K000~V-K001~4984202422877610920~PVECMAX_INST ROHR~V-K000~V-K001~4984202422877610920~PVECMIN_INST ROHR~V-K001~V-K002~4789218195240364437~SVEC ROHR~V-K001~V-K002~4789218195240364437~PVECMAX_INST ROHR~V-K001~V-K002~4789218195240364437~PVECMIN_INST ROHR~V-K002~V-K003~4614949065966596185~SVEC ROHR~V-K002~V-K003~4614949065966596185~PVECMAX_INST ROHR~V-K002~V-K003~4614949065966596185~PVECMIN_INST ROHR~V-K003~V-K004~5037777106796980248~SVEC ROHR~V-K003~V-K004~5037777106796980248~PVECMAX_INST ROHR~V-K003~V-K004~5037777106796980248~PVECMIN_INST ROHR~V-K004~V-K005~4713733238627697042~SVEC ROHR~V-K004~V-K005~4713733238627697042~PVECMAX_INST ROHR~V-K004~V-K005~4713733238627697042~PVECMIN_INST ROHR~V-K005~V-K006~5123819811204259837~SVEC ROHR~V-K005~V-K006~5123819811204259837~PVECMAX_INST ROHR~V-K005~V-K006~5123819811204259837~PVECMIN_INST ROHR~V-K006~V-K007~5620197984230756681~SVEC ROHR~V-K006~V-K007~5620197984230756681~PVECMAX_INST ROHR~V-K006~V-K007~5620197984230756681~PVECMIN_INST ROHR~R-L~R-K000~4769996343148550485~SVEC ROHR~R-L~R-K000~4769996343148550485~PVECMAX_INST ROHR~R-L~R-K000~4769996343148550485~PVECMIN_INST ROHR~R-K000~R-K001~5647213228462830353~SVEC ROHR~R-K000~R-K001~5647213228462830353~PVECMAX_INST ROHR~R-K000~R-K001~5647213228462830353~PVECMIN_INST ROHR~R-K001~R-K002~5266224553324203132~SVEC ROHR~R-K001~R-K002~5266224553324203132~PVECMAX_INST ROHR~R-K001~R-K002~5266224553324203132~PVECMIN_INST ROHR~R-K002~R-K003~5379365049009065623~SVEC ROHR~R-K002~R-K003~5379365049009065623~PVECMAX_INST ROHR~R-K002~R-K003~5379365049009065623~PVECMIN_INST ROHR~R-K003~R-K004~4637102239750163477~SVEC ROHR~R-K003~R-K004~4637102239750163477~PVECMAX_INST ROHR~R-K003~R-K004~4637102239750163477~PVECMIN_INST ROHR~R-K004~R-K005~4613782368750024999~SVEC ROHR~R-K004~R-K005~4613782368750024999~PVECMAX_INST ROHR~R-K004~R-K005~4613782368750024999~PVECMIN_INST ROHR~R-K005~R-K006~5611703699850694889~SVEC ROHR~R-K005~R-K006~5611703699850694889~PVECMAX_INST ROHR~R-K005~R-K006~5611703699850694889~PVECMIN_INST ROHR~R-K006~R-K007~4945727430885351042~SVEC ROHR~R-K006~R-K007~4945727430885351042~PVECMAX_INST ROHR~R-K006~R-K007~4945727430885351042~PVECMIN_INST                                   KNOT~*~~*~IAKTIV                                 ROHR~*~*~*~IAKTIV FWVB~*~*~*~IAKTIV VENT~*~*~*~IAKTIV                                   KNOT~*~~*~WALTER
   2004-09-22 08:30:00+00:00  (-2.498682737350464, -2.498682737350464, 5.531...  (985.130615234375, 985.0659790039062, 965.9049...  (20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20....  (0.007445760536938906, 0.15320147573947906, 0....  (3.327914237976074, 3.3353676795959473, 5.0274...  (1.5259402990341187, 1.875176191329956, 2.0857...  (57.1387939453125, 57.26806640625, 89.65847778...  (0.35816168785095215, 0.15507005155086517, 0.2...  (0.2713252604007721, 0.3324766755104065, 0.199...  (60.619232177734375, 89.65847778320312, 89.840...  (2.3279144763946533, 4.027433395385742, 4.1323...  (159.99974060058594, 199.99832153320312, 159.9...  (3.966980457305908, 7.128480434417725, 4.75972...  (-8.995257377624512, 19.912076950073242, -16.1...  (-0.2815546691417694, 0.6355504989624023, -0.5...                  (0.0, 68.5999984741211)          (5.178077697753906, 5.1733574867248535)          (5.178077697753906, 5.1733574867248535)                     (0.0, 76.4000015258789)             (5.173357009887695, 5.132317066192627)              (5.173357009887695, 5.132317066192627)                    (0.0, 195.52999877929688)             (5.132317066192627, 5.027432918548584)              (5.132317066192627, 5.027432918548584)                     (0.0, 405.9599914550781)             (5.027432918548584, 4.874778747558594)              (5.027432918548584, 4.874778747558594)                     (0.0, 83.55000305175781)             (4.874778747558594, 4.853854656219482)              (4.874778747558594, 4.853854656219482)                      (0.0, 88.0199966430664)            (4.853854656219482, 4.8466315269470215)             (4.853854656219482, 4.8466315269470215)                    (0.0, 164.91000366210938)            (4.8466315269470215, 4.843332767486572)             (4.8466315269470215, 4.843332767486572)                     (0.0, 109.7699966430664)             (4.843332767486572, 4.841135025024414)              (4.843332767486572, 4.841135025024414)                  (0.0, 73.41999816894531)          (3.000143051147461, 3.0053086280822754)          (3.000143051147461, 3.0053086280822754)                     (0.0, 76.4000015258789)            (3.0053086280822754, 3.046597957611084)             (3.0053086280822754, 3.046597957611084)                    (0.0, 195.52999877929688)             (3.046597957611084, 3.152257204055786)              (3.046597957611084, 3.152257204055786)                     (0.0, 405.9599914550781)            (3.152257204055786, 3.3066930770874023)             (3.152257204055786, 3.3066930770874023)                     (0.0, 83.55000305175781)            (3.3066930770874023, 3.327914237976074)             (3.3066930770874023, 3.327914237976074)                      (0.0, 88.0199966430664)            (3.327914237976074, 3.3353676795959473)             (3.327914237976074, 3.3353676795959473)                    (0.0, 164.91000366210938)            (3.335367441177368, 3.3388612270355225)             (3.335367441177368, 3.3388612270355225)                     (0.0, 109.7699966430664)            (3.3388612270355225, 3.341184377670288)             (3.3388612270355225, 3.341184377670288)   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)   (0, 0, 0, 0, 0)         (0, 0, 0)  (0.19981449842453003, 0.15507005155086517, 0.0...'''
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
>>> if os.path.exists(mx.h5FileMxsVecs):                        
...    os.remove(mx.h5FileMxsVecs)
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

# ---
# --- PT3S Imports
# ---
# keine

logger = logging.getLogger('PT3S.Mx')  

#Sir3sID
reSir3sID='(\S+)~([\S ]+)~(\S*)~(\S+)~(\S+)'
reSir3sIDcompiled=re.compile(reSir3sID) 
  
def getMicrosecondsFromRefTime(refTime=None,time=None):
    """
    returns microseconds since refTime
    """
    pass
    try:
        timeH5=time-refTime
        h5Key=int(math.floor(timeH5.total_seconds())*1000+timeH5.microseconds)
    except:
        pass
    finally:
        return h5Key

class MxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """
    Class Mx holds the following Dataframes:
    the .MX1-File Definition    self.mx1Df  
    the .MX2-File Definition    self.mx2Df  
    the .MXS-File Data (if any) self.df (Non Vectorchannels Only)
    ---
    the .MXS-File Data: calculations results 
    index:   TIMESTAMP (scenario time)
    columns: Values  
             The following (String-)ID - called Sir3sID - is used as Column-Label:
             OBJTYPE~NAME1~NAME2~OBJTYPE_PK~ATTRTYPE 
             A Sir3sID consists of ~ seperated MX1-File terms.
    ---
    Note the following implicit Effect:
        Calls To setResultsTo... 
        will dump Vectorchannel Data to .vec.h5    
    """
    def __init__(self,mx1File=None,NoH5Read=False,NoMxsRead=False): 
        """
        (re-)initialize the Set with an MX1-File.
        ---
        NoH5Read False:
        If a .h5-File exists _and is newer than an (existing) .MX1-File _and newer than an (existing) .MXS-File:
            The .h5-File is read _instead of the .MX1-File
        NoH5Read True:
            A .h5-File is not read.        
            An existing .h5-File is deleted.    
        ---
        NoMxsRead False:
        If a .MXS-File exists _and is newer (>=) than .MX1-File and .h5-File is not read:
            The .MXS-File is read.  
            The .vec.h5-File is newly created.         
        """
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
            self.mx2File=wD+os.path.sep+base+'.'+'MX2'   
                                                     
            #Determine corresponding .h5 Filename(s)
            self.h5File=wD+os.path.sep+base+'.'+'h5'    # mx1Df, mx2Df, df (Non Vectordata Only)
            self.h5FileMxsVecs=wD+os.path.sep+base+'.'+'vec'+'.'+'h5' # (Vectordata)           
            
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
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an (existing) mx1File {2:s} _and is newer than an (existing) mxsFile {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an (existing) mx1File (mxsFile exists).".format(logStr))   
                            h5Read=True
                        else:                                                             
                            h5Read=False  
                    else:
                        if not NoH5Read:
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an (existing) mx1File {2:s} _and there is no mxsFile like {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an (existing) mx1File.".format(logStr))   
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
                self.__initWithMx1()                    
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

    def __initWithMx1(self):
        """
        (re-)initialize the set with an existing MX1-File:
            self.mx1Df = MX1-File Content           
        self.__parseMx2()    
        self.__buildMxRecordStructUnpackFmtString()  
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

            self.__parseMx2()     
            self.__buildMxRecordStructUnpackFmtString()      
                            
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}mx1File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,self.mx1File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                    
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __parseMx2(self):
        """
        >self.mx2Df
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

    def __buildMxRecordStructUnpackFmtString(self):
        """    
        (re-)builds mxRecordStructFmtString and releated stuff:      
            >self.mxRecordStructFmtString: recordData = struct.unpack(self.mxRecordStructFmtString,record)              
            >self.bytesUnpacked
            >self.mx1Df['unpackIdx']
            >self.idxTIMESTAMP (idx of TIMESTAMP in MX1)
            >self.unpackIdxTIMESTAMP (idx of TIMESTAMP in recordData)
            >self.mxColumnNames=[] (of Non Vector Channels without TIMESTAMP in MX1-Sequence)
            >self.mxColumnNamesVecs=[] (of Vector Channels without TIMESTAMP in MX1-Sequence)
            >self.idxUnpackNonVectorChannels[] (idx in recordData)
            >self.idxUnpackVectorChannels[] (idx in recordData of the 1st ([0]) Element of the Vector)
            >self.idxOfNonVectorChannels[] (idx in MX1 without TIMESTAMP)
            >self.idxVectorChannels[] (idx in MX1)
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

            self.bytesUnpacked = MxRecordLengthFmt - bytesSkipped
            logger.debug("{0:s}Bytes per MX-Record={1:d}. Bytes Unpacked={2:d} (making up {3:06.2f} Bytes-%).".format(logStr,MxRecordLengthMx1,self.bytesUnpacked,self.bytesUnpacked/MxRecordLengthFmt*100))                                                  

            self.mx1Df['unpackIdx']=pd.Series(unpackIdx)
            self.mx1Df['unpackIdx']=self.mx1Df['unpackIdx'].astype('int64')      
            logger.debug("{0:s}mx1Df after generated Column: Shape: {1!s}.".format(logStr,self.mx1Df.shape))        
            
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
                
            # list all Channels with their relevant attributes         
            for idxChannel,idxUnpack in [(idxChannel,idxUnpack)  for idxChannel,idxUnpack in enumerate(self.mx1Df['unpackIdx']) if idxUnpack >=0]:                 
                sir3sID=self.mx1Df['Sir3sID'].iloc[idxChannel]
                idxUnpack=self.mx1Df['unpackIdx'].iloc[idxChannel]
                isVectorChannel=self.mx1Df['isVectorChannel'].iloc[idxChannel]
                isVectorChannelMx2=self.mx1Df['isVectorChannelMx2'].iloc[idxChannel]             
                isVectorChannelMx2Rvec=self.mx1Df['isVectorChannelMx2Rvec'].iloc[idxChannel]
                logger.debug("{:s}Channel-Nr. {:>6d} Sir3sID {:>60s} idxUnpack {:>6d}  isVectorChannel {!s:>6s} isVectorChannelMx2 {!s:>6s} isVectorChannelMx2Rvec {!s:>6s}.".format(logStr
                         ,idxChannel
                         ,sir3sID
                         ,idxUnpack
                         ,isVectorChannel
                         ,isVectorChannelMx2
                         ,isVectorChannelMx2Rvec))  
                                                                                     
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _readMxsFile(self,mxsFilePtr=None,mxsVecsH5StorePtr=None,firstTime=None,maxRecords=None):

        """
        Returns the File-Content (Non Vectordata Only) as df.  
        ---
        It is implied that the calculation results in the File originate from self.mx1File.  
        ---
        TIMESTAMP is used as index.
        ---
        df.index.is_unique 
        might be False 
        because of SIR 3S'
        1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
        ---        
        mxsVecsH5StorePtr is used to update the Vector-Data with mxsFilePtr-Data (MXS-Data): 
            Key:   microseconds from firstTime 
            Value: dfVecs (df with Vectordata for one TIMESTAMP):
                 TIMESTAMP is used as index.
            ---
            the Vectordata for a TIMESTAMP is only written
                when the Key does _not already exist 
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
            firstTime=None    
            
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
                            time = pd.to_datetime(timeISO8601,utc=True) 
                            time_read_after_to_datetime=time.strftime("%Y-%m-%d %H:%M:%S.%f%z") #%z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive)        
                            time = time + pd.to_timedelta('1 hour')   
                            time_read_finally=time.strftime("%Y-%m-%d %H:%M:%S.%f%z")       
                            if recsReadFromFile==0 and firstTime==None:
                                firstTime=time                                                                                                                                                                                                                                                                             
                        except:
                            logStrFinal="{0:s}process record time failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                
                        
                        # process record
                        try:                                                                                                                 
                            # Filter NonVectorChannels and Skip Timestamp (index not value)     
                            values=[recordData[idx] for idx in self.idxUnpackNonVectorChannels]
                            #recordData[0:self.idxTIMESTAMP]
                            #+recordData[self.idxTIMESTAMP+1:]                              
                            
                            # Vecs
                            valuesVecs=[] # all Vectors For One Timestep
                            for idxOf,idxUnpack in zip(self.idxOfVectorChannels,self.idxUnpackVectorChannels):                                                            
                                valueVec=recordData[idxUnpack:idxUnpack+self.mx1Df['NOfItems'].iloc[idxOf]] # one Vector For One Timestep
                                valuesVecs.append(valueVec)                            
                                                                                       
                        except:
                            logStrFinal="{0:s}process record failed. Error.".format(logStr)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)                                                                                                          
                                                  
                        # store record in memory
                        try:                            
                            mxTimes.append(time)                         
                            mxValues.append(values)                           
                        except:
                            logStrFinal="{0:s}store record in memory failed at Time={1!s}. Error.".format(logStr,time_read_finally)
                            logger.error(logStrFinal) 
                            raise MxError(logStrFinal)   
                        
                        h5DumpLog="{:s} NO (no Dumpfile).".format('H5Dump:')
                        if mxsVecsH5StorePtr != None:
                            # store record as df in H5
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
                                        #H5
                                        warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
                                        warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)                          
                                        mxsVecsH5StorePtr.put(str(h5Key),dfVecs)   
                                        h5DumpLog="{:s} Writing DataFrame {:s} with h5Key=/{!s:>20s}".format('H5Dump:','dfVecs',h5Key) 
                                                              
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
                                     
            logger.debug("{0:s}File finished: Records read={1:d}. Last Time read={2!s}. MB read={3:07.2f}. MB unpacked={4:07.2f} (making up {5:06.2f} %). ".format(logStr                                                                                                                                         
                                                                                    ,recsReadFromFile
                                                                                    ,time_read_finally
                                                                                    ,recsReadFromFile*MxRecordLength/pow(10,6)
                                                                                    ,recsReadFromFile*self.bytesUnpacked/pow(10,6)
                                                                                    ,self.bytesUnpacked/MxRecordLength*100
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
            return df

    def _checkMxsVecsFile(self,fullCheck=False):
        """
        returns (firstTime,lastTime,NOfTimes)
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:         
            with pd.HDFStore(self.h5FileMxsVecs) as mxsVecsH5Store: 
                                                                                                                                               
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
        
    def __handleMxsVecFileDeletion(self,mxsFile=None,NewH5Vec=False):
        """
        File .vec.h5 is deleted if 
            existing _and older than mxsFile
            or NewH5Vec                               
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
        
            # .vec.h5 Handling 
            if os.path.exists(self.h5FileMxsVecs):      

                if NewH5Vec:
                    logger.debug("{:s}Delete H5VecDump because NewH5Vec ...".format(logStr,self.h5FileMxsVecs)) 
                    os.remove(self.h5FileMxsVecs)   
                else:
                    if os.path.exists(mxsFile):                         
                        mxsFileTime=os.path.getmtime(mxsFile) 
                    else:
                        mxsFileTime=0
                    mxsH5FileTime=os.path.getmtime(self.h5FileMxsVecs)

                    if mxsFileTime>mxsH5FileTime:
                        # die zu lesende Mxs ist neuer als der Dump: Dump loeschen              
                        logger.debug("{:s}Delete H5VecDump because Mxs {:s} To Read is newer than H5VecDump {:s} ...".format(logStr,mxsFile,self.h5FileMxsVecs))                             
                        os.remove(self.h5FileMxsVecs)      
                        
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                      
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                                       
            
    def setResultsToMxsFile(self,mxsFile=None,add=False,NewH5Vec=False,maxRecords=None):
        """
        Sets or adds the MXS-Results to self.df.          
        ---
        Implicit specified is a MXS-File .MXS in the same directory as the MX1-File .MX1.  
        ---
        It is implied that the calculation results in the MXS-File originate from self.mx1File.        
        ---
        TIMESTAMP is used as index.
        ---
        self.df.index.is_unique 
        will be True 
            because in SIR 3S'
            1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
            +TIME       is dropped                                
            +TMIN/TMAX are dropped   
            ---
            and because resulting overlapping TIMESTAMPs due to intersections (add=True) are also dropped      
        ---        
        Note the following implicit Effect:
            File .vec.h5 is updated with mxsFile-Data                  
            ---
            File .vec.h5 is deleted if 
                existing _and older than mxsFile
                or NewH5Vec                                   
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 

            # Mxs specification 
            if mxsFile == None:
                logger.debug("{0:s}Mxs: Implicit specified.".format(logStr))                                
                mxsFile=self.mxsFile
            
            # .vec.h5 Handling 
            self.__handleMxsVecFileDeletion(mxsFile=mxsFile,NewH5Vec=NewH5Vec)
              
            mxsVecH5Store=pd.HDFStore(self.h5FileMxsVecs) 
                                                                                      
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
                dfMxs=self._readMxsFile(f,mxsVecsH5StorePtr=mxsVecH5Store,firstTime=firstTime,maxRecords=maxRecords)                                     
                           
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
                                           
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}mxsFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                       
        finally:
            mxsVecH5Store.close()
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def setResultsToMxsZipFile(self,mxsZipFile=None,add=False,NewH5Vec=False,maxRecords=None):
        """
        Sets or adds the MXS-Results in the Zip to self.df.                 
        ---
        Implicit specified is a Zip-File .ZIP in the same directory as the MX1-File .MX1.  
        ---
        It is implied that all calculation results in the Zip-File originate from self.mx1File.   
        ---
        The Mxs-Files in the Zip-File are read in alphabetical order.    
        ---
        TIMESTAMP is used as index.
        ---
        self.df.index.is_unique 
        will be True 
            because in SIR 3S' 
            1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  
            +TIME       is  dropped                                
            +TMIN/TMAX  are dropped 
            ---
            and because resulting overlapping TIMESTAMPs due to intersections between the Zip-MXS (or due to add=True) are also dropped
        ---        
        Note the following implicit Effect:
            File .vec.h5 is updated with mxsZipFile-Data
            see also __handleMxsVecFileDeletion       
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
            self.__handleMxsVecFileDeletion(mxsFile=mxsZipFile,NewH5Vec=NewH5Vec)
                
            mxsVecH5Store=pd.HDFStore(self.h5FileMxsVecs) 
                                                                                      
            if isinstance(self.df,pd.core.frame.DataFrame):   
                firstTime=self.df.index[0]
            else:
                firstTime=None
          
            # Zip reading ...              
            recsReadFromZip=0            
            dfZip=None
            for mxsFileName in sorted(z.namelist()):  
                # Mxs reading ...                        
                with z.open(mxsFileName,'r') as f: 
                    logger.debug("{0:s}Zip: {1:s}: {2:s} reading ...".format(logStr,mxsZipFile,mxsFileName))       
                    dfMxs=self._readMxsFile(f,mxsVecsH5StorePtr=mxsVecH5Store,firstTime=firstTime,maxRecords=maxRecords)   

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
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                 

    def ToH5(self,h5File=None):
        """
        Stores the Dataframes 
        mx1Df h5Key: .../MX1 
        mx2Df h5Key: .../MX2 
        df    h5Key: .../MXS  
        in a .h5-File.      
        ---
        If the .h5-File exists it is !DELETED! before.          
        ---
        Implicit specified is a .h5-File in the same directory as the .mx1-File.  
        ---
        If mx1Df is not defined mx1Df is not stored.
        If df    is not defined    df is not stored.
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
        """
        The h5File is read
        and the following Dataframes
        self.mx1Df (h5Key: .../MX1) 
        self.mx2Df (h5Key: .../MX1) 
        self.df    (h5Key: .../MXS) 
        are overwritten with the Dataframes in the h5File if any.     
        ---
        /MX1 in h5File:
        mxRecordStructUnpackFmtString and releated stuff is (re-)builded
        /MX2 in h5File: Check if .vec.h5 corresponds
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))  
        
        try:

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
                        self.__buildMxRecordStructUnpackFmtString()      
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
        returrns a list of dfs with MxsVecsFileData
        key in df: TIMESTAMP; one TIME per df 
        timesReq: list of requested TIMESTAMPs
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
           
            mxsVecsDfs=None

            if os.path.exists(self.h5FileMxsVecs):
                pass
            else:
                logStrFinal="{:s}{:s}: Not existing!".format(logStr,self.h5FileMxsVecs)
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
            with pd.HDFStore(self.h5FileMxsVecs) as h5Store:
                #available
                h5KeysAvailable=sorted(h5Store.keys())      
                for idx,h5Key in enumerate(h5KeysRequested):
                    if h5Key in h5KeysAvailable:
                        mxsVecsDfs.append(h5Store[h5Key])
                    else:
                        logger.debug("{:s}{:s}: Key {:s} (Time {:s}) not available.".format(logStr,self.h5FileMxsVecs,h5Key,timesReq[idx]))
                                                        
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
        """
        Dumps Data (self.df) in MXS-Format to mxsDumpFile (for testing purposes). 
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
                        with pd.HDFStore(self.h5FileMxsVecs) as mxsVecsH5Store: 
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
