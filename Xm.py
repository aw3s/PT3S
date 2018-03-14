"""
SIR 3S XML ModelFile To pandas DataFrames
        One DataFrame per SIR 3S Objecttype 
Some Views As pandas DataFrames
        The Views are designed to deal with tedious groundwork 
        The Views are aggregated somhwat arbitrary ...
        ... however usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views 
---------------------------
DOCTEST
---------------------------
>>> # ---
>>> # Imports
>>> # ---
>>> import os
>>> import pandas as pd
>>> import logging
>>> logger = logging.getLogger('PT3S.Xm')  
>>> path = os.path.dirname(__file__)
>>> # ---
>>> # Clean Up
>>> # ---
>>> h5File=os.path.join(path,'testdata\OneLPipe.h5')
>>> if os.path.exists(h5File):                        
...    os.remove(h5File)
>>> # ---
>>> # Init
>>> # ---
>>> xmlFile=os.path.join(path,'testdata\OneLPipe.XML')
>>> xm=Xm(xmlFile=xmlFile)
>>> # ---
>>> # a View
>>> # ---
>>> v='vKNOT'
>>> v in xm.dataFrames
True
>>> isinstance(xm.dataFrames[v],pd.core.frame.DataFrame)
True
>>> # ---
>>> # ToH5
>>> # ---
>>> xm.ToH5()
>>> os.path.exists(xm.h5File) 
True
>>> # ---
>>> # force Read H5 instead of Xml
>>> # ---
>>> os.rename(xm.xmlFile,xm.xmlFile+'.blind')
>>> xm=Xm(xmlFile=xmlFile)
>>> os.rename(xm.xmlFile+'.blind',xm.xmlFile)
>>> # ---
>>> vKNOT=xm.dataFrames['vKNOT']
>>> vKNOT[(vKNOT.KTYP.isin(['QKON','PKON'])) & (vKNOT.BESCHREIBUNG.fillna('').str.startswith('Template Element')==False)].shape
(2, 24)
>>> vROHR=xm.dataFrames['vROHR']
>>> vROHR.shape
(1, 73)
>>> isinstance(vROHR['pXCors'],pd.core.series.Series)
True
>>> vROHR['pXCors'][0]
[0.0, 500.0]
>>> vROHR.pYCors[0]
[0.0, 0.0]
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.31',1,'Bugfix',"__convertAndFix: self.dataFrames['KNOT_BZ']['TE']=pd.Series() if missing")) 
>>> 'TE' not in xm.dataFrames['KNOT'].columns
True
>>> 'TE' in xm.dataFrames['KNOT_BZ'].columns
True
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.31',2,'New',"getWDirModelDirModelName()")) 
>>> (wDir,modelDir,modelName)=xm.getWDirModelDirModelName()
>>> modelName
'M-1-0-1'
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',1,'Change','ToH5: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',2,'Change','FromH5: finally: h5.close()')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.32',3,'Bugfix','__init__: NoH5Read=True')) 
>>> if os.path.exists(xm.h5File):                        
...    os.remove(xm.h5File)
>>> xm=Xm(xmlFile=xmlFile)
>>> xm.ToH5()
>>> os.path.exists(xm.h5File)
True
>>> xm=Xm(xmlFile=xmlFile,NoH5Read=True)
>>> os.path.exists(xm.h5File)
False
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.33',1,'Change','__vKNOT: pX/YCorZero')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.34',1,'New','__vWBLZ')) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.34',2,'New',"vFWVB['WBLZ']")) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.34',3,'New',"vFWVB ... vLFKT ... how='left'")) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.34',4,'New',"vNODE ... without Template Element ...")) 
>>> pd.set_option('display.max_columns',None)
>>> pd.set_option('display.width',6666)
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vKNOT']).replace('\\n','\\n   ')))
'''  NAME BESCHREIBUNG             IDREFERENZ      CONT CONT_ID  CONT_LFDNR  CONT_VKNO  KTYP LFAKT    QM_EIN QVAR_NAME  QM  QM_min  QM_max KVR  TE  TM XKOR YKOR ZKOR                   pk                   tk  pXCor  pYCor
   0    I          NaN  3S5642914844465475844  OneLPipe    1001         NaN        NaN  QKON     1  176.7146       NaN NaN     NaN     NaN   0 NaN  10  300  600   10  5642914844465475844  5642914844465475844    0.0    0.0
   1    K          NaN  3S5289899964753656852  OneLPipe    1001         NaN        NaN  PKON     1         0       NaN NaN     NaN     NaN   0 NaN  10  800  600   10  5289899964753656852  5289899964753656852  500.0    0.0'''
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vROHR']).replace('\\n','\\n   ')))
'''  BESCHREIBUNG             IDREFERENZ BAUJAHR HAL IPLANUNG KENNUNG      L LZU   RAU ZAUS ZEIN ZUML JLAMBS LAMBDA0 ASOLL INDSCHALL fk2LROHR KVR AUSFALLZEIT DA   DI   DN KT PN REHABILITATION REPARATUR  S WSTEIG WTIEFE LTGR_NAME  LTGR_BESCHREIBUNG SICHTBARKEIT VERLEGEART DTRO_NAME                           DTRO_BESCHREIBUNG        E fkSTRASSE fkSRAT                   pk                   tk IRTRENN LECKSTART LECKEND LECKMENGE LECKORT LECKSTATUS QSVB ZVLIMPTNZ KANTENZV      CONT CONT_ID  CONT_LFDNR NAME_i KVR_i TM_i XKOR_i YKOR_i ZKOR_i NAME_k KVR_k TM_k XKOR_k YKOR_k ZKOR_k  pXCor_i  pYCor_i  pXCor_k  pYCor_k        pXCors      pYCors    pWAYPXCors  pWAYPYCors                              WAYP
   0          NaN  3S4737064599036143765    2017   0        1       0  10000   0  0.25    0    0    0      1   0.025  1000         0       -1   0           0  0  250  250  0  0              0         0  0      0      0   STDROHR                NaN            1     999999   STDROHR  Standard-Druckrohre mit di = DN (DIN 2402)  2.1E+11        -1     -1  4737064599036143765  4737064599036143765       0         0       0         0       0          0    0         0        0  OneLPipe    1001         NaN      I     0   10    300    600     10      K     0   10    800    600     10      0.0      0.0    500.0      0.0  [0.0, 500.0]  [0.0, 0.0]  [0.0, 500.0]  [0.0, 0.0]  [(300.0, 600.0), (800.0, 600.0)]'''
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(xm.h5File):                        
...    os.remove(xm.h5File)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> xmlFile=os.path.join(path,'testdata\LocalHeatingNetwork.XML')
>>> xm=Xm(xmlFile=xmlFile)
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vKNOT']).replace('\\n','\\n   ')))
'''           NAME                    BESCHREIBUNG IDREFERENZ                                      CONT CONT_ID CONT_LFDNR CONT_VKNO  KTYP LFAKT QM_EIN QVAR_NAME  QM  QM_min  QM_max KVR  TE  TM     XKOR     YKOR ZKOR                   pk                   tk   pXCor  pYCor
   0        R-K004                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541539  5706361   20  4638663808856251977  4638663808856251977   799.0  152.0
   1        V-K002                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2541059  5706265   20  4731792362611615619  4731792362611615619   319.0   56.0
   2        V-K001                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2540867  5706228   20  4756962427318766791  4756962427318766791   127.0   19.0
   3        V-K000                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2540793  5706209   20  4766681917240867943  4766681917240867943    53.0    0.0
   4        R-K001                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2540867  5706228   20  4807712987325933680  4807712987325933680   127.0   19.0
   5        R-K003                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541457  5706345   20  4891048046264179170  4891048046264179170   717.0  136.0
   6        R-K000                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2540793  5706209   20  4979785838440534851  4979785838440534851    53.0    0.0
   7        R-K005                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541627  5706363   20  5183147862966701025  5183147862966701025   887.0  154.0
   8           R-L                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1      BHKW  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2540740  5706225   20  5356267303828212700  5356267303828212700     0.0   16.0
   9        R-K002                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541059  5706265   20  5364712333175450942  5364712333175450942   319.0   56.0
   10       V-K004                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2541539  5706361   20  5370423799772591808  5370423799772591808   799.0  152.0
   11       V-K005                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2541627  5706363   20  5444644492819213978  5444644492819213978   887.0  154.0
   12       R-K007                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541899  5706325   20  5508992300317633799  5508992300317633799  1159.0  116.0
   13       V-K006                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2541790  5706338   20  5515313800585145571  5515313800585145571  1050.0  129.0
   14       R-K006                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541790  5706338   20  5543326527366090679  5543326527366090679  1050.0  129.0
   15       V-K003                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2541457  5706345   20  5646671866542823796  5646671866542823796   717.0  136.0
   16          V-L                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1      BHKW  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2540740  5706240   20  5736262931552588702  5736262931552588702     0.0   31.0
   17       V-K007                            None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90  2541899  5706325   20  5741235692335544560  5741235692335544560  1159.0  116.0
   18           R2                            None         -1                                      BHKW    1002         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60      170       20   20  5002109894154139899  5002109894154139899   170.0   20.0
   19          V-1                            None         -1                                      BHKW    1002         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   1  10  90      140      160   20  5049461676240771430  5049461676240771430   140.0  160.0
   20           R3                            None         -1                                      BHKW    1002         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60      140       20   20  5219230031772497417  5219230031772497417   140.0   20.0
   21  PKON-Knoten  Druckhaltung - 2 bar Ruhedruck         -1                                      BHKW    1002         -1       NaN  PKON     1      0       NaN NaN     NaN     NaN   2  60  60      200       40   20  5397990465339071638  5397990465339071638   200.0   40.0
   22          R-1          Anbindung Druckhaltung         -1                                      BHKW    1002         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60      195       20   20  5557222628687032084  5557222628687032084   195.0   20.0'''
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vROHR']).replace('\\n','\\n   ')))
'''   BESCHREIBUNG IDREFERENZ BAUJAHR HAL IPLANUNG KENNUNG       L LZU  RAU ZAUS ZEIN ZUML JLAMBS LAMBDA0 ASOLL INDSCHALL             fk2LROHR KVR  AUSFALLZEIT     DA     DI   DN     KT  PN  REHABILITATION  REPARATUR    S WSTEIG WTIEFE LTGR_NAME            LTGR_BESCHREIBUNG SICHTBARKEIT VERLEGEART DTRO_NAME                        DTRO_BESCHREIBUNG        E fkSTRASSE fkSRAT                   pk                   tk IRTRENN LECKSTART LECKEND LECKMENGE LECKORT LECKSTATUS QSVB ZVLIMPTNZ KANTENZV                                      CONT CONT_ID CONT_LFDNR  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_i  pYCor_i  pXCor_k  pYCor_k            pXCors          pYCors                        pWAYPXCors                      pWAYPYCors                                               WAYP
   0          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0  4713733238627697042   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4613782368750024999  4613782368750024999       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K004     2   60  2541539  5706361     20  R-K005     2   60  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]                   [807.9, 895.95]                 [140.1, 142.05]  [(2541547.9, 5706349.1), (2541635.95, 5706351....
   1          None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0  5379365049009065623   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4614949065966596185  4614949065966596185       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K002     1   90  2541059  5706265     20  V-K003     1   90  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]                   [319.0, 716.95]          [56.0499999998, 136.0]  [(2541059.0, 5706265.05), (2541456.95, 5706345...
   2          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0  5037777106796980248   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4637102239750163477  4637102239750163477       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K003     2   60  2541457  5706345     20  R-K004     2   60  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]                   [725.85, 807.9]                 [124.05, 140.1]  [(2541465.85, 5706333.05), (2541547.9, 5706349...
   3          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0  4613782368750024999   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4713733238627697042  4713733238627697042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K004     1   90  2541539  5706361     20  V-K005     1   90  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]                   [799.0, 887.05]                  [152.0, 154.0]  [(2541539.0, 5706361.0), (2541627.05, 5706363.0)]
   4          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0  5266224553324203132   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4789218195240364437  4789218195240364437       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K001     1   90  2540867  5706228     20  V-K002     1   90  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]                    [127.0, 319.0]           [19.0, 56.0499999998]  [(2540867.0, 5706228.0), (2541059.0, 5706265.05)]
   5          None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0  5620197984230756681   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4945727430885351042  4945727430885351042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K006     2   60  2541790  5706338     20  R-K007     2   60  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]                 [1058.85, 1167.9]                  [117.0, 104.1]  [(2541798.85, 5706326.0), (2541907.9, 5706313.1)]
   6          None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0  5647213228462830353   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4984202422877610920  4984202422877610920       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K000     1   90  2540793  5706209     20  V-K001     1   90  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]            [53.0499999998, 127.0]        [-0.0499999998137, 19.0]  [(2540793.05, 5706208.95), (2540867.0, 5706228...
   7          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0  4637102239750163477   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5037777106796980248  5037777106796980248       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K003     1   90  2541457  5706345     20  V-K004     1   90  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]                   [716.95, 799.0]                  [136.0, 152.0]  [(2541456.95, 5706345.0), (2541539.0, 5706361.0)]
   8          None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0  5611703699850694889   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5123819811204259837  5123819811204259837       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K005     1   90  2541627  5706363     20  V-K006     1   90  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]                 [887.05, 1049.95]                 [154.0, 128.95]  [(2541627.05, 5706363.0), (2541789.95, 5706337...
   9          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0  4789218195240364437   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5266224553324203132  5266224553324203132       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K001     2   60  2540867  5706228     20  R-K002     2   60  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]                    [135.9, 327.9]  [7.04999999981, 44.0999999996]  [(2540875.9, 5706216.05), (2541067.9, 5706253.1)]
   10         None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0  4614949065966596185   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5379365049009065623  5379365049009065623       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K002     2   60  2541059  5706265     20  R-K003     2   60  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]                   [327.9, 725.85]         [44.0999999996, 124.05]  [(2541067.9, 5706253.1), (2541465.85, 5706333....
   11         None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0  5123819811204259837   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5611703699850694889  5611703699850694889       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K005     2   60  2541627  5706363     20  R-K006     2   60  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]                 [895.95, 1058.85]                 [142.05, 117.0]  [(2541635.95, 5706351.05), (2541798.85, 570632...
   12         None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0  4945727430885351042   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5620197984230756681  5620197984230756681       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K006     1   90  2541790  5706338     20  V-K007     1   90  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]                 [1049.95, 1159.0]                [128.95, 116.05]  [(2541789.95, 5706337.95), (2541899.0, 5706325...
   13         None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0  4984202422877610920   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5647213228462830353  5647213228462830353       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K000     2   60  2540793  5706209     20  R-K001     2   60  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]            [61.9500000002, 135.9]          [-12.0, 7.04999999981]  [(2540801.95, 5706197.0), (2540875.9, 5706216....
   14         None         -1    None   0        1       0   73.42   0  0.1    0    0    0      1   0.025  1000         0  4939422678063487923   2          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4769996343148550485  4769996343148550485       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     R-L     2   60  2540740  5706225     20  R-K000     2   60  2540793  5706209     20      0.0     16.0     53.0      0.0       [0.0, 53.0]     [16.0, 0.0]  [0.0, 24.0, 45.0, 61.9500000002]      [16.0, 16.0, -12.0, -12.0]  [(2540740.0, 5706225.0), (2540764.0, 5706225.0...
   15         None         -1    None   0        1       0    68.6   0  0.1    0    0    0      1   0.025  1000         0  4769996343148550485   1          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4939422678063487923  4939422678063487923       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     V-L     1   90  2540740  5706240     20  V-K000     1   90  2540793  5706209     20      0.0     31.0     53.0      0.0       [0.0, 53.0]     [31.0, 0.0]        [0.0, 30.0, 53.0499999998]  [31.0, 31.0, -0.0499999998137]  [(2540740.0, 5706240.0), (2540770.0, 5706240.0...'''
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vWBLZ']).replace('\\n','\\n   ')))
'''   AKTIV BESCHREIBUNG IDIM       NAME                OBJID OBJTYPE                   pk
   0      1  Wärmebilanz    0      BLNZ1  4731792362611615619    KNOT  5579937562601803472
   1      1  Wärmebilanz    0      BLNZ1  5364712333175450942    KNOT  5579937562601803472
   2      1  Wärmebilanz    0      BLNZ5  5183147862966701025    KNOT  5581152085151655438
   3      1  Wärmebilanz    0      BLNZ5  5444644492819213978    KNOT  5581152085151655438
   4      1  Wärmebilanz    0    BLNZ1u5  5183147862966701025    KNOT  5187647097142898375
   5      1  Wärmebilanz    0    BLNZ1u5  5444644492819213978    KNOT  5187647097142898375
   6      1  Wärmebilanz    0    BLNZ1u5  4731792362611615619    KNOT  5187647097142898375
   7      1  Wärmebilanz    0    BLNZ1u5  5364712333175450942    KNOT  5187647097142898375
   8      1  Wärmebilanz    0  BLNZ1u5u7  5183147862966701025    KNOT  4694700216019268978
   9      1  Wärmebilanz    0  BLNZ1u5u7  5444644492819213978    KNOT  4694700216019268978
   10     1  Wärmebilanz    0  BLNZ1u5u7  4731792362611615619    KNOT  4694700216019268978
   11     1  Wärmebilanz    0  BLNZ1u5u7  5364712333175450942    KNOT  4694700216019268978
   12     1  Wärmebilanz    0  BLNZ1u5u7  5508992300317633799    KNOT  4694700216019268978
   13     1  Wärmebilanz    0  BLNZ1u5u7  5741235692335544560    KNOT  4694700216019268978'''
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vFWVB']).replace('\\n','\\n   ')))
'''  BESCHREIBUNG IDREFERENZ   W0  LFK  TVL0  TRS0 LFKT   W  W_min  W_max  INDTR  TRSK  VTYP  IMBG  IRFV                   pk                   tk  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  pXCor_i  pYCor_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_k  pYCor_k                                      CONT CONT_ID CONT_LFDNR                         WBLZ
   0            1         -1  200  0.8    90    50  NaN NaN    NaN    NaN      1    55     1     0   0.0  4643800032883366034  4643800032883366034  V-K002     1   90  2541059  5706265     20    319.0     56.0  R-K002     2   60  2541059  5706265     20    319.0     56.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  [BLNZ1, BLNZ1u5, BLNZ1u5u7]
   1            3         -1  200  1.0    90    65  NaN NaN    NaN    NaN      1    65     1     0   0.0  4704603947372595298  4704603947372595298  V-K004     1   90  2541539  5706361     20    799.0    152.0  R-K004     2   60  2541539  5706361     20    799.0    152.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           []
   2            4         -1  200  0.8    90    60  NaN NaN    NaN    NaN      1    60     1     0   0.0  5121101823283893406  5121101823283893406  V-K005     1   90  2541627  5706363     20    887.0    154.0  R-K005     2   60  2541627  5706363     20    887.0    154.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  [BLNZ1u5, BLNZ1u5u7, BLNZ5]
   3            5         -1  200  0.8    90    55  NaN NaN    NaN    NaN      1    55     1     0   0.0  5400405917816384862  5400405917816384862  V-K007     1   90  2541899  5706325     20   1159.0    116.0  R-K007     2   60  2541899  5706325     20   1159.0    116.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                  [BLNZ1u5u7]
   4            2         -1  200  0.6    90    60  NaN NaN    NaN    NaN      1    62     1     0   0.0  5695730293103267172  5695730293103267172  V-K003     1   90  2541457  5706345     20    717.0    136.0  R-K003     2   60  2541457  5706345     20    717.0    136.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           []'''
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.34',5,'New',"vNRCV")) 
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.34',6,'New',"vNRCV_Mx1")) 
>>> pd.set_option('display.max_rows',None)
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vLAYR'].sort_values(['LFDNR','NAME','OBJTYPE','OBJID'],ascending=True)).replace('\\n','\\n   ')))
'''   LFDNR           NAME OBJTYPE                OBJID                   pk                   tk  nrObjInGroup  nrObjtypeInGroup
   0      1        Vorlauf    FWES  5638756766880678918  5206516471428693478  5206516471428693478             1                 1
   1      1        Vorlauf    KNOT  4731792362611615619  5206516471428693478  5206516471428693478             2                 1
   2      1        Vorlauf    KNOT  4756962427318766791  5206516471428693478  5206516471428693478             3                 2
   3      1        Vorlauf    KNOT  4766681917240867943  5206516471428693478  5206516471428693478             4                 3
   4      1        Vorlauf    KNOT  5049461676240771430  5206516471428693478  5206516471428693478             5                 4
   5      1        Vorlauf    KNOT  5370423799772591808  5206516471428693478  5206516471428693478             6                 5
   6      1        Vorlauf    KNOT  5444644492819213978  5206516471428693478  5206516471428693478             7                 6
   7      1        Vorlauf    KNOT  5515313800585145571  5206516471428693478  5206516471428693478             8                 7
   8      1        Vorlauf    KNOT  5646671866542823796  5206516471428693478  5206516471428693478             9                 8
   9      1        Vorlauf    KNOT  5736262931552588702  5206516471428693478  5206516471428693478            10                 9
   10     1        Vorlauf    KNOT  5741235692335544560  5206516471428693478  5206516471428693478            11                10
   11     1        Vorlauf    ROHR  4614949065966596185  5206516471428693478  5206516471428693478            12                 1
   12     1        Vorlauf    ROHR  4713733238627697042  5206516471428693478  5206516471428693478            13                 2
   13     1        Vorlauf    ROHR  4789218195240364437  5206516471428693478  5206516471428693478            14                 3
   14     1        Vorlauf    ROHR  4939422678063487923  5206516471428693478  5206516471428693478            15                 4
   15     1        Vorlauf    ROHR  4984202422877610920  5206516471428693478  5206516471428693478            16                 5
   16     1        Vorlauf    ROHR  5037777106796980248  5206516471428693478  5206516471428693478            17                 6
   17     1        Vorlauf    ROHR  5123819811204259837  5206516471428693478  5206516471428693478            18                 7
   18     1        Vorlauf    ROHR  5620197984230756681  5206516471428693478  5206516471428693478            19                 8
   19     1        Vorlauf    VENT  4678923650983295610  5206516471428693478  5206516471428693478            20                 1
   20     2       Rücklauf    KLAP  4801110583764519435  4693347477612662930  4693347477612662930             1                 1
   21     2       Rücklauf    KNOT  4638663808856251977  4693347477612662930  4693347477612662930             2                 1
   22     2       Rücklauf    KNOT  4807712987325933680  4693347477612662930  4693347477612662930             3                 2
   23     2       Rücklauf    KNOT  4891048046264179170  4693347477612662930  4693347477612662930             4                 3
   24     2       Rücklauf    KNOT  4979785838440534851  4693347477612662930  4693347477612662930             5                 4
   25     2       Rücklauf    KNOT  5002109894154139899  4693347477612662930  4693347477612662930             6                 5
   26     2       Rücklauf    KNOT  5183147862966701025  4693347477612662930  4693347477612662930             7                 6
   27     2       Rücklauf    KNOT  5219230031772497417  4693347477612662930  4693347477612662930             8                 7
   28     2       Rücklauf    KNOT  5356267303828212700  4693347477612662930  4693347477612662930             9                 8
   29     2       Rücklauf    KNOT  5364712333175450942  4693347477612662930  4693347477612662930            10                 9
   30     2       Rücklauf    KNOT  5397990465339071638  4693347477612662930  4693347477612662930            11                10
   31     2       Rücklauf    KNOT  5508992300317633799  4693347477612662930  4693347477612662930            12                11
   32     2       Rücklauf    KNOT  5543326527366090679  4693347477612662930  4693347477612662930            13                12
   33     2       Rücklauf    KNOT  5557222628687032084  4693347477612662930  4693347477612662930            14                13
   34     2       Rücklauf    PUMP  5481331875203087055  4693347477612662930  4693347477612662930            15                 1
   35     2       Rücklauf    ROHR  4613782368750024999  4693347477612662930  4693347477612662930            16                 1
   36     2       Rücklauf    ROHR  4637102239750163477  4693347477612662930  4693347477612662930            17                 2
   37     2       Rücklauf    ROHR  4769996343148550485  4693347477612662930  4693347477612662930            18                 3
   38     2       Rücklauf    ROHR  4945727430885351042  4693347477612662930  4693347477612662930            19                 4
   39     2       Rücklauf    ROHR  5266224553324203132  4693347477612662930  4693347477612662930            20                 5
   40     2       Rücklauf    ROHR  5379365049009065623  4693347477612662930  4693347477612662930            21                 6
   41     2       Rücklauf    ROHR  5611703699850694889  4693347477612662930  4693347477612662930            22                 7
   42     2       Rücklauf    ROHR  5647213228462830353  4693347477612662930  4693347477612662930            23                 8
   43     2       Rücklauf    VENT  4897018421024717974  4693347477612662930  4693347477612662930            24                 1
   44     2       Rücklauf    VENT  5525310316015533093  4693347477612662930  4693347477612662930            25                 2
   45     3  Kundenanlagen    FWVB  4643800032883366034  5003333277973347346  5003333277973347346             1                 1
   46     3  Kundenanlagen    FWVB  4704603947372595298  5003333277973347346  5003333277973347346             2                 2
   47     3  Kundenanlagen    FWVB  5121101823283893406  5003333277973347346  5003333277973347346             3                 3
   48     3  Kundenanlagen    FWVB  5400405917816384862  5003333277973347346  5003333277973347346             4                 4
   49     3  Kundenanlagen    FWVB  5695730293103267172  5003333277973347346  5003333277973347346             5                 5
   50     4           BHKW    BSYM  5043395081363401573  5555393404073362943  5555393404073362943             1                 1
   51     4           BHKW    TEXT  5056836766824229789  5555393404073362943  5555393404073362943             2                 1
   52     4           BHKW    TEXT  5329748935118523443  5555393404073362943  5555393404073362943             3                 2
   53     5          Texte    ARRW  4664845735864571219  5394410243594912680  5394410243594912680             1                 1
   54     5          Texte    ARRW  4902474974831811106  5394410243594912680  5394410243594912680             2                 2
   55     5          Texte    ARRW  5026846801782366678  5394410243594912680  5394410243594912680             3                 3
   56     5          Texte    ARRW  5688313372729413840  5394410243594912680  5394410243594912680             4                 4
   57     5          Texte    NRCV  4681213816714574464  5394410243594912680  5394410243594912680             5                 1
   58     5          Texte    NRCV  4857294696992797631  5394410243594912680  5394410243594912680             6                 2
   59     5          Texte    NRCV  4914949875368816179  5394410243594912680  5394410243594912680             7                 3
   60     5          Texte    NRCV  4946584950744559030  5394410243594912680  5394410243594912680             8                 4
   61     5          Texte    NRCV  4968703141722117357  5394410243594912680  5394410243594912680             9                 5
   62     5          Texte    NRCV  5091374651838464239  5394410243594912680  5394410243594912680            10                 6
   63     5          Texte    NRCV  5097127385155151127  5394410243594912680  5394410243594912680            11                 7
   64     5          Texte    NRCV  5179988968597313889  5394410243594912680  5394410243594912680            12                 8
   65     5          Texte    NRCV  5281885868749421521  5394410243594912680  5394410243594912680            13                 9
   66     5          Texte    NRCV  5410904806390050339  5394410243594912680  5394410243594912680            14                10
   67     5          Texte    NRCV  5476262878682325254  5394410243594912680  5394410243594912680            15                11
   68     5          Texte    NRCV  5557806245003742769  5394410243594912680  5394410243594912680            16                12
   69     5          Texte    RECT  4994817837124479818  5394410243594912680  5394410243594912680            17                 1
   70     5          Texte    RPFL  5158870568935841216  5394410243594912680  5394410243594912680            18                 1
   71     5          Texte    TEXT  4628671704393700430  5394410243594912680  5394410243594912680            19                 1
   72     5          Texte    TEXT  4654104397990769217  5394410243594912680  5394410243594912680            20                 2
   73     5          Texte    TEXT  4666644549022031339  5394410243594912680  5394410243594912680            21                 3
   74     5          Texte    TEXT  4693143208412077585  5394410243594912680  5394410243594912680            22                 4
   75     5          Texte    TEXT  4768731522550494423  5394410243594912680  5394410243594912680            23                 5
   76     5          Texte    TEXT  4770844990228490264  5394410243594912680  5394410243594912680            24                 6
   77     5          Texte    TEXT  4782197969172967134  5394410243594912680  5394410243594912680            25                 7
   78     5          Texte    TEXT  4855692488683645764  5394410243594912680  5394410243594912680            26                 8
   79     5          Texte    TEXT  4965628942555351751  5394410243594912680  5394410243594912680            27                 9
   80     5          Texte    TEXT  4995961504641886710  5394410243594912680  5394410243594912680            28                10
   81     5          Texte    TEXT  5017907661719368413  5394410243594912680  5394410243594912680            29                11
   82     5          Texte    TEXT  5028052147238787802  5394410243594912680  5394410243594912680            30                12
   83     5          Texte    TEXT  5036153631350515544  5394410243594912680  5394410243594912680            31                13
   84     5          Texte    TEXT  5054433315422452796  5394410243594912680  5394410243594912680            32                14
   85     5          Texte    TEXT  5108336975548011049  5394410243594912680  5394410243594912680            33                15
   86     5          Texte    TEXT  5262441422409836340  5394410243594912680  5394410243594912680            34                16
   87     5          Texte    TEXT  5297832234834839298  5394410243594912680  5394410243594912680            35                17
   88     5          Texte    TEXT  5370727463979416592  5394410243594912680  5394410243594912680            36                18
   89     5          Texte    TEXT  5421223289472778073  5394410243594912680  5394410243594912680            37                19
   90     5          Texte    TEXT  5501963349880613918  5394410243594912680  5394410243594912680            38                20
   91     5          Texte    TEXT  5502619581048467908  5394410243594912680  5394410243594912680            39                21
   92     5          Texte    TEXT  5540395812045688781  5394410243594912680  5394410243594912680            40                22
   93     5          Texte    TEXT  5550982489075668484  5394410243594912680  5394410243594912680            41                23
   94     5          Texte    TEXT  5610916400841895317  5394410243594912680  5394410243594912680            42                24
   95     5          Texte    TEXT  5646820849868629537  5394410243594912680  5394410243594912680            43                25
   96     5          Texte    TEXT  5696590398594231893  5394410243594912680  5394410243594912680            44                26
   97     5          Texte    TEXT  5697088036451277538  5394410243594912680  5394410243594912680            45                27'''
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.39',1,'New',"vNRCV: pXYLB")) 
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vNRCV'].sort_values(['OBJTYPE','fkOBJTYPE','ATTRTYPE','cRefLfdNr'],ascending=True)).replace('\\n','\\n   ')))
'''   cRefLfdNr                                      CONT CONT_ID CONT_LFDNR         DPGR OBJTYPE            fkOBJTYPE ATTRTYPE              pk_ROWS              tk_ROWS                   pk                   tk                                  pXYLB
   0          1                                      BHKW    1002         -1  UserDefined    FWES  5638756766880678918        W  5762106696740202356  5762106696740202356  4857294696992797631  4857294696992797631                           (90.0, 65.0)
   1          1                                      BHKW    1002         -1  UserDefined    KNOT  5049461676240771430        T  4723443975311885965  4723443975311885965  5097127385155151127  5097127385155151127                           (90.0, 95.0)
   2          1                                      BHKW    1002         -1  UserDefined    KNOT  5219230031772497417        T  5602301870151014230  5602301870151014230  5557806245003742769  5557806245003742769                           (90.0, 35.0)
   3          1                                      BHKW    1002         -1  UserDefined    KNOT  5356267303828212700       PH  5000989080893535213  5000989080893535213  4968703141722117357  4968703141722117357                          (220.0, 25.0)
   4          1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  UserDefined    KNOT  5397990465339071638       QM  5134531789044068877  5134531789044068877  5410059595276504750  5410059595276504750                          (91.0, -94.0)
   5          2                                      BHKW    1002         -1  UserDefined    KNOT  5397990465339071638       QM  5134531789044068877  5134531789044068877  5357021981944933535  5357021981944933535  (184.999999464624, 57.99999953107601)
   6          1                                      BHKW    1002         -1  UserDefined    KNOT  5736262931552588702       PH  4754881272083464445  4754881272083464445  4681213816714574464  4681213816714574464                          (220.0, 85.0)
   7          1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  UserDefined    KNOT  5741235692335544560       DP  4949183695502554728  4949183695502554728  4914949875368816179  4914949875368816179                         (1234.0, 83.0)
   8          1                                      BHKW    1002         -1  UserDefined    PUMP  5481331875203087055        N  5563842594211689762  5563842594211689762  5091374651838464239  5091374651838464239                          (170.0, 45.0)
   9          1                                      BHKW    1002         -1  UserDefined    VENT  4678923650983295610       QM  5126307362398248950  5126307362398248950  5410904806390050339  5410904806390050339                         (200.0, 110.0)
   10         1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  UserDefined    WBLZ  4694700216019268978      WVB  4778244458749966216  4778244458749966216  4991097791264453745  4991097791264453745                        (354.0, -225.0)
   11         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299      WES  5690691957596882133  5690691957596882133  5179988968597313889  5179988968597313889                          (90.0, 155.0)
   12         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299    WSPEI  5153847813311339683  5153847813311339683  4946584950744559030  4946584950744559030                          (90.0, 140.0)
   13         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299      WVB  5214984699859365639  5214984699859365639  5281885868749421521  5281885868749421521                          (90.0, 150.0)
   14         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299    WVERL  4722863010266870887  4722863010266870887  5476262878682325254  5476262878682325254                          (90.0, 145.0)'''
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.37',1,'New',"Mx(),__Mx2() and ReOrg __Mx1()")) 
>>> vROHR=xm.dataFrames['vROHR']
>>> vROHR.shape
(16, 73)
>>> 'vNRCV_Mx1' in xm.dataFrames
False
>>> xm.Mx()
>>> 'vNRCV_Mx1' in xm.dataFrames
True
>>> vROHR.shape
(16, 75)
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vROHR']).replace('\\n','\\n   ')))
'''   BESCHREIBUNG IDREFERENZ BAUJAHR HAL IPLANUNG KENNUNG       L LZU  RAU ZAUS ZEIN ZUML JLAMBS LAMBDA0 ASOLL INDSCHALL             fk2LROHR KVR  AUSFALLZEIT     DA     DI   DN     KT  PN  REHABILITATION  REPARATUR    S WSTEIG WTIEFE LTGR_NAME            LTGR_BESCHREIBUNG SICHTBARKEIT VERLEGEART DTRO_NAME                        DTRO_BESCHREIBUNG        E fkSTRASSE fkSRAT                   pk                   tk IRTRENN LECKSTART LECKEND LECKMENGE LECKORT LECKSTATUS QSVB ZVLIMPTNZ KANTENZV                                      CONT CONT_ID CONT_LFDNR  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_i  pYCor_i  pXCor_k  pYCor_k            pXCors          pYCors                        pWAYPXCors                      pWAYPYCors                                               WAYP  mx2Idx  mx2NofPts
   0          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0  4713733238627697042   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4613782368750024999  4613782368750024999       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K004     2   60  2541539  5706361     20  R-K005     2   60  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]                   [807.9, 895.95]                 [140.1, 142.05]  [(2541547.9, 5706349.1), (2541635.95, 5706351....       0          2
   1          None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0  5379365049009065623   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4614949065966596185  4614949065966596185       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K002     1   90  2541059  5706265     20  V-K003     1   90  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]                   [319.0, 716.95]          [56.0499999998, 136.0]  [(2541059.0, 5706265.05), (2541456.95, 5706345...       1          2
   2          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0  5037777106796980248   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4637102239750163477  4637102239750163477       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K003     2   60  2541457  5706345     20  R-K004     2   60  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]                   [725.85, 807.9]                 [124.05, 140.1]  [(2541465.85, 5706333.05), (2541547.9, 5706349...       2          2
   3          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0  4613782368750024999   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4713733238627697042  4713733238627697042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K004     1   90  2541539  5706361     20  V-K005     1   90  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]                   [799.0, 887.05]                  [152.0, 154.0]  [(2541539.0, 5706361.0), (2541627.05, 5706363.0)]       3          2
   4          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0  5266224553324203132   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4789218195240364437  4789218195240364437       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K001     1   90  2540867  5706228     20  V-K002     1   90  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]                    [127.0, 319.0]           [19.0, 56.0499999998]  [(2540867.0, 5706228.0), (2541059.0, 5706265.05)]       5          2
   5          None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0  5620197984230756681   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4945727430885351042  4945727430885351042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K006     2   60  2541790  5706338     20  R-K007     2   60  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]                 [1058.85, 1167.9]                  [117.0, 104.1]  [(2541798.85, 5706326.0), (2541907.9, 5706313.1)]       7          2
   6          None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0  5647213228462830353   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4984202422877610920  4984202422877610920       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K000     1   90  2540793  5706209     20  V-K001     1   90  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]            [53.0499999998, 127.0]        [-0.0499999998137, 19.0]  [(2540793.05, 5706208.95), (2540867.0, 5706228...       8          2
   7          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0  4637102239750163477   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5037777106796980248  5037777106796980248       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K003     1   90  2541457  5706345     20  V-K004     1   90  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]                   [716.95, 799.0]                  [136.0, 152.0]  [(2541456.95, 5706345.0), (2541539.0, 5706361.0)]       9          2
   8          None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0  5611703699850694889   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5123819811204259837  5123819811204259837       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K005     1   90  2541627  5706363     20  V-K006     1   90  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]                 [887.05, 1049.95]                 [154.0, 128.95]  [(2541627.05, 5706363.0), (2541789.95, 5706337...      10          2
   9          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0  4789218195240364437   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5266224553324203132  5266224553324203132       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K001     2   60  2540867  5706228     20  R-K002     2   60  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]                    [135.9, 327.9]  [7.04999999981, 44.0999999996]  [(2540875.9, 5706216.05), (2541067.9, 5706253.1)]      11          2
   10         None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0  4614949065966596185   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5379365049009065623  5379365049009065623       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K002     2   60  2541059  5706265     20  R-K003     2   60  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]                   [327.9, 725.85]         [44.0999999996, 124.05]  [(2541067.9, 5706253.1), (2541465.85, 5706333....      12          2
   11         None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0  5123819811204259837   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5611703699850694889  5611703699850694889       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K005     2   60  2541627  5706363     20  R-K006     2   60  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]                 [895.95, 1058.85]                 [142.05, 117.0]  [(2541635.95, 5706351.05), (2541798.85, 570632...      13          2
   12         None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0  4945727430885351042   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5620197984230756681  5620197984230756681       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K006     1   90  2541790  5706338     20  V-K007     1   90  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]                 [1049.95, 1159.0]                [128.95, 116.05]  [(2541789.95, 5706337.95), (2541899.0, 5706325...      14          2
   13         None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0  4984202422877610920   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5647213228462830353  5647213228462830353       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K000     2   60  2540793  5706209     20  R-K001     2   60  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]            [61.9500000002, 135.9]          [-12.0, 7.04999999981]  [(2540801.95, 5706197.0), (2540875.9, 5706216....      15          2
   14         None         -1    None   0        1       0   73.42   0  0.1    0    0    0      1   0.025  1000         0  4939422678063487923   2          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4769996343148550485  4769996343148550485       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     R-L     2   60  2540740  5706225     20  R-K000     2   60  2540793  5706209     20      0.0     16.0     53.0      0.0       [0.0, 53.0]     [16.0, 0.0]  [0.0, 24.0, 45.0, 61.9500000002]      [16.0, 16.0, -12.0, -12.0]  [(2540740.0, 5706225.0), (2540764.0, 5706225.0...       4          2
   15         None         -1    None   0        1       0    68.6   0  0.1    0    0    0      1   0.025  1000         0  4769996343148550485   1          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4939422678063487923  4939422678063487923       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     V-L     1   90  2540740  5706240     20  V-K000     1   90  2540793  5706209     20      0.0     31.0     53.0      0.0       [0.0, 53.0]     [31.0, 0.0]        [0.0, 30.0, 53.0499999998]  [31.0, 31.0, -0.0499999998137]  [(2540740.0, 5706240.0), (2540770.0, 5706240.0...       6          2'''
>>> xmlFile=os.path.join(path,'testdata\LocalHeatingNetwork.XML')
>>> xm=Xm(xmlFile=xmlFile)
>>> vROHR=xm.dataFrames['vROHR']
>>> (wDir,modelDir,modelName)=xm.getWDirModelDirModelName()
>>> mx1File=os.path.join(wDir,os.path.join(modelDir,modelName))+'.MX1'    
>>> mx=Mx(mx1File=mx1File)
>>> vROHR.shape
(16, 73)
>>> 'vNRCV_Mx1' in xm.dataFrames
False
>>> xm.Mx(mx=mx)
>>> vROHR.shape
(16, 75)
>>> 'vNRCV_Mx1' in xm.dataFrames
True
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.39',2,'New',"vGTXT")) 
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vGTXT']).replace('\\n','\\n   ')))
'''                                        CONT CONT_ID CONT_LFDNR                                     GRAFTEXT                   pk                   tk               pXYLB
   0   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           Georeferenzpunkt 2  4628671704393700430  4628671704393700430   (1115.95, -323.0)
   1   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                                        Block  4666644549022031339  4666644549022031339      (-58.0, -77.0)
   2   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           numerische Anzeige  4693143208412077585  4693143208412077585      (1211.0, -9.0)
   3   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                             Knoten und Rohre  4995961504641886710  4995961504641886710      (570.0, -49.0)
   4   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                                Vorlaufstrang  5017907661719368413  5017907661719368413  (358.207, 220.395)
   5   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                          LocalHeatingNetwork  5028052147238787802  5028052147238787802     (1163.0, 536.0)
   6   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1   Tel. 05131 - 4980-0 ; Fax. 05131 - 4980-15  5054433315422452796  5054433315422452796   (-230.0, -1143.0)
   7   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  eMail. info@3SConsult.de ; www.3SConsult.de  5370727463979416592  5370727463979416592   (-230.0, -1204.0)
   8   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                Differenzdruck VL-/ RL-Knoten  5502619581048467908  5502619581048467908     (1211.0, -49.0)
   9   Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                                 Kundenanlage  5540395812045688781  5540395812045688781   (1131.95, 283.95)
   10  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                         Fernwärmeverbraucher  5550982489075668484  5550982489075668484     (1050.0, 239.0)
   11  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                               Rücklaufstrang  5610916400841895317  5610916400841895317       (570.0, -9.0)
   12  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                             Knoten und Rohre  5646820849868629537  5646820849868629537  (358.207, 174.395)
   13  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                          numerische Anzeige:  4614148870174765680  4614148870174765680     (219.0, -278.0)
   14  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                        Wärmebilanz: 3 Kunden  5150752151066924202  5150752151066924202     (219.0, -318.0)
   15  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                    Kontrolle: DH-Massenstrom  5100960407865990868  5100960407865990868     (-60.0, -160.0)
   16                                      BHKW    1002         -1                          Fernwärmeeinspeiser  4654104397990769217  4654104397990769217       (115.0, 80.0)
   17                                      BHKW    1002         -1                                        Pumpe  4768731522550494423  4768731522550494423       (175.0, 25.0)
   18                                      BHKW    1002         -1                            Wärmebilanz Netz:  4770844990228490264  4770844990228490264       (90.0, 160.0)
   19                                      BHKW    1002         -1                                  Speicherung  4782197969172967134  4782197969172967134      (110.0, 140.0)
   20                                      BHKW    1002         -1                               Richtungspfeil  4855692488683645764  4855692488683645764      (220.0, 105.0)
   21                                      BHKW    1002         -1                                     Verluste  4965628942555351751  4965628942555351751      (110.0, 145.0)
   22                                      BHKW    1002         -1                          (Element verbinden)  5036153631350515544  5036153631350515544       (150.0, 90.0)
   23                                      BHKW    1002         -1                    BHKW Modul 1000 kW therm.  5056836766824229789  5056836766824229789        (35.0, 55.0)
   24                                      BHKW    1002         -1                                       Ventil  5108336975548011049  5108336975548011049       (205.0, 25.0)
   25                                      BHKW    1002         -1                                    Verbrauch  5262441422409836340  5262441422409836340      (110.0, 150.0)
   26                                      BHKW    1002         -1                                  Einspeisung  5297832234834839298  5297832234834839298      (110.0, 155.0)
   27                                      BHKW    1002         -1                           Druckhaltung 2 bar  5329748935118523443  5329748935118523443       (180.0, 65.0)
   28                                      BHKW    1002         -1                           Numerische Anzeige  5421223289472778073  5421223289472778073      (190.0, 115.0)
   29                                      BHKW    1002         -1                             Verbindungslinie  5501963349880613918  5501963349880613918       (150.0, 95.0)
   30                                      BHKW    1002         -1                                       (Text)  5696590398594231893  5696590398594231893        (35.0, 50.0)
   31                                      BHKW    1002         -1                                       Klappe  5697088036451277538  5697088036451277538       (145.0, 25.0)'''
>>> logger.debug("{:s}: CHANGEHISTORY: {:>10s}: {:>3d}: {:>6s}: {:s}".format('DOCTEST','0.0.40',1,'New',"vNRCV_Mx1: pXYLB")) 
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vNRCV_Mx1'].sort_values(['Sir3sID'],ascending=True)).replace('\\n','\\n   ')))
'''                                         Sir3sID cRefLfdNr                                      CONT CONT_ID CONT_LFDNR         DPGR OBJTYPE            fkOBJTYPE ATTRTYPE              pk_ROWS              tk_ROWS                   pk                   tk            pXYLB
   0              FWES~R3~V-1~5638756766880678918~W         1                                      BHKW    1002         -1  UserDefined    FWES  5638756766880678918        W  5762106696740202356  5762106696740202356  4857294696992797631  4857294696992797631     (90.0, 65.0)
   1       KNOT~PKON-Knoten~~5397990465339071638~QM         1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  UserDefined    KNOT  5397990465339071638       QM  5134531789044068877  5134531789044068877  5410059595276504750  5410059595276504750    (91.0, -94.0)
   2               KNOT~R-L~~5356267303828212700~PH         1                                      BHKW    1002         -1  UserDefined    KNOT  5356267303828212700       PH  5000989080893535213  5000989080893535213  4968703141722117357  4968703141722117357    (220.0, 25.0)
   3                 KNOT~R3~~5219230031772497417~T         1                                      BHKW    1002         -1  UserDefined    KNOT  5219230031772497417        T  5602301870151014230  5602301870151014230  5557806245003742769  5557806245003742769     (90.0, 35.0)
   4                KNOT~V-1~~5049461676240771430~T         1                                      BHKW    1002         -1  UserDefined    KNOT  5049461676240771430        T  4723443975311885965  4723443975311885965  5097127385155151127  5097127385155151127     (90.0, 95.0)
   5            KNOT~V-K007~~5741235692335544560~DP         1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  UserDefined    KNOT  5741235692335544560       DP  4949183695502554728  4949183695502554728  4914949875368816179  4914949875368816179   (1234.0, 83.0)
   6               KNOT~V-L~~5736262931552588702~PH         1                                      BHKW    1002         -1  UserDefined    KNOT  5736262931552588702       PH  4754881272083464445  4754881272083464445  4681213816714574464  4681213816714574464    (220.0, 85.0)
   7              PUMP~R-1~R2~5481331875203087055~N         1                                      BHKW    1002         -1  UserDefined    PUMP  5481331875203087055        N  5563842594211689762  5563842594211689762  5091374651838464239  5091374651838464239    (170.0, 45.0)
   8            VENT~V-1~V-L~4678923650983295610~QM         1                                      BHKW    1002         -1  UserDefined    VENT  4678923650983295610       QM  5126307362398248950  5126307362398248950  5410904806390050339  5410904806390050339   (200.0, 110.0)
   9        WBLZ~BLNZ1u5u7~~4694700216019268978~WVB         1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  UserDefined    WBLZ  4694700216019268978      WVB  4778244458749966216  4778244458749966216  4991097791264453745  4991097791264453745  (354.0, -225.0)
   10    WBLZ~WärmeblnzGes~~5262603207038486299~WES         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299      WES  5690691957596882133  5690691957596882133  5179988968597313889  5179988968597313889    (90.0, 155.0)
   11  WBLZ~WärmeblnzGes~~5262603207038486299~WSPEI         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299    WSPEI  5153847813311339683  5153847813311339683  4946584950744559030  4946584950744559030    (90.0, 140.0)
   12    WBLZ~WärmeblnzGes~~5262603207038486299~WVB         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299      WVB  5214984699859365639  5214984699859365639  5281885868749421521  5281885868749421521    (90.0, 150.0)
   13  WBLZ~WärmeblnzGes~~5262603207038486299~WVERL         1                                      BHKW    1002         -1  UserDefined    WBLZ  5262603207038486299    WVERL  4722863010266870887  4722863010266870887  5476262878682325254  5476262878682325254    (90.0, 145.0)'''
"""


