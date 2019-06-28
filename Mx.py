"""
SIR 3S MX-Interface (short: MX)

    MX is a file based, channel-oriented interface for SIR 3S' calculation results.
    
    This module contains stuff to utilize SIR 3S' MX calculation results in pure Python.  

    SIR 3S MX calculation results overview:

        * Binary .MXS-Files contain the SIR 3S calculations results. 
        * A Model calculation run creates at least one .MXS-File.
        * There is one .MX1-File (an XML-File) for the corresponding .MXS-File(s).    
        * This .MX1-File defines (in XML) a sequence of MX-Channels in the corresponding .MXS-File(s). 
        * And - as a result - the Byte-Layout of a single Record in the corresponding .MXS-File(s).
        * A single Record is called a MX3-Record. .MXS-File(s) contain a sequence of MX3-Records.
        * A MX3-Record contains calculation results for one TIMESTAMP. TIMESTAMP ist Scenariotime.
        * A corresponding .MX3-File contains one MX3-Record - the last Scenariotime calculated.
        * Summary:
        * .MXS-File(s): MX3-Records: MX-Channels 
        * MX3-Record Byte-Layout (the MX-Channels) defined in corresponding .MX1-File.

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
...       logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ',"path = '.' because __file__ not defined and: "," from Mx import Mx")) 
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
>>> mx.delFiles()
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
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
>>> mx.delFiles()
>>> if os.path.exists(mx.mxsZipFile):                        
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):                        
...    os.remove(mxsDumpFile)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDLocalHeatingNetwork\B1\V0\BZ1\M-1-0-1'+dotResolution+'.MX1')) 
>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
>>> # ---
>>> # Clean Up LocalHeatingNetwork
>>> # ---
>>> mx.delFiles()
>>> if os.path.exists(mx.mxsZipFile):         
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):           
...    os.remove(mxsDumpFile)
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
>>> mx.delFiles()
>>> if os.path.exists(mx.mxsZipFile):         
...    os.remove(mx.mxsZipFile)
>>> mxsDumpFile=mx.mxsFile+'.dump'
>>> if os.path.exists(mxsDumpFile):           
...    os.remove(mxsDumpFile)
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
>>> mx.delFiles()
>>> # ---
>>> # GPipe
>>> # ---
>>> mx1File=os.path.join(path,os.path.join(testDir,'WDGPipe\B1\V0\BZ1\M-1-0-1'+dotResolution+'.MX1'))
>>> mx=Mx(mx1File=mx1File)
>>> plotTimeDfs=mx.getMxsVecsFileData()
>>> len(plotTimeDfs[0]['ROHR~*~*~*~PVEC'].iloc[0]) == mx.mx2Df[mx.mx2Df['AttrType'].str.contains('N_OF_POINTS')].iloc[0].Data[0]
True
>>> plotTimeDfs[0]['ROHR~*~*~*~PVEC'].iloc[0][0]
41.0
>>> # ---
>>> # Clean Up GPipe
>>> # ---
>>> mx.delFiles()
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
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

# ---
# --- main Imports
# ---
import argparse
import unittest
import doctest

# Sir3sID regExp Example
reSir3sIDSep='~'
reSir3sID='(?P<OBJTYPE>\S+)'+reSir3sIDSep+'(?P<NAME1>[\S ]*)'+reSir3sIDSep+'(?P<NAME2>\S*)'+reSir3sIDSep+'(?P<OBJTYPE_PK>\d+)'+reSir3sIDSep+'(?P<ATTRTYPE>\S+)'    
reSir3sIDcompiled=re.compile(reSir3sID) 

try:
    from PT3S import Xm
except ImportError:
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: ImportError: ','from PT3S import Xm - trying import Xm instead ... maybe pip install -e . is active ...')) 
    import Xm

# Q-Col Ends (Q-Cols: mx2Idx-referenced Channels for Flow) for Edges defined in Xm.vVBEL_edges:
vVBEL_edgesQ=['QMAV','QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'']
#vVBEL_edges=['ROHR','VENT','FWVB','FWES','PUMP','KLAP','REGV','PREG','MREG','DPRG','PGRP']

def filterQColsForEdgesInDf(df):
    """Filters all Q-Cols (Flow-Cols) for Edges in the df and returns the Q-Cols as List.
    """

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:            
            QCols=[]
            for idx,vbel in enumerate(Xm.vVBEL_edges):              
                if vbel != 'ROHR':
                    dfTmp=df.filter(regex=reSir3sIDSep+vVBEL_edgesQ[idx]+'$').filter(regex='^'+vbel)
                else:
                    dfTmp=df.filter(regex=reSir3sIDSep+vVBEL_edgesQ[idx]+'$').filter(regex='^'+vbel).filter(regex='^(?!.*VEC)')
                if dfTmp.empty:
                    continue
                shape=dfTmp.shape
    
                if shape[1]==0:
                    continue # Spalte nicht vorhanden
                if shape[1]>1:
                    continue # mehr als 1 matchende Spalte?!
                QCols.extend(dfTmp.columns.tolist())

    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.debug(logStrFinal)           
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
        return QCols   
  
def getMicrosecondsFromRefTime(refTime,time):
    """Returns time in microseconds since refTime.

    Args:
        * refTime
        * time

    Raises:
        MxError

   >>> import pandas as pd
   >>> timeReadFromMx=b'2019-01-01 00:00:12.500000      '
   >>> timeRefMx=b'2019-01-01 00:00:00.000000      '
   >>> timeStampTimeReadFromMx=pd.to_datetime(timeReadFromMx.decode(),utc=True)
   >>> timeStampTimeRefFromMx=pd.to_datetime(timeRefMx.decode(),utc=True)
   >>> timeDelta=timeStampTimeReadFromMx-timeStampTimeRefFromMx 
   >>> timeDelta.total_seconds()
   12.5
   >>> import Mx
   >>> Mx.getMicrosecondsFromRefTime(timeStampTimeRefFromMx,timeStampTimeReadFromMx)
   12500
    """
    try:
        timeH5=time-refTime
        #h5Key=int(math.floor(timeH5.total_seconds())*1000+timeH5.microseconds)
        h5Key=int(timeH5.total_seconds()*1000)
    except Exception as e:
        logStrFinal="{:s}: Exception: Line: {:d}: {!s:s}: {:s}".format('getMicrosecondsFromRefTime',sys.exc_info()[-1].tb_lineno,type(e),str(e)) 
        raise MxError(logStrFinal)              
    finally:
        return h5Key
    
def getMxsVecsFileDataAggsCalcAggs(df,mIndex):
    """Returns dfAggs, a dataFrame with Level 1 Aggregates of MultiIndexed df.
        
    Args:
        df: MultiIndexed dataFrame:
            Level 0: TYPE: TIMESTAMPs or Aggregates (MIN, MAX, ...)
            Level 1: Sir3sID: Sir3sIDs
            col-Labels: mx2Ids; IptIds for Pipe-Vecs
            col-Values: Vec-Values
        mIndex: MultiIndex as described above
    """

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:            
        cols=mIndex.get_level_values('Sir3sID').values.tolist()         
        # calc Aggs ---
        dfAggLst=[]
        # MIN
        dfAgg=df.min(level=1)   
        # construct mIndex for Agg
        arrays=[['MIN']*len(cols),cols]
        tuples = list(zip(*arrays))        
        mIndex = pd.MultiIndex.from_tuples(tuples, names=['TYPE', 'Sir3sID'])     
        dfAggLst.append(pd.DataFrame(dfAgg.values,index=mIndex,columns=dfAgg.columns))
        # MAX
        dfAgg=df.max(level=1)   
        # construct mIndex for Agg
        arrays=[['MAX']*len(cols),cols]
        tuples = list(zip(*arrays))        
        mIndex = pd.MultiIndex.from_tuples(tuples, names=['TYPE', 'Sir3sID'])     
        dfAggLst.append(pd.DataFrame(dfAgg.values,index=mIndex,columns=dfAgg.columns))            
        dfAggs=pd.concat(dfAggLst) # --- 
            
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.debug(logStrFinal)    
        dfAggs=pd.DataFrame()
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
        return dfAggs   

class MxError(Exception):
    """MxError.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Mx():
    """Reading SIR 3S' MX-Files. 

    Summary:
        * (mx1File): use this to profit from previous reads finalized with ToH5()
        * (mx1File,NoH5Read=True): use this for a fresh start with implicit .MXS-File read; finalize with ToH5()
        * (mx1File,NoH5Read=True,NoMxsRead=True): use this for a fresh start; call setResultsTo...() explicit; finalize with ToH5()
        * note that base.Y.h5-File has to be dunped explicitely with ToH5()
        * and base.Y.vec.h5-File is written implicitely while (implicit or explicit calls to) setResultsTo...() 
        * and is deleted explicitely (mx1File,NoH5Read=True) or implicitely (because it is i.e. to old) 

    Args:
        * mx1File (str): base.MX1-File (an XML-File) (base.Y.MX1-File from 90-10 on)

        * NoH5Read (bool): 
            False (default - use this to profit from previous reads finalized with ToH5()): 
                * If a base.Y.h5-File 
                    * exists 
                    * and is newer (>) than an .MX1-File (base.Y.Mx1-File from 90-10 on) 
                    * and is newer (>) than an .MXS-File (base.Y.MXS-File from 90-10 on):

                        * The base.Y.h5-File is read instead of the .MX1-File.                        

            True (use this for a fresh start):             
                * An  base.Y.h5-File is deleted if existing.  
                * The base.Y.Mx1-File is read. 
                * The base.Y.vec.h5-File is newly created in case of an .MXS-File read.

        * NoMxsRead (bool):
            True:
                * a base.Y.MXS-File is not read 
                * a base.Y.vec.h5-File is not touched

            False (default):
                * If a base.Y.MXS-File
                    * exists
                    * and is newer (>=) than base.Y.Mx1-File
                    * and base.Y.h5-File is not read:

                        * The base.Y.MXS-File is read.      
                        * NoH5Read=True will delete base.Y.vec.h5-File.

    Attributes:
        * states
            * h5Read: True, if read from H5

        * fileNames
            * .mx1File: base.Y.MX1-File 

            derived from mx1File
                * .mx2File: base.MX2-File 
                * .mxsFile: base.Y.MXS-File
                * .mxsZipFile base.ZIP
                *  constructed from MX during Init and Usage:
                *  ------------------------------------------
                * .h5File: base.Y.h5-File
                * .h5FileVecs: base.Y.vec.h5-File: MXS-H5Dump written implicitely 
                * .h5FileMx1FmtString: base.Y.h5-File.metadata written implicitely
      
        * .mxRecordStructFmtString
            * usage: struct.unpack(self.mxRecordStructFmtString,a_MXS_Record)  
            * .h5FileMx1FmtString:
                * it was not possible to store mxRecordStructFmtString in H5-Format as Metadata
                * therefore mxRecordStructFmtString is stored in a file named .h5FileMx1FmtString
                * in .h5File the Link to this file is stored as Metadata
                * as pointed out with usage above mxRecordStructFmtString has nothing to do with writing to or reading from H5
                * mxRecordStructFmtString is only about reading from (and writing to for test purposes) MXS
                * the .mxRecordStructFmtString/.h5FileMx1FmtString stuff is only about performance:
                * if after reading from H5 only a(nother) MXS shall be read again ...
                * ... the stuff avoids the time-consuming reconstruction of mxRecordStructFmtString 

        * dataFrames
            * .mx1Df  
            * .mx2Df 
            * .df
                * the base.Y.MXS-File(s) Content 
                * non Vectordata only
                * index:   TIMESTAMP (scenario time)
                * columns: Values  
                    * The following (String-)ID - called Sir3sID - is used as Columnlabel:                    
                    * this Sir3sID consists of ~ (Mx.reSir3sIDSep) separated .MX1-File terms:
                    * OBJTYPE~NAME1~NAME2~OBJTYPE_PK~ATTRTYPE  
                    * Sir3sID regExp Example: Mx.reSir3sID: (?P<OBJTYPE>\S+)~(?P<NAME1>[\S ]*)~(?P<NAME1>\S*)~(?P<OBJTYPE_PK>\d+)~(?P<ATTRTYPE>\S+)'    
            * .dfVecAggs
                * some base.Y.vec.h5-File Aggregates as df
                * MultiIndex:
                    * TYPE: SNAPSHOTTYPEs: TIME,TMIN,TMAX (from _readMxsFile) or Aggregates from 2 Times: MIN,MAX,... (from getVecAggs)
                    * Sir3sID
                    * TIMESTAMPL
                    * TIMESTAMPR
                * Cols: mx2Idx
    Raises:
        MxError
    """
    def __init__(self,mx1File,NoH5Read=False,NoMxsRead=False): 
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            if type(mx1File) == str:
                    self.mx1File=mx1File  # base.MX1-File (an XML-File) (base.Y.MX1-File from 90-10 on)
            else:
                    logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,mx1File)                                 
                    raise MxError(logStrFinal)     

            # determine base
            (wD,fileName)=os.path.split(self.mx1File)
            (base,ext)=os.path.splitext(fileName)
            (base,dotResolution)=os.path.splitext(base) # dotResolution: '.Y' from 90-10 on; '' before

            #Determine corresponding .MX2 Filename
            self.mx2File=wD+os.path.sep+base+'.'+'MX2'   
                                                     
            #Determine corresponding .h5 Filename(s)
            self.h5File=wD+os.path.sep+base+'.'+'h5'    # mx1Df, mx2Df, df (non Vectordata only)
            self.h5FileVecs=wD+os.path.sep+base+dotResolution+'.'+'vec'+'.'+'h5' # (Vectordata)     
            self.h5FileMx1FmtString=self.h5File+'.metadata'
                        
            #Determine corresponding .MXS Filename
            self.mxsFile=wD+os.path.sep+base+dotResolution+'.'+'MXS'  
          
            #Determine corresponding .MXS Zip-Filename
            self.mxsZipFile=wD+os.path.sep+base+dotResolution+'.'+'ZIP'   

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
                            self.h5Read=True
                        else:                                                             
                            self.h5Read=False  
                    else:
                        if not NoH5Read:
                            logger.debug("{0:s}h5File {1:s} exists _and is newer than an mx1File {2:s} _and there is no mxsFile like {3:s} _and NoH5Read False:".format(logStr,self.h5File,self.mx1File,self.mxsFile))     
                            logger.debug("{0:s}The h5File is read _instead of an mx1File.".format(logStr))   
                            self.h5Read=True  
                        else:
                            self.h5Read=False  
                else:                    
                    self.h5Read=False
            else:
                self.h5Read=False

            self.df=None   
            self.mx1Df=None
            self.mx2Df=None 
            self.dfVecAggs=pd.DataFrame()
            # to handle 90-09 TIMESTAMP UTC offset:
            self.timeDeltaReadOffset=None
            self.timeDeltaWriteOffset=None

            if not self.h5Read:
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
                        self.setResultsToMxsFile(NewH5Vec=NoH5Read)  # wenn kein H5 gelesen werden soll, dann soll auch das H5Vec neu angelegt werden
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

    def delFiles(self): 
        """Deletes Files constructed by MX during Init and Usage.
        """
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:           
            if os.path.exists(self.h5File):                        
               os.remove(self.h5File)    
               logger.debug("{0:s} File {1:s} deleted.".format(logStr,self.h5File)) 
            if os.path.exists(self.h5FileVecs):                        
               os.remove(self.h5FileVecs)   
               logger.debug("{0:s} File {1:s} deleted.".format(logStr,self.h5FileVecs)) 
            if os.path.exists(self.h5FileMx1FmtString):                        
               os.remove(self.h5FileMx1FmtString)    
               logger.debug("{0:s} File {1:s} deleted.".format(logStr,self.h5FileMx1FmtString)) 
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
            sep=reSir3sIDSep
            self.mx1Df['Sir3sID']=self.mx1Df['OBJTYPE']+sep+self.mx1Df['NAME1']+sep+self.mx1Df['NAME2']+sep+self.mx1Df['OBJTYPE_PK']+sep+self.mx1Df['ATTRTYPE']
            self.mx1Df['Sir3sID']=self.mx1Df['Sir3sID'].astype(str)

            #markVectorChannels
            self.mx1Df['NOfItems']=[int(cDLength/cDTypeLength) for cDLength,cDTypeLength in zip(self.mx1Df['DATALENGTH'],self.mx1Df['DATATYPELENGTH'])]             
            #self.mx1Df['isVectorChannel']=[True if nItems>1 else False for nItems in self.mx1Df['NOfItems']] 
            self.mx1Df['isVectorChannel']=[True if nItems>1 or (len(OBJTYPE_PK) < 3 and OBJTYPE != 'ALLG') else False for nItems,OBJTYPE_PK,OBJTYPE in zip(self.mx1Df['NOfItems'],self.mx1Df['OBJTYPE_PK'],self.mx1Df['OBJTYPE'])] 
           
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

            # SNAPSHOTTYPE
            self.idxSNAPSHOTTYPE=self.mx1Df['Sir3sID'][
                self.mx1Df['ATTRTYPE']=='SNAPSHOTTYPE'
                ].index[0]           
            self.unpackIdxSNAPSHOTTYPE=self.mx1Df['unpackIdx'][               
                self.mx1Df['ATTRTYPE']=='SNAPSHOTTYPE'
                ].iloc[0]    
            logger.debug("{:s}idxSNAPSHOTTYPE={:d} (idx in MX1) unpackIdxSNAPSHOTTYPE={:d} (idx in recordData).".format(logStr,self.idxSNAPSHOTTYPE,self.unpackIdxSNAPSHOTTYPE))         
            
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

        >>> mx=mxs['LocalHeatingNetwork']   
        >>> mx.delFiles()       
        >>> mx.setResultsToMxsFile() # reads 5 TIMESTAMPS and constructs .vec.h5 while reading
        5
        >>> mx.dfVecAggs.loc[(['TIME','TMIN','TMAX'],'KNOT~*~*~*~PH',slice(None),slice(None)),0:22]  
                                                                          0         1         2         3         4         5         6         7         8         9         10        11        12        13   14        15        16        17        18   19        20        21        22
        TYPE Sir3sID       TIMESTAMPL          TIMESTAMPR                                                                                                                                                                                                                                     
        TIME KNOT~*~*~*~PH 2004-09-22 08:30:00 2004-09-22 08:30:00  2.302971  3.985846  4.083384  4.121495  2.043288  2.283566  2.004937  4.311307  4.126019  2.309655  4.291591  2.000133  2.141440  3.825970  2.0  3.819467  2.314658  3.816599  2.312659  2.0  3.845104  4.125885  3.814690
        TMIN KNOT~*~*~*~PH 2004-09-22 08:30:00 2004-09-22 08:31:00  2.052100  2.183028  2.200011  2.206647  2.007717  2.048865  2.000910  2.248923  2.207463  2.053240  2.234365  2.000021  2.025138  2.156905  2.0  2.155822  2.054124  2.155325  2.053771  2.0  2.160025  2.207441  2.154995
        TMAX KNOT~*~*~*~PH 2004-09-22 08:30:00 2004-09-22 08:31:00  2.302971  4.085822  4.183360  4.221471  2.043288  2.283566  2.004937  4.411284  4.225996  2.309655  4.391567  2.000133  2.141440  3.925947  2.0  3.919444  2.314658  3.916576  2.312659  2.0  3.945080  4.225861  3.914667
        >>> mx.dfVecAggs
                                                                                      0           1             2           3           4           5           6           7           8           9           10          11          12          13          14          15          16          17          18          19          20          21          22          23          24          25          26          27          28          29          30          31
        TYPE Sir3sID                 TIMESTAMPL          TIMESTAMPR                                                                                                                                                                                                                                                                                                                                                                                                           
        TIME ROHR~*~*~*~QMI          2004-09-22 08:30:00 2004-09-22 08:30:00   -8.509475   19.059780 -1.537890e+01    8.509476  -22.987946   22.987946   22.987947   -3.928166   22.987947   15.378901    3.928167  -22.987946  -19.059778   -3.928166    3.928167  -22.987946         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~P            2004-09-22 08:30:00 2004-09-22 08:30:00    3.302971    4.985846  5.083384e+00    5.121495    3.043288    3.283566    3.004937    5.311307    5.126019    3.309655    5.291591    3.000133    3.141440    4.825970    3.000000    4.819467    3.314658    4.816599    3.312659    3.000000    4.845104    5.125885    4.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWES~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:30:00   22.987947         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~HMAX_INST    2004-09-22 08:30:00 2004-09-22 08:30:00    2.302971    3.985846  4.083384e+00    4.121495    2.043288    2.283566    2.004937    4.311307    4.126019    2.309655    4.291591    2.000133    2.141440    3.825970    2.000000    3.819467    2.314658    3.816599    2.312659    2.000000    3.845104    4.125885    3.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~PVECMIN_INST 2004-09-22 08:30:00 2004-09-22 08:30:00    3.302971    3.309655  4.985845e+00    4.845103    3.283566    3.302971    4.825970    4.819467    3.000133    3.004937    5.083383    4.985845    5.125884    5.121495    3.312659    3.314658    5.121495    5.083383    4.845103    4.825970    4.819467    4.816599    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.816599    4.814690    3.004937    3.043288
             VENT~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:30:00   22.987947   22.987946  2.199973e-06         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~H            2004-09-22 08:30:00 2004-09-22 08:30:00    2.302971    3.985846  4.083384e+00    4.121495    2.043288    2.283566    2.004937    4.311307    4.126019    2.309655    4.291591    2.000133    2.141440    3.825970    2.000000    3.819467    2.314658    3.816599    2.312659    2.000000    3.845104    4.125885    3.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~SVEC         2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000   88.019997  0.000000e+00  405.959991    0.000000   83.550003    0.000000   88.019997    0.000000   73.419998    0.000000  195.529999    0.000000   68.599998    0.000000  109.769997    0.000000   76.400002    0.000000   83.550003    0.000000  164.910004    0.000000  195.529999    0.000000  405.959991    0.000000  164.910004    0.000000  109.769997    0.000000   76.400002
             ROHR~*~*~*~PVEC         2004-09-22 08:30:00 2004-09-22 08:30:00    3.302971    3.309655  4.985845e+00    4.845103    3.283566    3.302971    4.825970    4.819467    3.000133    3.004937    5.083383    4.985845    5.125884    5.121495    3.312659    3.314659    5.121495    5.083383    4.845103    4.825970    4.819467    4.816599    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.816599    4.814690    3.004937    3.043288
             ROHR~*~*~*~VI           2004-09-22 08:30:00 2004-09-22 08:30:00   -0.266728    0.608561 -4.820491e-01    0.271700   -0.321646    0.733984    0.327641   -0.123128    0.733984    0.491034    0.125423   -0.720553   -0.597426   -0.123128    0.125423   -0.720553         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~T            2004-09-22 08:30:00 2004-09-22 08:30:00   60.000000   90.000000  9.000000e+01   90.000000   60.000000   60.000000   60.000000   60.000000   90.000000   60.000000   60.000000   60.000000   60.000000   90.000000   60.000000   90.000000   60.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:30:00   22.987947         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~RHOVEC       2004-09-22 08:30:00 2004-09-22 08:30:00  983.700012  983.700012  9.657000e+02  965.700012  983.700012  983.700012  965.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012  965.700012  965.700012  965.700012  983.700012  983.700012  983.700012  983.700012  983.700012  983.700012  965.700012  965.700012  983.700012  983.700012
             ROHR~*~*~*~TVEC         2004-09-22 08:30:00 2004-09-22 08:30:00   60.000000   60.000000  9.000000e+01   90.000000   60.000000   60.000000   90.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000   90.000000   90.000000   90.000000   60.000000   60.000000   60.000000   60.000000   60.000000   60.000000   90.000000   90.000000   60.000000   60.000000
             FWES~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:30:00    1.291413         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~MVEC         2004-09-22 08:30:00 2004-09-22 08:30:00   -2.363743   -2.363743  5.294384e+00    5.294384   -4.271917   -4.271917    2.363743    2.363743   -6.385540   -6.385540    6.385540    6.385540    6.385541    6.385541   -1.091157   -1.091157    6.385540    6.385540    4.271917    4.271917    1.091157    1.091157   -6.385540   -6.385540   -5.294383   -5.294383   -1.091157   -1.091157    1.091157    1.091157   -6.385540   -6.385540
             ROHR~*~*~*~VK           2004-09-22 08:30:00 2004-09-22 08:30:00   -0.266728    0.608561 -4.820491e-01    0.271700   -0.321646    0.733984    0.327641   -0.123128    0.733984    0.491034    0.125423   -0.720553   -0.597426   -0.123128    0.125423   -0.720553         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             PUMP~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:30:00   22.987947         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PDAMPF       2004-09-22 08:30:00 2004-09-22 08:30:00    0.199200    0.701100  7.011000e-01    0.701100    0.199200    0.199200    0.199200    0.199200    0.701100    0.199200    0.199200    0.199200    0.199200    0.701100    0.199200    0.701100    0.199200    0.701100    0.199200    0.199200    0.701100    0.701100    0.701100         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~PVECMAX_INST 2004-09-22 08:30:00 2004-09-22 08:30:00    3.302971    3.309655  4.985845e+00    4.845104    3.283566    3.302971    4.825970    4.819468    3.000133    3.004937    5.083383    4.985845    5.125884    5.121495    3.312659    3.314659    5.121495    5.083383    4.845104    4.825970    4.819468    4.816599    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.816599    4.814690    3.004937    3.043288
             VENT~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:30:00    0.374182    0.367335  3.163897e-07         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~HMIN_INST    2004-09-22 08:30:00 2004-09-22 08:30:00    2.302971    3.985846  4.083384e+00    4.121495    2.043288    2.283565    2.004937    4.311307    4.126019    2.309655    4.291591    2.000133    2.141440    3.825970    2.000000    3.819467    2.314658    3.816599    2.312659    2.000000    3.845104    4.125885    3.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~QMK          2004-09-22 08:30:00 2004-09-22 08:30:00   -8.509475   19.059780 -1.537890e+01    8.509476  -22.987946   22.987946   22.987947   -3.928166   22.987947   15.378901    3.928167  -22.987946  -19.059778   -3.928166    3.928167  -22.987946         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PMIN_INST    2004-09-22 08:30:00 2004-09-22 08:30:00    3.302971    4.985846  5.083384e+00    5.121495    3.043288    3.283565    3.004937    5.311307    5.126019    3.309655    5.291591    3.000133    3.141440    4.825970    3.000000    4.819467    3.314658    4.816599    3.312659    3.000000    4.845104    5.125885    4.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~RHO          2004-09-22 08:30:00 2004-09-22 08:30:00  983.700012  965.700012  9.657000e+02  965.700012  983.700012  983.700012  983.700012  983.700012  965.700012  983.700012  983.700012  983.700012  983.700012  965.700012  983.700012  965.700012  983.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~ZVEC         2004-09-22 08:30:00 2004-09-22 08:30:00   20.000000   20.000000  2.000000e+01   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000
             KNOT~*~*~*~PMAX_INST    2004-09-22 08:30:00 2004-09-22 08:30:00    3.302971    4.985846  5.083384e+00    5.121495    3.043288    3.283566    3.004937    5.311307    5.126019    3.309655    5.291591    3.000133    3.141440    4.825970    3.000000    4.819468    3.314658    4.816599    3.312659    3.000000    4.845104    5.125885    4.814691         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:30:00    1.291413         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~WALTER       2004-09-22 08:30:00 2004-09-22 08:30:00    0.209004    0.161072  8.707356e-02    0.058160    0.403910    0.207487    0.433363    0.496769    0.000000    0.286059    0.496769    0.496769    0.328532    0.393637    0.000000    0.483626    0.000000    0.848857    0.247643    0.496769    0.346373    0.000000    1.091969         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PH           2004-09-22 08:30:00 2004-09-22 08:30:00    2.302971    3.985846  4.083384e+00    4.121495    2.043288    2.283566    2.004937    4.311307    4.126019    2.309655    4.291591    2.000133    2.141440    3.825970    2.000000    3.819467    2.314658    3.816599    2.312659    2.000000    3.845104    4.125885    3.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~W            2004-09-22 08:30:00 2004-09-22 08:30:00  160.000000  200.000000  1.600000e+02  160.000000  120.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:30:00    3.928166    6.869426  4.581308e+00    3.928166    3.680879         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~QMAV         2004-09-22 08:30:00 2004-09-22 08:30:00   -8.509475   19.059780 -1.537890e+01    8.509476  -22.987946   22.987946   22.987947   -3.928166   22.987947   15.378901    3.928167  -22.987946  -19.059778   -3.928166    3.928167  -22.987946         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~VAV          2004-09-22 08:30:00 2004-09-22 08:30:00   -0.266728    0.608561 -4.820491e-01    0.271700   -0.321646    0.733984    0.327641   -0.123128    0.733984    0.491034    0.125423   -0.720553   -0.597426   -0.123128    0.125423   -0.720553         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             VENT~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000    0.000000  0.000000e+00         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             PUMP~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWES~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:30:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
        TMIN ROHR~*~*~*~QMI          2004-09-22 08:30:00 2004-09-22 08:31:00   -8.509475    7.394749 -1.537890e+01    3.256006  -22.987946    9.266180    9.266181   -3.928166    9.266181    5.923044    1.496261  -22.987946  -19.059778   -3.928166    1.496260  -22.987946         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~P            2004-09-22 08:30:00 2004-09-22 08:31:00    3.052100    3.183028  3.200011e+00    3.206647    3.007717    3.048865    3.000910    3.248923    3.207463    3.053240    3.234365    3.000021    3.025138    3.156905    3.000000    3.155822    3.054124    3.155325    3.053771    3.000000    3.160025    3.207441    3.154995         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWES~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00    9.266181         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~HMAX_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    2.302971    3.985846  4.083384e+00    4.121495    2.043288    2.283565    2.004937    4.311307    4.126019    2.309655    4.291591    2.000133    2.141440    3.825970    2.000000    3.819467    2.314658    3.816599    2.312659    2.000000    3.845104    4.125885    3.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~PVECMIN_INST 2004-09-22 08:30:00 2004-09-22 08:31:00    3.052100    3.053240  3.183028e+00    3.160025    3.048864    3.052100    3.156905    3.155822    3.000022    3.000910    3.200011    3.183028    3.207441    3.206647    3.053771    3.054124    3.206647    3.200011    3.160025    3.156905    3.155822    3.155326    3.007717    3.025139    3.025139    3.048864    3.053240    3.053771    3.155326    3.154995    3.000910    3.007717
             VENT~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00    9.266181    9.266179  2.199715e-06         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~H            2004-09-22 08:30:00 2004-09-22 08:31:00    2.052100    2.183028  2.200011e+00    2.206647    2.007717    2.048865    2.000910    2.248923    2.207463    2.053240    2.234365    2.000021    2.025138    2.156905    2.000000    2.155822    2.054124    2.155325    2.053771    2.000000    2.160025    2.207441    2.154995         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~SVEC         2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000   88.019997  0.000000e+00  405.959991    0.000000   83.550003    0.000000   88.019997    0.000000   73.419998    0.000000  195.529999    0.000000   68.599998    0.000000  109.769997    0.000000   76.400002    0.000000   83.550003    0.000000  164.910004    0.000000  195.529999    0.000000  405.959991    0.000000  164.910004    0.000000  109.769997    0.000000   76.400002
             ROHR~*~*~*~PVEC         2004-09-22 08:30:00 2004-09-22 08:31:00    3.052100    3.053240  3.183028e+00    3.160025    3.048864    3.052100    3.156905    3.155822    3.000022    3.000910    3.200011    3.183028    3.207441    3.206647    3.053771    3.054124    3.206647    3.200011    3.160025    3.156905    3.155822    3.155326    3.007717    3.025139    3.025139    3.048864    3.053240    3.053771    3.155326    3.154995    3.000910    3.007717
             ROHR~*~*~*~VI           2004-09-22 08:30:00 2004-09-22 08:31:00   -0.266728    0.236108 -4.820491e-01    0.103961   -0.321646    0.295861    0.132068   -0.123128    0.295861    0.189117    0.047774   -0.720553   -0.597426   -0.123128    0.047774   -0.720553         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~T            2004-09-22 08:30:00 2004-09-22 08:31:00   60.000000   90.000000  9.000000e+01   90.000000   60.000000   60.000000   60.000000   60.000000   90.000000   60.000000   60.000000   60.000000   60.000000   90.000000   60.000000   90.000000   60.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00    9.266181         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~RHOVEC       2004-09-22 08:30:00 2004-09-22 08:31:00  983.700012  983.700012  9.657000e+02  965.700012  983.700012  983.700012  965.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012  965.700012  965.700012  965.700012  983.700012  983.700012  983.700012  983.700012  983.700012  983.700012  965.700012  965.700012  983.700012  983.700012
             ROHR~*~*~*~TVEC         2004-09-22 08:30:00 2004-09-22 08:31:00   60.000000   60.000000  9.000000e+01   90.000000   60.000000   60.000000   90.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000   90.000000   90.000000   90.000000   60.000000   60.000000   60.000000   60.000000   60.000000   60.000000   90.000000   90.000000   60.000000   60.000000
             FWES~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:31:00    0.520554         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~MVEC         2004-09-22 08:30:00 2004-09-22 08:31:00   -2.363743   -2.363743  2.054097e+00    2.054097   -4.271917   -4.271917    0.904446    0.904446   -6.385540   -6.385540    2.573939    2.573939    2.573939    2.573939   -1.091157   -1.091157    2.573939    2.573939    1.645290    1.645290    0.415628    0.415628   -6.385540   -6.385540   -5.294383   -5.294383   -1.091157   -1.091157    0.415628    0.415628   -6.385540   -6.385540
             ROHR~*~*~*~VK           2004-09-22 08:30:00 2004-09-22 08:31:00   -0.266728    0.236108 -4.820491e-01    0.103961   -0.321646    0.295861    0.132068   -0.123128    0.295861    0.189117    0.047774   -0.720553   -0.597426   -0.123128    0.047774   -0.720553         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             PUMP~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00    9.266181         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PDAMPF       2004-09-22 08:30:00 2004-09-22 08:31:00    0.199200    0.701100  7.011000e-01    0.701100    0.199200    0.199200    0.199200    0.199200    0.701100    0.199200    0.199200    0.199200    0.199200    0.701100    0.199200    0.701100    0.199200    0.701100    0.199200    0.199200    0.701100    0.701100    0.701100         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~PVECMAX_INST 2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    3.309655  4.985845e+00    4.845104    3.283566    3.302971    4.825970    4.819468    3.000133    3.004937    5.083383    4.985845    5.125884    5.121495    3.312659    3.314658    5.121495    5.083383    4.845104    4.825970    4.819468    4.816599    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.816599    4.814690    3.004937    3.043288
             VENT~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:31:00    0.150829    0.148069  3.163526e-07         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~HMIN_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    2.052100    2.183028  2.200011e+00    2.206647    2.007717    2.048865    2.000910    2.248923    2.207463    2.053240    2.234365    2.000021    2.025138    2.156905    2.000000    2.155822    2.054124    2.155325    2.053771    2.000000    2.160025    2.207441    2.154995         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~QMK          2004-09-22 08:30:00 2004-09-22 08:31:00   -8.509475    7.394749 -1.537890e+01    3.256006  -22.987946    9.266180    9.266181   -3.928166    9.266181    5.923044    1.496261  -22.987946  -19.059778   -3.928166    1.496260  -22.987946         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PMIN_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    3.052100    3.183028  3.200011e+00    3.206647    3.007717    3.048865    3.000910    3.248923    3.207463    3.053240    3.234365    3.000021    3.025138    3.156905    3.000000    3.155822    3.054124    3.155325    3.053771    3.000000    3.160025    3.207441    3.154995         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~RHO          2004-09-22 08:30:00 2004-09-22 08:31:00  983.700012  965.700012  9.657000e+02  965.700012  983.700012  983.700012  983.700012  983.700012  965.700012  983.700012  983.700012  983.700012  983.700012  965.700012  983.700012  965.700012  983.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~ZVEC         2004-09-22 08:30:00 2004-09-22 08:31:00   20.000000   20.000000  2.000000e+01   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000
             KNOT~*~*~*~PMAX_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    4.985846  5.083384e+00    5.121495    3.043288    3.283565    3.004937    5.311307    5.126019    3.309655    5.291591    3.000133    3.141440    4.825970    3.000000    4.819468    3.314658    4.816599    3.312659    3.000000    4.845104    5.125885    4.814691         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:31:00    0.520554         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~WALTER       2004-09-22 08:30:00 2004-09-22 08:31:00    0.209004    0.161072  8.707356e-02    0.058160    0.403910    0.207487    0.433363    0.496769    0.000000    0.286059    0.496769    0.496769    0.328532    0.393637    0.000000    0.483626    0.000000    0.848857    0.247643    0.496769    0.346373    0.000000    1.091969         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PH           2004-09-22 08:30:00 2004-09-22 08:31:00    2.052100    2.183028  2.200011e+00    2.206647    2.007717    2.048865    2.000910    2.248923    2.207463    2.053240    2.234365    2.000021    2.025138    2.156905    2.000000    2.155822    2.054124    2.155325    2.053771    2.000000    2.160025    2.207441    2.154995         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~W            2004-09-22 08:30:00 2004-09-22 08:31:00   76.226158   77.649529  6.145824e+01   60.944885   47.978928         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00    1.871431    2.667038  1.759745e+00    1.496260    1.471705         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~QMAV         2004-09-22 08:30:00 2004-09-22 08:31:00   -8.509475    7.394749 -1.537890e+01    3.256006  -22.987946    9.266180    9.266181   -3.928166    9.266181    5.923044    1.496261  -22.987946  -19.059778   -3.928166    1.496260  -22.987946         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~VAV          2004-09-22 08:30:00 2004-09-22 08:31:00   -0.266728    0.236108 -4.820491e-01    0.103961   -0.321646    0.295861    0.132068   -0.123128    0.295861    0.189117    0.047774   -0.720553   -0.597426   -0.123128    0.047774   -0.720553         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             VENT~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             PUMP~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWES~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
        TMAX ROHR~*~*~*~QMI          2004-09-22 08:30:00 2004-09-22 08:31:00   -3.256005   19.059780 -5.923043e+00    8.509476   -9.266179   22.987946   22.987947   -1.496260   22.987947   15.378901    3.928167   -9.266179   -7.394748   -1.496260    3.928167   -9.266179         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~P            2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    5.085822  5.183360e+00    5.221471    3.043288    3.283566    3.004937    5.411284    5.225996    3.309655    5.391567    3.000133    3.141440    4.925947    3.000000    4.919444    3.314658    4.916576    3.312659    3.000000    4.945080    5.225861    4.914667         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWES~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00   22.987947         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~HMAX_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    2.302971    4.085822  4.183360e+00    4.221471    2.043288    2.283566    2.004937    4.411284    4.225996    2.309655    4.391567    2.000133    2.141440    3.925947    2.000000    3.919444    2.314658    3.916576    2.312659    2.000000    3.945080    4.225861    3.914667         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~PVECMIN_INST 2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    3.309655  4.985845e+00    4.845104    3.283566    3.302971    4.825970    4.819468    3.000133    3.004937    5.083383    4.985845    5.125884    5.121495    3.312659    3.314658    5.121495    5.083383    4.845104    4.825970    4.819468    4.816599    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.816599    4.814690    3.004937    3.043288
             VENT~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00   22.987947   22.987946  2.199973e-06         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~H            2004-09-22 08:30:00 2004-09-22 08:31:00    2.302971    4.085822  4.183360e+00    4.221471    2.043288    2.283566    2.004937    4.411284    4.225996    2.309655    4.391567    2.000133    2.141440    3.925947    2.000000    3.919444    2.314658    3.916576    2.312659    2.000000    3.945080    4.225861    3.914667         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~SVEC         2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000   88.019997  0.000000e+00  405.959991    0.000000   83.550003    0.000000   88.019997    0.000000   73.419998    0.000000  195.529999    0.000000   68.599998    0.000000  109.769997    0.000000   76.400002    0.000000   83.550003    0.000000  164.910004    0.000000  195.529999    0.000000  405.959991    0.000000  164.910004    0.000000  109.769997    0.000000   76.400002
             ROHR~*~*~*~PVEC         2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    3.309655  5.085822e+00    4.945080    3.283566    3.302971    4.925946    4.919444    3.000133    3.004937    5.183360    5.085822    5.225861    5.221471    3.312659    3.314659    5.221471    5.183360    4.945080    4.925946    4.919444    4.916576    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.916576    4.914667    3.004937    3.043288
             ROHR~*~*~*~VI           2004-09-22 08:30:00 2004-09-22 08:31:00   -0.102059    0.608561 -1.856568e-01    0.271700   -0.129652    0.733984    0.327641   -0.046900    0.733984    0.491034    0.125423   -0.290447   -0.231787   -0.046900    0.125423   -0.290447         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~T            2004-09-22 08:30:00 2004-09-22 08:31:00   60.000000   90.000000  9.000000e+01   90.000000   60.000000   60.000000   60.000000   60.000000   90.000000   60.000000   60.000000   60.000000   60.000000   90.000000   60.000000   90.000000   60.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00   22.987947         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~RHOVEC       2004-09-22 08:30:00 2004-09-22 08:31:00  983.700012  983.700012  9.657000e+02  965.700012  983.700012  983.700012  965.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012  965.700012  965.700012  965.700012  983.700012  983.700012  983.700012  983.700012  983.700012  983.700012  965.700012  965.700012  983.700012  983.700012
             ROHR~*~*~*~TVEC         2004-09-22 08:30:00 2004-09-22 08:31:00   60.000000   60.000000  9.000000e+01   90.000000   60.000000   60.000000   90.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000   90.000000   60.000000   60.000000   90.000000   90.000000   90.000000   90.000000   90.000000   90.000000   60.000000   60.000000   60.000000   60.000000   60.000000   60.000000   90.000000   90.000000   60.000000   60.000000
             FWES~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:31:00    1.291413         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~MVEC         2004-09-22 08:30:00 2004-09-22 08:31:00   -0.904446   -0.904446  5.294384e+00    5.294384   -1.645290   -1.645290    2.363743    2.363743   -2.573939   -2.573939    6.385540    6.385540    6.385541    6.385541   -0.415628   -0.415628    6.385540    6.385540    4.271917    4.271917    1.091157    1.091157   -2.573939   -2.573939   -2.054097   -2.054097   -0.415628   -0.415628    1.091157    1.091157   -2.573939   -2.573939
             ROHR~*~*~*~VK           2004-09-22 08:30:00 2004-09-22 08:31:00   -0.102059    0.608561 -1.856568e-01    0.271700   -0.129652    0.733984    0.327641   -0.046900    0.733984    0.491034    0.125423   -0.290447   -0.231787   -0.046900    0.125423   -0.290447         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             PUMP~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00   22.987947         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PDAMPF       2004-09-22 08:30:00 2004-09-22 08:31:00    0.199200    0.701100  7.011000e-01    0.701100    0.199200    0.199200    0.199200    0.199200    0.701100    0.199200    0.199200    0.199200    0.199200    0.701100    0.199200    0.701100    0.199200    0.701100    0.199200    0.199200    0.701100    0.701100    0.701100         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~PVECMAX_INST 2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    3.309655  5.085822e+00    4.945080    3.283566    3.302971    4.925946    4.919444    3.000133    3.004937    5.183360    5.085822    5.225861    5.221471    3.312659    3.314659    5.221471    5.183360    4.945080    4.925946    4.919444    4.916576    3.043288    3.141441    3.141441    3.283566    3.309655    3.312659    4.916576    4.914667    3.004937    3.043288
             VENT~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:31:00    0.374182    0.367335  3.163897e-07         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~HMIN_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    2.302971    3.985846  4.083384e+00    4.121495    2.043288    2.283565    2.004937    4.311307    4.126019    2.309655    4.291591    2.000133    2.141440    3.825970    2.000000    3.819467    2.314658    3.816599    2.312659    2.000000    3.845104    4.125885    3.814690         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~QMK          2004-09-22 08:30:00 2004-09-22 08:31:00   -3.256005   19.059780 -5.923043e+00    8.509476   -9.266179   22.987946   22.987947   -1.496260   22.987947   15.378901    3.928167   -9.266179   -7.394748   -1.496260    3.928167   -9.266179         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PMIN_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    4.985846  5.083384e+00    5.121495    3.043288    3.283565    3.004937    5.311307    5.126019    3.309655    5.291591    3.000133    3.141440    4.825970    3.000000    4.819468    3.314658    4.816599    3.312659    3.000000    4.845104    5.125885    4.814691         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~RHO          2004-09-22 08:30:00 2004-09-22 08:31:00  983.700012  965.700012  9.657000e+02  965.700012  983.700012  983.700012  983.700012  983.700012  965.700012  983.700012  983.700012  983.700012  983.700012  965.700012  983.700012  965.700012  983.700012  965.700012  983.700012  983.700012  965.700012  965.700012  965.700012         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~ZVEC         2004-09-22 08:30:00 2004-09-22 08:31:00   20.000000   20.000000  2.000000e+01   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000   20.000000
             KNOT~*~*~*~PMAX_INST    2004-09-22 08:30:00 2004-09-22 08:31:00    3.302971    5.085822  5.183360e+00    5.221471    3.043288    3.283566    3.004937    5.411284    5.225996    3.309655    5.391567    3.000133    3.141440    4.925947    3.000000    4.919444    3.314658    4.916576    3.312659    3.000000    4.945080    5.225861    4.914667         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~V            2004-09-22 08:30:00 2004-09-22 08:31:00    1.291413         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~WALTER       2004-09-22 08:30:00 2004-09-22 08:31:00    0.542668    0.399595  2.160159e-01    0.144285    1.002038    0.534794    1.075106    1.232407    0.000000    0.747607    1.232407    1.232407    0.815037    0.999922    0.000000    1.235105    0.000000    2.193956    0.650142    1.232407    0.877202    0.000000    2.832201         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~PH           2004-09-22 08:30:00 2004-09-22 08:31:00    2.302971    4.085822  4.183360e+00    4.221471    2.043288    2.283566    2.004937    4.411284    4.225996    2.309655    4.391567    2.000133    2.141440    3.925947    2.000000    3.919444    2.314658    3.916576    2.312659    2.000000    3.945080    4.225861    3.914667         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~W            2004-09-22 08:30:00 2004-09-22 08:31:00  160.000000  200.000000  1.600000e+02  160.000000  120.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~QM           2004-09-22 08:30:00 2004-09-22 08:31:00    3.928166    6.869426  4.581308e+00    3.928166    3.680879         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~QMAV         2004-09-22 08:30:00 2004-09-22 08:31:00   -3.256005   19.059780 -5.923043e+00    8.509476   -9.266179   22.987946   22.987947   -1.496260   22.987947   15.378901    3.928167   -9.266179   -7.394748   -1.496260    3.928167   -9.266179         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~VAV          2004-09-22 08:30:00 2004-09-22 08:31:00   -0.102059    0.608561 -1.856568e-01    0.271700   -0.129652    0.733984    0.327641   -0.046900    0.733984    0.491034    0.125423   -0.290447   -0.231787   -0.046900    0.125423   -0.290447         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KNOT~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             ROHR~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             VENT~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             KLAP~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             PUMP~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWVB~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000    0.000000  0.000000e+00    0.000000    0.000000         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
             FWES~*~*~*~IAKTIV       2004-09-22 08:30:00 2004-09-22 08:31:00    0.000000         NaN           NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN         NaN
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
                keysInH5Store=mxsVecsH5StorePtr.keys()
                                                                     
            with mxsFilePtr: 
                try:                    
                    while True:   # while f.tell() != os.fstat(f.fileno()).st_size does NOT work with Zip's file objects ...    
                            
                        # read record 
                        try: 
                            record=mxsFilePtr.read(MxRecordLength)
                            recordData = struct.unpack(self.mxRecordStructFmtString,record)  
                        except struct.error as e:                                      
                            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                    
                            logger.debug(logStrFinal) 
                            logger.debug("{0:s}record=f.read(MxRecordLength) failed (struct.error). EOF assumed.".format(logStr))  
                            raise EOFError
                        except EOFError as e:
                            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                    
                            logger.debug(logStrFinal) 
                            logger.debug("{0:s}record=f.read(MxRecordLength) failed (EOFError).".format(logStr))  
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

                        # process SNAPSHOTTYPE
                        try:
                            cSNAPSHOTTYPE=recordData[self.unpackIdxSNAPSHOTTYPE].decode('utf-8')                                                                                                                                                                                                                                                                   
                        except Exception as e:
                            logStrFinal="{0:s}process SNAPSHOTTYPE failed. Error.".format(logStr)
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
                            #try:      
                                 h5DumpLog="{:s} NO:".format('H5Dump:')
                                 h5Key=getMicrosecondsFromRefTime(refTime=firstTime,time=time)   
                                
                                 h5Dump=True
                                 if '/'+str(h5Key) in keysInH5Store:    
                                     h5DumpLog="{:s} key=/{!s:>20s} in keys. Actual SNAPSHOTTYPE: {:s}".format(h5DumpLog,h5Key,cSNAPSHOTTYPE)  
                                     h5Dump=False
                                 #keys=mxsVecsH5StorePtr.keys()
                                 #if '/'+str(h5Key) in keys:  
                                 #    h5DumpLog="{:s} key=/{!s:>20s} already written. Actual SNAPSHOTTYPE: {:s}".format(h5DumpLog,h5Key,cSNAPSHOTTYPE)
                                 #    h5Dump=False

                                 if h5Dump:                                  
                                        try:                                            
                                            dfVecs = pd.DataFrame.from_records([valuesVecs],index=[time],columns=self.mxColumnNamesVecs)                                                                                              
                                            # write H5
                                            warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
                                            warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)                          
                                            mxsVecsH5StorePtr.put(str(h5Key),dfVecs)   
                                            
                                        except Exception as e:
                                            logger.error("{0:s}store record as df in H5 failed at Time={1!s}. Error.".format(logStr,time_read_finally))
                                            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                                            logger.error(logStrFinal) 
                                            raise MxError(logStrFinal)  

                                        timesWrittenToMxsVecs+=1
                                        h5DumpLog="{:s}     Written DataFrame {:s} (Nr. {:6d}) with h5Key=/{!s:>20s}".format('H5Dump:','dfVecs',timesWrittenToMxsVecs,h5Key) 
                                        keysInH5Store.append('/'+str(h5Key))
                                 else:
                                        if cSNAPSHOTTYPE in ['TIME','TMIN','TMAX']:       
                                            try:
                                                h5DumpLogOld=h5DumpLog
                                                h5DumpLog="{:s} trying to process to dfVecAggs with TIMESTAMPL: {!s:s}...".format(h5DumpLog,time_read_finally)         
                                                if cSNAPSHOTTYPE == 'TIME':
                                                    arrays=[[cSNAPSHOTTYPE]*len(self.mxColumnNamesVecs),self.mxColumnNamesVecs,[time.tz_localize(None)]*len(self.mxColumnNamesVecs),[time.tz_localize(None)]*len(self.mxColumnNamesVecs)]
                                                elif cSNAPSHOTTYPE in ['TMIN','TMAX']:    
                                                    arrays=[[cSNAPSHOTTYPE]*len(self.mxColumnNamesVecs),self.mxColumnNamesVecs,[firstTime.tz_localize(None)]*len(self.mxColumnNamesVecs),[time.tz_localize(None)]*len(self.mxColumnNamesVecs)]
                                                tuples=list(zip(*arrays))        
                                                mIndex=pd.MultiIndex.from_tuples(tuples,names=['TYPE','Sir3sID','TIMESTAMPL','TIMESTAMPR'])
                                            
                                                arrays2=[[cSNAPSHOTTYPE]*len(self.mxColumnNamesVecs),self.mxColumnNamesVecs]
                                                tuples2=list(zip(*arrays2))        
                                                mIndex2=pd.MultiIndex.from_tuples(tuples2,names=['TYPE','Sir3sID'])          
                                            
                                                dfVecs = pd.DataFrame.from_records([valuesVecs],index=[time.tz_localize(None)],columns=self.mxColumnNamesVecs)  
                                                df=self.unPackMxsVecsFileDataDf(dfVecs,mIndex2)
                                                df=pd.DataFrame(df.values,index=mIndex,columns=df.columns)
                                                if self.dfVecAggs.empty:                                                    
                                                    self.dfVecAggs=df
                                                    h5DumpLog="{:s} processed to (empty) dfVecAggs with TIMESTAMPL: {!s:s}".format(h5DumpLogOld,time_read_finally)  
                                                else:  
                                                    dfVecAggsAdd=True
                                                    if self.dfVecAggs.index.isin([x[0] for x in df.index],level=0).any(): # cSNAPSHOTTYPE existiert schon
                                                        if self.dfVecAggs.loc[(cSNAPSHOTTYPE,slice(None),slice(None),slice(None)),:].index.isin([x[2] for x in df.index],level=2).any(): # mit time                                                       
                                                            h5DumpLog="{:s} ... failed because cSNAPSHOTTYPE {:s} existiert schon mit Zeit {!s:s} ".format(h5DumpLog,cSNAPSHOTTYPE,time_read_finally)  
                                                            dfVecAggsAdd=False
                                                    if dfVecAggsAdd:     
                                                        try:
                                                            self.dfVecAggs=pd.concat([self.dfVecAggs,df])
                                                            h5DumpLog="{:s} processed to         dfVecAggs with TIMESTAMPL: {!s:s}".format(h5DumpLogOld,time_read_finally)  
                                                        except Exception as e:           
                                                            h5DumpLog="{:s}... failed because concat failed?!".format(h5DumpLog)  
                                                            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                                                            logger.error(logStrFinal)  
                                                            for idx,index in enumerate(df.index):                                                                
                                                                logger.debug("{:s}df-Index:        Nr.: {:5d} Wert: {!s:10s} {!s:30s} {!s:20s} {!s:20s} Index: {!s:s}".format(logStr,idx,str(index[0]),str(index[1]),str(index[2]),str(index[3]),index))
                                                            for idx,index in enumerate(self.dfVecAggs.index):
                                                                logger.debug("{:s}dfVecAggs-Index: Nr.: {:5d} Wert: {!s:10s} {!s:30s} {!s:20s} {!s:20s} Index: {!s:s}".format(logStr,idx,str(index[0]),str(index[1]),str(index[2]),str(index[3]),index))

                                            except Exception as e:
                                                logger.error("{0:s}dfVecAggs: Error?!".format(logStr))
                                                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                                                logger.error(logStrFinal)                                                                                                                                            
                                                     
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
            * newMxsVecsFile (default: False)

        mxsVecsFile is DELETED! if: 
            * existing and older than mxsFile
            * or newMxsVecsFile is True                 
            
        Raises:
            MxError                         
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try: 
        
            # .vec.h5 Handling 
            if os.path.exists(self.h5FileVecs):      

                if newMxsVecsFile:
                    logger.debug("{:s}Delete {:s} because NewH5Vec ...".format(logStr,self.h5FileVecs)) 
                    os.remove(self.h5FileVecs)   
                else:
                    if os.path.exists(mxsFile):                         
                        mxsFileTime=os.path.getmtime(mxsFile) 
                    else:
                        mxsFileTime=0
                    mxsH5FileTime=os.path.getmtime(self.h5FileVecs)

                    if mxsFileTime>mxsH5FileTime:
                        # die zu lesende Mxs ist neuer als der Dump: Dump loeschen              
                        logger.debug("{:s}Delete H5Dump because Mxs {:s} To Read is newer than H5Dump {:s} ...".format(logStr,mxsFile,self.h5FileVecs))                             
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
            * NewH5Vec: False (default); if True, an existing mxsVecsFile will be deleted even if it is newer than mxsFile
            * maxRecords

        Returns:
            * timesWrittenToMxsVecs
             
        .df
            * index: TIMESTAMP
            
            * self.df.index.is_unique will be True 

            * because in SIR 3S'
            * 1st Time twice (SNAPSHOTTYPE: STAT+TIME) and Last Time triple (SNAPSHOTTYPE: TIME+TMIN/TMAX)  

                * +TIME       is dropped (STAT is used in df)                               
                * +TMIN/TMAX are dropped (not used in df)
                   
            * and because resulting overlapping TIMESTAMPs due to intersections (add=True) are also dropped      

        .h5FileVecs

            * is updated with mxsFile-Content

            * is DELETED! before if existing and 
                * older than mxsFile
                * or newMxsVecsFile        
                
        Raises:
            MxError     
                    
        >>> mx=mxs['GPipes']
        >>> mx.df
        >>> mx.setResultsToMxsFile(NewH5Vec=True)
        1
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
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      
            return timesWrittenToMxsVecs         

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
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      
            return timesWrittenToMxsVecsFromZip
                       
    def ToH5(self,h5File=None):
        """Stores .mx1Df, .mx2Df, .df, .dfVecAggs to h5File.

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

                    recordStructFmtStringFile=self.h5FileMx1FmtString #self.h5File+'.metadata'
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

                if isinstance(self.dfVecAggs,pd.core.frame.DataFrame):    
                    h5Key=relPath2Mx1FromCurDirH5BaseKey+h5KeySep+'VecAggs'  
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,'df',h5Key))         
                    h5Store.put(h5Key,self.dfVecAggs)
             
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
        """Sets .mx1Df, .mx2Df, .df, .dfVecAggs to h5File-Content.

        Args:
            * h5File(str)
                * None (default): .h5File is used  

        Keys expected
            * /MX1
            * /MX2
            * /MXS
            * /VecAggs

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
                            
                    if key == 'VecAggs':                           
                        logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to {3:s}.".format(logStr,h5File,h5Key,key)) 
                        self.dfVecAggs=h5Store[h5Key]
                        
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                           
        finally: 
            h5Store.close()            
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))                

    def getMxsVecsFileData(self,timesReq=None,fastMode=False):
        """Returns List of dfs with mxsVecsFileData. One TIMESTAMP (index) per df.   

        Args:
            * timesReq: List of TIMESTAMPs
                * if None: a List with a single time only, the 1st Time, is constructed as timesReq
            * fastMode (default: False): H5-Access with no Checks
                               
        Returns:
            * List of dfs with mxsVecsFileData 
            * empty List if no TIMESTAMP could be found
            * one df per TIMESTAMP
            * index: TIMESTAMP

        Raises:
            MxError


        >>> mx=mxs['LocalHeatingNetwork']
        >>> mx.delFiles()
        >>> mx.setResultsToMxsFile() # reads 5 TIMESTAMPS and constructs .vec.h5 while reading
        5
        >>> mxVecsFileDataLst=mx.getMxsVecsFileData()
        >>> len(mxVecsFileDataLst)
        1
        >>> mxVecsFileData=mxVecsFileDataLst[0]
        >>> type(mxVecsFileData)
        <class 'pandas.core.frame.DataFrame'>
        >>> mxVecsFileData.index[0]
        Timestamp('2004-09-22 08:30:00+0000', tz='UTC')
        >>> vecsFileDataOneCol=mxVecsFileData['ROHR~*~*~*~SVEC']
        >>> vecsFileDataOneColResult=vecsFileDataOneCol[0]
        >>> vecsFileDataOneColResult[-1]
        76.4000015258789
        >>> mxVecsFileDataLst=mx.getMxsVecsFileData(fastMode=True)
        >>> mxVecsFileData=mxVecsFileDataLst[0]
        >>> vecsFileDataOneCol=mxVecsFileData['ROHR~*~*~*~SVEC']
        >>> vecsFileDataOneColResult=vecsFileDataOneCol[0]
        >>> vecsFileDataOneColResult[-1]
        76.4000015258789
        """

        logStr = "{0:s}.{1:s}: {2:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name,self.mx1File)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
           
            mxsVecsDfs=[]

            if os.path.exists(self.h5FileVecs):
                pass
            else:
                logStrFinal="{:s}{:s}: Not existing!".format(logStr,self.h5FileVecs)
                logger.error(logStrFinal) 
                raise MxError(logStrFinal)         

            #fuer h5Key Ermittlung
            h5KeysRequested=[]
            firstTime=self.df.index[0]
            lastTime=self.df.index[-1]

            if timesReq == None:
                key=getMicrosecondsFromRefTime(refTime=firstTime,time=firstTime)
                h5KeysRequested.append(key)
                timesReq=[]
                timesReq.append(firstTime)
            else:
                #h5Keys ermitteln
                for timeReq in timesReq:
                    key=getMicrosecondsFromRefTime(refTime=firstTime,time=timeReq)
                    h5KeysRequested.append(key)
            # h5Keys finalisieren
            h5KeysRequested=['/'+str(key) for key in h5KeysRequested]         
            
            if fastMode:
                with pd.HDFStore(self.h5FileVecs) as h5Store:                                                    
                    for h5KeyReq in h5KeysRequested:      
                        df=h5Store[h5KeyReq]
                        mxsVecsDfs.append(df)
                                                                    
            with pd.HDFStore(self.h5FileVecs) as h5Store:                
                # ueber alle verlangten keys
                h5KeysAvailable=sorted(h5Store.keys())                      
                for idx,h5KeyReq in enumerate(h5KeysRequested):                       
                    df=pd.DataFrame()
                    logStrAdditional=''
                    if h5KeyReq in h5KeysAvailable:                                                
                        df=h5Store[h5KeyReq]                                            
                        if df.index[0]!=timesReq[idx]:                           
                            logStrAdditional="{:s}{:s}: Key {:s} available - BUT TimeReq {:s} matched not H5-Time for this Key which is: {:s})!".format(logStr
                                                                                                                                                        ,self.h5FileVecs
                                                                                                                                                        ,h5KeyReq
                                                                                                                                                        ,str(timesReq[idx])
                                                                                                                                                        ,str(df.index[0]))                                           
                    else:                        
                        # ueber alle vorhandenen Keys
                        for h5KeyAva in h5KeysAvailable:                            
                            dfTmp=h5Store[h5KeyAva]                            
                            timeStamp=dfTmp.index[0]                                             
                            if timeStamp==timesReq[idx]:                                                    
                                df=dfTmp
                                logStrAdditional="{:s}{:s}: Key {:s} NOT available - BUT this Key {:s} matched Time requested {:s} first".format(logStr,self.h5FileVecs,h5KeyReq,h5KeyAva,str(timesReq[idx]))                                                        
                                break  
                        else:                            
                            logStrAdditional="{:s}{:s}: .Key {:s} (for Time requested {:s}) also as TIMESTAMP NOT available".format(logStr,self.h5FileVecs,h5KeyReq,str(timesReq[idx]))

                    if not df.empty:
                        logger.debug("{:s}    Ok: Time requested: {:s} corresponding Key: {:20s} Time stored: {:s} logStrAdditional: {:s}.".format(logStr,str(timesReq[idx]),h5KeyReq,str(df.index[0]),logStrAdditional))
                        mxsVecsDfs.append(df)  
                    else:
                        logger.debug("{:s}NOT Ok: Time requested: {:s} corresponding Key: {:20s} logStrAdditional: {:s}.".format(logStr,str(timesReq[idx]),h5KeyReq,logStrAdditional))
                                                
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                           
        finally:                      
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return mxsVecsDfs

    def unPackMxsVecsFileDataDf(self,mxVecsFileData,mIndex,returnMultiIndex=True):
        """Unpacks mxVecsFileData-Content into a returned df.   

        Args:
            * mxVecsFileData: the stuff returned by getMxsVecsFileData is: List of dfs with mxsVecsFileData. One TIMESTAMP (index) per df. One of these dfs.   
            * mIndex: MultiIndex to be used
                * 1st Level: Timestamps
                * 2nd Level: cols (Sir3sIds to be unpacked)   
            * returnMultiIndex (default: True):
                * if True, the data is unpacked row-wise (stored in cols) and the index is mIndex and the col-Labels are mx2Idx
                * if False, the data is unpacked col-wise (stored in rows) and the index is mx2Idx and th col-Labels are the cols (the Sir3sIds)
        Returns:
            * df           

        Raises:
            MxError

        >>> mx=mxs['LocalHeatingNetwork']   
        >>> mx.delFiles()       
        >>> mx.setResultsToMxsFile() # reads 5 TIMESTAMPS and constructs .vec.h5 while reading
        5
        >>> timesReq=list(mx.df.index[:]) # all times       
        >>> mxVecsFileDataLst=mx.getMxsVecsFileData(timesReq=timesReq)      
        >>> len(mxVecsFileDataLst)
        5
        >>> mxVecsFileData=mxVecsFileDataLst[0]           
        >>> # construct MultiIndex Start ... ---
        >>> colsToBeUnpacked=['ROHR~*~*~*~SVEC','ROHR~*~*~*~QMAV','KNOT~*~*~*~PH'] # mxVecsFileData.columns.tolist() for all columns        
        >>> arrays=[[mxVecsFileData.index[0]]*len(colsToBeUnpacked),colsToBeUnpacked]
        >>> tuples = list(zip(*arrays))
        >>> import pandas as pd
        >>> mIndex = pd.MultiIndex.from_tuples(tuples, names=['Timestamp', 'Sir3sID'])        
        >>> mIndex
        MultiIndex(levels=[[2004-09-22 08:30:00+00:00], ['KNOT~*~*~*~PH', 'ROHR~*~*~*~QMAV', 'ROHR~*~*~*~SVEC']],
                   labels=[[0, 0, 0], [2, 1, 0]],
                   names=['Timestamp', 'Sir3sID'])
        >>> colIdx=mIndex.get_level_values('Sir3sID')
        >>> colIdx
        Index(['ROHR~*~*~*~SVEC', 'ROHR~*~*~*~QMAV', 'KNOT~*~*~*~PH'], dtype='object', name='Sir3sID')
        >>> colIdx.values.tolist()      
        ['ROHR~*~*~*~SVEC', 'ROHR~*~*~*~QMAV', 'KNOT~*~*~*~PH']
        >>> # construct MultiIndex End ... ---
        >>> mx.unPackMxsVecsFileDataDf(mxVecsFileData,mIndex,returnMultiIndex=False)
            ROHR~*~*~*~SVEC  ROHR~*~*~*~QMAV  KNOT~*~*~*~PH
        0          0.000000        -8.509475       2.302971
        1         88.019997        19.059780       3.985846
        2          0.000000       -15.378901       4.083384
        3        405.959991         8.509476       4.121495
        4          0.000000       -22.987946       2.043288
        5         83.550003        22.987946       2.283565
        6          0.000000        22.987947       2.004937
        7         88.019997        -3.928166       4.311307
        8          0.000000        22.987947       4.126019
        9         73.419998        15.378901       2.309655
        10         0.000000         3.928167       4.291591
        11       195.529999       -22.987946       2.000133
        12         0.000000       -19.059778       2.141440
        13        68.599998        -3.928166       3.825970
        14         0.000000         3.928167       2.000000
        15       109.769997       -22.987946       3.819467
        16         0.000000              NaN       2.314658
        17        76.400002              NaN       3.816599
        18         0.000000              NaN       2.312659
        19        83.550003              NaN       2.000000
        20         0.000000              NaN       3.845104
        21       164.910004              NaN       4.125885
        22         0.000000              NaN       3.814690
        23       195.529999              NaN            NaN
        24         0.000000              NaN            NaN
        25       405.959991              NaN            NaN
        26         0.000000              NaN            NaN
        27       164.910004              NaN            NaN
        28         0.000000              NaN            NaN
        29       109.769997              NaN            NaN
        30         0.000000              NaN            NaN
        31        76.400002              NaN            NaN
        >>> mx.unPackMxsVecsFileDataDf(mxVecsFileData,mIndex)        
                                                         0          1          2           3          4          5          6          7          8          9         10          11         12         13        14          15        16         17        18         19        20          21       22          23   24          25   26          27   28          29   30         31
        Timestamp                 Sir3sID                                                                                                                                                                                                                                                                                                                                                
        2004-09-22 08:30:00+00:00 ROHR~*~*~*~SVEC  0.000000  88.019997   0.000000  405.959991   0.000000  83.550003   0.000000  88.019997   0.000000  73.419998  0.000000  195.529999   0.000000  68.599998  0.000000  109.769997  0.000000  76.400002  0.000000  83.550003  0.000000  164.910004  0.00000  195.529999  0.0  405.959991  0.0  164.910004  0.0  109.769997  0.0  76.400002
                                  ROHR~*~*~*~QMAV -8.509475  19.059780 -15.378901    8.509476 -22.987946  22.987946  22.987947  -3.928166  22.987947  15.378901  3.928167  -22.987946 -19.059778  -3.928166  3.928167  -22.987946       NaN        NaN       NaN        NaN       NaN         NaN      NaN         NaN  NaN         NaN  NaN         NaN  NaN         NaN  NaN        NaN
                                  KNOT~*~*~*~PH    2.302971   3.985846   4.083384    4.121495   2.043288   2.283565   2.004937   4.311307   4.126019   2.309655  4.291591    2.000133   2.141440   3.825970  2.000000    3.819467  2.314658   3.816599  2.312659   2.000000  3.845104    4.125885  3.81469         NaN  NaN         NaN  NaN         NaN  NaN         NaN  NaN        NaN
        >>> dfs=[]
        >>> for idx,mxVecsFileData in enumerate(mxVecsFileDataLst):
        ...     arrays=[[mxVecsFileData.index[0]]*len(colsToBeUnpacked),colsToBeUnpacked]
        ...     tuples = list(zip(*arrays))        
        ...     mIndex = pd.MultiIndex.from_tuples(tuples, names=['Timestamp', 'Sir3sID'])               
        ...     dfs.append(mx.unPackMxsVecsFileDataDf(mxVecsFileData,mIndex))        
        >>> df=pd.concat(dfs)        
        >>> idx=pd.IndexSlice
        >>> dfOneVecChannel=df.loc[(idx[:],'KNOT~*~*~*~PH'),0:22] # df.loc[(idx[:],idx[:]),idx[:]]: everything   
        >>> dfOneVecChannel
                                                       0         1         2         3         4         5         6         7         8         9         10        11        12        13   14        15        16        17        18   19        20        21        22
        Timestamp                 Sir3sID                                                                                                                                                                                                                                  
        2004-09-22 08:30:00+00:00 KNOT~*~*~*~PH  2.302971  3.985846  4.083384  4.121495  2.043288  2.283565  2.004937  4.311307  4.126019  2.309655  4.291591  2.000133  2.141440  3.825970  2.0  3.819467  2.314658  3.816599  2.312659  2.0  3.845104  4.125885  3.814690
        2004-09-22 08:30:15+00:00 KNOT~*~*~*~PH  2.272133  3.034820  3.123339  3.157926  2.039330  2.255054  2.004493  3.331398  3.162040  2.277968  3.311887  2.000120  2.128487  2.892818  2.0  2.887151  2.282320  2.884661  2.280581  2.0  2.909634  3.161918  2.883003
        2004-09-22 08:30:30+00:00 KNOT~*~*~*~PH  2.144123  2.528542  2.576208  2.594833  2.021343  2.135238  2.002467  2.694164  2.597075  2.147196  2.676144  2.000063  2.069655  2.455464  2.0  2.452505  2.149524  2.451183  2.148594  2.0  2.464144  2.597010  2.450303
        2004-09-22 08:30:45+00:00 KNOT~*~*~*~PH  2.052100  2.183028  2.200011  2.206647  2.007717  2.048865  2.000910  2.248923  2.207463  2.053240  2.234365  2.000021  2.025138  2.156905  2.0  2.155822  2.054124  2.155325  2.053771  2.0  2.160025  2.207441  2.154995
        2004-09-22 08:31:00+00:00 KNOT~*~*~*~PH  2.302971  4.085822  4.183360  4.221471  2.043288  2.283566  2.004937  4.411284  4.225996  2.309655  4.391567  2.000133  2.141440  3.925947  2.0  3.919444  2.314658  3.916576  2.312659  2.0  3.945080  4.225861  3.914667
        >>> dfOneVecChannel.min()
        0     2.052100
        1     2.183028
        2     2.200011
        3     2.206647
        4     2.007717
        5     2.048865
        6     2.000910
        7     2.248923
        8     2.207463
        9     2.053240
        10    2.234365
        11    2.000021
        12    2.025138
        13    2.156905
        14    2.000000
        15    2.155822
        16    2.054124
        17    2.155325
        18    2.053771
        19    2.000000
        20    2.160025
        21    2.207441
        22    2.154995
        dtype: float64
        >>> df.min(level=1)
                               0          1          2           3          4          5         6          7         8          9         10          11         12         13       14          15        16         17        18         19        20          21        22          23   24          25   26          27   28          29   30         31
        Sir3sID                                                                                                                                                                                                                                                                                                                                              
        ROHR~*~*~*~SVEC  0.000000  88.019997   0.000000  405.959991   0.000000  83.550003  0.000000  88.019997  0.000000  73.419998  0.000000  195.529999   0.000000  68.599998  0.00000  109.769997  0.000000  76.400002  0.000000  83.550003  0.000000  164.910004  0.000000  195.529999  0.0  405.959991  0.0  164.910004  0.0  109.769997  0.0  76.400002
        ROHR~*~*~*~QMAV -8.509475   7.394749 -15.378901    3.256006 -22.987946   9.266180  9.266181  -3.928166  9.266181   5.923044  1.496261  -22.987946 -19.059778  -3.928166  1.49626  -22.987946       NaN        NaN       NaN        NaN       NaN         NaN       NaN         NaN  NaN         NaN  NaN         NaN  NaN         NaN  NaN        NaN
        KNOT~*~*~*~PH    2.052100   2.183028   2.200011    2.206647   2.007717   2.048865  2.000910   2.248923  2.207463   2.053240  2.234365    2.000021   2.025138   2.156905  2.00000    2.155822  2.054124   2.155325  2.053771   2.000000  2.160025    2.207441  2.154995         NaN  NaN         NaN  NaN         NaN  NaN         NaN  NaN        NaN
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            df=pd.DataFrame()
            colsToBeUnpacked=mIndex.get_level_values(1).values.tolist()      
      
            anError=False
            dct={}     
            colsUnpacked=[]
            for col in colsToBeUnpacked:
                #eine Spalte eines Frames liefert eine Series ...
                #2004-09-22 08:30:00+00:00  (-8.509474754333496,...)
                #Name: ROHR~*~*~*~QMAV
                try:
                    vecsFileDataOneCol=mxVecsFileData[col]
                                
                    #erster Wert der Series:
                    #Tuple:
                    #(-8.509474754333496,...)
                    vecsFileDataOneColResult=vecsFileDataOneCol[0]
    
                    #Series aus Tuple
                    vecsFileDataOneColResultSeries=pd.Series(vecsFileDataOneColResult)
                
                    #Series merken
                    dct[col]=vecsFileDataOneColResultSeries

                    colsUnpacked.append(col)
                except:                   
                    anError=True
            if anError:
                logger.error("{0:s}An error occured. Probably not all requested cols are available. Cols not available: {1:s}.".format(logStr,str(list(set(colsToBeUnpacked)-set(colsUnpacked)))))  
            #DataFrame aus Dct aus Series
            df=pd.DataFrame(dct)
            if returnMultiIndex:
                dfT=df.transpose(copy=True)
                df=pd.DataFrame(dfT.values,index=mIndex,columns=dfT.columns)
                                          
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}h5File: {:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,h5File,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                           
        finally:                      
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return df

    def getVecAggs(self,time1st=None,time1stIncluded=True,time2nd=None,time2ndIncluded=True):
        """Gets (or calcs) Aggregates (MIN, MAX, ...) of mxsVecsFileData between the 2 Times.   

        * Newly calced Aggregates are stored in dfVecAggs.

        Args:
            * time1st: TIMESTAMP (first if None)
            * time2nd: TIMESTAMP (last if None)
                           
        Returns:
            * dfs with MultiIndex: 
                * Level 0: 'MIN', 'MAX', ...
                * Level 1: col (Sir3sID)
                *  cols: mx2Idx

            * TIMESTAMPL: left  ScenTimeStamp included in calculating the Aggregate
            * TIMESTAMPR: right ScenTimeStamp included in calculating the Aggregate

        Raises:
            MxError
                
        >>> mx=mxs['LocalHeatingNetwork']   
        >>> mx.delFiles()      
        >>> mx.setResultsToMxsFile() # reads 5 TIMESTAMPS and constructs .vec.h5 while reading
        5
        >>> # check dfVecAggs to demonstrate how getVecAggs stores to / reads from getVecAggs
        >>> Sir3sIDs=mx.dfVecAggs.index.unique(level=1).values
        >>> len(Sir3sIDs)
        41
        >>> mx.dfVecAggs.index.unique(level=0).values
        array(['TIME', 'TMIN', 'TMAX'], dtype=object)
        >>> len(mx.dfVecAggs.columns.tolist())
        32
        >>> mx.dfVecAggs.shape # (3*41,32)
        (123, 32)
        >>> df,tL,tR=mx.getVecAggs()
        >>> mx.dfVecAggs.index.unique(level=0).values
        array(['TIME', 'TMIN', 'TMAX', 'MIN', 'MAX', 'DIF'], dtype=object)
        >>> mx.dfVecAggs.shape 
        (246, 32)
        >>> import pandas as pd
        >>> #idx=pd.IndexSlice        
        >>> df.loc[(['MIN','MAX','DIF'],'KNOT~*~*~*~PH'),0:22].round(6) ## df.loc[(slice(None),'KNOT~*~*~*~PH'),slice(None)] # df.loc[(idx[:],'KNOT~*~*~*~PH'),idx[:]]
                                  0         1         2         3         4         5         6         7         8         9         10        11        12        13   14        15        16        17        18   19        20        21        22
        TYPE Sir3sID                                                                                                                                                                                                                                  
        MIN  KNOT~*~*~*~PH  2.052100  2.183028  2.200011  2.206647  2.007717  2.048865  2.000910  2.248923  2.207463  2.053240  2.234365  2.000021  2.025138  2.156905  2.0  2.155822  2.054124  2.155325  2.053771  2.0  2.160025  2.207441  2.154995
        MAX  KNOT~*~*~*~PH  2.302971  4.085822  4.183360  4.221471  2.043288  2.283566  2.004937  4.411284  4.225996  2.309655  4.391567  2.000133  2.141440  3.925947  2.0  3.919444  2.314658  3.916576  2.312659  2.0  3.945080  4.225861  3.914667
        DIF  KNOT~*~*~*~PH  0.000000  0.099977  0.099977  0.099977  0.000000  0.000000  0.000000  0.099977  0.099977  0.000000  0.099977  0.000000  0.000000  0.099977  0.0  0.099977  0.000000  0.099977  0.000000  0.0  0.099977  0.099977  0.099977
        >>> # demonstrate how to transform an getVecAggs()-df-Result for Xm...
        >>> dfT=df.loc[('MIN',df.index.get_level_values(1).tolist()),:].transpose(copy=True) ## dfT=df.loc[('MIN',slice(None)),:].transpose(copy=True)   # dfT=df.loc[('MIN',idx[:]),idx[:]].transpose(copy=True)   
        >>> colIndex=dfT.columns.droplevel(level=0)
        >>> colIndex.name=None
        >>> pd.DataFrame(dfT.values,columns=colIndex)[['ROHR~*~*~*~SVEC', 'ROHR~*~*~*~QMAV', 'KNOT~*~*~*~PH']]
            ROHR~*~*~*~SVEC  ROHR~*~*~*~QMAV  KNOT~*~*~*~PH
        0          0.000000        -8.509475       2.052100
        1         88.019997         7.394749       2.183028
        2          0.000000       -15.378901       2.200011
        3        405.959991         3.256006       2.206647
        4          0.000000       -22.987946       2.007717
        5         83.550003         9.266180       2.048865
        6          0.000000         9.266181       2.000910
        7         88.019997        -3.928166       2.248923
        8          0.000000         9.266181       2.207463
        9         73.419998         5.923044       2.053240
        10         0.000000         1.496261       2.234365
        11       195.529999       -22.987946       2.000021
        12         0.000000       -19.059778       2.025138
        13        68.599998        -3.928166       2.156905
        14         0.000000         1.496260       2.000000
        15       109.769997       -22.987946       2.155822
        16         0.000000              NaN       2.054124
        17        76.400002              NaN       2.155325
        18         0.000000              NaN       2.053771
        19        83.550003              NaN       2.000000
        20         0.000000              NaN       2.160025
        21       164.910004              NaN       2.207441
        22         0.000000              NaN       2.154995
        23       195.529999              NaN            NaN
        24         0.000000              NaN            NaN
        25       405.959991              NaN            NaN
        26         0.000000              NaN            NaN
        27       164.910004              NaN            NaN
        28         0.000000              NaN            NaN
        29       109.769997              NaN            NaN
        30         0.000000              NaN            NaN
        31        76.400002              NaN            NaN
        >>> df,tL,tR=mx.getVecAggs()
        >>> mx.dfVecAggs.shape 
        (246, 32)
        >>> # demonstrate how to transform an AggEntry for Xm...
        >>> df=mx.dfVecAggs.loc[('TMIN',slice(None),mx.df.index[0],mx.df.index[-1]),:]
        >>> dfT=df.transpose(copy=True)
        >>> colIndex=dfT.columns.droplevel(level=0)
        >>> colIndex=colIndex.droplevel(level=1)
        >>> colIndex=colIndex.droplevel(level=1)
        >>> colIndex.name=None
        >>> pd.DataFrame(dfT.values,columns=colIndex)[['ROHR~*~*~*~SVEC', 'ROHR~*~*~*~QMAV', 'KNOT~*~*~*~PH']]
            ROHR~*~*~*~SVEC  ROHR~*~*~*~QMAV  KNOT~*~*~*~PH
        0          0.000000        -8.509475       2.052100
        1         88.019997         7.394749       2.183028
        2          0.000000       -15.378901       2.200011
        3        405.959991         3.256006       2.206647
        4          0.000000       -22.987946       2.007717
        5         83.550003         9.266180       2.048865
        6          0.000000         9.266181       2.000910
        7         88.019997        -3.928166       2.248923
        8          0.000000         9.266181       2.207463
        9         73.419998         5.923044       2.053240
        10         0.000000         1.496261       2.234365
        11       195.529999       -22.987946       2.000021
        12         0.000000       -19.059778       2.025138
        13        68.599998        -3.928166       2.156905
        14         0.000000         1.496260       2.000000
        15       109.769997       -22.987946       2.155822
        16         0.000000              NaN       2.054124
        17        76.400002              NaN       2.155325
        18         0.000000              NaN       2.053771
        19        83.550003              NaN       2.000000
        20         0.000000              NaN       2.160025
        21       164.910004              NaN       2.207441
        22         0.000000              NaN       2.154995
        23       195.529999              NaN            NaN
        24         0.000000              NaN            NaN
        25       405.959991              NaN            NaN
        26         0.000000              NaN            NaN
        27       164.910004              NaN            NaN
        28         0.000000              NaN            NaN
        29       109.769997              NaN            NaN
        30         0.000000              NaN            NaN
        31        76.400002              NaN            NaN
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:           
            df=pd.DataFrame()

            if time1st==None:
                time1st=self.df.index[0]
            if time2nd==None:
                time2nd=self.df.index[-1]

            if time2nd <= time1st:
                logger.error("{:s}Time2nd: {:s} <= Time1st {:s} ?!".format(logStr,str(time2nd),str(time1st)))    
                raise MxError
           
            if time1st not in self.df.index:
                logger.error("{:s}Time1st {:s} not available ?!".format(logStr,str(time1st)))    
                raise MxError      
            else:
                time1stIdx=self.df.index.get_loc(time1st)
                        
            if time2nd not in self.df.index:
                logger.error("{:s}Time2nd {:s} not available ?!".format(logStr,str(time2nd)))    
                raise MxError   
            else:
                time2ndIdx=self.df.index.get_loc(time2nd)

            if time2ndIncluded:
                time2ndIncludedOffset=1
            else:
                time2ndIncludedOffset=0
            if time1stIncluded:
                time1stIncludedOffset=0
            else:
                time1stIncludedOffset=1
            timesReq=list(self.df.index[time1stIdx+time1stIncludedOffset:time2ndIdx+time2ndIncludedOffset])  

            #check if Aggregates were already calculated
            inDfVecAggs=False
            if self.dfVecAggs.index.isin(['MIN'],level=0).any(): # 'MIN' (exemplarisch) existiert schon
                if self.dfVecAggs.loc[('MIN',slice(None),slice(None),slice(None)),:].index.isin([timesReq[0]],level=2).any(): # mit dieser ZeitL
                    if self.dfVecAggs.loc[('MIN',slice(None),timesReq[0],slice(None)),:].index.isin([timesReq[-1]],level=3).any(): # mit dieser ZeitR
                        inDfVecAggs=True

            if inDfVecAggs:                                 
                df=self.dfVecAggs.loc[(['MIN','MAX'],slice(None),timesReq[0],timesReq[-1]),:]
                mIndex=df.index.droplevel(level=3)
                mIndex=mIndex.droplevel(level=2)
                df=pd.DataFrame(df.values,index=mIndex,columns=df.columns)
                logger.debug("{:s}Index: MIN etc. {!s:30s} {!s:30s} already in dfVecAggs.".format(logStr,timesReq[0],timesReq[-1]))   

            if not inDfVecAggs:                                           
                # read the 1st Time
                mxVecsFileDataLst=self.getMxsVecsFileData(timesReq=[timesReq[0]])
                mxVecsFileData=mxVecsFileDataLst[0]
                # unpack it                
                Sir3sIDs=mxVecsFileData.columns.tolist()
             
                arrays=[[mxVecsFileData.index[0]]*len(Sir3sIDs),Sir3sIDs]
                tuples = list(zip(*arrays))        
                mIndex = pd.MultiIndex.from_tuples(tuples, names=['TYPE', 'Sir3sID'])               
                # store it with Time (create the df)
                df=self.unPackMxsVecsFileDataDf(mxVecsFileData,mIndex)            
                # calc Aggs
                dfAggs=getMxsVecsFileDataAggsCalcAggs(df,mIndex)            
                # store Aggs with Agg
                df=pd.concat([df,dfAggs])
                # 1 TIMETAMP 
                # all Aggregates

                # over all Times            
                oldTime=timesReq[0]
                for time in timesReq[1:]:               
                    # drop oldTime
                    df.drop(oldTime,level=0,inplace=True)
                    # add new Time
                    # read it
                    mxVecsFileDataLst=self.getMxsVecsFileData(timesReq=[time],fastMode=True) 
                    mxVecsFileData=mxVecsFileDataLst[0]
                    # unpack ...             
                    arrays=[[mxVecsFileData.index[0]]*len(Sir3sIDs),Sir3sIDs]
                    tuples = list(zip(*arrays))        
                    mIndex = pd.MultiIndex.from_tuples(tuples, names=['TYPE', 'Sir3sID'])               
                    # ... and store it  
                    df=pd.concat([df,self.unPackMxsVecsFileDataDf(mxVecsFileData,mIndex)])
                
                    # df:
                    # 1 (new) TIMETAMP 
                    # all (old) Aggs
                    dfAggs=getMxsVecsFileDataAggsCalcAggs(df,mIndex)
                
                    # drop old Aggs
                    df.drop('MIN',level=0,inplace=True)
                    df.drop('MAX',level=0,inplace=True)
            
                    # store new Aggs
                    df=pd.concat([df,dfAggs])
                    # 1 TIMETAMP 
                    # all Aggregates                
                               
                    oldTime=time
                
                df.drop(oldTime,level=0,inplace=True)                       
                #mIndex:
                #MultiIndex(levels=[[2019-01-01 00:30:00, 'MAX', 'MIN'],...: droped oldTime otherwise still in levels ?!: 
                mIndex=df.index.remove_unused_levels()
                
                df=pd.DataFrame(df.values,index=mIndex,columns=df.columns)
                
                # Read both Times
                mxVecsFileDataLst=self.getMxsVecsFileData(timesReq=[timesReq[0],timesReq[-1]],fastMode=True) 
                # construct Index for unpacking 
                arrays=[['DIF']*len(Sir3sIDs),Sir3sIDs]
                tuples=list(zip(*arrays))        
                mIndex=pd.MultiIndex.from_tuples(tuples, names=['TYPE', 'Sir3sID'])       
                # calc the difference
                dfDIF=self.unPackMxsVecsFileDataDf(mxVecsFileDataLst[1],mIndex).sub(self.unPackMxsVecsFileDataDf(mxVecsFileDataLst[0],mIndex))       
                # ... and store it  
                df=pd.concat([df,dfDIF])

                # store in dfVecAggs
                Sir3sIDs=df.index.unique(level=1).values
                for aggType in df.index.unique(level=0).values:
                    try:
                        arrays=[[aggType]*len(Sir3sIDs),Sir3sIDs,[timesReq[0].tz_localize(None)]*len(Sir3sIDs),[timesReq[-1].tz_localize(None)]*len(Sir3sIDs)]
                        tuples=list(zip(*arrays))        
                        mIndex=pd.MultiIndex.from_tuples(tuples,names=['TYPE','Sir3sID','TIMESTAMPL','TIMESTAMPR'])
                        self.dfVecAggs=pd.concat([self.dfVecAggs,pd.DataFrame(df.loc[(aggType,slice(None)),:].values,index=mIndex,columns=df.columns)])
                        logger.debug("{:s}Index: MIN etc. {!s:30s} {!s:30s} stored in dfVecAggs.".format(logStr,timesReq[0],timesReq[-1]))     
                    except Exception as e:
                        logStrFinal="{:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                        logger.error(logStrFinal) 
                        raise MxError(logStrFinal)       

                                          
        except MxError:
            raise
        except Exception as e:
            logStrFinal="{:s}: Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,aggType(e),str(e))
            logger.error(logStrFinal) 
            raise MxError(logStrFinal)                           
        finally:                      
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return df,timesReq[0],timesReq[-1]

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

            f=lambda x: "{:9.1f}".format(x)
            for colName in dfFiltered.columns.tolist():
                mo=re.match(reSir3sIDcompiled,colName)
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
        parser.add_argument('--dotResolution',type=str,default='.1',help="value for global 'dotResolution' i.e. .1 (default); use NONE for no dotResolution")      
        
        parser.add_argument("-m","--moduleTest", help="execute the Module's Doctest On/Off: -m 1 (default)", action="store",default='1')      
        parser.add_argument("-s","--singleTest", help="execute single Doctest: -s Mx: Doctest names matching Mx are executed", action="append",default=[])        

        args = parser.parse_args()

        if args.verbose:  # default         
            logger.setLevel(logging.DEBUG)  
        if args.quiet:    # Debug Messages are turned Off
            logger.setLevel(logging.ERROR)  
            args.verbose=False 
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        if args.dotResolution == 'NONE':
            args.dotResolution=''


        if args.moduleTest == '1':
            dtFinder=doctest.DocTestFinder(recurse=False,verbose=args.verbose) # recurse = False findet nur den Modultest
            suite=doctest.DocTestSuite(test_finder=dtFinder #,setUp=setUpFct
                                   ,globs={'testDir':args.testDir
                                           ,'dotResolution':args.dotResolution
                                           })   
            unittest.TextTestRunner().run(suite)
                   
        if len(args.singleTest)>0:
            testModels=['OneLPipe','LocalHeatingNetwork','GPipes','GPipe'] # ['LocalHeatingNetwork'] 
            mxs={} 
            for testModel in testModels:
                mx1File=os.path.join('.',os.path.join(args.testDir,'WD'+testModel+'\B1\V0\BZ1\M-1-0-1'+args.dotResolution+'.MX1')) 
                mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True) # avoid doing anything than just plain Init                               
                mxs[testModel]=mx

            dtFinder=doctest.DocTestFinder(verbose=args.verbose)
            dtRunner=doctest.DocTestRunner(verbose=args.verbose) 
            dTests=dtFinder.find(getMicrosecondsFromRefTime,globs={'testDir':args.testDir
                                          ,'dotResolution':args.dotResolution
                                           ,'mxs':mxs}) 
            dTests=dTests+dtFinder.find(Mx,globs={'testDir':args.testDir
                                          ,'dotResolution':args.dotResolution
                                           ,'mxs':mxs}) 
            for expr in args.singleTest:
                logger.debug("{0:s}{1:s}: {2:s} ...".format(logStr,'Searching Tests for Expr',expr))                
                testsForExpr=[test for test in dTests if re.search(expr,test.name) != None]
                for test in testsForExpr:                                           
                        logger.debug("{0:s}{1:s}: {2:s} ...".format(logStr,'Running Test',test.name)) 
                        dtRunner.run(test)        

            # Clean-Up
            for testModel in testModels:                                           
                mx=mxs[testModel]
                mx.delFiles()               
                if os.path.exists(mx.mxsZipFile):                        
                   os.remove(mx.mxsZipFile)
                mxsDumpFile=mx.mxsFile+'.dump'
                if os.path.exists(mxsDumpFile):                        
                   os.remove(mxsDumpFile)
               
        
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
