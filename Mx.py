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
>>> # ---
>>> # dotResolution
>>> # ---
>>> # globs={'dotResolution':''}
>>> try:
...     dummy= dotResolution
... except NameError:
...     dotResolution='' 
>>> import zipfile
>>> import pandas as pd
>>> # ---
>>> # Init
>>> # ---
>>> h5File=os.path.join(path,os.path.join(testDir,'OneLPipe.h5')) 
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDOneLPipe\B1\V0\BZ1\M-1-0-1'+dotResolution+'.MX1')) 
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
(12, 8)
>>> # ---
>>> # Read Dump
>>> # ---
>>> logger.debug("{0:s}: Read Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsFile(mxsFile=mxsDumpFile)
12
>>> with zipfile.ZipFile(mx.mxsZipFile,'w') as myzip:
...     myzip.write(mx.mxsFile)  
...     myzip.write(mxsDumpFile)  
>>> # ---
>>> # Read Zip with Orig and Dump
>>> # ---
>>> logger.debug("{0:s}: Read Zip with Orig and Dump".format('DOCTEST')) 
>>> mx.setResultsToMxsZipFile()
12
>>> (rows,cols)=mx.df.shape
>>> rows
12
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
>>> sir3sIdTimestamp=mx.mx1Df['Sir3sID'].iloc[mx.idxTIMESTAMP]
>>> mx.mx1Df['Sir3sID'][mx.mx1Df['Sir3sID']==sir3sIdTimestamp].index[0]   
0
>>> mx.mx1Df['unpackIdx'][mx.mx1Df['Sir3sID']==sir3sIdTimestamp].iloc[0]
0
>>> (rows,cols)=mx.df.shape
>>> rows
12
>>> isinstance(mx.df.index[0],pd.tslib.Timestamp)
True
>>> str(mx.df.index[0])
'2018-03-03 00:00:00+00:00'
>>> sir3sId=mx.mx1Df['Sir3sID'][mx.mx1Df['Sir3sID'].str.contains('KNOT~\S*~~5642914844465475844~QM')].iloc[0] #KNOT~I~~5642914844465475844~QM
>>> ts=mx.df[sir3sId]
>>> isinstance(ts,pd.core.series.Series)
True
>>> "{:06.2f}".format(round(ts.iloc[0],2))
'176.71'
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.31',1,'New','_checkMxsVecsFile: (...,fullCheck=False,...)')) 
>>> mx._checkMxsVecsFile()
(Timestamp('2018-03-03 00:00:00+0000', tz='UTC'), Timestamp('2018-03-03 00:00:11+0000', tz='UTC'), 12)
>>> mx._checkMxsVecsFile(fullCheck=True)
(Timestamp('2018-03-03 00:00:00+0000', tz='UTC'), Timestamp('2018-03-03 00:00:11+0000', tz='UTC'), 12)
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
>>> print(mx._getMx1DfAsOneString().replace('\\n','\\n '))
ATTRTYPE  DATALENGTH DATATYPE  DATATYPELENGTH  FLAGS OBJTYPE           OBJTYPE_PK                TITLE    UNIT
      PH           4     REAL               4   1265    KNOT  5289899964753656852                Druck   [bar]
      QM           4     REAL               4   1265    KNOT  5289899964753656852  Externer Durchfluss  [m3/h]
      PH           4     REAL               4   1265    KNOT  5642914844465475844                Druck   [bar]
      QM           4     REAL               4   1265    KNOT  5642914844465475844  Externer Durchfluss  [m3/h]
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
>>> print(mx._getDfAsOneString())
                          KNOT~~~5289899964753656852~PH KNOT~~~5289899964753656852~QM KNOT~~~5642914844465475844~PH KNOT~~~5642914844465475844~QM
2018-03-03 00:00:00+00:00                           0.0                        -176.7                           4.2                         176.7
2018-03-03 00:00:01+00:00                           0.0                        -176.7                           4.2                         176.7
2018-03-03 00:00:02+00:00                           0.0                        -176.7                           4.2                         176.7
2018-03-03 00:00:03+00:00                           0.0                        -176.7                           4.2                         176.7
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
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1'+dotResolution+'.MX1')) 
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
>>> print(mx._getDfAsOneString())
                          KNOT~~~5356267303828212700~PH KNOT~~~5397990465339071638~QM KNOT~~~5736262931552588702~PH
2004-09-22 08:30:00+00:00                           2.0                           0.0                           4.1
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.41',1,'New',"getMxsVecsFileData")) 
>>> timesReq=[]
>>> timesReq.append(mx.df.index[0])
>>> plotTimeDfs=mx.getMxsVecsFileData(timesReq=timesReq)
>>> len(plotTimeDfs)
1
>>> isinstance(plotTimeDfs[0],pd.core.frame.DataFrame)
True
>>> print(mx._getDfVecAsOneString(df=plotTimeDfs[0],regex='KNOT~\S*~\S*~\S*~T$'))
                           KNOT~~~~T
2004-09-22 08:30:00+00:00      60.00
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
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDTinyWDN\B1\V0\BZ1\M-1-0-1'+dotResolution+'.MX1'))
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> print(mx._getMx1DfAsOneString().replace('\\n','\\n '))
ATTRTYPE  DATALENGTH DATATYPE  DATATYPELENGTH  FLAGS OBJTYPE           OBJTYPE_PK TITLE    UNIT
      PH           4     REAL               4      1    KNOT  4711309381204507891         [bar]
      PH           4     REAL               4      1    KNOT  5179406559406617933         [bar]
      QM           4     REAL               4      1    KNOT  5179406559406617933        [m3/h]
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
>>> print(mx._getDfAsOneString())
                          KNOT~~~4711309381204507891~PH KNOT~~~5179406559406617933~PH KNOT~~~5179406559406617933~QM
2002-05-22 16:16:16+00:00                           1.0                           3.0                         140.0
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
        * and base.vec.h5-File is written implicitely while (implicit or explicit calls to) setResultsTo...() 
        * and is deleted explicitely (mx1File,NoH5Read=True) or implicitely (because i.e. too old) 

    Args:
        * mx1File (str): base.MX1-File (an XML-File) (base.1.MX1-File from 90-10 on)

        * NoH5Read (bool): 
            False (default - use this to profit from previous reads finalized with ToH5()): 
                * If a base.h5-File 
                    * exists 
                    * and is newer (>) than an .MX1-File (base.1.Mx1-File from 90-10 on) 
                    * and is newer (>) than an .MXS-File (base.1.MXS-File from 90-10 on):

                        * The base.h5-File is read instead of the .MX1-File.                        

            True (use this for a fresh start):             
                * An base.h5-File is deleted if existing.  
                * The .MX1-File is read. (base.1.Mx1-File from 90-10 on)
                * The .vec.h5-File is newly created in case of an .MXS-File read. (.1.MXS-File read from 90-10 on)       

        * NoMxsRead (bool):
            True:
                * a .MXS-File is not read (.1.MXS-File read from 90-10 on)
                * a .vec.h5-File is not touched

            False (default):
                * If a .MXS-File (.1.Mx1-File from 90-10 on)
                    * exists
                    * and is newer (>=) than .MX1-File (.1.Mx1-File from 90-10 on)
                    * and base.h5-File is not read:

                        * The .MXS-File is read.  (.1.MXS-File is read from 90-10 on)             
                        * NoH5Read=True will delete .vec.h5-File.

    Attributes:
        * fileNames
            * .mx1File: base.MX1-File (.1.Mx1-File from 90-10 on) 

            derived from mx1File
                * .mx2File: base.MX2-File 
                * .mxsFile: base.MXS-File (.1.MXS-File from 90-10 on)
                * .mxsZipFile base.ZIP
                * .h5File: base.h5-File
                * .h5FileVecs: base.vec.h5-File

        * .mxRecordStructFmtString

        * dataFrames
            * .mx1Df  
            * .mx2Df 
            * .df
                * the .MXS-File(s) Content  (.1.MXS-File from 90-10 on)
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
                    self.mx1File=mx1File  # base.MX1-File (an XML-File) (base.1.MX1-File from 90-10 on)
            else:
                    logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,mx1File)                                 
                    raise MxError(logStrFinal)     

            # determine base
            (wD,fileName)=os.path.split(self.mx1File)
            (base,ext)=os.path.splitext(fileName)
            (base,dotResolution)=os.path.splitext(base) # dotResolution: '.1' from 90-10 on; '' before

            #Determine corresponding .MX2 Filename
            self.mx2File=wD+os.path.sep+base+'.'+'MX2'   
                                                     
            #Determine corresponding .h5 Filename(s)
            self.h5File=wD+os.path.sep+base+'.'+'h5'    # mx1Df, mx2Df, df (non Vectordata only)
            self.h5FileVecs=wD+os.path.sep+base+'.'+'vec'+'.'+'h5' # (Vectordata)           
            
            #Determine corresponding .MXS Filename
            self.mxsFile=wD+os.path.sep+base+dotResolution+'.'+'MXS'  
          
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
            # to handle 90-09 TIMESTAMP UTC offset:
            self.timeDeltaReadOffset=None
            self.timeDeltaWriteOffset=None

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

            pd.set_option('display.max_columns',None)
            pd.set_option('display.max_rows',None)
            pd.set_option('display.max_colwidth',666666)   
            pd.set_option('display.width',666666666)
            logger.debug("{0:s}\n{1!s}".format(logStr
                                             ,repr(self.mx1Df)#.replace('\\n','\\n   ')
                                             ))    
                                                                            
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
            * .idxCVERSO (idx of CVERSO in MX1) 
            * .unpackIdxCVERSO (idx of CVERSO in recordData)            
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
            # CVERSO
            self.idxCVERSO=self.mx1Df['Sir3sID'][
                self.mx1Df['ATTRTYPE']=='CVERSO'
                ].index[0]           
            self.unpackIdxCVERSO=self.mx1Df['unpackIdx'][               
                self.mx1Df['ATTRTYPE']=='CVERSO'
                ].iloc[0]    
            
            # TIMESTAMP
            self.idxTIMESTAMP=self.mx1Df['Sir3sID'][                
                self.mx1Df['ATTRTYPE']=='TIMESTAMP'
                ].index[0]           
            self.unpackIdxTIMESTAMP=self.mx1Df['unpackIdx'][
                self.mx1Df['ATTRTYPE']=='TIMESTAMP'
                ].iloc[0]    
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
            sir3sIdTimestamp=self.mx1Df['Sir3sID'].iloc[self.idxTIMESTAMP]
            idxTIMESTAMP=self.mxColumnNames.index(sir3sIdTimestamp)#'ALLG~~~-1~TIMESTAMP')
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
                * else:
                    * caller sets firstTime - in general the youngest TIMESTAMP in the df to be extended                   

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
                    * can be all negative if firstTime (in general the youngest TIMESTAMP in the df to be extended) is older than the oldest TIMESTAMP in the .MXS-File

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

                        # process CVERSO
                        if self.timeDeltaReadOffset==None:
                            try:
                                cVerso = recordData[self.unpackIdxCVERSO].decode('utf-8') # 'SIR 3S 90-11-00-02 3S Consult, 30827 Garbsen - 02.09.2018 09:47 - M-1-0-1       '
                                logger.debug("{0:s}CVERSO: {1!s}.".format(logStr,cVerso))
                                matchExp='SIR 3S (\d{2})-(\d{2})-(\d{2})-(\d{2})'
                                mo=re.search(matchExp,cVerso)
                                subVersion=int(mo.group(2))
                            
                                if subVersion < 10:
                                    self.timeDeltaReadOffset=pd.to_timedelta('1 hour') # the MX-TIMESTAMPS contain +01:00
                                    self.timeDeltaWriteOffset='+01:00' # this has to be written 
                                else:
                                    self.timeDeltaReadOffset=pd.to_timedelta('0 seconds') # the MX-TIMESTAMPS contain no UTC offset information  
                                    self.timeDeltaWriteOffset=''
                                                                                                                                                                                                                                                           
                            except Exception as e:                           
                                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                    
                                logger.error(logStrFinal) 
                                raise MxError(logStrFinal) 

                        # process record time
                        try:
                            timeISO8601 = recordData[self.unpackIdxTIMESTAMP] 
                            #  09                               b'2018-03-03 00:00:00.000000+01:00'
                                # d.h. die Version schreibt offenbar ein UTC offset 
                            #>=10 (11 checked):                 b'2018-03-03 00:00:00.000000      '                 
                                # d.h. die Version schreibt kein UTC offset          
                            time = pd.to_datetime(timeISO8601.decode(),utc=True) # 3.6
                            #  09               numpy.datetime64('2018-03-02T23:00:00.000000000') # in die errechnete Zeit geht das UTC offset ein 
                            #>=10 (11 checked): numpy.datetime64('2018-03-03T00:00:00.000000000')                            

                            time_read_after_to_datetime=time.strftime("%Y-%m-%d %H:%M:%S.%f%z") #%z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive) # %z delivers always +0000 ?!   
                            #  09               2018-03-02 23:00:00.000000+0000 
                            #>=10 (11 checked): 2018-03-03 00:00:00.000000+0000 

                            time = time + self.timeDeltaReadOffset 
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
                        msForTime=getMicrosecondsFromRefTime(firstTime,time)
                        if msForTime != keys[idx]:
                            logger.debug("{:s}TimeNr. {:>6d} with key {!s:>20s} and TIMESTAMP {!s:s}: ms (>key) NOT ms {!s:>20s} for TIMESTAMP.".format(logStr,idx+1,key,time,msForTime))  
                        if idx>0:
                            if time <= lastTime:
                                 logger.debug("{:s}TimeNr. {:>6d} with key {!s:>20s} and TIMESTAMP {!s:s}: NOT > lastTimeRead {!s:s}.".format(logStr,idx+1,key,time,lastTime))  


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
            
            #logger.debug("{0:s}\n{1!s}".format(logStr
            #                                 ,repr(self.df)#.replace('\\n','\\n   ')
            #                                 ))                                              

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
                                                                    
            #logger.debug("{0:s}\n{1!s}".format(logStr
            #                                 ,repr(self.df)#.replace('\\n','\\n   ')
            #                                 ))               
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
                * None, if none of the req. TIMESTAMPs was found                

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
                # ueber alle verlangten keys
                h5KeysAvailable=sorted(h5Store.keys())      
                for idx,h5KeyReq in enumerate(h5KeysRequested):
                    if h5KeyReq in h5KeysAvailable:
                        df=h5Store[h5KeyReq]
                        mxsVecsDfs.append(df)
                        if df.index[0]!=timesReq[idx]:
                            logger.debug("{:s}{:s}: Key {:s} available - BUT TimeReq {:s} matched not H5-Time for this Key which is: {:s}.".format(logStr,self.h5FileVecs,h5KeyReq,str(timesReq[idx]),str(df.index[0])))                        

                    else:
                        logger.debug("{:s}{:s}: Key {:s} (Time {:s}) not available.".format(logStr,self.h5FileVecs,h5KeyReq,str(timesReq[idx])))
                        # ueber alle vorhandenen Keys
                        for h5KeyAva in h5KeysAvailable:                            
                            df=h5Store[h5KeyAva]
                            timeStamp=df.index[0]
                            logger.debug("{:s}{:s}: KeyAva {:s} (Time {:s}).".format(logStr,self.h5FileVecs,h5KeyAva,str(timeStamp)))                            
                            if timeStamp==timesReq[idx]:
                                mxsVecsDfs.append(df)
                                logger.debug("{:s}{:s}: Key {:s} matched Time {:s}.".format(logStr,self.h5FileVecs,h5KeyAva,str(timesReq[idx])))                        
                                break  
                        else:                            
                            logger.debug("{:s}{:s}: Key {:s} (Time {:s}) also as TIMESTAMP not available.".format(logStr,self.h5FileVecs,h5KeyReq,str(timesReq[idx])))
                                                        
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

        Returns:
            * (TimeStampsDumped, TimeStampsFoundInH5)
                * normally:  TimeStampsDumped=TimeStampsFoundInH5
                * if TimesStamps in self.df are manipulated ...
                * ... the H5-Content remains unchanged
                * in effect the H5-Content can be different from self.df-Content ...
                * während in self.df die Zeiten (Index) immer geordnet und voneinander verschieden sind
                * sind beim H5-Content nur die Keys voneinander verschieden
                * um pruefen zu koennen, ob alle Zeiten in self.df im H5-Content auch gefunden wurden, wird TimeStampsFoundInH5 mit ausgegeben
                * gedumped werden immer alle Zeiten aus self.df 
                * - fuer jede im H5-Content nicht gefundene Zeit wird das Ergebnis der zuletzt zuvor gefundenen Zeit ausgegeben  
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
                TimeStampsDumped=0
                TimeStampsFoundInH5=0
                for idx,row in enumerate(self.df.itertuples(index=False)):
                    
                    # TIMESTAMP herrichten
                    try:                        
                        scenTime=self.df.index[idx]                                                                                                                                               
                        scenTimeStr=scenTime.strftime("%Y-%m-%d %H:%M:%S.%f"+self.timeDeltaWriteOffset) 
                        scenTimeStrBytes=scenTimeStr.encode('utf-8')
                    except:
                        logStrFinal="{0:s}h5File: {1!s}: TIMESTAMP herrichten: Error.".format(logStr,mxsDumpFile)
                        logger.error(logStrFinal) 
                        raise MxError(logStrFinal)    

                    # Values herrichten und Satz schreiben
                    try:    
                        # valuesNonVec
                        valuesNonVec=list(row)

                        # valuesVec  
                        try:
                            # h5-Satz suchen                                            
                            timesReq=[]
                            timesReq.append(scenTime)
                            dfVecs=self.getMxsVecsFileData(timesReq=timesReq)[0]
                        except  Exception as e:
                            logStrFinal="{:s}mxsDumpFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsDumpFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                            logger.debug(logStrFinal)   
                            logger.debug("{:s}mxsDumpFile: {:s}: TimeNr. {:>6d} with TIMESTAMP: {:s}: Not found in H5-Content. Using H5-Content read before.".format(logStr,mxsDumpFile,TimeStampsDumped,scenTimeStr))    
                            dfVecs=dfVecsOld                            
                        else:
                            dfVecsOld=dfVecs
                            TimeStampsFoundInH5=TimeStampsFoundInH5+1
                        finally:
                            for row in dfVecs.itertuples(index=False):
                                # one row only
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
                        logger.debug("{:s}mxsDumpFile: {:s}: TimeNr. {:>6d} with TIMESTAMP: {:s}: Dumped.".format(logStr,mxsDumpFile,TimeStampsDumped,scenTimeStr))    
                        TimeStampsDumped=TimeStampsDumped+1                                                                 

                    except Exception as e:                        
                        logStrFinal="{:s}mxsDumpFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsDumpFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                        logger.error(logStrFinal)                        
                        raise MxError(logStrFinal)                                                                                          
                                                                                    
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}mxsDumpFile: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,mxsDumpFile,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                                  
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return(TimeStampsDumped, TimeStampsFoundInH5)

    def _getMx1DfAsOneString(self,regex='KNOT~\S*~\S*~\d+~[P|Q]{1}[H|M]{1}$'):
        """Returns .mx1Df-Content as one String (for Doctest-Purposes).
           
        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        mx1DfContentAsOneString=None
        try:     
            dfFiltered=self.mx1Df.loc[
                (~self.mx1Df['OBJTYPE'].isin(['ALLG'])) 
                & 
                (self.mx1Df['Sir3sID'].str.match(regex)) 
                ]
            dfDropped=dfFiltered.drop(['NAME1','NAME2','NAME3','LINKED_CHANNEL','Sir3sID','DATAOFFSET','unpackIdx','UPPER_LIMIT','LOWER_LIMIT','ADDEND','FACTOR','DEVIATION','NOfItems','isVectorChannel','isVectorChannelMx2','isVectorChannelMx2Rvec','OPCITEM_ID','CLIENT_ID','CLIENT_FLAGS'],axis=1)
            dfSorted=dfDropped.sort_values(['OBJTYPE_PK','ATTRTYPE']).reset_index(drop=True)
            mx1DfContentAsOneString=dfSorted.to_string(index=False)                                                                            
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return mx1DfContentAsOneString

    def _getDfAsOneString(self,regex='KNOT~\S*~\S*~\d+~[P|Q]{1}[H|M]{1}$'):
        """Returns .df-Content as one String (for Doctest-Purposes).
           
        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        dfContentAsOneString=None
        try:     
            dfFiltered=self.df.filter(regex=regex,axis=1)

            newColNames={}
            formatters={}
            matchexp='(\S+)~(\S*)~(\S*)~(\d+)~(\S+)'
            f=lambda x: "{:9.1f}".format(x)
            for colName in dfFiltered.columns.tolist():
                mo=re.match(matchexp,colName)
                colNameNew=mo.group(1)+'~~~'+mo.group(4)+'~'+mo.group(5)
                newColNames[colName]=colNameNew
                formatters[colNameNew]=f
            dfRenamed=dfFiltered.rename(newColNames,axis='columns')

            dfSorted=dfRenamed.reindex_axis(sorted(dfRenamed.columns), axis=1)
            
            dfContentAsOneString=dfSorted.to_string(formatters=formatters)                                                                            
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return dfContentAsOneString

    def _getDfVecAsOneString(self,df=None,regex='KNOT~\S*~\S*~\S*~[P|Q]{1}[H|M]{1}$'):
        """Returns dfVec-Content as one String (for Doctest-Purposes).
           
        Raises:
            MxError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        dfContentAsOneString=None
        try:     
            dfFiltered=df.filter(regex=regex,axis=1)

            newColNames={}
            formatters={}
            matchexp='(\S+)~(\S*)~(\S*)~(\S*)~(\S+)'
            f=lambda x: "{:9.2f}".format(x[0])
            for colName in dfFiltered.columns.tolist():
                mo=re.match(matchexp,colName)
                colNameNew=mo.group(1)+'~~~~'+mo.group(5)
                newColNames[colName]=colNameNew
                formatters[colNameNew]=f
            dfRenamed=dfFiltered.rename(newColNames,axis='columns')

            dfSorted=dfRenamed.reindex_axis(sorted(dfRenamed.columns), axis=1)
            
            dfContentAsOneString=dfSorted.to_string(formatters=formatters)                                                                            
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return dfContentAsOneString

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
        parser.add_argument('--testDir',type=str,default='testdata',help="value for global 'testDir' i.e. testdata")
        parser.add_argument('--dotResolution',type=str,default='',help="value for global 'dotResolution' i.e. .1")        
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        suite=doctest.DocTestSuite(globs={'testDir':args.testDir,'dotResolution':args.dotResolution})  
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