# ---
# --- PT3S Imports
# ---
if __name__ == "__main__":
    from Mx import Mx
else:
    from PT3S.Mx import Mx

import os
import sys
import logging
logger = logging.getLogger('PT3S.Xm')     
import argparse

import unittest
import doctest

import xml.etree.ElementTree as ET
import re
import pandas as pd
import numpy as np
import warnings
import tables

import h5py

import base64
import struct


class XmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Xm():
    """
    SIR 3S XML ModelFile To pandas DataFrames
            One DataFrame per SIR 3S Objecttype 
    Some Views As pandas DataFrames
            The Views are designed to deal with tedious groundwork 
            Views are aggregated somhwat arbitrary ...
            ... however usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views     
    """
    def __init__(self,xmlFile=None,NoH5Read=False):
        """
        Reads SIR 3S XML ModelFile xmlFile
        Stores all SIR 3S ModelData in DataFrames:
             self.dataFrames[tableName]
             tableName example: SWVT_ROWT
        Performs fixes and basic conversions inplace the DataFrames 
        Creates some Views as DataFrames:
            self.dataFrames[viewName]
            viewName example: vKNOT
        ---
        If a .h5-File exists and is newer than an (existing) xmlFile:
            The .h5-File is read (instead) of the xmlFile
        NoH5Read True:
            A .h5-File is not read.        
            An existing .h5-File is deleted.    
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if type(xmlFile) == str:
                self.xmlFile=xmlFile  
                #check if xmlFile exists ...
                if not os.path.exists(self.xmlFile) and NoH5Read: 
                    logStrFinal="{0:s}{1:s}: Not existing!".format(logStr,xmlFile)                                 
                    raise XmError(logStrFinal)  
            else:
                logStrFinal="{0:s}{1!s}: Not of type str!".format(logStr,xmlFile)                                 
                raise XmError(logStrFinal)     
                              
            #Determine corresponding .h5 Filename
            (wD,fileName)=os.path.split(self.xmlFile)
            (base,ext)=os.path.splitext(fileName)
            self.h5File=wD+os.path.sep+base+'.'+'h5'

            if NoH5Read: 
                if os.path.exists(self.h5File):  
                    logger.debug("{0:s}{1:s}: Delete ...".format(logStr,self.h5File))     
                    os.remove(self.h5File)

            if os.path.exists(self.xmlFile):  
                xmlFileTime=os.path.getmtime(self.xmlFile) 
            else:
                xmlFileTime=0

            #check if h5File exists 
            if os.path.exists(self.h5File):  
                #check if h5File is newer
                h5FileTime=os.path.getmtime(self.h5File)
                if(h5FileTime>xmlFileTime):
                    logger.debug("{0:s}h5File {1:s} exists and is newer than an (existing) xmlFile {2:s}:".format(logStr,self.h5File,self.xmlFile))     
                    logger.debug("{0:s}The h5File is read (instead) of the xmlFile.".format(logStr))   
                    h5Read=True  
                else:
                    logger.debug("{0:s}h5File {1:s} exists parallel but is NOT newer than xmlFile {2:s}.".format(logStr,self.h5File,self.xmlFile))     
                    h5Read=False
            else:
                h5Read=False               
            
            if not h5Read:                
                self.__xmlRead()
            else:
                self.FromH5(h5File=self.h5File)
                          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __xmlRead(self):
        """
        Reads SIR 3S XML ModelFile xmlFile
        Stores all SIR 3S ModelData in DataFrames:
             self.dataFrames[tableName]
             tableName example: SWVT_ROWT
        Performs fixes and basic conversions inplace the DataFrames 
        Creates some Views as DataFrames:
            self.dataFrames[viewName]
            viewName example: vKNOT       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            logger.debug("{0:s}xmlFile: {1:s} parse Xml ...".format(logStr,self.xmlFile))                     
            tree = ET.parse(self.xmlFile) # ElementTree                 
            root = tree.getroot()  # Element
            pm = {c:p for p in root.iter() for c in p}   # parentMap
            logger.debug("{0:s}xmlFile: {1:s} done.".format(logStr,self.xmlFile)) 


            logger.debug("{0:s}xmlFile: {1:s} Xml to pandas DataFrames ...".format(logStr,self.xmlFile))      
            tableNames=[]
            oldTableName=None
            for element in root.iter():
                p = None
                if element in pm:
                    p = pm[element]
                if p != root:
                    continue
                actTableName=element.tag
                if actTableName != oldTableName:
                    tableNames.append(actTableName)
                    oldTableName=actTableName                
            self.dataFrames={}
            for tableName in tableNames:
                all_records = []
                for elementRow in root.iter(tag=tableName):
                    record = {}
                    for elementCol in elementRow:
                        record[elementCol.tag] = elementCol.text
                    all_records.append(record)
                self.dataFrames[tableName]=pd.DataFrame(all_records) 
            logger.debug("{0:s}xmlFile: {1:s} done.".format(logStr,self.xmlFile)) 
            logger.debug("{:s}xmlFile: {:s}: tableNames: {!s:s}.".format(logStr,self.xmlFile,sorted(self.dataFrames.keys()))) 

            #fixes and conversions
            self.__convertAndFix()

            #Views
            self.__vXXXX()
                                            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def FromH5(self,h5File=None):
        """
        The h5File is read
        and self.dataFrames is filled with the dfs in the h5File   
        existing dfs in self.dataFrames are deleted
        Note that after FromH5 the content of self.dataFrames can differ from the content of self.xmlFile
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        if h5File == None:
            h5File=self.h5File

        #Check if h5File exists
        if not os.path.exists(h5File):    
            logStrFinal="{0:s}{1:s}: Not Existing!".format(logStr,h5File)                                 
            raise XmError(logStrFinal)           
  
        try:
            self.dataFrames={}   
            with pd.HDFStore(h5File) as h5Store:
                h5Keys=sorted(h5Store.keys())
                for h5Key in h5Keys:
                    match=re.search('(/)(\w+$)',h5Key)
                    key=match.group(2)
                    logger.debug("{0:s}{1:s}: Reading h5Key {2:s} to tableName {3:s}.".format(logStr,h5File,h5Key,key)) 
                    self.dataFrames[key]=h5Store[h5Key]
                

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                                            
      
        finally:
            h5Store.close()
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def ToH5(self,h5File=None):
        """
        Stores all Dataframes in a .h5 File        
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if h5File == None:
                h5File=self.h5File

            #Delete .h5 File if exists
            if os.path.exists(h5File):                        
                logger.debug("{0:s}{1:s}: Delete ...".format(logStr,h5File))     
                os.remove(h5File)

            #Determine .h5 BaseKey

            #XmlFile=r'C:\3S\Modelle\MVV_FW.XML'
            relPath2XmlromCurDir=os.path.normpath(os.path.relpath(os.path.normpath(self.xmlFile),start=os.path.normpath(os.path.curdir))) # ..\..\..\..\..\3S\Modelle\MVV_FW.XML
            #print(repr(relPath2XmlromCurDir)) # '..\\..\\..\\..\\..\\3S\\Modelle\\MVV_FW.XML'
            h5KeySep='/'
            h5KeyCharForDot='_'
            h5KeyCharForMinus='_'
            relPath2XmlromCurDirH5BaseKey=re.sub('\.',h5KeyCharForDot,re.sub(r'\\',h5KeySep,re.sub('-',h5KeyCharForMinus,re.sub('.xml','',relPath2XmlromCurDir,flags=re.IGNORECASE))))
            #__/__/__/__/__/3S/Modelle/MVV_FW

            warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning) #your performance may suffer as PyTables will pickle object types that it cannot map directly to c-types 
            warnings.filterwarnings('ignore',category=tables.exceptions.NaturalNameWarning) #\lib\site-packages\tables\path.py:100: NaturalNameWarning: object name is not a valid Python identifier: '3S'; it does not match the pattern ``^[a-zA-Z_][a-zA-Z0-9_]*$``; you will not be able to use natural naming to access this object; using ``getattr()`` will still work, though)
                         
            #Write .h5 File
            logger.debug("{0:s}pd.HDFStore({1:s}) ...".format(logStr,h5File))                 
            with pd.HDFStore(h5File) as h5Store: 
                #for tableName,table in self.dataFrames.items():
                for tableName in sorted(self.dataFrames.keys()):
                    table=self.dataFrames[tableName]
                    h5Key=relPath2XmlromCurDirH5BaseKey+h5KeySep+tableName      
                    logger.debug("{0:s}{1:s}: Writing DataFrame {2:s} with h5Key={3:s}".format(logStr,h5File,tableName,h5Key))                                                
                    h5Store.put(h5Key,table)#,format='table')                  

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                                           
            
        finally:
            h5Store.close()
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __convertAndFix(self):
        """
        Performs fixes and basic conversions inplace the DataFrames
        Fixes and conbversions here are integrity-oriented
        Usage-oriented conversions (i.e. pd.to_numeric and base64.b64decode) are done in the vXXXX-functions
        conversions: 
        - , > . (converted in: SWVT_ROWT, LFKT_ROWT, QVAR_ROWT)
        fixes:
        - 1st Time without Value?! (fixed in: SWVT_ROWT, LFKT_ROWT, QVAR_ROWT)       
        - in new Models constructed from SIR 3S in Xml not all Attrubutes of an Object are written?!   
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            self.dataFrames['SWVT_ROWT'].ZEIT=self.dataFrames['SWVT_ROWT'].ZEIT.str.replace(',', '.')
            self.dataFrames['SWVT_ROWT'].W=self.dataFrames['SWVT_ROWT'].W.str.replace(',', '.')

            self.dataFrames['LFKT_ROWT'].ZEIT=self.dataFrames['LFKT_ROWT'].ZEIT.str.replace(',', '.')
            self.dataFrames['LFKT_ROWT'].LF=self.dataFrames['LFKT_ROWT'].LF.str.replace(',', '.')

            self.dataFrames['QVAR_ROWT'].ZEIT=self.dataFrames['QVAR_ROWT'].ZEIT.str.replace(',', '.')
            self.dataFrames['QVAR_ROWT'].QM=self.dataFrames['QVAR_ROWT'].QM.str.replace(',', '.')

            self.dataFrames['SWVT_ROWT']=self.dataFrames['SWVT_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
            self.dataFrames['LFKT_ROWT']=self.dataFrames['LFKT_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
            self.dataFrames['QVAR_ROWT']=self.dataFrames['QVAR_ROWT'].fillna(0) # 1. Zeit ohne Wert fuer ZEIT?!
            
            # Template Node
            self.dataFrames['KNOT']=self.dataFrames['KNOT'][self.dataFrames['KNOT'].NAME.fillna('').astype(str).isin(['TemplateNode','TemplNode-VL','TemplNode-RL'])==False]            
            
            # TE only in Heatingmodels ? ...
            try:
                isinstance(self.dataFrames['KNOT_BZ']['TE'],pd.core.series.Series)
            except:
                logger.debug("{:s}ERROR/EXCEPTION: {:s}: {:s}.".format(logStr,"self.dataFrames['KNOT_BZ']['TE']",'TE only in Heatingmodels?!')) 
                self.dataFrames['KNOT_BZ']['TE']=pd.Series()     

            # Models with only one Standard LTGR ...
            try:
                isinstance(self.dataFrames['LTGR']['BESCHREIBUNG'],pd.core.series.Series)
            except:
                self.dataFrames['LTGR']['BESCHREIBUNG']=pd.Series()    

            # Models with no CONTs ...
            try:
                isinstance(self.dataFrames['CONT']['LFDNR'],pd.core.series.Series)
            except:
                self.dataFrames['CONT']['LFDNR']=pd.Series()    
            try:
                isinstance(self.dataFrames['CONT']['GRAF'],pd.core.series.Series)
            except:
                self.dataFrames['CONT']['GRAF']=pd.Series()    

            # Models with old DTRO_ROWD
            # ['AUSFALLZEIT' 'PN' 'REHABILITATION' 'REPARATUR']

            try:
                isinstance(self.dataFrames['DTRO_ROWD']['AUSFALLZEIT'],pd.core.series.Series)
            except:
                self.dataFrames['DTRO_ROWD']['AUSFALLZEIT']=pd.Series()    
            try:
                isinstance(self.dataFrames['DTRO_ROWD']['PN'],pd.core.series.Series)
            except:
                self.dataFrames['DTRO_ROWD']['PN']=pd.Series()    
            try:
                isinstance(self.dataFrames['DTRO_ROWD']['REHABILITATION'],pd.core.series.Series)
            except:
                self.dataFrames['DTRO_ROWD']['REHABILITATION']=pd.Series()    
            try:
                isinstance(self.dataFrames['DTRO_ROWD']['REPARATUR'],pd.core.series.Series)
            except:
                self.dataFrames['DTRO_ROWD']['REPARATUR']=pd.Series()    



        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)             
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def getWDirModelDirModelName(self):
        """
        returns (wDir,modelDir,modelName)
        calculated from SYSTEMKONFIG, DATENEBENE, MODELL
        mx1FileName: os.path.join(wDir,os.path.join(modelDir,modelName))+'.MX1'    
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        result=tuple(['','',''])
        
        try:    
            t=self.dataFrames['SYSTEMKONFIG']
            wDir=t[t['ID'].astype(int)==1]['WERT'].iloc[0] 

            t=self.dataFrames['DATENEBENE']
            B=t[t['TYP'].str.contains('BASIS')]['ORDNERNAME'].iloc[0] 
            V=t[t['TYP'].str.contains('VARIANTE')]['ORDNERNAME'].iloc[0]
            BZ=t[t['TYP'].str.contains('BZ')]['ORDNERNAME'].iloc[0]
            modelDir=os.path.join(B,os.path.join(V,BZ))

            t=self.dataFrames['MODELL']
            modelName=t['BEZEICHNER'].iloc[0]          
            
            mx1Filename=os.path.join(wDir,os.path.join(modelDir,modelName))+'.MX1'                              
            logger.debug("{:s}mx1FileName: {:s}".format(logStr,mx1Filename))
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal)       
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return (wDir,modelDir,modelName)

    def __vXXXX(self):
        """
        Creates some Views as DataFrames:
            self.vXXX[viewName]=pd.merge(...)
            viewName example: vKNOT

        The Views are designed to deal with tedious groundwork 
        Views are aggregated somhwat arbitrary ...
        ... however usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views 

        View-Data:
        Most Colummn-Names will be unchanged
        If suitable renames (i.e. pd.to_numeric and base64.b64decode) are performed inplace

        Some Model-oriented calculations are performed
         
        Most types will be unchanged (pandas' Object-Type)
        If suitable conversions (i.e. pd.to_numeric and base64.b64decode) are performed inplace

        Views created:
            #Ansichtsgruppen
            vLAYR

            #Wblz
            vWBLZ

            #time-Tables
            vLFKT
            vQVAR
            vSWVT

            #Signal-Model
            vRSLW
           
            #Block-Nodes    
            vVKNO
            
            #Nodes
            vKNOT

            vNRCV
            vGTXT
            
            #Pipes
            vROHR
            
            #House-Stations (district heating)
            vFWVB        
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            #Layr
            self.dataFrames['vLAYR']=self.__vLAYR()

            #Wblz
            self.dataFrames['vWBLZ']=self.__vWBLZ()

            #time-Tables
            self.dataFrames['vLFKT']=self.__vLFKT()   
            self.dataFrames['vQVAR']=self.__vQVAR()                   
            self.dataFrames['vSWVT']=self.__vSWVT()


            self.dataFrames['vRSLW']=self.__vRSLW(vSWVT=self.dataFrames['vSWVT']
                                             ) #SWVT-Usage
            
            #nodes    
            self.dataFrames['vVKNO']=self.__vVKNO()
            self.dataFrames['vKNOT']=self.__vKNOT(
                 vVKNO=self.dataFrames['vVKNO']
                ,vQVAR=self.dataFrames['vQVAR']
                )

            vKNOT=self.dataFrames['vKNOT']
            self.pXCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & 
                (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['XKOR'].astype(np.double).min()

            self.pYCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['YKOR'].astype(np.double).min()

            # NRCV
            self.dataFrames['vNRCV']=self.__vNRCV()
            # GTXT
            self.dataFrames['vGTXT']=self.__vGTXT()

            #elements
            self.dataFrames['vROHR']=self.__vROHR(vKNOT=self.dataFrames['vKNOT'])
            self.dataFrames['vFWVB']=self.__vFWVB(vKNOT=self.dataFrames['vKNOT']
                                            ,vLFKT=self.dataFrames['vLFKT']
                                            ,vWBLZ=self.dataFrames['vWBLZ']
                                            )                                             
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __vLAYR(self):
        """
            vLAYR:
                One row per LAYR and OBJ:
                #LAYR_DATA (vLAYR_DATA)
                'LFDNR'
                ,'NAME'
                #LAYR_OBJS (vLAYR_OBJS)
                ,'OBJTYPE' #type (i.e.ROHR) of a LAYR OBJ
                ,'OBJID' #pk (or tk?!) of a LAYR OBJ               
                #IDs (of the LAYR)
                ,'pk','tk'         
                # 
                ,rObjInGroup #Element Nr.  ... in Gruppe                 
                ,nrObjtypeInGroup #Element Nr. ... vom Typ x in Gruppe             
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vLAYR=None

            vLAYR_DATA=self.dataFrames['LAYR'][pd.notnull(self.dataFrames['LAYR']['OBJS'])][['LFDNR','NAME','OBJS','pk','tk']]
            vLAYR_DATA['OBJS']=vLAYR_DATA['OBJS'].apply(lambda x: base64.b64decode(x)).str.decode('utf-8')
            vLAYR_DATA['LFDNR']=pd.to_numeric(vLAYR_DATA.LFDNR,errors='coerce').fillna(-1).astype(np.int64)

            vLAYR_OBJS=pd.concat(
            [
             pd.Series(
             row['LFDNR'],
             row['OBJS'].split('\t')
              )              
            for _, row in vLAYR_DATA.iterrows() 
            ]
            ).reset_index() # When we reset the index, the old index is added as a column, and a new sequential index is used

            vLAYR_DATA.drop(['OBJS'],axis=1,inplace=True)
            
            vLAYR_OBJS.rename(columns={'index':'ETYPEEID',0:'LFDNR'},inplace=True)
            vLAYR_OBJS=vLAYR_OBJS[vLAYR_OBJS['ETYPEEID'].notnull()]
            vLAYR_OBJS=vLAYR_OBJS[vLAYR_OBJS['ETYPEEID'].str.len()>5]
            vLAYR_OBJS['OBJID']=vLAYR_OBJS['ETYPEEID'].str[5:]
            vLAYR_OBJS['OBJTYPE']=vLAYR_OBJS['ETYPEEID'].str[:4]

            vLAYR_OBJS.drop(['ETYPEEID'],axis=1,inplace=True)

            vLAYR=pd.merge(vLAYR_DATA,vLAYR_OBJS,left_on='LFDNR',right_on='LFDNR')

            vLAYR=vLAYR[[
            'LFDNR'
            ,'NAME'
            #from LAYR's OBJS: 
            ,'OBJTYPE' #type (i.e.ROHR) of a LAYR OBJ
            ,'OBJID' #pk (or tk?!) of a LAYR OBJ          
            #IDs (of the LAYR)
            ,'pk','tk'
            ]]

            vLAYR.sort_values(['LFDNR','NAME','OBJTYPE','OBJID'],ascending=True,inplace=True)

            #reindex:
            vLAYR=pd.DataFrame(vLAYR.values,columns=vLAYR.columns)

            #Element Nr.  ... in Gruppe
            vLAYR=vLAYR.assign(nrObjInGroup=vLAYR.sort_values(['LFDNR','OBJTYPE','OBJID']).groupby(['LFDNR']).cumcount()+1)
            #Element Nr. ... vom Typ x in Gruppe 
            vLAYR=vLAYR.assign(nrObjtypeInGroup=vLAYR.sort_values(['LFDNR','OBJTYPE','OBJID']).groupby(['LFDNR','OBJTYPE']).cumcount()+1)
          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vLAYR,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vLAYR=pd.DataFrame()                   
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vLAYR

    def __vWBLZ(self):
        """
            vWBLZ:
                One row per WBLZ and OBJ:
            #WBLZ_DATA (vWBLZ_DATA)
                'AKTIV'            
               ,'BESCHREIBUNG'
               ,'IDIM'
               ,'NAME'
            #from WBLZ's OBJS: 
               ,'OBJID' #pk (or tk?!) of a WBLZ OBJ
               ,'OBJTYPE' #type (i.e. KNOT) of a WBLZ OBJ
            #IDs (of the WBLZ)
               ,'pk'                          
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vWBLZ=None

            vWBLZ_DATA=self.dataFrames['WBLZ'][pd.notnull(self.dataFrames['WBLZ']['OBJS'])][['AKTIV','BESCHREIBUNG','IDIM','NAME','OBJS','pk']]
            vWBLZ_DATA['OBJS']=vWBLZ_DATA['OBJS'].apply(lambda x: base64.b64decode(x)).str.decode('utf-8')

            sList=[pd.Series(row['pk'],index=row['OBJS'].split('\t'),name='pk_Echo')  for index,row in vWBLZ_DATA.iterrows()]

            # sList[0]:
            # KNOT~4668229590574507160    5403356857783326643
            # KNOT~4698059932328245370    5403356857783326643

            vWBLZ_OBJS=pd.concat(sList).reset_index() # When we reset the index, the old index is added as a column named 'index', and a new sequential index is used
            vWBLZ_OBJS.rename(columns={'index':'ETYPEEID'},inplace=True)
            # vWBLZ_OBJS:
            #	ETYPEEID	                pk_Echo
            # 0	KNOT~4668229590574507160	5403356857783326643
            # 1	KNOT~4698059932328245370	5403356857783326643

            vWBLZ_DATA.drop(['OBJS'],axis=1,inplace=True)
            
            vWBLZ_OBJS=vWBLZ_OBJS[vWBLZ_OBJS['ETYPEEID'].notnull()]
            vWBLZ_OBJS=vWBLZ_OBJS[vWBLZ_OBJS['ETYPEEID'].str.len()>5]
            vWBLZ_OBJS['OBJID']=vWBLZ_OBJS['ETYPEEID'].str[5:]
            vWBLZ_OBJS['OBJTYPE']=vWBLZ_OBJS['ETYPEEID'].str[:4]
            vWBLZ_OBJS.drop(['ETYPEEID'],axis=1,inplace=True)

            vWBLZ=pd.merge(vWBLZ_DATA,vWBLZ_OBJS,left_on='pk',right_on='pk_Echo')

            vWBLZ=vWBLZ[[
             'AKTIV'            
            ,'BESCHREIBUNG'
            ,'IDIM'
            ,'NAME'
            #from WBLZ's OBJS: 
            ,'OBJID' #pk (or tk?!) of a WBLZ OBJ
            ,'OBJTYPE' #type (i.e. KNOT) of a WBLZ OBJ
            #IDs (of the WBLZ)
            ,'pk'
            ]]
          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vWBLZ,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vWBLZ=pd.DataFrame()   
                vWBLZ['AKTIV']=pd.Series()  
                vWBLZ['BESCHREIBUNG']=pd.Series()  
                vWBLZ['IDIM']=pd.Series()  
                vWBLZ['NAME']=pd.Series()  
                vWBLZ['OBJID']=pd.Series()  
                vWBLZ['OBJTYPE']=pd.Series()  
                vWBLZ['pk']=pd.Series()     
               
                                                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vWBLZ

    def __vLFKT(self):
        """
        vLFKT:
            One row per Loadfactor time-Table:
            #LFKT
             'NAME'
            ,'BESCHREIBUNG'
            ,'INTPOL'
            ,'ZEITOPTION'
            #ROWT
            ,'LF' #1st Value
            #time-Table aggregates:
            ,'LF_min','LF_max'
            #ID (of the LFKT)
            ,'pk'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vLFKT=None
            vLFKT=pd.merge(self.dataFrames['LFKT'],self.dataFrames['LFKT_ROWT'],left_on='pk',right_on='fk')
            vLFKT['ZEIT']=pd.to_numeric(vLFKT['ZEIT']) 
            vLFKT['LF']=pd.to_numeric(vLFKT['LF']) 
            vLFKT['ZEIT_RANG']=vLFKT.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vLFKT_gLF=vLFKT.groupby(['pk_x'], as_index=False).agg({'LF':[np.min,np.max]})
            vLFKT_gLF.columns= [tup[0]+tup[1] for tup in zip(vLFKT_gLF.columns.get_level_values(0),vLFKT_gLF.columns.get_level_values(1))]
            vLFKT_gLF.rename(columns={'LFamin':'LF_min','LFamax':'LF_max'},inplace=True)
            #
            vLFKT=pd.merge(vLFKT,vLFKT_gLF,left_on='pk_x',right_on='pk_x')
            #
            vLFKT=vLFKT[vLFKT['ZEIT_RANG']==1]
            #
            vLFKT=vLFKT[['NAME','BESCHREIBUNG','LF','LF_min','LF_max','INTPOL','ZEITOPTION','pk_x']]
            #
            vLFKT.rename(columns={'pk_x':'pk'},inplace=True)
            #
            vLFKT=vLFKT[[
                'NAME','BESCHREIBUNG'
                ,'LF','LF_min','LF_max'
                ,'INTPOL','ZEITOPTION'
                ,'pk'
                ]]
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vLFKT  

    def __vNRCV(self):
        """
        vNRCV:
            One row per NRCV:           
               'cRefLfdNr' 
              # CONT
              ,'CONT'
              ,'CONT_ID'
              ,'CONT_LFDNR'
              # DPGR
              ,'DPGR'
               # Data (of the DPGR_ROW)
              ,'OBJTYPE'
              ,'fkOBJTYPE'
              ,'ATTRTYPE'
              # IDs (of the DPGR_ROW)
              ,'pk_ROWS'
              ,'tk_ROWS'       
              # IDs (of the NRCV)
              ,'pk'
              ,'tk'          
              # PLot Coordinates XY LeftBottom
              ,'pXYLB'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vNRCV=None
            vNRCV=self.dataFrames['NRCV']
            vNRCV=vNRCV.merge(self.dataFrames['DPGR_ROWS'],left_on='fkDPGR_ROWS',right_on='pk',suffixes=['_NR','_DR'])
            vNRCV=vNRCV.merge(self.dataFrames['DPGR'],left_on='fk',right_on='pk',suffixes=['_DR2','_DG'])
            vNRCV=vNRCV.merge(self.dataFrames['CONT'],left_on='fkCONT',right_on='pk',suffixes=['_DR3','_CONT'])


            # GRAF ###
            xyLeftBottom=[]
            for index,row in vNRCV.iterrows():
                if pd.isnull(row.GRAF_DR3):                 
                    xyLeftBottom.append(())
                    continue
                geomBytes=base64.b64decode(row.GRAF_DR3)               
                XYLeftBottom=struct.unpack('2d',geomBytes[8:24]) 
                xyLeftBottom.append(XYLeftBottom)

         
            pXyLeftBottom=[]
            for index,row in vNRCV.iterrows():
                 xyLB=xyLeftBottom[index]
                 if int(row.ID)!=1001:
                    pXyLeftBottom.append(xyLB)
                 else:
                    x,y=xyLB
                    x=x-self.pXCorZero
                    y=y-self.pYCorZero
                    pXyLeftBottom.append((x,y))
            vNRCV['pXYLB']=pd.Series(pXyLeftBottom)

            vNRCV=vNRCV[[
               'NAME_CONT'
              ,'ID'
              ,'LFDNR'              
              # DPGR
              ,'NAME_DR3'
               # Data (of the DPGR_ROW)
              ,'OBJTYPE'
              ,'fkOBJTYPE'
              ,'ATTRTYPE'
              # IDs (of the DPGR_ROW)
              ,'pk_DR'
              ,'tk_DR'       
              # IDs (of the NRCV)
              ,'pk_NR'
              ,'tk_NR'
              ,'pXYLB'
            ]]

            vNRCV.rename(columns={'NAME_CONT':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'
                      ,'NAME_DR3':'DPGR'
                     ,'pk_NR':'pk'
                     ,'tk_NR':'tk'
                     ,'pk_DR':'pk_ROWS'
                     ,'tk_DR':'tk_ROWS'},inplace=True)  

            vNRCV=vNRCV.assign(cRefLfdNr=vNRCV.sort_values(['CONT_ID','pk'], ascending=True)
                   .groupby(['OBJTYPE','fkOBJTYPE','ATTRTYPE']).cumcount()+1)

            vNRCV=vNRCV[[
               'cRefLfdNr' 
              # CONT
              ,'CONT'
              ,'CONT_ID'
              ,'CONT_LFDNR'
              # DPGR
              ,'DPGR'
               # Data (of the DPGR_ROW)
              ,'OBJTYPE'
              ,'fkOBJTYPE'
              ,'ATTRTYPE'
              # IDs (of the DPGR_ROW)
              ,'pk_ROWS'
              ,'tk_ROWS'       
              # IDs (of the NRCV)
              ,'pk'
              ,'tk'
              ,'pXYLB'
            ]]

            vNRCV.sort_values(['OBJTYPE','fkOBJTYPE','ATTRTYPE','cRefLfdNr'],ascending=True,inplace=True)
            vNRCV=pd.DataFrame(vNRCV.values,columns=vNRCV.columns)
                                                        
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vNRCV,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vNRCV=pd.DataFrame()                 
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vNRCV

    def __vGTXT(self):
        """
        vGTXT:
            One row per GTXT:                          
              # CONT
               'CONT'
              ,'CONT_ID'
              ,'CONT_LFDNR'
              #
              ,'GRAFTEXT'
              # IDs (of the GTXT)
              ,'pk'
              ,'tk'          
              # PLot Coordinates XY LeftBottom
              ,'pXYLB'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vGTXT=None
            vGTXT=self.dataFrames['GTXT']            
            vGTXT=vGTXT.merge(self.dataFrames['CONT'],left_on='fkCONT',right_on='pk',suffixes=['_DR3','_CONT'])

            # GRAF ###
            xyLeftBottom=[]
            for index,row in vGTXT.iterrows():
                if pd.isnull(row.GRAF_DR3):                 
                    xyLeftBottom.append(())
                    continue
                geomBytes=base64.b64decode(row.GRAF_DR3)               
                XYLeftBottom=struct.unpack('2d',geomBytes[4:20]) 
                xyLeftBottom.append(XYLeftBottom)
           
            pXyLeftBottom=[]
            for index,row in vGTXT.iterrows():
                 xyLB=xyLeftBottom[index]
                 if int(row.ID)!=1001:
                    pXyLeftBottom.append(xyLB)
                 else:
                    x,y=xyLB
                    x=x-self.pXCorZero
                    y=y-self.pYCorZero
                    pXyLeftBottom.append((x,y))
            vGTXT['pXYLB']=pd.Series(pXyLeftBottom)

            vGTXT=vGTXT[[
               'NAME'
              ,'ID'
              ,'LFDNR'   
              ,'GRAFTEXT'                     
              # IDs (of the NRCV)
              ,'pk_DR3'
              ,'tk_DR3'
              ,'pXYLB'
            ]]

            vGTXT.rename(columns={'NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'                    
                     ,'pk_DR3':'pk'
                     ,'tk_DR3':'tk'
                     ,'pk_DR':'pk_ROWS'
                     ,'tk_DR':'tk_ROWS'},inplace=True)             

            vGTXT=vGTXT[[
             
              # CONT
               'CONT'
              ,'CONT_ID'
              ,'CONT_LFDNR'
              ,'GRAFTEXT'
              # IDs (of the NRCV)
              ,'pk'
              ,'tk'
              ,'pXYLB'
            ]]
                                                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vGTXT,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vGTXT=pd.DataFrame()                 
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vGTXT

    def __vSWVT(self):
        """
        vSWVT:
            #SWVT
             'NAME'
            ,'BESCHREIBUNG'
            ,'INTPOL','ZEITOPTION'
            #ROWT
            ,'W' #1st Value
            #time-Table aggregates:
            ,'W_min','W_max'
            #ID (of the SWVT)
            ,'pk'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vSWVT = None
            vSWVT=pd.merge(self.dataFrames['SWVT'],self.dataFrames['SWVT_ROWT'],left_on='pk',right_on='fk')
            vSWVT['ZEIT']=pd.to_numeric(vSWVT['ZEIT']) 
            vSWVT['W']=pd.to_numeric(vSWVT['W']) 
            vSWVT['ZEIT_RANG']=vSWVT.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vSWVT_g=vSWVT.groupby(['pk_x'], as_index=False).agg({'W':[np.min,np.max]})
            vSWVT_g.columns= [tup[0]+tup[1] for tup in zip(vSWVT_g.columns.get_level_values(0),vSWVT_g.columns.get_level_values(1))]
            vSWVT_g.rename(columns={'Wamin':'W_min','Wamax':'W_max'},inplace=True)
            #
            vSWVT=pd.merge(vSWVT,vSWVT_g,left_on='pk_x',right_on='pk_x')
            #
            vSWVT=vSWVT[vSWVT['ZEIT_RANG']==1]
            #
            vSWVT=vSWVT[['NAME','BESCHREIBUNG','INTPOL','ZEITOPTION','W','W_min','W_max','pk_x']]
            #
            vSWVT.rename(columns={'pk_x':'pk'},inplace=True)
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return vSWVT   

    def __vRSLW(self,vSWVT=None):
        """
        vRSLW:
            # RSLW
            'KA'
            ,'BESCHREIBUNG'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'CONT' #(NAME)
            ,'ID'          
            # vSWVT
            ,'SWVT' #(NAME)
            ,'BESCHREIBUNG_SWVT' #(BESCHREIBUNG)
            ,'INTPOL','ZEITOPTION'
            ,'W','W_min','W_max'
            # RSLW IDs   
            ,'pk','tk'
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:      
            vRSLW=None                  
                         
            vRSLW=pd.merge(self.dataFrames['RSLW'],self.dataFrames['RSLW_BZ'],left_on='pk',right_on='fk')
            vRSLW=pd.merge(vRSLW,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')

            vRSLW=vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON','fkSWVT' 
            # CONT
            ,'NAME','ID'
            # RSLW IDs   
            ,'pk_x', 'tk_x'
                 ]]

            vRSLW=pd.merge(vRSLW,vSWVT,left_on='fkSWVT',right_on='pk',how='left')

            vRSLW=vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG_x'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'NAME_x','ID'          
            # vSWVT
            ,'NAME_y', 'BESCHREIBUNG_y', 'W', 'W_min', 'W_max', 'INTPOL','ZEITOPTION'
            # RSLW IDs   
            ,'pk_x', 'tk_x'
                 ]]            

            vRSLW.rename(columns=
            {'BESCHREIBUNG_x': 'BESCHREIBUNG',
             'BESCHREIBUNG_y': 'BESCHREIBUNG_SWVT',
             'NAME_x': 'CONT',
             'NAME_y': 'SWVT',
             'pk_x': 'pk',
             'tk_x': 'tk'}
            ,inplace=True)

            vRSLW=vRSLW[[
            # RSLW
            'KA'
            ,'BESCHREIBUNG'
            ,'INDWBG','INDWNO'
            # RSLW BZ
            ,'INDSLW','SLWKON'
            # CONT
            ,'CONT','ID'          
            # vSWVT
            ,'SWVT', 'BESCHREIBUNG_SWVT', 'W', 'W_min', 'W_max', 'INTPOL','ZEITOPTION'
            # RSLW IDs   
            ,'pk','tk'
                 ]]          
            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vRSLW,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vRSLW=pd.DataFrame()              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vRSLW

    def __vQVAR(self):
        """
        vQVAR:
            'NAME'
           ,'BESCHREIBUNG'
           ,'INTPOL'
           ,'ZEITOPTION'
           ,'QM'
           ,'QM_min','QM_max'
           ,'pk'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vQVAR = None
            vQVAR=pd.merge(self.dataFrames['QVAR'],self.dataFrames['QVAR_ROWT'],left_on='pk',right_on='fk')
            vQVAR['ZEIT']=pd.to_numeric(vQVAR['ZEIT']) 
            vQVAR['QM']=pd.to_numeric(vQVAR['QM']) 
            vQVAR['ZEIT_RANG']=vQVAR.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vQVAR_gQM=vQVAR.groupby(['pk_x'], as_index=False).agg({'QM':[np.min,np.max]})
            vQVAR_gQM.columns= [tup[0]+tup[1] for tup in zip(vQVAR_gQM.columns.get_level_values(0),vQVAR_gQM.columns.get_level_values(1))]
            vQVAR_gQM.rename(columns={'QMamin':'QM_min','QMamax':'QM_max'},inplace=True)
            #
            vQVAR=pd.merge(vQVAR,vQVAR_gQM,left_on='pk_x',right_on='pk_x')
            #
            vQVAR=vQVAR[vQVAR['ZEIT_RANG']==1]
            #
            vQVAR=vQVAR[['NAME','BESCHREIBUNG','INTPOL','ZEITOPTION','QM','QM_min','QM_max','pk_x']]
            #
            vQVAR.rename(columns={'pk_x':'pk'},inplace=True)
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vQVAR
            
    def __vVKNO(self):
        """
        vVKNO:
           'NAME' # der Name des Knotens
          ,'CONT' # der Blockname des Blockes fuer den der Knoten Blockknoten ist
          ,'fkKNOT'
          ,'fkCONT'       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:     
            vVKNO=None        
            vVKNO=pd.merge(self.dataFrames['VKNO'],self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            vVKNO=pd.merge(vVKNO,self.dataFrames['KNOT'],left_on='fkKNOT',right_on='pk')

            vVKNO=vVKNO[[
               'NAME_x'     
              ,'NAME_y'     
              ,'fkCONT_x','fkKNOT' 
            ]]
            vVKNO.rename(columns={'NAME_x':'CONT','NAME_y':'NAME','fkCONT_x':'fkCONT'},inplace=True)

            vVKNO=vVKNO[[
                'NAME' # der Name des Knotens
               ,'CONT' # der Blockname des Blockes fuer den der Knoten Blockknoten ist
               ,'fkKNOT'
               ,'fkCONT'
            ]]
                               
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vVKNO,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vVKNO=pd.DataFrame()       
                vVKNO['NAME']=pd.Series()     
                vVKNO['CONT']=pd.Series()     
                vVKNO['fkKNOT']=pd.Series()     
                vVKNO['fkCONT']=pd.Series()                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vVKNO

    def __vKNOT(self,vVKNO=None,vQVAR=None):
        """
        vKNOT:
            'NAME'
           ,'BESCHREIBUNG'
           ,'IDREFERENZ'
           ,'CONT' # aus KNOT>CONT (der Blockname des Knotens)
           ,'CONT_ID' # aus KNOT>CONT
           ,'CONT_LFDNR' # aus KNOT>CONT
           ,'CONT_VKNO' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
           ,'KTYP'
           ,'LFAKT','QM_EIN'
           ,'QVAR_NAME'
           ,'QM','QM_min','QM_max'     
           ,'KVR' 
           ,'TE','TM' 
           ,'XKOR','YKOR','ZKOR'
           ,'pk','tk'
           #plotCors
           ,'pXCor' 
           ,'pYCor' 
          
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            vKNOT=None

            vKNOT=pd.merge(self.dataFrames['KNOT'],self.dataFrames['KNOT_BZ'],left_on='pk',right_on='fk')
            vKNOT=pd.merge(vKNOT,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')
            vKNOT=pd.merge(vKNOT,vVKNO,left_on='pk_x',right_on='fkKNOT',how='left')

            #logger.debug("{:s}vKNOT columns before TE: {:s}".format(logStr,str(vKNOT.columns))) 
                      
            vKNOT=vKNOT[[
                    'NAME_x'
                   ,'BESCHREIBUNG','IDREFERENZ'
                   ,'NAME_y' # aus KNOT>CONT (der Blockname des Knotens)
                   ,'ID' # aus KNOT>CONT
                   ,'LFDNR' # aus KNOT>CONT
                   ,'CONT' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
                   ,'KTYP'
                   ,'LFAKT','QM_EIN','fkQVAR'       
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk_x','tk_x'
                ]]

            vKNOT.rename(columns={'NAME_x':'NAME'
                                       ,'NAME_y':'CONT'
                                       ,'ID':'CONT_ID'
                                       ,'LFDNR':'CONT_LFDNR'
                                       ,'ID':'CONT_ID','LFDNR':'CONT_LFDNR'
                                       ,'CONT':'CONT_VKNO'
                                       ,'pk_x':'pk'
                                       ,'tk_x':'tk'},inplace=True)

            vKNOT=pd.merge(vKNOT,vQVAR,left_on='fkQVAR',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'QVAR_NAME'},inplace=True)
            vKNOT.rename(columns={'pk_x':'pk'},inplace=True)

            vKNOT=vKNOT[[
                    'NAME'
                   ,'BESCHREIBUNG'
                   ,'IDREFERENZ'
                   ,'CONT' # aus KNOT>CONT (der Blockname des Knotens)
                   ,'CONT_ID' # aus KNOT>CONT
                   ,'CONT_LFDNR' # aus KNOT>CONT
                   ,'CONT_VKNO' # aus vVKNO (der Blockname des Blocks fuer den der Knoten Blockknoten ist)
                   ,'KTYP'
                   ,'LFAKT','QM_EIN'
                   ,'QVAR_NAME'
                   ,'QM','QM_min','QM_max'     
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]
          
            pXCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & 
                (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['XKOR'].astype(np.double).min()

            vKNOT['pXCor'] = [
                 x-pXCorZero 
                 if 
                 y==1001 and not z
                 else
                 x
                 for x,y,z in zip(vKNOT['XKOR'].astype(np.double)
                             ,vKNOT['CONT_ID'].astype(int)
                             ,vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element')
                             )
                ] 

            pYCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['YKOR'].astype(np.double).min()

            vKNOT['pYCor'] = [
                 x-pYCorZero 
                 if 
                 y==1001 and not z
                 else
                 x
                 for x,y,z in zip(vKNOT['YKOR'].astype(np.double)
                             ,vKNOT['CONT_ID'].astype(int)
                             ,vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element')
                             )
                ] 
            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vKNOT

    def __vROHR(self,vKNOT=None):
        """
        vROHR:
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT','DA','DI','DN','KT','PN','REHABILITATION','REPARATUR','S','WSTEIG','WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'DTRO_NAME'
                    ,'DTRO_BESCHREIBUNG'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                    #IDs 
                    ,'pk','tk'
                    #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                    #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                    #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                    #Ki
                    ,'NAME_i'
                    ,'KVR_i','TM_i'
                    ,'XKOR_i','YKOR_i','ZKOR_i'                 
                    #Kk
                    ,'NAME_k'
                    ,'KVR_k','TM_k'
                    ,'XKOR_k','YKOR_k','ZKOR_k'
                    #plotCors
                    ,'pXCor_i','pYCor_i'
                    ,'pXCor_k','pYCor_k'
                    # matplotlibs's .plot(pXCors,pYCors,...)
                    ,'pXCors','pYCors' # nur die Endpunkte
                    ,'pWAYPXCors','pWAYPYCors' # alle Wegpunkte                         
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vROHR=None            
                                         
            vROHR=pd.merge(self.dataFrames['ROHR'],self.dataFrames['ROHR_BZ'],left_on='pk',right_on='fk')

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #Ref.
                    ,'fkCONT'
                    ,'fkDTRO_ROWD'
                    ,'fkLTGR','fkSTRASSE'
                    ,'fkKI','fkKK'
                   #IDs 
                    ,'pk_x','tk'
                    ,'GEOM','GRAF'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                            ]]

            vROHR.rename(columns={'pk_x':'pk'},inplace=True)
            vROHR=pd.merge(vROHR,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')

            vROHR=vROHR[[
             'BESCHREIBUNG'
            ,'IDREFERENZ'
            #Asset
            ,'BAUJAHR','HAL'
            ,'IPLANUNG','KENNUNG'
            #Reibung
            ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
            ,'JLAMBS','LAMBDA0'
            #inst.
            ,'ASOLL','INDSCHALL'
            #FW
            ,'fk2LROHR','KVR'
            #Ref.
            ,'fkDTRO_ROWD'
            ,'fkLTGR','fkSTRASSE'
            ,'fkKI','fkKK'
           #IDs 
            ,'pk_x','tk_x'
            ,'GEOM_x','GRAF_x'
           #BZ
            ,'IRTRENN'
            ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
           #Rest
            ,'QSVB'
            ,'ZVLIMPTNZ'
            ,'KANTENZV'
           #CONT
            ,'NAME' 
            ,'ID'
            ,'LFDNR'
                    ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'},inplace=True)    
            vROHR=pd.merge(vROHR,self.dataFrames['DTRO_ROWD'],left_on='fkDTRO_ROWD',right_on='pk')   

            vROHR=vROHR[[
             'BESCHREIBUNG'
            ,'IDREFERENZ'
            #Asset
            ,'BAUJAHR','HAL'
            ,'IPLANUNG','KENNUNG'
            #Reibung
            ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
            ,'JLAMBS','LAMBDA0'
            #inst.
            ,'ASOLL','INDSCHALL'
            #FW
            ,'fk2LROHR','KVR'
            #DTRO_ROWD
            ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
            #Ref.
            ,'fkLTGR','fkSTRASSE'
            ,'fkKI','fkKK'
           #IDs 
            ,'pk_x','tk_x'
            ,'GEOM_x','GRAF_x'
           #BZ
            ,'IRTRENN'
            ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
           #Rest
            ,'QSVB'
            ,'ZVLIMPTNZ'
            ,'KANTENZV'
           #CONT
            ,'CONT' 
            ,'CONT_ID'
            ,'CONT_LFDNR'
                    ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk'},inplace=True)
            vROHR=pd.merge(vROHR,self.dataFrames['LTGR'],left_on='fkLTGR',right_on='pk')

            vROHR=vROHR[[
             'BESCHREIBUNG_x'
            ,'IDREFERENZ'
            #Asset
            ,'BAUJAHR','HAL'
            ,'IPLANUNG','KENNUNG'
            #Reibung
            ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
            ,'JLAMBS','LAMBDA0'
            #inst.
            ,'ASOLL','INDSCHALL'
            #FW
            ,'fk2LROHR','KVR'
            #DTRO_ROWD
            ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
            #LTGR
            ,'NAME','BESCHREIBUNG_y','SICHTBARKEIT','VERLEGEART','fkDTRO','fkSRAT'
            #Ref.
            ,'fkSTRASSE'
            ,'fkKI','fkKK'
           #IDs 
            ,'pk_x','tk_x'
            ,'GEOM_x','GRAF_x'
           #BZ
            ,'IRTRENN'
            ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
           #Rest
            ,'QSVB'
            ,'ZVLIMPTNZ'
            ,'KANTENZV'
           #CONT
            ,'CONT' 
            ,'CONT_ID'
            ,'CONT_LFDNR'
                    ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'LTGR_NAME','BESCHREIBUNG_y':'LTGR_BESCHREIBUNG','BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART','fkDTRO','fkSRAT'
                    #Ref.
                    ,'fkSTRASSE'
                    ,'fkKI','fkKK'
                   #IDs 
                    ,'pk','tk'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                            ]]
                                 
            vROHR=pd.merge(vROHR,self.dataFrames['DTRO'],left_on='fkDTRO',right_on='pk')

            vROHR=vROHR[[
                     'BESCHREIBUNG_x'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'NAME'
                    ,'BESCHREIBUNG_y'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                    ,'fkKI','fkKK'
                   #IDs 
                    ,'pk_x','tk_x'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                            ]]
            vROHR.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'DTRO_NAME','BESCHREIBUNG_y':'DTRO_BESCHREIBUNG','BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)
            
            #logger.debug("{:s} vor fkKI: {!s:s}".format(logStr,(vROHR)))   
            vROHR=pd.merge(vROHR,vKNOT,left_on='fkKI',right_on='pk')   
            #logger.debug("{:s} nach fkKI: {!s:s}".format(logStr,(vROHR)))   
            vROHR.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ'
                                       ,'pk_x':'pk','tk_x':'tk'
                                       ,'CONT_ID_x':'CONT_ID','CONT_LFDNR_x':'CONT_LFDNR'
                                       },inplace=True) 

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR_x'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'DTRO_NAME'
                    ,'DTRO_BESCHREIBUNG'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                    ,'fkKK'
                   #IDs 
                    ,'pk','tk'
                    ,'GEOM_x','GRAF_x'
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT_x' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                   #Ki
                   ,'NAME'
                   ,'KVR_y','TM'
                   ,'XKOR','YKOR','ZKOR'
                   ,'pXCor','pYCor'
                            ]]

            vROHR.rename(columns={'NAME':'NAME_i','KVR_x':'KVR','KVR_y':'KVR_i','TM':'TM_i','CONT_x':'CONT'},inplace=True)  
            vROHR.rename(columns={'XKOR':'XKOR_i','YKOR':'YKOR_i','ZKOR':'ZKOR_i'
                                       ,'pXCor':'pXCor_i'
                                       ,'pYCor':'pYCor_i'
                                       },inplace=True)    
            
            vROHR=pd.merge(vROHR,vKNOT,left_on='fkKK',right_on='pk')    
            vROHR.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ'
                                       ,'pk_x':'pk','tk_x':'tk'
                                       ,'CONT_ID_x':'CONT_ID','CONT_LFDNR_x':'CONT_LFDNR'
                                       },inplace=True)  

            vROHR.rename(columns={'NAME':'NAME_k','KVR_x':'KVR','KVR_y':'KVR_k','TM':'TM_k','CONT_x':'CONT'},inplace=True)  
            vROHR.rename(columns={'XKOR':'XKOR_k','YKOR':'YKOR_k','ZKOR':'ZKOR_k'
                                       ,'pXCor':'pXCor_k'
                                       ,'pYCor':'pYCor_k'
                                       },inplace=True)                                   

            vROHR['pXCors']=[[xi,xk] for xi,xk in zip(vROHR['pXCor_i'],vROHR['pXCor_k'])]
            vROHR['pYCors']=[[xi,xk] for xi,xk in zip(vROHR['pYCor_i'],vROHR['pYCor_k'])]
            
            # WAYP ###
            vROHR['WAYP']=[list() for dummy in vROHR['pk']] # leere Liste von Wegpunkten
            for index,row in vROHR.iterrows():
                if pd.isnull(row.GEOM_x):                    
                    continue
                geomBytes=base64.b64decode(row.GEOM_x)
                # 1. Byte: Endianess: 0=little
                # 1. Byte auslassen
    
                # 2 ints lesen ...
                headerData = struct.unpack('2i',geomBytes[1:9])                
                graphType,NOfWaypoints=headerData #  graphType: Werte von 1 bis 6 bedeuten: Point, LineString, Polygon, MultiPoint, ...
    
                # xy-Koordinatenpaare lesen                 
                # 2 double: xi, yi
                for idx in range(NOfWaypoints):
                    offset=9+idx*16                   
                    end=offset+16                  
                    waypXY=struct.unpack('2d',geomBytes[offset:end])                    
                    row.WAYP.append(waypXY)
          
            vROHR['pWAYPXCors']=[list() for dummy in vROHR['pk']] # leere Liste von pWegpunkten X
            vROHR['pWAYPYCors']=[list() for dummy in vROHR['pk']] # leere Liste von pWegpunkten Y
            for index,row in vROHR.iterrows():
                for waypXY in row.WAYP:
                    X,Y=waypXY
                    if int(row.CONT_ID)==1001:
                        row.pWAYPXCors.append(X-self.pXCorZero)
                        row.pWAYPYCors.append(Y-self.pYCorZero)
                    else:
                        row.pWAYPXCors.append(X)
                        row.pWAYPYCors.append(Y)

            vROHR=vROHR[[
                     'BESCHREIBUNG'
                    ,'IDREFERENZ'
                    #Asset
                    ,'BAUJAHR','HAL'
                    ,'IPLANUNG','KENNUNG'
                    #Reibung
                    ,'L','LZU','RAU','ZAUS','ZEIN','ZUML'
                    ,'JLAMBS','LAMBDA0'
                    #inst.
                    ,'ASOLL','INDSCHALL'
                    #FW
                    ,'fk2LROHR','KVR'
                    #DTRO_ROWD
                    ,'AUSFALLZEIT', 'DA', 'DI', 'DN', 'KT', 'PN', 'REHABILITATION','REPARATUR', 'S', 'WSTEIG', 'WTIEFE'
                    #LTGR
                    ,'LTGR_NAME','LTGR_BESCHREIBUNG','SICHTBARKEIT','VERLEGEART'
                    #DTRO
                    ,'DTRO_NAME'
                    ,'DTRO_BESCHREIBUNG'
                    ,'E'
                    #Ref.
                    ,'fkSTRASSE','fkSRAT'
                   #IDs 
                    ,'pk','tk'          
                   #BZ
                    ,'IRTRENN'
                    ,'LECKSTART','LECKEND','LECKMENGE','LECKORT','LECKSTATUS'
                   #Rest
                    ,'QSVB'
                    ,'ZVLIMPTNZ'
                    ,'KANTENZV'
                   #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR'
                   #Ki
                   ,'NAME_i'
                   ,'KVR_i','TM_i'
                   ,'XKOR_i','YKOR_i','ZKOR_i'                 
                   #Kk
                   ,'NAME_k'
                   ,'KVR_k','TM_k'
                   ,'XKOR_k','YKOR_k','ZKOR_k'
                   #plotCors
                   ,'pXCor_i','pYCor_i'
                   ,'pXCor_k','pYCor_k'
                   # matplotlibs's .plot(pXCors,pYCors,...)
                   ,'pXCors','pYCors' # nur die Endpunkte
                   ,'pWAYPXCors','pWAYPYCors' # alle Wegpunkte
                   #WAYP
                   ,'WAYP' #List of Tuples: [(x1,y1),...,(xN,yN)] 
                            ]]

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)           
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))         
            return vROHR 

    def __vFWVB(self,vKNOT=None,vLFKT=None,vWBLZ=None):
        """
        vFWVB:
             'BESCHREIBUNG'
            ,'IDREFERENZ'
            ,'W0'
            ,'LFK' ,'TVL0' ,'TRS0'
            #LFKT
            ,'LFKT'
            ,'W','W_min','W_max'
            #FWVB contd.
            ,'INDTR' ,'TRSK'
            ,'VTYP' ,'IMBG' ,'IRFV'
            #FWVB IDs
            ,'pk','tk'  
            #Ki
            ,'NAME_i'
            ,'KVR_i','TM_i'
            ,'XKOR_i','YKOR_i','ZKOR_i'
            ,'pXCor_i','pYCor_i'
            #Kk
            ,'NAME_k'
            ,'KVR_k','TM_k'
            ,'XKOR_k','YKOR_k','ZKOR_k'  
            ,'pXCor_k','pYCor_k'
            #CONT
            ,'CONT' 
            ,'CONT_ID'
            ,'CONT_LFDNR' 
            #WBLZ
            ,['BLZ1','BLZ2',...]] 
                # list of the WBLZ-Names of the FWVB in alphabetical Order  
                # empty, if FWVB is not a WBLZ-Member      
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:         
            vFWVB=None

            #logger.debug("{:s} vor _BZ: {!s:s}".format(logStr,(vFWVB)))
                            
            vFWVB=pd.merge(self.dataFrames['FWVB'],self.dataFrames['FWVB_BZ'],left_on='pk',right_on='fk')

            #logger.debug("{:s} nach _BZ: {!s:s}".format(logStr,(vFWVB)))
            #
            vFWVB=vFWVB[vFWVB['W0'].notnull()]
            vFWVB['W0']=vFWVB['W0'].str.replace(',', '.')
            vFWVB['W0']=pd.to_numeric(vFWVB['W0']) 
            #
            vFWVB['LFK']=pd.to_numeric(vFWVB['LFK']) 
            vFWVB['TVL0']=pd.to_numeric(vFWVB['TVL0']) 
            vFWVB['TRS0']=pd.to_numeric(vFWVB['TRS0'])  
            vFWVB['INDTR']=pd.to_numeric(vFWVB['INDTR'])  
            vFWVB['TRSK']=pd.to_numeric(vFWVB['TRSK'])  
            vFWVB['VTYP']=pd.to_numeric(vFWVB['VTYP'])  
            vFWVB['IMBG']=pd.to_numeric(vFWVB['IMBG']) 
            vFWVB['IRFV']=pd.to_numeric(vFWVB['IRFV']) 
            
            #
            vFWVB=pd.merge(vFWVB,vLFKT,left_on='fkLFKT',right_on='pk',how='left')
            #logger.debug("{:s} nach vLFKT: {!s:s}".format(logStr,(vFWVB)))
            #
            vFWVB['W']      = vFWVB.apply(lambda row: row.LF     * row.W0, axis=1)
            vFWVB['W_min']  = vFWVB.apply(lambda row: row.LF_min * row.W0, axis=1)
            vFWVB['W_max']  = vFWVB.apply(lambda row: row.LF_max * row.W0, axis=1)
            #
            vFWVB=vFWVB[[
                    'BESCHREIBUNG_x','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                   ,'W','W_min','W_max'
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                   ,'pk_x','tk'
                   ,'NAME','BESCHREIBUNG_y'
                   ,'fkKI','fkKK'
                   ,'fkCONT'
                 ]]
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','pk_x':'pk','NAME':'LFKT'},inplace=True)       
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                   ,'fkKI','fkKK'   
                   ,'fkCONT'            
                 ]]    

            #logger.debug("{:s} vor fkKI: {!s:s}".format(logStr,(vFWVB)))

            vFWVB=pd.merge(vFWVB,vKNOT,left_on='fkKI',right_on='pk')   
            #logger.debug("{:s} nach fkKI: {!s:s}".format(logStr,(vFWVB)))
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ','pk_x':'pk','tk_x':'tk'},inplace=True)  
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                    #Ki
                   ,'NAME'
                   ,'KVR','TM'
                   ,'XKOR','YKOR','ZKOR'
                   ,'pXCor','pYCor'
                   ,'fkKK'    
                   ,'fkCONT'           
                 ]]     
            vFWVB.rename(columns={'NAME':'NAME_i','KVR':'KVR_i','TM':'TM_i'},inplace=True)  
            vFWVB.rename(columns={'XKOR':'XKOR_i','YKOR':'YKOR_i','ZKOR':'ZKOR_i'
                                       ,'pXCor':'pXCor_i'
                                       ,'pYCor':'pYCor_i'},inplace=True)    
            
            vFWVB=pd.merge(vFWVB,vKNOT,left_on='fkKK',right_on='pk')    
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','IDREFERENZ_x':'IDREFERENZ','pk_x':'pk','tk_x':'tk'},inplace=True)  
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                    #Ki
                   ,'NAME_i'
                   ,'KVR_i','TM_i'
                   ,'XKOR_i','YKOR_i','ZKOR_i'
                   ,'pXCor_i','pYCor_i'
                    #Kk
                   ,'NAME'
                   ,'KVR','TM'
                   ,'XKOR','YKOR','ZKOR'  
                   ,'pXCor','pYCor'
                   ,'fkCONT'        
                 ]]     
            vFWVB.rename(columns={'NAME':'NAME_k','KVR':'KVR_k','TM':'TM_k'},inplace=True)  
            vFWVB.rename(columns={'XKOR':'XKOR_k','YKOR':'YKOR_k','ZKOR':'ZKOR_k'
                                       ,'pXCor':'pXCor_k'
                                       ,'pYCor':'pYCor_k'},inplace=True)     
                        
            vFWVB=pd.merge(vFWVB,self.dataFrames['CONT'],left_on='fkCONT',right_on='pk')  
            vFWVB.rename(columns={'pk_x':'pk','tk_x':'tk','NAME':'CONT','ID':'CONT_ID','LFDNR':'CONT_LFDNR'},inplace=True)    
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK' ,'TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' ,'IMBG' ,'IRFV'
                    #FWVB IDs
                   ,'pk','tk'  
                    #Ki
                   ,'NAME_i'
                   ,'KVR_i','TM_i'
                   ,'XKOR_i','YKOR_i','ZKOR_i'
                   ,'pXCor_i','pYCor_i'
                    #Kk
                   ,'NAME_k'
                   ,'KVR_k','TM_k'
                   ,'XKOR_k','YKOR_k','ZKOR_k'  
                   ,'pXCor_k','pYCor_k'
                    #CONT
                    ,'CONT' 
                    ,'CONT_ID'
                    ,'CONT_LFDNR' 
                     ]]

            
            #logger.debug("{:s} vor WBLZ: {!s:s}".format(logStr,(vFWVB)))

            # Waermebilanzenzugehoerigkeit            
            blzKnoten=vWBLZ.merge(vKNOT,left_on='OBJID',right_on='tk')
            rowsTk,cols=blzKnoten.shape
            blzKnotenPk=vWBLZ.merge(vKNOT,left_on='OBJID',right_on='pk')
            rowsPk,cols=blzKnotenPk.shape
            # pks oder tks in OBJID?
            if rowsTk>=rowsPk:
                pass    
            else:
                # warning
                logger.warning("{:s}pk select: {:d} > tk select {:d}?!".format(logStr,rowsPk,rowsTk))

            blzKnoten=blzKnoten[[
             'AKTIV'            
            ,'BESCHREIBUNG_x'
            ,'IDIM'
            ,'NAME_x'
            #IDs (of the WBLZ)
            ,'pk_x'
            #
            ,'pk_y'
            ,'tk'
            ,'NAME_y'
            #
            ]]
            
            blzKnoten.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)
            blzKnoten.rename(columns={'NAME_x':'NAME'},inplace=True)
            blzKnoten.rename(columns={'pk_x':'pk'},inplace=True)
            blzKnoten.rename(columns={'pk_y':'pk_NODE'},inplace=True)
            blzKnoten.rename(columns={'NAME_y':'NAME_NODE'},inplace=True)

            #VL --------------
            blzKnotenFwvbVL=blzKnoten.merge(vFWVB,left_on='NAME_NODE',right_on='NAME_i') 

            blzKnotenFwvbVL.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)
            blzKnotenFwvbVL.rename(columns={'pk_x':'pk'},inplace=True)
            blzKnotenFwvbVL.rename(columns={'tk_x':'tk_NODE'},inplace=True)
            blzKnotenFwvbVL.rename(columns={'pk_y':'pk_FWVB'},inplace=True)
            blzKnotenFwvbVL.rename(columns={'tk_y':'tk_FWVB'},inplace=True)

            blzKnotenFwvbVL=blzKnotenFwvbVL[[
             'AKTIV'            
            ,'BESCHREIBUNG'
            ,'IDIM'
            ,'NAME'
            #IDs (of the WBLZ)
            ,'pk'
            #
            ,'pk_NODE'
            ,'tk_NODE'
            ,'NAME_NODE'
            #
            ,'pk_FWVB'
            ,'tk_FWVB'
            #
            ]]

            #RL ----------------
            blzKnotenFwvbRL=blzKnoten.merge(vFWVB,left_on='NAME_NODE',right_on='NAME_k') 

            blzKnotenFwvbRL.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG'},inplace=True)
            blzKnotenFwvbRL.rename(columns={'pk_x':'pk'},inplace=True)
            blzKnotenFwvbRL.rename(columns={'tk_x':'tk_NODE'},inplace=True)
            blzKnotenFwvbRL.rename(columns={'pk_y':'pk_FWVB'},inplace=True)
            blzKnotenFwvbRL.rename(columns={'tk_y':'tk_FWVB'},inplace=True)

            blzKnotenFwvbRL=blzKnotenFwvbRL[[
             'AKTIV'            
            ,'BESCHREIBUNG'
            ,'IDIM'
            ,'NAME'
            #IDs (of the WBLZ)
            ,'pk'
            #
            ,'pk_NODE'
            ,'tk_NODE'
            ,'NAME_NODE'
            #
            ,'pk_FWVB'
            ,'tk_FWVB'
            #
            ]]

            VLOk=vFWVB.merge(blzKnotenFwvbVL,left_on='NAME_i',right_on='NAME_NODE',suffixes=['_1','_2'])
            RLOk=vFWVB.merge(blzKnotenFwvbRL,left_on='NAME_k',right_on='NAME_NODE',suffixes=['_1','_2'])

            VLRLOk=VLOk.merge(RLOk,left_on='pk_FWVB',right_on='pk_FWVB',suffixes=['_VL','_RL'])
            #logger.debug("{:s}{!s:s}".format(logStr,(VLRLOk)))
            VLRLOk=VLRLOk[VLRLOk['NAME_VL']==VLRLOk['NAME_RL']][['pk_FWVB','NAME_VL']]
            VLRLOk.rename(columns={'NAME_VL':'NAME'},inplace=True)
            
            VLRLOk=VLRLOk.assign(wblzLfdNr=VLRLOk.sort_values(['NAME'], ascending=True)
                          .groupby(['pk_FWVB'])
                          .cumcount() + 1)

            vFWVB['WBLZ']=[list() for dummy in vFWVB['pk']]
            for index, row in vFWVB.merge(VLRLOk,left_on='pk',right_on='pk_FWVB',how='left').sort_values(by=['pk','NAME'],na_position='first').iterrows():                
                if pd.isnull(row.NAME):
                    continue
                row.WBLZ.append(row.NAME)

            #vFWVB[vFWVB['WBLZ'].apply(lambda x: 'BLNZ1' in x)]
            
            ## Last Kategorien (Load Categories); kategorisieren der FWVB nach Anschlusswert
            #Load=vFWVB.W0

            #bins=[]
            #binlabels=[]

            #bins.append(0)
            #binlabels.append('=0')

            #epsZero=0.001 #to distinguish FWVB Cat. with W0=0 from those with W0>0
            #bins.append(epsZero)
            #binlabels.append('>0')

            #bins.append(Load.quantile(.25))
            #binlabels.append('>=25%-Quart.')

            #if Load.median() < Load.mean(): #50%-Quartil < Mittelwert
            #    bins.append(Load.median()) 
            #    binlabels.append('>=Median')

            #bins.append(Load.mean())
            #binlabels.append('>=Mittelwert')

            #bins.append(bins[-1]*2)
            #binlabels.append('>=2xMittelw.')

            #if bins[-1] < Load.std():
            #    bins.append(Load.std())
            #    binlabels.append('>=Standardabw.')

            #if bins[-1] < 2*Load.std():
            #    bins.append(2*Load.std())
            #    binlabels.append('>=2*Standardabw.')

            #if bins[-1] < Load.quantile(.90):
            #    bins.append(Load.quantile(.90))
            #    binlabels.append('>=90%-Quartil')
            #else: 
            #    if bins[-1] < Load.quantile(.95):
            #        bins.append(Load.quantile(.95))
            #        binlabels.append('>=95%-Quartil')

            #bins.append(Load.max())
            #binlabels.append('Max.')

            #W0cat=pd.cut(Load,bins,include_lowest=True,right=True,precision=1)

            #W0catLabels=[x + '-: ' +  re.sub('\]$','[',re.sub('\(' ,'[', y))  for x,y in zip(binlabels[:-1],W0cat.cat.categories)]
            #W0catLabels[-1]=re.sub('\[$',']',W0catLabels[-1])

            #W0cat.cat.rename_categories(W0catLabels,inplace=True)

            ##vFWVB['W0cat']=W0cat
            ##vFWVB.groupby('W0Cat').describe()
            ##vFWVB.groupby('W0Cat').W0.sum()

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vFWVB,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vFWVB=pd.DataFrame()                 
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return vFWVB             

    #def vFWVB_Plt_Hist(self
    #                   ,epsZero=0.001 #to distinguish FWVB Cat. with W0=0 from those with W0>0
    #                   ,spaceBetweenCats=0.3 #the Space between the Categories; 1.0: no Space 
    #                   ):
    #    """
    #    Plots a Histogram-alike Presentation on gca().  
       
    #    """

    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
    #    try:  
    #        #Categories 
    #        bins=[]
    #        binlabels=[]

    #        bins.append(0)
    #        binlabels.append('=0')

    #        bins.append(epsZero)
    #        binlabels.append('>0')

    #        bins.append(vFWVB.W0.quantile(.25))
    #        binlabels.append('>=25%-Quart.')

    #        if vFWVB.W0.median() < vFWVB.W0.mean(): #50%-Quartil < Mittelwert
    #            bins.append(vFWVB.W0.median()) 
    #            binlabels.append('>=Median')

    #        bins.append(vFWVB.W0.mean())
    #        binlabels.append('>=Mittelwert')

    #        bins.append(bins[-1]*2)
    #        binlabels.append('>=2xMittelw.')

    #        if bins[-1] < vFWVB.W0.std():
    #            bins.append(vFWVB.W0.std())
    #            binlabels.append('>=Standardabw.')

    #        if bins[-1] < vFWVB.W0.quantile(.95):
    #            bins.append(vFWVB.W0.quantile(.95))
    #            binlabels.append('>=95%-Quartil')

    #        bins.append(vFWVB.W0.max())
    #        binlabels.append('Max.')

    #        W0cat=pd.cut(vFWVB.W0,bins,include_lowest=True,right=True,precision=1)

    #        W0catLabels=[x + '-: ' +  re.sub('\]$','[',re.sub('\(' ,'[', y))  for x,y in zip(binlabels[:-1],W0cat.cat.categories)]
    #        W0catLabels[-1]=re.sub('\[$',']',W0catLabels[-1])

    #        #Category Data
    #        W0catSumPercent=vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.sum()  /vFWVB[vFWVB.W0>=0].W0.sum() # kW Summe
    #        W0catAnzPercent=vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.count()/vFWVB[vFWVB.W0>=0].W0.count() # Anzahl Summe

    #        W0catSumPercentcs=W0catSumPercent.cumsum()
    #        W0catAnzPercentcs=W0catAnzPercent.cumsum()

    #        #Bar Layout
    #        numOfBarsPerCat=2 # MW u. Anzahl
    #        numOfCats=len(W0cat.cat.categories)
    #        widthPerBar=numOfCats/(numOfCats*numOfBarsPerCat)*min(1.-spaceBetweenCats,1.0)
    #        xCats0=np.arange(numOfCats) # the x-Coordinate of the left-most Bar per Cat


    #        ax=plt.gca()

    #        #1st MW Bars
    #        barsW0catSumPercent = ax.bar(xCats0,W0catSumPercent,widthPerBar)
    #        norm = colors.Normalize(W0catSumPercentcs.min(),W0catSumPercentcs.max())
    #        colorSumPercent=[]
    #        for thisfrac, thisbar in zip(W0catSumPercentcs,barsW0catSumPercent):
    #            color = plt.cm.cool(norm(thisfrac))
    #            thisbar.set_facecolor(color)
    #            colorSumPercent.append(color)

    #        #2nd Anz Bars
    #        barsW0catAnzPercent = ax.bar(xCats0+widthPerBar,W0catAnzPercent,widthPerBar)
    #        norm = colors.Normalize(W0catAnzPercentcs.min(),W0catAnzPercentcs.max())
    #        colorAnzPercent=[]
    #        for thisfrac, thisbar in zip(W0catAnzPercentcs,barsW0catAnzPercent):
    #            color = plt.cm.autumn(norm(thisfrac))
    #            thisbar.set_facecolor(color)
    #            colorAnzPercent.append(color)

    #        #xTicks
    #        xTicks=ax.set_xticks(xCats0+numOfBarsPerCat*widthPerBar/2) #xTicks in the Middle of each Cat.
    #        xTickValues=ax.get_xticks()

    #        #xLabels
    #        xTickLabels=ax.set_xticklabels(W0catLabels,rotation='vertical')
    #        for xTickLabel in xTickLabels:
    #            x,y=xTickLabel.get_position()
    #            xTickLabel.set_position((x,y-0.0625*numOfBarsPerCat)) #Space for Cat Datanumbers (one row per Measure)

    #        #yTicks rechts (0-1)
    #        yTicksR=[x/10 for x in np.arange(10)+1]
    #        yTicksR.insert(0,0)

    #        #yTicks links
    #        # 10 Abstaende / 11 Ticks wie die r. y-Achse
    #        yMaxL=max(W0catSumPercent.max(),W0catAnzPercent.max())
    #        dyMinL=yMaxL/(len(yTicksR)-1)
    #        dyMinLr=round(dyMinL,2)
    #        if dyMinLr*(len(yTicksR)-1) < yMaxL:
    #            dyL=dyMinLr+0.01
    #        else:
    #            dyL=dyMinLr
    #        yTicksL=[x*dyL for x in np.arange(10)+1]
    #        yTicksL.insert(0,0)
    #        yTicksLObjects=ax.set_yticks(yTicksL)
    #        yTicksL=ax.get_yticks()

    #        #r. y-Achse
    #        ax2 = ax.twinx()
    #        yTicksRObjects=ax2.set_yticks(yTicksR)
    #        yTicksR=ax2.get_yticks()

    #        #Sum Curves
    #        lineW0catSumPercent,=ax2.plot(xTickValues,W0catSumPercentcs,color='gray',linewidth=1.0, ls='-',marker='s',clip_on=False)
    #        lineW0catAnzPercent,=ax2.plot(xTickValues,W0catAnzPercentcs,color='gray',linewidth=1.0, ls='-',marker='o',clip_on=False)

    #        # Cat Datanumbers (one row per Measure)
    #        measureIdx=1

    #        for kWSum, x,color in zip(vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.sum(),xTickValues,colorSumPercent):
    #            txt="{0:.0f}".format(float(kWSum)/1000)
    #            ax.annotate(txt 
    #                        ,xy=(x, 0), xycoords=('data', 'axes fraction')
    #                        ,xytext=(0, measureIdx*-10), textcoords='offset points', va='top', ha='center'
    #                        ,color=color
    #                       )
    #        ax.annotate("{0:.0f} MW Ges.".format(float(vFWVB[vFWVB.W0>=0].W0.sum())/1000) 
    #                        ,xy=(x, 0), xycoords=('data', 'axes fraction')
    #                        ,xytext=(+20,measureIdx*-10), textcoords='offset points', va='top', ha='left'
    #                   )             

    #        measureIdx=measureIdx+1
    #        for count,x,color in zip(vFWVB[vFWVB.W0>=0].groupby(W0cat).W0.count(),xTickValues,colorAnzPercent):
    #            txt="{0:d}".format(int(count))
    #            ax.annotate(txt
    #                       ,xy=(x, 0),xycoords=('data', 'axes fraction')
    #                       ,xytext=(0, measureIdx*-10),textcoords='offset points', va='top', ha='center'
    #                       ,color=color
    #                       )
    #        ax.annotate("{0:d} Anz Ges.".format(int(vFWVB[vFWVB.W0>=0].W0.count())) 
    #                      ,xy=(x, 0),xycoords=('data', 'axes fraction')
    #                      ,xytext=(+20, measureIdx*-10), textcoords='offset points', va='top', ha='left'
    #                   )  
            
    #        #y-Labels 
    #        txyl=ax.set_ylabel('MW/MW Ges. u. Anz/Anz Ges.')
    #        txyr=ax2.set_ylabel('MW kum. in % u. Anz kum. in %')

    #        legend=plt.legend([lineW0catSumPercent,lineW0catAnzPercent],['MW kum. in %','Anz kum. in %'],loc='upper left')
    #        plt.grid()

    #    except Exception as e:
    #        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
    #        logger.error(logStrFinal) 
    #        raise XmError(logStrFinal)                
    #    else:
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def Mx(self,mx=None):
        """
        Mapping of Xm to Mx   
        >self.mx
        >self.__Mx1() (vNRCV_Mx1)
        >self.__Mx2() (vROHR-Attributes)                 
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            if isinstance(mx,Mx):
                self.mx=mx
            else:
                (wDir,modelDir,modelName)=self.getWDirModelDirModelName()
                mx1File=os.path.join(wDir,os.path.join(modelDir,modelName))+'.MX1'            
                self.mx=Mx(mx1File=mx1File,NoMxsRead=True)

            self.__Mx1()
            self.__Mx2()
                                                       
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                       
            logger.error(logStrFinal) 
                     
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    def __Mx1(self):
        """
        vNRCV_Mx1:
            One row per NRCV-referenced Sir3sID in mx1Df:
               'Sir3sID'
              ,'cRefLfdNr' 
              # CONT
              ,'CONT'
              ,'CONT_ID'
              ,'CONT_LFDNR'
              # DPGR
              ,'DPGR'
               # Data (of the DPGR_ROW)
              ,'OBJTYPE'
              ,'fkOBJTYPE'
              ,'ATTRTYPE'
              # IDs (of the DPGR_ROW)
              ,'pk_ROWS'
              ,'tk_ROWS'       
              # IDs (of the NRCV)
              ,'pk'
              ,'tk' 
              ,'pXYLB'                   
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             

            vNRCV_Mx1=None
            vNRCV=self.dataFrames['vNRCV']
            
            vNRCV_Mx1=vNRCV.merge(self.mx.mx1Df,left_on='fkOBJTYPE',right_on='OBJTYPE_PK',suffixes=['_NR','_MX1'])

            vNRCV_Mx1=vNRCV_Mx1[(vNRCV_Mx1['cRefLfdNr']==1)
                  &
                  (vNRCV_Mx1['OBJTYPE_NR']==vNRCV_Mx1['OBJTYPE_MX1'])
                  &
                  (vNRCV_Mx1['ATTRTYPE_NR']==vNRCV_Mx1['ATTRTYPE_MX1'])
                 ]

            # reindex:
            vNRCV_Mx1=pd.DataFrame(vNRCV_Mx1.values,columns=vNRCV_Mx1.columns)
            
            vNRCV_Mx1=vNRCV_Mx1[[  'Sir3sID'
              ,'cRefLfdNr' 
              # CONT
              ,'CONT'
              ,'CONT_ID'
              ,'CONT_LFDNR'
              # DPGR
              ,'DPGR'
               # Data (of the DPGR_ROW)
              ,'OBJTYPE_NR'
              ,'fkOBJTYPE'
              ,'ATTRTYPE_NR'
              # IDs (of the DPGR_ROW)
              ,'pk_ROWS'
              ,'tk_ROWS'       
              # IDs (of the NRCV)
              ,'pk'
              ,'tk'
              ,'pXYLB'
            ]]

            vNRCV_Mx1.rename(columns={'OBJTYPE_NR':'OBJTYPE','ATTRTYPE_NR':'ATTRTYPE'},inplace=True)  

            vNRCV_Mx1.sort_values(['Sir3sID'],ascending=True,inplace=True)
            #reindex:
            vNRCV_Mx1=pd.DataFrame(vNRCV_Mx1.values,columns=vNRCV_Mx1.columns)
                                            
        except Exception as e:            
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vNRCV,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vNRCV_Mx1=pd.DataFrame()                 
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            self.dataFrames['vNRCV_Mx1']=vNRCV_Mx1

    def __Mx2(self):
        """
        mx2Idx    for Pipes (vROHR)
        mx2NofPts for Pipes (vROHR)
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            tksROHRMx=self.mx.mx2Df[
            (self.mx.mx2Df['ObjType'].str.contains('ROHR'))
            &
            ~(self.mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
            ]['Data'].iloc[0]

            vROHR=self.dataFrames['vROHR']

            tksROHRXm=vROHR['tk']
            mxTkRohrIdx=[tksROHRMx.index(tk) for tk in tksROHRXm]

            vROHR['mx2Idx']=pd.Series(mxTkRohrIdx)
            
            nOfPtsROHRMx=self.mx.mx2Df[
            (self.mx.mx2Df['ObjType'].str.contains('ROHR'))
            &
            (self.mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
            ]['Data'].iloc[0]

            vROHR['mx2NofPts']=pd.Series(nOfPtsROHRMx)
                                                                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal) 
                          
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

