"""
>>> # ---
>>> # Imports
>>> # ---
>>> import os
>>> import logging
>>> logger = logging.getLogger('PT3S.Xm')  
>>> # ---
>>> # path
>>> # ---
>>> if __name__ == "__main__":
...   try:
...      dummy=__file__
...      logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ','path = os.path.dirname(__file__)'," .")) 
...      path = os.path.dirname(__file__)
...   except NameError:    
...      logger.debug("{0:s}{1:s}{2:s}".format('DOCTEST: __main__ Context: ',"path = '.' because __file__ not defined: ","from Xm import Xm follows ...")) 
...      path = '.'
...      from Xm import Xm
... else:
...    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('DOCTEST: Not __main__ Context: ','__name__: ',__name__,"path = '.'")) 
...    path = '.'
>>> try:
...    from PT3S import Mx
... except ImportError:
...    logger.debug("{0:s}{1:s}".format("DOCTEST: ImportError: from PT3S import Mx: ","- trying import Mx instead ... maybe pip install -e . is active ..."))  
...    import Mx
>>> # ---
>>> # testDir
>>> # ---
>>> # globs={'testDir':'testdata'}
>>> try:
...    dummy= testDir
... except NameError:
...    testDir='testdata' 
>>> import pandas as pd
>>> # ---
>>> # Clean Up
>>> # ---
>>> h5File=os.path.join(os.path.join(path,testDir),'OneLPipe.h5')
>>> if os.path.exists(h5File):                        
...    os.remove(h5File)
>>> # ---
>>> # Init
>>> # ---
>>> xmlFile=os.path.join(os.path.join(path,testDir),'OneLPipe.XML')
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
(2, 41)
>>> vROHR=xm.dataFrames['vROHR']
>>> vROHR.shape
(1, 74)
>>> isinstance(vROHR['pXCors'],pd.core.series.Series)
True
>>> vROHR['pXCors'][0]
[0.0, 500.0]
>>> vROHR.pYCors[0]
[0.0, 0.0]
>>> # ---
>>> # getWDirModelDirModelName()
>>> # ---
>>> (wDir,modelDir,modelName,mx1File)=xm.getWDirModelDirModelName()
>>> modelName
'M-1-0-1'
>>> # ---
>>> # H5-Deletion if NoH5Read=True
>>> # ---
>>> if os.path.exists(xm.h5File):                        
...    os.remove(xm.h5File)
>>> xm=Xm(xmlFile=xmlFile)
>>> xm.ToH5()
>>> os.path.exists(xm.h5File)
True
>>> xm=Xm(xmlFile=xmlFile,NoH5Read=True)
>>> os.path.exists(xm.h5File)
False
>>> # ---
>>> # print-Options
>>> # ---
>>> pd.set_option('display.max_columns',None)
>>> pd.set_option('display.max_rows',None)
>>> pd.set_option('display.max_colwidth',666666)   
>>> pd.set_option('display.width',666666666)
>>> # ---
>>> # vKNOT
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vKNOT',dropColList=['LFKT_NAME','LF','LF_min','LF_max','PVAR_NAME','PH','PH_min','PH_max','PZON_NAME','FSTF_NAME','STOF_NAME','GMIX_NAME','UTMP_NAME','2L_NAME','2L_KVR','fkHYDR','fkFQPS']))
  NAME BESCHREIBUNG             IDREFERENZ      CONT CONT_ID  CONT_LFDNR  CONT_VKNO  KTYP LFAKT    QM_EIN QVAR_NAME  QM  QM_min  QM_max KVR  TE  TM XKOR YKOR ZKOR                   pk                   tk  pXCor  pYCor
0    I          NaN  3S5642914844465475844  OneLPipe    1001         NaN        NaN  QKON     1  176.7146       NaN NaN     NaN     NaN   0 NaN  10  300  600   10  5642914844465475844  5642914844465475844    0.0    0.0
1    K          NaN  3S5289899964753656852  OneLPipe    1001         NaN        NaN  PKON     1         0       NaN NaN     NaN     NaN   0 NaN  10  800  600   10  5289899964753656852  5289899964753656852  500.0    0.0
>>> # ---
>>> # vROHR
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vROHR',dropColList=['NAME_i_2L','NAME_k_2L']))
  BESCHREIBUNG             IDREFERENZ BAUJAHR HAL IPLANUNG KENNUNG      L LZU   RAU ZAUS ZEIN ZUML JLAMBS LAMBDA0 ASOLL INDSCHALL KVR AUSFALLZEIT DA   DI   DN KT PN REHABILITATION REPARATUR  S WSTEIG WTIEFE LTGR_NAME  LTGR_BESCHREIBUNG SICHTBARKEIT VERLEGEART DTRO_NAME                           DTRO_BESCHREIBUNG        E fkSTRASSE fkSRAT                   pk                   tk IRTRENN LECKSTART LECKEND LECKMENGE LECKORT LECKSTATUS QSVB ZVLIMPTNZ KANTENZV      CONT CONT_ID  CONT_LFDNR NAME_i KVR_i TM_i XKOR_i YKOR_i ZKOR_i NAME_k KVR_k TM_k XKOR_k YKOR_k ZKOR_k  pXCor_i  pYCor_i  pXCor_k  pYCor_k        pXCors      pYCors    pWAYPXCors  pWAYPYCors                              WAYP
0          NaN  3S4737064599036143765    2017   0        1       0  10000   0  0.25    0    0    0      1   0.025  1000         0   0           0  0  250  250  0  0              0         0  0      0      0   STDROHR                NaN            1     999999   STDROHR  Standard-Druckrohre mit di = DN (DIN 2402)  2.1E+11        -1     -1  4737064599036143765  4737064599036143765       0         0       0         0       0          0    0         0        0  OneLPipe    1001         NaN      I     0   10    300    600     10      K     0   10    800    600     10      0.0      0.0    500.0      0.0  [0.0, 500.0]  [0.0, 0.0]  [0.0, 500.0]  [0.0, 0.0]  [(300.0, 600.0), (800.0, 600.0)]
>>> # ---
>>> # Clean Up
>>> # ---
>>> if os.path.exists(xm.h5File):                        
...    os.remove(xm.h5File)
>>> # ---
>>> # LocalHeatingNetwork
>>> # ---
>>> xmlFile=os.path.join(os.path.join(path,testDir),'LocalHeatingNetwork.XML')
>>> xm=Xm(xmlFile=xmlFile)
>>> # ---
>>> # vKNOT
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vKNOT',dropColList=['LFKT_NAME','LF','LF_min','LF_max','PVAR_NAME','PH','PH_min','PH_max','PZON_NAME','FSTF_NAME','STOF_NAME','GMIX_NAME','UTMP_NAME','2L_NAME','2L_KVR','fkHYDR','fkFQPS']))
           NAME                    BESCHREIBUNG IDREFERENZ                                      CONT CONT_ID CONT_LFDNR CONT_VKNO  KTYP LFAKT QM_EIN QVAR_NAME  QM  QM_min  QM_max KVR  TE  TM     XKOR     YKOR ZKOR                   pk                   tk   pXCor  pYCor
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
22          R-1          Anbindung Druckhaltung         -1                                      BHKW    1002         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60      195       20   20  5557222628687032084  5557222628687032084   195.0   20.0
>>> # ---
>>> # vROHR
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vROHR',dropColList=['NAME_i_2L','NAME_k_2L']))
   BESCHREIBUNG IDREFERENZ BAUJAHR HAL IPLANUNG KENNUNG       L LZU  RAU ZAUS ZEIN ZUML JLAMBS LAMBDA0 ASOLL INDSCHALL KVR  AUSFALLZEIT     DA     DI   DN     KT  PN  REHABILITATION  REPARATUR    S WSTEIG WTIEFE LTGR_NAME            LTGR_BESCHREIBUNG SICHTBARKEIT VERLEGEART DTRO_NAME                        DTRO_BESCHREIBUNG        E fkSTRASSE fkSRAT                   pk                   tk IRTRENN LECKSTART LECKEND LECKMENGE LECKORT LECKSTATUS QSVB ZVLIMPTNZ KANTENZV                                      CONT CONT_ID CONT_LFDNR  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_i  pYCor_i  pXCor_k  pYCor_k            pXCors          pYCors                                pWAYPXCors                                pWAYPYCors                                                                                               WAYP
0          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4613782368750024999  4613782368750024999       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K004     2   60  2541539  5706361     20  R-K005     2   60  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]    [807.8999999999069, 895.9500000001863]  [140.09999999962747, 142.04999999981374]                                                 [(2541547.9, 5706349.1), (2541635.95, 5706351.05)]
1          None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4614949065966596185  4614949065966596185       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K002     1   90  2541059  5706265     20  V-K003     1   90  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]                [319.0, 716.9500000001863]               [56.049999999813735, 136.0]                                                 [(2541059.0, 5706265.05), (2541456.95, 5706345.0)]
2          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4637102239750163477  4637102239750163477       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K003     2   60  2541457  5706345     20  R-K004     2   60  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]    [725.8500000000931, 807.8999999999069]  [124.04999999981374, 140.09999999962747]                                                 [(2541465.85, 5706333.05), (2541547.9, 5706349.1)]
3          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4713733238627697042  4713733238627697042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K004     1   90  2541539  5706361     20  V-K005     1   90  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]                [799.0, 887.0499999998137]                            [152.0, 154.0]                                                  [(2541539.0, 5706361.0), (2541627.05, 5706363.0)]
4          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4789218195240364437  4789218195240364437       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K001     1   90  2540867  5706228     20  V-K002     1   90  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]                            [127.0, 319.0]                [19.0, 56.049999999813735]                                                  [(2540867.0, 5706228.0), (2541059.0, 5706265.05)]
5          None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4945727430885351042  4945727430885351042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K006     2   60  2541790  5706338     20  R-K007     2   60  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]  [1058.8500000000931, 1167.8999999999069]               [117.0, 104.09999999962747]                                                  [(2541798.85, 5706326.0), (2541907.9, 5706313.1)]
6          None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4984202422877610920  4984202422877610920       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K000     1   90  2540793  5706209     20  V-K001     1   90  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]               [53.049999999813735, 127.0]             [-0.049999999813735485, 19.0]                                                 [(2540793.05, 5706208.95), (2540867.0, 5706228.0)]
7          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5037777106796980248  5037777106796980248       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K003     1   90  2541457  5706345     20  V-K004     1   90  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]                [716.9500000001863, 799.0]                            [136.0, 152.0]                                                  [(2541456.95, 5706345.0), (2541539.0, 5706361.0)]
8          None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5123819811204259837  5123819811204259837       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K005     1   90  2541627  5706363     20  V-K006     1   90  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]   [887.0499999998137, 1049.9500000001863]               [154.0, 128.95000000018626]                                                [(2541627.05, 5706363.0), (2541789.95, 5706337.95)]
9          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5266224553324203132  5266224553324203132       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K001     2   60  2540867  5706228     20  R-K002     2   60  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]  [135.89999999990687, 327.89999999990687]   [7.0499999998137355, 44.09999999962747]                                                  [(2540875.9, 5706216.05), (2541067.9, 5706253.1)]
10         None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5379365049009065623  5379365049009065623       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K002     2   60  2541059  5706265     20  R-K003     2   60  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]   [327.89999999990687, 725.8500000000931]   [44.09999999962747, 124.04999999981374]                                                 [(2541067.9, 5706253.1), (2541465.85, 5706333.05)]
11         None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5611703699850694889  5611703699850694889       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K005     2   60  2541627  5706363     20  R-K006     2   60  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]   [895.9500000001863, 1058.8500000000931]               [142.04999999981374, 117.0]                                                [(2541635.95, 5706351.05), (2541798.85, 5706326.0)]
12         None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5620197984230756681  5620197984230756681       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K006     1   90  2541790  5706338     20  V-K007     1   90  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]              [1049.9500000001863, 1159.0]  [128.95000000018626, 116.04999999981374]                                                [(2541789.95, 5706337.95), (2541899.0, 5706325.05)]
13         None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5647213228462830353  5647213228462830353       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K000     2   60  2540793  5706209     20  R-K001     2   60  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]  [61.950000000186265, 135.89999999990687]               [-12.0, 7.0499999998137355]                                                 [(2540801.95, 5706197.0), (2540875.9, 5706216.05)]
14         None         -1    None   0        1       0   73.42   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4769996343148550485  4769996343148550485       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     R-L     2   60  2540740  5706225     20  R-K000     2   60  2540793  5706209     20      0.0     16.0     53.0      0.0       [0.0, 53.0]     [16.0, 0.0]     [0.0, 24.0, 45.0, 61.950000000186265]                [16.0, 16.0, -12.0, -12.0]  [(2540740.0, 5706225.0), (2540764.0, 5706225.0), (2540785.0, 5706197.0), (2540801.95, 5706197.0)]
15         None         -1    None   0        1       0    68.6   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4939422678063487923  4939422678063487923       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     V-L     1   90  2540740  5706240     20  V-K000     1   90  2540793  5706209     20      0.0     31.0     53.0      0.0       [0.0, 53.0]     [31.0, 0.0]           [0.0, 30.0, 53.049999999813735]       [31.0, 31.0, -0.049999999813735485]                         [(2540740.0, 5706240.0), (2540770.0, 5706240.0), (2540793.05, 5706208.95)]
>>> # ---
>>> # vWBLZ
>>> # ---
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vWBLZ']).replace('\\n','\\n   ')))
'''   AKTIV BESCHREIBUNG IDIM       NAME OBJTYPE                OBJID                   pk
   0      1  Wärmebilanz    0      BLNZ1    KNOT  4731792362611615619  5579937562601803472
   1      1  Wärmebilanz    0      BLNZ1    KNOT  5364712333175450942  5579937562601803472
   2      1  Wärmebilanz    0    BLNZ1u5    KNOT  5183147862966701025  5187647097142898375
   3      1  Wärmebilanz    0    BLNZ1u5    KNOT  5444644492819213978  5187647097142898375
   4      1  Wärmebilanz    0    BLNZ1u5    KNOT  4731792362611615619  5187647097142898375
   5      1  Wärmebilanz    0    BLNZ1u5    KNOT  5364712333175450942  5187647097142898375
   6      1  Wärmebilanz    0  BLNZ1u5u7    KNOT  5183147862966701025  4694700216019268978
   7      1  Wärmebilanz    0  BLNZ1u5u7    KNOT  5444644492819213978  4694700216019268978
   8      1  Wärmebilanz    0  BLNZ1u5u7    KNOT  4731792362611615619  4694700216019268978
   9      1  Wärmebilanz    0  BLNZ1u5u7    KNOT  5364712333175450942  4694700216019268978
   10     1  Wärmebilanz    0  BLNZ1u5u7    KNOT  5508992300317633799  4694700216019268978
   11     1  Wärmebilanz    0  BLNZ1u5u7    KNOT  5741235692335544560  4694700216019268978
   12     1  Wärmebilanz    0      BLNZ5    KNOT  5183147862966701025  5581152085151655438
   13     1  Wärmebilanz    0      BLNZ5    KNOT  5444644492819213978  5581152085151655438'''
>>> # ---
>>> # vAGSN
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vAGSN',end=7,dropColList=['nrObjIdTypeInAgsn']))
  LFDNR                                      NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  Layer nextNODE  compNr
0     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  4939422678063487923  5252525269080005909  5252525269080005909              1      1   V-K000       1
1     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  4984202422877610920  5252525269080005909  5252525269080005909              2      1   V-K001       1
2     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  4789218195240364437  5252525269080005909  5252525269080005909              3      1   V-K002       1
3     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  4614949065966596185  5252525269080005909  5252525269080005909              4      1   V-K003       1
4     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  5037777106796980248  5252525269080005909  5252525269080005909              5      1   V-K004       1
5     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  4713733238627697042  5252525269080005909  5252525269080005909              6      1   V-K005       1
6     1  Netzdruckdiagramm VL/RL: BHKW - Netzende   101    ROHR  5123819811204259837  5252525269080005909  5252525269080005909              7      1   V-K006       1
>>> # ---
>>> # vFWVB
>>> # ---
>>> print("'''{:s}'''".format(repr(xm.dataFrames['vFWVB']).replace('\\n','\\n   ')))
'''  BESCHREIBUNG IDREFERENZ   W0  LFK  W0LFK  TVL0  TRS0  LFKT      W  W_min  W_max  INDTR  TRSK  VTYP  DPHAUS  IMBG  IRFV                   pk                   tk  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  pXCor_i  pYCor_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_k  pYCor_k                                      CONT CONT_ID CONT_LFDNR                         WBLZ
   0            1         -1  200  0.8  160.0    90    50  LFKT  160.0  160.0  160.0      1    55    14     0.7     0   0.0  4643800032883366034  4643800032883366034  V-K002     1   90  2541059  5706265     20    319.0     56.0  R-K002     2   60  2541059  5706265     20    319.0     56.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  [BLNZ1, BLNZ1u5, BLNZ1u5u7]
   1            3         -1  200  1.0  200.0    90    65  LFKT  200.0  200.0  200.0      1    65    14     0.7     0   0.0  4704603947372595298  4704603947372595298  V-K004     1   90  2541539  5706361     20    799.0    152.0  R-K004     2   60  2541539  5706361     20    799.0    152.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           []
   2            4         -1  200  0.8  160.0    90    60  LFKT  160.0  160.0  160.0      1    60    14     0.7     0   0.0  5121101823283893406  5121101823283893406  V-K005     1   90  2541627  5706363     20    887.0    154.0  R-K005     2   60  2541627  5706363     20    887.0    154.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  [BLNZ1u5, BLNZ1u5u7, BLNZ5]
   3            5         -1  200  0.8  160.0    90    55  LFKT  160.0  160.0  160.0      1    55    14     0.7     0   0.0  5400405917816384862  5400405917816384862  V-K007     1   90  2541899  5706325     20   1159.0    116.0  R-K007     2   60  2541899  5706325     20   1159.0    116.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                  [BLNZ1u5u7]
   4            2         -1  200  0.6  120.0    90    60  LFKT  120.0  120.0  120.0      1    62    14     0.7     0   0.0  5695730293103267172  5695730293103267172  V-K003     1   90  2541457  5706345     20    717.0    136.0  R-K003     2   60  2541457  5706345     20    717.0    136.0  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1                           []'''
>>> # ---
>>> # vLAYR
>>> # ---
>>> # print("'''{:s}'''".format(repr(xm.dataFrames['vLAYR'].sort_values(['LFDNR','NAME','OBJTYPE','OBJID'],ascending=True)).replace('\\n','\\n   ')))
>>> print(xm._getvXXXXAsOneString(vXXXX='vLAYR'))
   LFDNR           NAME OBJTYPE                OBJID                   pk                   tk  nrObjInGroup  nrObjtypeInGroup
0      1        Vorlauf    FWES  5638756766880678918  5206516471428693478  5206516471428693478             1                 1
1      1        Vorlauf    KNOT  4731792362611615619  5206516471428693478  5206516471428693478             1                 1
2      1        Vorlauf    KNOT  4756962427318766791  5206516471428693478  5206516471428693478             1                 2
3      1        Vorlauf    KNOT  4766681917240867943  5206516471428693478  5206516471428693478             1                 3
4      1        Vorlauf    KNOT  5049461676240771430  5206516471428693478  5206516471428693478             1                 4
5      1        Vorlauf    KNOT  5370423799772591808  5206516471428693478  5206516471428693478             1                 5
6      1        Vorlauf    KNOT  5444644492819213978  5206516471428693478  5206516471428693478             1                 6
7      1        Vorlauf    KNOT  5515313800585145571  5206516471428693478  5206516471428693478             1                 7
8      1        Vorlauf    KNOT  5646671866542823796  5206516471428693478  5206516471428693478             1                 8
9      1        Vorlauf    KNOT  5736262931552588702  5206516471428693478  5206516471428693478             1                 9
10     1        Vorlauf    KNOT  5741235692335544560  5206516471428693478  5206516471428693478             1                10
11     1        Vorlauf    ROHR  4614949065966596185  5206516471428693478  5206516471428693478             1                 1
12     1        Vorlauf    ROHR  4713733238627697042  5206516471428693478  5206516471428693478             1                 2
13     1        Vorlauf    ROHR  4789218195240364437  5206516471428693478  5206516471428693478             1                 3
14     1        Vorlauf    ROHR  4939422678063487923  5206516471428693478  5206516471428693478             1                 4
15     1        Vorlauf    ROHR  4984202422877610920  5206516471428693478  5206516471428693478             1                 5
16     1        Vorlauf    ROHR  5037777106796980248  5206516471428693478  5206516471428693478             1                 6
17     1        Vorlauf    ROHR  5123819811204259837  5206516471428693478  5206516471428693478             1                 7
18     1        Vorlauf    ROHR  5620197984230756681  5206516471428693478  5206516471428693478             1                 8
19     1        Vorlauf    VENT  4678923650983295610  5206516471428693478  5206516471428693478             1                 1
20     2       Rücklauf    KLAP  4801110583764519435  4693347477612662930  4693347477612662930             1                 1
21     2       Rücklauf    KNOT  4638663808856251977  4693347477612662930  4693347477612662930             1                 1
22     2       Rücklauf    KNOT  4807712987325933680  4693347477612662930  4693347477612662930             1                 2
23     2       Rücklauf    KNOT  4891048046264179170  4693347477612662930  4693347477612662930             1                 3
24     2       Rücklauf    KNOT  4979785838440534851  4693347477612662930  4693347477612662930             1                 4
25     2       Rücklauf    KNOT  5002109894154139899  4693347477612662930  4693347477612662930             1                 5
26     2       Rücklauf    KNOT  5183147862966701025  4693347477612662930  4693347477612662930             1                 6
27     2       Rücklauf    KNOT  5219230031772497417  4693347477612662930  4693347477612662930             1                 7
28     2       Rücklauf    KNOT  5356267303828212700  4693347477612662930  4693347477612662930             1                 8
29     2       Rücklauf    KNOT  5364712333175450942  4693347477612662930  4693347477612662930             1                 9
30     2       Rücklauf    KNOT  5397990465339071638  4693347477612662930  4693347477612662930             1                10
31     2       Rücklauf    KNOT  5508992300317633799  4693347477612662930  4693347477612662930             1                11
32     2       Rücklauf    KNOT  5543326527366090679  4693347477612662930  4693347477612662930             1                12
33     2       Rücklauf    KNOT  5557222628687032084  4693347477612662930  4693347477612662930             1                13
34     2       Rücklauf    PUMP  5481331875203087055  4693347477612662930  4693347477612662930             1                 1
35     2       Rücklauf    ROHR  4613782368750024999  4693347477612662930  4693347477612662930             1                 1
36     2       Rücklauf    ROHR  4637102239750163477  4693347477612662930  4693347477612662930             1                 2
37     2       Rücklauf    ROHR  4769996343148550485  4693347477612662930  4693347477612662930             1                 3
38     2       Rücklauf    ROHR  4945727430885351042  4693347477612662930  4693347477612662930             1                 4
39     2       Rücklauf    ROHR  5266224553324203132  4693347477612662930  4693347477612662930             1                 5
40     2       Rücklauf    ROHR  5379365049009065623  4693347477612662930  4693347477612662930             1                 6
41     2       Rücklauf    ROHR  5611703699850694889  4693347477612662930  4693347477612662930             1                 7
42     2       Rücklauf    ROHR  5647213228462830353  4693347477612662930  4693347477612662930             1                 8
43     2       Rücklauf    VENT  4897018421024717974  4693347477612662930  4693347477612662930             1                 1
44     2       Rücklauf    VENT  5525310316015533093  4693347477612662930  4693347477612662930             1                 2
45     3  Kundenanlagen    FWVB  4643800032883366034  5003333277973347346  5003333277973347346             1                 1
46     3  Kundenanlagen    FWVB  4704603947372595298  5003333277973347346  5003333277973347346             1                 2
47     3  Kundenanlagen    FWVB  5121101823283893406  5003333277973347346  5003333277973347346             1                 3
48     3  Kundenanlagen    FWVB  5400405917816384862  5003333277973347346  5003333277973347346             1                 4
49     3  Kundenanlagen    FWVB  5695730293103267172  5003333277973347346  5003333277973347346             1                 5
50     4           BHKW    BSYM  5043395081363401573  5555393404073362943  5555393404073362943             1                 1
51     4           BHKW    TEXT  5056836766824229789  5555393404073362943  5555393404073362943             1                 1
52     4           BHKW    TEXT  5329748935118523443  5555393404073362943  5555393404073362943             1                 2
53     5          Texte    ARRW  4664845735864571219  5394410243594912680  5394410243594912680             1                 1
54     5          Texte    ARRW  4902474974831811106  5394410243594912680  5394410243594912680             1                 2
55     5          Texte    ARRW  5026846801782366678  5394410243594912680  5394410243594912680             1                 3
56     5          Texte    ARRW  5688313372729413840  5394410243594912680  5394410243594912680             1                 4
57     5          Texte    NRCV  4681213816714574464  5394410243594912680  5394410243594912680             1                 1
58     5          Texte    NRCV  4857294696992797631  5394410243594912680  5394410243594912680             1                 2
59     5          Texte    NRCV  4914949875368816179  5394410243594912680  5394410243594912680             1                 3
60     5          Texte    NRCV  4946584950744559030  5394410243594912680  5394410243594912680             1                 4
61     5          Texte    NRCV  4968703141722117357  5394410243594912680  5394410243594912680             1                 5
62     5          Texte    NRCV  5091374651838464239  5394410243594912680  5394410243594912680             1                 6
63     5          Texte    NRCV  5097127385155151127  5394410243594912680  5394410243594912680             1                 7
64     5          Texte    NRCV  5179988968597313889  5394410243594912680  5394410243594912680             1                 8
65     5          Texte    NRCV  5281885868749421521  5394410243594912680  5394410243594912680             1                 9
66     5          Texte    NRCV  5410904806390050339  5394410243594912680  5394410243594912680             1                10
67     5          Texte    NRCV  5476262878682325254  5394410243594912680  5394410243594912680             1                11
68     5          Texte    NRCV  5557806245003742769  5394410243594912680  5394410243594912680             1                12
69     5          Texte    RECT  4994817837124479818  5394410243594912680  5394410243594912680             1                 1
70     5          Texte    RPFL  5158870568935841216  5394410243594912680  5394410243594912680             1                 1
71     5          Texte    TEXT  4628671704393700430  5394410243594912680  5394410243594912680             1                 1
72     5          Texte    TEXT  4654104397990769217  5394410243594912680  5394410243594912680             1                 2
73     5          Texte    TEXT  4666644549022031339  5394410243594912680  5394410243594912680             1                 3
74     5          Texte    TEXT  4693143208412077585  5394410243594912680  5394410243594912680             1                 4
75     5          Texte    TEXT  4768731522550494423  5394410243594912680  5394410243594912680             1                 5
76     5          Texte    TEXT  4770844990228490264  5394410243594912680  5394410243594912680             1                 6
77     5          Texte    TEXT  4782197969172967134  5394410243594912680  5394410243594912680             1                 7
78     5          Texte    TEXT  4855692488683645764  5394410243594912680  5394410243594912680             1                 8
79     5          Texte    TEXT  4965628942555351751  5394410243594912680  5394410243594912680             1                 9
80     5          Texte    TEXT  4995961504641886710  5394410243594912680  5394410243594912680             1                10
81     5          Texte    TEXT  5017907661719368413  5394410243594912680  5394410243594912680             1                11
82     5          Texte    TEXT  5028052147238787802  5394410243594912680  5394410243594912680             1                12
83     5          Texte    TEXT  5036153631350515544  5394410243594912680  5394410243594912680             1                13
84     5          Texte    TEXT  5054433315422452796  5394410243594912680  5394410243594912680             1                14
85     5          Texte    TEXT  5108336975548011049  5394410243594912680  5394410243594912680             1                15
86     5          Texte    TEXT  5262441422409836340  5394410243594912680  5394410243594912680             1                16
87     5          Texte    TEXT  5297832234834839298  5394410243594912680  5394410243594912680             1                17
88     5          Texte    TEXT  5370727463979416592  5394410243594912680  5394410243594912680             1                18
89     5          Texte    TEXT  5421223289472778073  5394410243594912680  5394410243594912680             1                19
90     5          Texte    TEXT  5501963349880613918  5394410243594912680  5394410243594912680             1                20
91     5          Texte    TEXT  5502619581048467908  5394410243594912680  5394410243594912680             1                21
92     5          Texte    TEXT  5540395812045688781  5394410243594912680  5394410243594912680             1                22
93     5          Texte    TEXT  5550982489075668484  5394410243594912680  5394410243594912680             1                23
94     5          Texte    TEXT  5610916400841895317  5394410243594912680  5394410243594912680             1                24
95     5          Texte    TEXT  5646820849868629537  5394410243594912680  5394410243594912680             1                25
96     5          Texte    TEXT  5696590398594231893  5394410243594912680  5394410243594912680             1                26
97     5          Texte    TEXT  5697088036451277538  5394410243594912680  5394410243594912680             1                27
>>> # ---
>>> # vGTXT
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vGTXT',sortList=['CONT_ID','pk'],index=False,header=False))                                 
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                          numerische Anzeige:  4614148870174765680  4614148870174765680                           (219.0, -278.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                           Georeferenzpunkt 2  4628671704393700430  4628671704393700430              (1115.9500000001863, -323.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                                        Block  4666644549022031339  4666644549022031339                            (-58.0, -77.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                           numerische Anzeige  4693143208412077585  4693143208412077585                            (1211.0, -9.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                             Knoten und Rohre  4995961504641886710  4995961504641886710                            (570.0, -49.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                                Vorlaufstrang  5017907661719368413  5017907661719368413  (358.20699999993667, 220.39499999955297)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                          LocalHeatingNetwork  5028052147238787802  5028052147238787802                           (1163.0, 536.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1   Tel. 05131 - 4980-0 ; Fax. 05131 - 4980-15  5054433315422452796  5054433315422452796                         (-230.0, -1143.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                    Kontrolle: DH-Massenstrom  5100960407865990868  5100960407865990868                           (-60.0, -160.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                        Wärmebilanz: 3 Kunden  5150752151066924202  5150752151066924202                           (219.0, -318.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1  eMail. info@3SConsult.de ; www.3SConsult.de  5370727463979416592  5370727463979416592                         (-230.0, -1204.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                Differenzdruck VL-/ RL-Knoten  5502619581048467908  5502619581048467908                           (1211.0, -49.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                                 Kundenanlage  5540395812045688781  5540395812045688781  (1131.9500000001863, 283.95000000018626)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                         Fernwärmeverbraucher  5550982489075668484  5550982489075668484                           (1050.0, 239.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                               Rücklaufstrang  5610916400841895317  5610916400841895317                             (570.0, -9.0)
Nahwärmenetz mit 1000 kW Anschlussleistu  1001  -1                             Knoten und Rohre  5646820849868629537  5646820849868629537  (358.20699999993667, 174.39499999955297)
                                    BHKW  1002  -1                          Fernwärmeeinspeiser  4654104397990769217  4654104397990769217                             (115.0, 80.0)
                                    BHKW  1002  -1                                        Pumpe  4768731522550494423  4768731522550494423                             (175.0, 25.0)
                                    BHKW  1002  -1                            Wärmebilanz Netz:  4770844990228490264  4770844990228490264                             (90.0, 160.0)
                                    BHKW  1002  -1                                  Speicherung  4782197969172967134  4782197969172967134                            (110.0, 140.0)
                                    BHKW  1002  -1                               Richtungspfeil  4855692488683645764  4855692488683645764                            (220.0, 105.0)
                                    BHKW  1002  -1                                     Verluste  4965628942555351751  4965628942555351751                            (110.0, 145.0)
                                    BHKW  1002  -1                          (Element verbinden)  5036153631350515544  5036153631350515544                             (150.0, 90.0)
                                    BHKW  1002  -1                    BHKW Modul 1000 kW therm.  5056836766824229789  5056836766824229789                              (35.0, 55.0)
                                    BHKW  1002  -1                                       Ventil  5108336975548011049  5108336975548011049                             (205.0, 25.0)
                                    BHKW  1002  -1                                    Verbrauch  5262441422409836340  5262441422409836340                            (110.0, 150.0)
                                    BHKW  1002  -1                                  Einspeisung  5297832234834839298  5297832234834839298                            (110.0, 155.0)
                                    BHKW  1002  -1                           Druckhaltung 2 bar  5329748935118523443  5329748935118523443                             (180.0, 65.0)
                                    BHKW  1002  -1                           Numerische Anzeige  5421223289472778073  5421223289472778073                            (190.0, 115.0)
                                    BHKW  1002  -1                             Verbindungslinie  5501963349880613918  5501963349880613918                             (150.0, 95.0)
                                    BHKW  1002  -1                                       (Text)  5696590398594231893  5696590398594231893                              (35.0, 50.0)
                                    BHKW  1002  -1                                       Klappe  5697088036451277538  5697088036451277538                             (145.0, 25.0)
>>> # ---
>>> # vNRCV
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vNRCV',end=14,dropColList=['DPGR','CONT_LFDNR','pk_ROWS'],sortList=['OBJTYPE','fkOBJTYPE','ATTRTYPE','cRefLfdNr']))
   cRefLfdNr                                      CONT CONT_ID OBJTYPE            fkOBJTYPE ATTRTYPE              tk_ROWS                   pk                   tk                                  pXYLB
0          1                                      BHKW    1002    FWES  5638756766880678918        W  5762106696740202356  4857294696992797631  4857294696992797631                           (90.0, 65.0)
1          1                                      BHKW    1002    KNOT  5049461676240771430        T  4723443975311885965  5097127385155151127  5097127385155151127                           (90.0, 95.0)
2          1                                      BHKW    1002    KNOT  5219230031772497417        T  5602301870151014230  5557806245003742769  5557806245003742769                           (90.0, 35.0)
3          1                                      BHKW    1002    KNOT  5356267303828212700       PH  5000989080893535213  4968703141722117357  4968703141722117357                          (220.0, 25.0)
4          1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001    KNOT  5397990465339071638       QM  5134531789044068877  5410059595276504750  5410059595276504750                          (91.0, -94.0)
5          2                                      BHKW    1002    KNOT  5397990465339071638       QM  5134531789044068877  5357021981944933535  5357021981944933535  (184.999999464624, 57.99999953107601)
6          1                                      BHKW    1002    KNOT  5736262931552588702       PH  4754881272083464445  4681213816714574464  4681213816714574464                          (220.0, 85.0)
7          1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001    KNOT  5741235692335544560       DP  4949183695502554728  4914949875368816179  4914949875368816179                         (1234.0, 83.0)
8          1                                      BHKW    1002    PUMP  5481331875203087055        N  5563842594211689762  5091374651838464239  5091374651838464239                          (170.0, 45.0)
9          1                                      BHKW    1002    VENT  4678923650983295610       QM  5126307362398248950  5410904806390050339  5410904806390050339                         (200.0, 110.0)
10         1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001    WBLZ  4694700216019268978      WVB  4778244458749966216  4991097791264453745  4991097791264453745                        (354.0, -225.0)
11         1                                      BHKW    1002    WBLZ  5262603207038486299      WES  5690691957596882133  5179988968597313889  5179988968597313889                          (90.0, 155.0)
12         1                                      BHKW    1002    WBLZ  5262603207038486299    WSPEI  5153847813311339683  4946584950744559030  4946584950744559030                          (90.0, 140.0)
13         1                                      BHKW    1002    WBLZ  5262603207038486299      WVB  5214984699859365639  5281885868749421521  5281885868749421521                          (90.0, 150.0)
>>> # ---
>>> # MxSync() - without Mx-Object
>>> # ---
>>> vROHR=xm.dataFrames['vROHR']
>>> vROHR.shape
(16, 74)
>>> 'vNRCV_Mx1' in xm.dataFrames
False
>>> xm.MxSync()
>>> 'vNRCV_Mx1' in xm.dataFrames
True
>>> vROHR.shape
(16, 76)
>>> print(xm._getvXXXXAsOneString(vXXXX='vROHR',dropColList=['NAME_i_2L','NAME_k_2L']))
   BESCHREIBUNG IDREFERENZ BAUJAHR HAL IPLANUNG KENNUNG       L LZU  RAU ZAUS ZEIN ZUML JLAMBS LAMBDA0 ASOLL INDSCHALL KVR  AUSFALLZEIT     DA     DI   DN     KT  PN  REHABILITATION  REPARATUR    S WSTEIG WTIEFE LTGR_NAME            LTGR_BESCHREIBUNG SICHTBARKEIT VERLEGEART DTRO_NAME                        DTRO_BESCHREIBUNG        E fkSTRASSE fkSRAT                   pk                   tk IRTRENN LECKSTART LECKEND LECKMENGE LECKORT LECKSTATUS QSVB ZVLIMPTNZ KANTENZV                                      CONT CONT_ID CONT_LFDNR  NAME_i KVR_i TM_i   XKOR_i   YKOR_i ZKOR_i  NAME_k KVR_k TM_k   XKOR_k   YKOR_k ZKOR_k  pXCor_i  pYCor_i  pXCor_k  pYCor_k            pXCors          pYCors                                pWAYPXCors                                pWAYPYCors                                                                                               WAYP  mx2NofPts  mx2Idx
0          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4613782368750024999  4613782368750024999       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K004     2   60  2541539  5706361     20  R-K005     2   60  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]    [807.8999999999069, 895.9500000001863]  [140.09999999962747, 142.04999999981374]                                                 [(2541547.9, 5706349.1), (2541635.95, 5706351.05)]          2       0
1          None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4614949065966596185  4614949065966596185       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K002     1   90  2541059  5706265     20  V-K003     1   90  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]                [319.0, 716.9500000001863]               [56.049999999813735, 136.0]                                                 [(2541059.0, 5706265.05), (2541456.95, 5706345.0)]          2       1
2          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4637102239750163477  4637102239750163477       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K003     2   60  2541457  5706345     20  R-K004     2   60  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]    [725.8500000000931, 807.8999999999069]  [124.04999999981374, 140.09999999962747]                                                 [(2541465.85, 5706333.05), (2541547.9, 5706349.1)]          2       2
3          None         -1    None   0        1       0   88.02   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4713733238627697042  4713733238627697042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K004     1   90  2541539  5706361     20  V-K005     1   90  2541627  5706363     20    799.0    152.0    887.0    154.0    [799.0, 887.0]  [152.0, 154.0]                [799.0, 887.0499999998137]                            [152.0, 154.0]                                                  [(2541539.0, 5706361.0), (2541627.05, 5706363.0)]          2       3
4          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4789218195240364437  4789218195240364437       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K001     1   90  2540867  5706228     20  V-K002     1   90  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]                            [127.0, 319.0]                [19.0, 56.049999999813735]                                                  [(2540867.0, 5706228.0), (2541059.0, 5706265.05)]          2       5
5          None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4945727430885351042  4945727430885351042       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K006     2   60  2541790  5706338     20  R-K007     2   60  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]  [1058.8500000000931, 1167.8999999999069]               [117.0, 104.09999999962747]                                                  [(2541798.85, 5706326.0), (2541907.9, 5706313.1)]          2       7
6          None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4984202422877610920  4984202422877610920       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K000     1   90  2540793  5706209     20  V-K001     1   90  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]               [53.049999999813735, 127.0]             [-0.049999999813735485, 19.0]                                                 [(2540793.05, 5706208.95), (2540867.0, 5706228.0)]          2       8
7          None         -1    None   0        1       0   83.55   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5037777106796980248  5037777106796980248       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K003     1   90  2541457  5706345     20  V-K004     1   90  2541539  5706361     20    717.0    136.0    799.0    152.0    [717.0, 799.0]  [136.0, 152.0]                [716.9500000001863, 799.0]                            [136.0, 152.0]                                                  [(2541456.95, 5706345.0), (2541539.0, 5706361.0)]          2       9
8          None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5123819811204259837  5123819811204259837       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K005     1   90  2541627  5706363     20  V-K006     1   90  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]   [887.0499999998137, 1049.9500000001863]               [154.0, 128.95000000018626]                                                [(2541627.05, 5706363.0), (2541789.95, 5706337.95)]          2      10
9          None         -1    None   0        1       0  195.53   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5266224553324203132  5266224553324203132       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K001     2   60  2540867  5706228     20  R-K002     2   60  2541059  5706265     20    127.0     19.0    319.0     56.0    [127.0, 319.0]    [19.0, 56.0]  [135.89999999990687, 327.89999999990687]   [7.0499999998137355, 44.09999999962747]                                                  [(2540875.9, 5706216.05), (2541067.9, 5706253.1)]          2      11
10         None         -1    None   0        1       0  405.96   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5379365049009065623  5379365049009065623       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K002     2   60  2541059  5706265     20  R-K003     2   60  2541457  5706345     20    319.0     56.0    717.0    136.0    [319.0, 717.0]   [56.0, 136.0]   [327.89999999990687, 725.8500000000931]   [44.09999999962747, 124.04999999981374]                                                 [(2541067.9, 5706253.1), (2541465.85, 5706333.05)]          2      12
11         None         -1    None   0        1       0  164.91   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5611703699850694889  5611703699850694889       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K005     2   60  2541627  5706363     20  R-K006     2   60  2541790  5706338     20    887.0    154.0   1050.0    129.0   [887.0, 1050.0]  [154.0, 129.0]   [895.9500000001863, 1058.8500000000931]               [142.04999999981374, 117.0]                                                [(2541635.95, 5706351.05), (2541798.85, 5706326.0)]          2      13
12         None         -1    None   0        1       0  109.77   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5620197984230756681  5620197984230756681       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  V-K006     1   90  2541790  5706338     20  V-K007     1   90  2541899  5706325     20   1050.0    129.0   1159.0    116.0  [1050.0, 1159.0]  [129.0, 116.0]              [1049.9500000001863, 1159.0]  [128.95000000018626, 116.04999999981374]                                                [(2541789.95, 5706337.95), (2541899.0, 5706325.05)]          2      14
13         None         -1    None   0        1       0    76.4   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  114.3  107.1  100  0.325 NaN             NaN        NaN  3.6    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  5647213228462830353  5647213228462830353       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1  R-K000     2   60  2540793  5706209     20  R-K001     2   60  2540867  5706228     20     53.0      0.0    127.0     19.0     [53.0, 127.0]     [0.0, 19.0]  [61.950000000186265, 135.89999999990687]               [-12.0, 7.0499999998137355]                                                 [(2540801.95, 5706197.0), (2540875.9, 5706216.05)]          2      15
14         None         -1    None   0        1       0   73.42   0  0.1    0    0    0      1   0.025  1000         0   2          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4769996343148550485  4769996343148550485       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     R-L     2   60  2540740  5706225     20  R-K000     2   60  2540793  5706209     20      0.0     16.0     53.0      0.0       [0.0, 53.0]     [16.0, 0.0]     [0.0, 24.0, 45.0, 61.950000000186265]                [16.0, 16.0, -12.0, -12.0]  [(2540740.0, 5706225.0), (2540764.0, 5706225.0), (2540785.0, 5706197.0), (2540801.95, 5706197.0)]          2       4
15         None         -1    None   0        1       0    68.6   0  0.1    0    0    0      1   0.025  1000         0   1          NaN  168.3  160.3  150   0.45 NaN             NaN        NaN    4    NaN    NaN   KUMANRO  Beschreibung Leitungsgruppe            1     999999   KUMANRO  Kunststoffmantelrohr DN20-800 PANISOVIT  2.1E+11        -1     -1  4939422678063487923  4939422678063487923       0         0       0         0       0          0    0       NaN      NaN  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1     V-L     1   90  2540740  5706240     20  V-K000     1   90  2540793  5706209     20      0.0     31.0     53.0      0.0       [0.0, 53.0]     [31.0, 0.0]           [0.0, 30.0, 53.049999999813735]       [31.0, 31.0, -0.049999999813735485]                         [(2540740.0, 5706240.0), (2540770.0, 5706240.0), (2540793.05, 5706208.95)]          2       6
>>> # ---------
>>> # MxSync() 
>>> # ---------
>>> xm=Xm(xmlFile=xmlFile)
>>> vROHR=xm.dataFrames['vROHR']
>>> vROHR.shape
(16, 74)
>>> 'vNRCV_Mx1' in xm.dataFrames
False
>>> (wDir,modelDir,modelName,mx1File)=xm.getWDirModelDirModelName()    
>>> mx=Mx.Mx(mx1File=mx1File)
>>> xm.MxSync(mx=mx)
>>> vROHR.shape
(16, 76)
>>> 'vNRCV_Mx1' in xm.dataFrames
True
>>> # ---
>>> # vNRCV_Mx1
>>> # ---
>>> import re
>>> f=lambda s: re.match('(\S+)~(\S*)~(\S*)~(\d+)~(\S+)',s).group(1)+'~~~'+re.match('(\S+)~(\S*)~(\S*)~(\d+)~(\S+)',s).group(4)+'~'+re.match('(\S+)~(\S*)~(\S*)~(\d+)~(\S+)',s).group(5)
>>> print(xm._getvXXXXAsOneString(vXXXX='vNRCV_Mx1',end=14,dropColList=['DPGR','CONT_LFDNR','pk_ROWS'],mapFunc={'Sir3sID':f},sortList=['Sir3sID'],fmtFunc={'Sir3sID':f},index=False,header=False))
FWES~~~5638756766880678918~W  1                                      BHKW  1002  FWES  5638756766880678918      W  5762106696740202356  4857294696992797631  4857294696992797631     (90.0, 65.0)
    KNOT~~~5049461676240771430~T  1                                      BHKW  1002  KNOT  5049461676240771430      T  4723443975311885965  5097127385155151127  5097127385155151127     (90.0, 95.0)
    KNOT~~~5219230031772497417~T  1                                      BHKW  1002  KNOT  5219230031772497417      T  5602301870151014230  5557806245003742769  5557806245003742769     (90.0, 35.0)
   KNOT~~~5356267303828212700~PH  1                                      BHKW  1002  KNOT  5356267303828212700     PH  5000989080893535213  4968703141722117357  4968703141722117357    (220.0, 25.0)
   KNOT~~~5397990465339071638~QM  1  Nahwärmenetz mit 1000 kW Anschlussleistu  1001  KNOT  5397990465339071638     QM  5134531789044068877  5410059595276504750  5410059595276504750    (91.0, -94.0)
   KNOT~~~5736262931552588702~PH  1                                      BHKW  1002  KNOT  5736262931552588702     PH  4754881272083464445  4681213816714574464  4681213816714574464    (220.0, 85.0)
   KNOT~~~5741235692335544560~DP  1  Nahwärmenetz mit 1000 kW Anschlussleistu  1001  KNOT  5741235692335544560     DP  4949183695502554728  4914949875368816179  4914949875368816179   (1234.0, 83.0)
    PUMP~~~5481331875203087055~N  1                                      BHKW  1002  PUMP  5481331875203087055      N  5563842594211689762  5091374651838464239  5091374651838464239    (170.0, 45.0)
   VENT~~~4678923650983295610~QM  1                                      BHKW  1002  VENT  4678923650983295610     QM  5126307362398248950  5410904806390050339  5410904806390050339   (200.0, 110.0)
  WBLZ~~~4694700216019268978~WVB  1  Nahwärmenetz mit 1000 kW Anschlussleistu  1001  WBLZ  4694700216019268978    WVB  4778244458749966216  4991097791264453745  4991097791264453745  (354.0, -225.0)
  WBLZ~~~5262603207038486299~WES  1                                      BHKW  1002  WBLZ  5262603207038486299    WES  5690691957596882133  5179988968597313889  5179988968597313889    (90.0, 155.0)
WBLZ~~~5262603207038486299~WSPEI  1                                      BHKW  1002  WBLZ  5262603207038486299  WSPEI  5153847813311339683  4946584950744559030  4946584950744559030    (90.0, 140.0)
  WBLZ~~~5262603207038486299~WVB  1                                      BHKW  1002  WBLZ  5262603207038486299    WVB  5214984699859365639  5281885868749421521  5281885868749421521    (90.0, 150.0)
WBLZ~~~5262603207038486299~WVERL  1                                      BHKW  1002  WBLZ  5262603207038486299  WVERL  4722863010266870887  5476262878682325254  5476262878682325254    (90.0, 145.0)
>>> # ---
>>> # vKNOT
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vKNOT',end=1,dropColList=['LFKT_NAME','LF','LF_min','LF_max','PVAR_NAME','PH','PH_min','PH_max','PZON_NAME','FSTF_NAME','STOF_NAME','GMIX_NAME','UTMP_NAME','2L_NAME','2L_KVR','fkHYDR','fkFQPS']))
     NAME BESCHREIBUNG IDREFERENZ                                      CONT CONT_ID CONT_LFDNR CONT_VKNO  KTYP LFAKT QM_EIN QVAR_NAME  QM  QM_min  QM_max KVR  TE  TM     XKOR     YKOR ZKOR                   pk                   tk  pXCor  pYCor  mx2Idx
0  R-K004         None         -1  Nahwärmenetz mit 1000 kW Anschlussleistu    1001         -1       NaN  QKON     1      0       NaN NaN     NaN     NaN   2  10  60  2541539  5706361   20  4638663808856251977  4638663808856251977  799.0  152.0       0
>>> print(xm._getvXXXXAsOneString(vXXXX='vFWVB',dropColList=['BESCHREIBUNG','IDREFERENZ','W0','W','IRFV','LFK','TVL0','TRS0','LFKT','W_min','W_max','INDTR','TRSK','VTYP','DPHAUS','IMBG', 'pk','tk','KVR_i','TM_i', 'XKOR_i','YKOR_i','ZKOR_i','pXCor_i','pYCor_i','KVR_k','TM_k', 'XKOR_k','YKOR_k','ZKOR_k','pXCor_k', 'pYCor_k','CONT','CONT_ID', 'CONT_LFDNR']))
   W0LFK  NAME_i  NAME_k                         WBLZ  mx2Idx
0  160.0  V-K002  R-K002  [BLNZ1, BLNZ1u5, BLNZ1u5u7]       0
1  200.0  V-K004  R-K004                           []       1
2  160.0  V-K005  R-K005  [BLNZ1u5, BLNZ1u5u7, BLNZ5]       2
3  160.0  V-K007  R-K007                  [BLNZ1u5u7]       3
4  120.0  V-K003  R-K003                           []       4
>>> # ---
>>> # vXXXX
>>> # ---
>>> xm.dataFrames['vVBEL_forTestOnly']=xm.dataFrames['vVBEL'].reset_index(inplace=False) # Multiindex to Cols
>>> print(xm._getvXXXXAsOneString(vXXXX='vVBEL_forTestOnly',index=True,dropColList=['Z_i','pk_i','CONT_i','CONT_VKNO_i','Z_k','pk_k','CONT_k','CONT_VKNO_k','IDREFERENZ','tk']))
   OBJTYPE                OBJID                   BESCHREIBUNG       NAME_i  NAME_k             LAYR       L      D  mx2Idx
0     FWES  5638756766880678918  BHKW - Modul - 1000 kW therm.           R3     V-1        [Vorlauf]       0     80       0
1     FWVB  4643800032883366034                              1       V-K002  R-K002  [Kundenanlagen]       0    NaN       0
2     FWVB  4704603947372595298                              3       V-K004  R-K004  [Kundenanlagen]       0    NaN       1
3     FWVB  5121101823283893406                              4       V-K005  R-K005  [Kundenanlagen]       0    NaN       2
4     FWVB  5400405917816384862                              5       V-K007  R-K007  [Kundenanlagen]       0    NaN       3
5     FWVB  5695730293103267172                              2       V-K003  R-K003  [Kundenanlagen]       0    NaN       4
6     KLAP  4801110583764519435                           None           R2      R3       [Rücklauf]       0     80       0
7     PGRP  4986517622672493603                   Pumpengruppe          R-1      R3               []       0    NaN       0
8     PUMP  5481331875203087055                    Umwälzpumpe          R-1      R2       [Rücklauf]       0    NaN       0
9     ROHR  4613782368750024999                           None       R-K004  R-K005       [Rücklauf]   88.02  107.1       0
10    ROHR  4614949065966596185                           None       V-K002  V-K003        [Vorlauf]  405.96  107.1       1
11    ROHR  4637102239750163477                           None       R-K003  R-K004       [Rücklauf]   83.55  107.1       2
12    ROHR  4713733238627697042                           None       V-K004  V-K005        [Vorlauf]   88.02  107.1       3
13    ROHR  4769996343148550485                           None          R-L  R-K000       [Rücklauf]   73.42  160.3       4
14    ROHR  4789218195240364437                           None       V-K001  V-K002        [Vorlauf]  195.53  107.1       5
15    ROHR  4939422678063487923                           None          V-L  V-K000        [Vorlauf]    68.6  160.3       6
16    ROHR  4945727430885351042                           None       R-K006  R-K007       [Rücklauf]  109.77  107.1       7
17    ROHR  4984202422877610920                           None       V-K000  V-K001        [Vorlauf]    76.4  107.1       8
18    ROHR  5037777106796980248                           None       V-K003  V-K004        [Vorlauf]   83.55  107.1       9
19    ROHR  5123819811204259837                           None       V-K005  V-K006        [Vorlauf]  164.91  107.1      10
20    ROHR  5266224553324203132                           None       R-K001  R-K002       [Rücklauf]  195.53  107.1      11
21    ROHR  5379365049009065623                           None       R-K002  R-K003       [Rücklauf]  405.96  107.1      12
22    ROHR  5611703699850694889                           None       R-K005  R-K006       [Rücklauf]  164.91  107.1      13
23    ROHR  5620197984230756681                           None       V-K006  V-K007        [Vorlauf]  109.77  107.1      14
24    ROHR  5647213228462830353                           None       R-K000  R-K001       [Rücklauf]    76.4  107.1      15
25    VENT  4678923650983295610                           None          V-1     V-L        [Vorlauf]       0    150       0
26    VENT  4897018421024717974                           None          R-L     R-1       [Rücklauf]       0    150       1
27    VENT  5525310316015533093                           None  PKON-Knoten     R-1       [Rücklauf]       0     50       2
>>> # ---
>>> # vRART
>>> # ---
>>> print(xm._getvXXXXAsOneString(vXXXX='vRART',index=True,sortList=['INDSTD','NAME']))
  NAME              BESCHREIBUNG                                   INDSTD_TXT  INDSTD   DWDT WSOSTD                   pk NAME_KREF1 NAME_KREF2 NAME_SWVT
0   dp  Bezeichnung Regelungsart  Differenzdruck Druckseite, Sollwert Tabelle      55  1E+20      0  5552938346422332788     V-K007     R-K007      SWVT
>>> # ------
>>> # MxAdd
>>> # ------
>>> if 'vNRCV_Mx1' in xm.dataFrames:
...    del xm.dataFrames['vNRCV_Mx1'] # delete MxSync-Result to force MxSync-Call in MxAdd
>>> oldShape=xm.dataFrames['vKNOT'].shape
>>> xm.MxAdd()
>>> firstShape=xm.dataFrames['vKNOT'].shape
>>> oldShape[1]<firstShape[1]
True
>>> xm.MxAdd(mx=mx)
>>> secondShape=xm.dataFrames['vKNOT'].shape
>>> secondShape==firstShape
True
>>> xm.MxAdd(mx=mx)
>>> thirdShape=xm.dataFrames['vKNOT'].shape
>>> thirdShape==firstShape
True
>>> xm.dataFrames['vKNOT_forTestOnly']=xm.dataFrames['vKNOT'].rename(columns={'KNOT~*~*~*~PH':'Druck'})
>>> if 'Druck' not in xm.dataFrames['vKNOT_forTestOnly']:
...     xm.dataFrames['vKNOT_forTestOnly'].rename(columns={'KNOT~*~*~*~H':'Druck'},inplace=True)
>>> if 'Druck' not in xm.dataFrames['vKNOT_forTestOnly']:
...     xm.dataFrames['vKNOT_forTestOnly'].rename(columns={'KNOT~*~~*~PH':'Druck'},inplace=True) #09 
>>> f = lambda x: round(x,1) if x != None else None  
>>> print(xm._getvXXXXAsOneString(vXXXX='vKNOT_forTestOnly',filterColList=['mx2Idx','KVR','NAME','Druck'],mapFunc={'Druck':f},index=True))
    mx2Idx KVR         NAME  Druck
0        0   2       R-K004    2.3
1        1   1       V-K002    4.0
2        2   1       V-K001    4.1
3        3   1       V-K000    4.1
4        4   2       R-K001    2.0
5        5   2       R-K003    2.3
6        6   2       R-K000    2.0
7        9   2       R-K005    2.3
8       11   2          R-L    2.0
9       12   2       R-K002    2.1
10      13   1       V-K004    3.8
11      15   1       V-K005    3.8
12      16   2       R-K007    2.3
13      17   1       V-K006    3.8
14      18   2       R-K006    2.3
15      20   1       V-K003    3.8
16      21   1          V-L    4.1
17      22   1       V-K007    3.8
18       7   2           R2    4.3
19       8   1          V-1    4.1
20      10   2           R3    4.3
21      14   2  PKON-Knoten    2.0
22      19   2          R-1    2.0
>>> print(xm._getvXXXXAsOneString(vXXXX='vROHR',filterColList=['mx2Idx','L','KVR','NAME_i','NAME_k','ROHR~*~*~*~QMAV'],mapFunc={'ROHR~*~*~*~QMAV':f},sortList=['ROHR~*~*~*~QMAV','NAME_i'],index=True))
    mx2Idx       L KVR  NAME_i  NAME_k  ROHR~*~*~*~QMAV
13      15    76.4   2  R-K000  R-K001            -23.0
9       11  195.53   2  R-K001  R-K002            -23.0
14       4   73.42   2     R-L  R-K000            -23.0
10      12  405.96   2  R-K002  R-K003            -19.1
2        2   83.55   2  R-K003  R-K004            -15.4
0        0   88.02   2  R-K004  R-K005             -8.5
11      13  164.91   2  R-K005  R-K006             -3.9
5        7  109.77   2  R-K006  R-K007             -3.9
8       10  164.91   1  V-K005  V-K006              3.9
12      14  109.77   1  V-K006  V-K007              3.9
3        3   88.02   1  V-K004  V-K005              8.5
7        9   83.55   1  V-K003  V-K004             15.4
1        1  405.96   1  V-K002  V-K003             19.1
6        8    76.4   1  V-K000  V-K001             23.0
4        5  195.53   1  V-K001  V-K002             23.0
15       6    68.6   1     V-L  V-K000             23.0
>>> print(xm._getvXXXXAsOneString(vXXXX='vFWVB',filterColList=['mx2Idx','NAME_i','NAME_k','FWVB~*~*~*~W'],mapFunc={'FWVB~*~*~*~W':f},sortList=['FWVB~*~*~*~W','NAME_i'],index=True))
   mx2Idx  NAME_i  NAME_k  FWVB~*~*~*~W
4       4  V-K003  R-K003         120.0
0       0  V-K002  R-K002         160.0
2       2  V-K005  R-K005         160.0
3       3  V-K007  R-K007         160.0
1       1  V-K004  R-K004         200.0
>>> xm.dataFrames['vVBEL_forTestOnly2']=xm.dataFrames['vVBEL'].loc[['ROHR','FWVB'],:].reset_index(inplace=False) # Multiindex to Cols
>>> xm.dataFrames['vVBEL_forTestOnly2'].rename(columns={'KNOT~*~*~*~PH_i':'Druck_i'},inplace=True)
>>> if 'Druck_i' not in xm.dataFrames['vVBEL_forTestOnly2']:
...     xm.dataFrames['vVBEL_forTestOnly2'].rename(columns={'KNOT~*~*~*~H_i':'Druck_i'},inplace=True)
>>> if 'Druck_i' not in xm.dataFrames['vVBEL_forTestOnly2']:
...     xm.dataFrames['vVBEL_forTestOnly2'].rename(columns={'KNOT~*~~*~PH_i':'Druck_i'},inplace=True) #09 
>>> f = lambda x: round(x,1) if x != None else None  
>>> print(xm._getvXXXXAsOneString(vXXXX='vVBEL_forTestOnly2',filterColList=['OBJTYPE','mx2Idx','L','D','NAME_i','NAME_k','Druck_i','Q'],mapFunc={'Druck_i':f,'Q':f},sortList=['OBJTYPE','NAME_i','Q'],index=True))
   OBJTYPE  mx2Idx       L      D  NAME_i  NAME_k  Druck_i     Q
0     FWVB       0       0    NaN  V-K002  R-K002      4.0   3.9
4     FWVB       4       0    NaN  V-K003  R-K003      3.8   3.7
1     FWVB       1       0    NaN  V-K004  R-K004      3.8   6.9
2     FWVB       2       0    NaN  V-K005  R-K005      3.8   4.6
3     FWVB       3       0    NaN  V-K007  R-K007      3.8   3.9
20    ROHR      15    76.4  107.1  R-K000  R-K001      2.0 -23.0
16    ROHR      11  195.53  107.1  R-K001  R-K002      2.0 -23.0
17    ROHR      12  405.96  107.1  R-K002  R-K003      2.1 -19.1
7     ROHR       2   83.55  107.1  R-K003  R-K004      2.3 -15.4
5     ROHR       0   88.02  107.1  R-K004  R-K005      2.3  -8.5
18    ROHR      13  164.91  107.1  R-K005  R-K006      2.3  -3.9
12    ROHR       7  109.77  107.1  R-K006  R-K007      2.3  -3.9
9     ROHR       4   73.42  160.3     R-L  R-K000      2.0 -23.0
13    ROHR       8    76.4  107.1  V-K000  V-K001      4.1  23.0
10    ROHR       5  195.53  107.1  V-K001  V-K002      4.1  23.0
6     ROHR       1  405.96  107.1  V-K002  V-K003      4.0  19.1
14    ROHR       9   83.55  107.1  V-K003  V-K004      3.8  15.4
8     ROHR       3   88.02  107.1  V-K004  V-K005      3.8   8.5
15    ROHR      10  164.91  107.1  V-K005  V-K006      3.8   3.9
19    ROHR      14  109.77  107.1  V-K006  V-K007      3.8   3.9
11    ROHR       6    68.6  160.3     V-L  V-K000      4.1  23.0
>>> # ---
>>> # Clean Up LocalHeatingNetwork Xm and Mx
>>> # ---
>>> if os.path.exists(xm.h5File):                        
...    os.remove(xm.h5File)
>>> if os.path.exists(mx.h5FileVecs):                        
...    os.remove(mx.h5FileVecs)
>>> if os.path.exists(mx.h5File):                        
...    os.remove(mx.h5File)
>>> # ---
>>> # TinyWDN
>>> # ---
>>> xmlFile=os.path.join(os.path.join(path,testDir),'TinyWDN.XML')
>>> xm=Xm(xmlFile=xmlFile)
>>> # ---
>>> # GPipe
>>> # ---
>>> xmlFile=os.path.join(os.path.join(path,testDir),'GPipe.XML')
>>> xm=Xm(xmlFile=xmlFile)
"""

import warnings # 3.6
#...\Anaconda3\lib\site-packages\h5py\__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
#  from ._conv import register_converters as _register_converters
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import sys

import xml.etree.ElementTree as ET
import re
import pandas as pd
import numpy as np
import warnings
import tables

import h5py
import time

import base64
import struct

import logging

import glob

import networkx as nx

# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S.Xm')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context: ',' .')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

try:
    from PT3S import Mx
except ImportError:
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: ImportError: ','from PT3S import Mx - trying import Mx instead ... maybe pip install -e . is active ...')) 
    import Mx

# ---
# --- main Imports
# ---
import argparse
import unittest
import doctest

vVBEL_edges =['ROHR','VENT','FWVB','FWES','PUMP','KLAP','REGV','PREG','MREG','DPRG','PGRP']
vVBEL_edgesD=[''    ,'DN'  ,''    ,'DN'  ,''    ,'DN'  ,'DN'  ,'DN'  ,'DN'  ,'DN'  ,'']
vVBEL_edgesQ=['QMAV','QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'QM'  ,'']
   
class XmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Xm():
    """SIR 3S modelFile to pandas DataFrames.

    Args:
        * xmlFile (str): SIR 3S modelFile
        * NoH5Read (bool): 
                False (default): 
                    * An existing and newer h5File will be read _instead of xmlFile.
                    * xmlFile will _not be read (it does even not have to exist)
                True:
                    * An existing h5File will be deleted.
                    * xmlFile will be read.
    
    Attributes:
        * states
            * h5Read: True, if read from H5

        * xmlFile
        * h5File: corresponding h5File(name) derived from xmlFile(name)
        * dataFrames
            * dict with pandas DataFrames
            * one pandas DataFrame per SIR 3S Objecttype (i.e. KNOT, ROHR, ...)
            * keys: KNOT, ROHR, ... and vKNOT, vROHR, ...
            * some Views as pandas DataFrames 
                * i.e. vKNOT, vROHR, ...
                * The Views are designed to deal with tedious groundwork.
                * The Views are aggregated somewhat arbitrary.
                * However: Usage of SIR 3S Modeldata is more convenient and efficient with appropriate Views.      
        * pXCorZero, pYCorZero
   
    Raises:
        XmError
    """
    def __init__(self,xmlFile,NoH5Read=False):

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
                    if os.access(self.h5File,os.W_OK):
                        pass
                    else:
                        logger.debug("{0:s}{1:s}: not os.W_OK ... sleep(1) ...".format(logStr,self.h5File))     
                        time.sleep(1)
                    logger.debug("{0:s}{1:s}: Delete ...".format(logStr,self.h5File))     
                    try:
                        os.remove(self.h5File)
                    except PermissionError:
                        logger.debug("{0:s}{1:s}: PermissionError ... sleep(1) ...".format(logStr,self.h5File))     
                        time.sleep(1)
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
                    self.h5Read=True  
                else:
                    logger.debug("{0:s}h5File {1:s} exists parallel but is NOT newer than xmlFile {2:s}.".format(logStr,self.h5File,self.xmlFile))     
                    self.h5Read=False
            else:
                self.h5Read=False               
            
            if not self.h5Read:                
                self._xmlRead()
            else:
                self.FromH5(h5File=self.h5File)
                          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _xmlRead(self):
        """Reads the SIR 3S modelFile.
           
        * Performs fixes and basic conversions inplace the dataFrames read from modelFile: _convertAndFix()
        * Creates some Views: _vXXXX()

        Raises:
            XmError
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
            self._convertAndFix()

            #Views
            self._vXXXX()
                                            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)                
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def FromH5(self,h5File=None):
        """Reads all dataFrames stored in h5File into self.DataFrames.
        
        Args:
            h5File: 
                * (str): the h5File(name) to be read
                * (None): self.h5File will be read
            
          
        * Reads all keys.
        * Existing keys in self.dataFrames are overwritten.

        Note that after .FromH5() the content of self.dataFrames may differ from the content given by an existing self.xmlFile.

        Raises:
            XmError
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
        """Stores self.dataFrames to h5File.

        Args:
            h5File: 
                * (str): the h5File(name) to be used
                * (None): self.h5File will be used

        * Stores all keys.
        * Existing keys in h5File are overwritten.       
        
        Raises:
            XmError         
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

            relPath2XmlromCurDir=os.path.normpath(os.path.relpath(os.path.normpath(self.xmlFile),start=os.path.normpath(os.path.curdir))) # ..\..\..\..\..\3S\Modelle\....XML
            #print(repr(relPath2XmlromCurDir)) # '..\\..\\..\\..\\..\\3S\\Modelle\\....XML'
            h5KeySep='/'
            h5KeyCharForDot='_'
            h5KeyCharForMinus='_'
            relPath2XmlromCurDirH5BaseKey=re.sub('\.',h5KeyCharForDot,re.sub(r'\\',h5KeySep,re.sub('-',h5KeyCharForMinus,re.sub('.xml','',relPath2XmlromCurDir,flags=re.IGNORECASE))))
            #__/__/__/__/__/3S/Modelle/...

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

    def _convertAndFix(self):
        """Performs fixes and basic conversions inplace the dataFrames read from self.xmlFile.

        * Fixes and conversions here are integrity-oriented.
        * Usage-oriented conversions (i.e. pd.to_numeric and base64.b64decode) are done in the ._vXXXX-methods.

        Conversions: 
            * , > . (converted in: SWVT_ROWT, LFKT_ROWT, QVAR_ROWT, PVAR_ROWT)

        Fixes:
            * No SWVT_ROWT, LFKT_ROWT, QVAR_ROWT, PVAR_ROWT?!
                *  * SWVT, LFKT, QVAR, PVAR are constructed to
            * 1st Time without Value?! (fixed in: SWVT_ROWT, LFKT_ROWT, QVAR_ROWT, PVAR_ROWT)       
            * Template Node(s)?!
            * in new Models constructed from SIR 3S 
               * not all Objectattributes are written?!   
                    * KMOT/TE
                    * FWVB/LFK
                    * LTGR/BESCHREIBUNG
                    * DTRO_ROWD
                        * AUSFALLZEIT
                        * PN
                        * REHABILITATION
                        * REPARATUR
                        * WSTEIG, WTIEFE

                * not all Objecttypes are written?!
                    * CONT    
            * Models with no PZONs ...
            * Models with no GMIXs ...
            * Models with no STOFs ...
            * empty WBLZ OBJS-BLOBs
            * empty LAYR OBJS-BLOBs
        Raises:
            XmError                                       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            if 'SWVT_ROWT' not in self.dataFrames:
                self.dataFrames['SWVT_ROWT']=self._constructEmptyDf(['pk','fk','ZEIT','W'])
                self.dataFrames['SWVT']=self._constructEmptyDf(['pk','NAME','BESCHREIBUNG','INTPOL','ZEITOPTION'])

            if not self.dataFrames['SWVT_ROWT'].empty:
                self.dataFrames['SWVT_ROWT'].ZEIT=self.dataFrames['SWVT_ROWT'].ZEIT.str.replace(',', '.')
                self.dataFrames['SWVT_ROWT'].W=self.dataFrames['SWVT_ROWT'].W.str.replace(',', '.')

            if 'LFKT_ROWT' not in self.dataFrames:
                self.dataFrames['LFKT_ROWT']=self._constructEmptyDf(['pk','fk','ZEIT','LF'])     
                self.dataFrames['LFKT']=self._constructEmptyDf(['pk','NAME','BESCHREIBUNG','INTPOL','ZEITOPTION'])

            if not self.dataFrames['LFKT_ROWT'].empty:
                self.dataFrames['LFKT_ROWT'].ZEIT=self.dataFrames['LFKT_ROWT'].ZEIT.str.replace(',', '.')
                self.dataFrames['LFKT_ROWT'].LF=self.dataFrames['LFKT_ROWT'].LF.str.replace(',', '.')

            if 'QVAR_ROWT' not in self.dataFrames:
                self.dataFrames['QVAR_ROWT']=self._constructEmptyDf(['pk','fk','ZEIT','QM'])    
                self.dataFrames['QVAR']=self._constructEmptyDf(['pk','NAME','BESCHREIBUNG','INTPOL','ZEITOPTION'])

            if not self.dataFrames['QVAR_ROWT'].empty:
                self.dataFrames['QVAR_ROWT'].ZEIT=self.dataFrames['QVAR_ROWT'].ZEIT.str.replace(',', '.')
                self.dataFrames['QVAR_ROWT'].QM=self.dataFrames['QVAR_ROWT'].QM.str.replace(',', '.')

            if 'PVAR_ROWT' not in self.dataFrames:
                self.dataFrames['PVAR_ROWT']=self._constructEmptyDf(['pk','fk','ZEIT','PH'])     
                self.dataFrames['PVAR']=self._constructEmptyDf(['pk','NAME','BESCHREIBUNG','INTPOL','ZEITOPTION'])

            if not self.dataFrames['PVAR_ROWT'].empty:
                self.dataFrames['PVAR_ROWT'].ZEIT=self.dataFrames['PVAR_ROWT'].ZEIT.str.replace(',', '.')
                self.dataFrames['PVAR_ROWT'].PH=self.dataFrames['PVAR_ROWT'].PH.str.replace(',', '.')

            # 1st Time without Value?!
            self.dataFrames['SWVT_ROWT']=self.dataFrames['SWVT_ROWT'].fillna(0) 
            self.dataFrames['LFKT_ROWT']=self.dataFrames['LFKT_ROWT'].fillna(0) 
            self.dataFrames['QVAR_ROWT']=self.dataFrames['QVAR_ROWT'].fillna(0) 
            self.dataFrames['PVAR_ROWT']=self.dataFrames['PVAR_ROWT'].fillna(0) 
                        
            # Template Node
            self.dataFrames['KNOT']=self.dataFrames['KNOT'][self.dataFrames['KNOT'].NAME.fillna('').astype(str).isin(['TemplateNode','TemplNode-VL','TemplNode-RL'])==False]            
            
            # TE only in Heatingmodels ? ...
            try:
                isinstance(self.dataFrames['KNOT_BZ']['TE'],pd.core.series.Series)
            except:
                logger.debug("{:s}Error: {:s}: {:s}.".format(logStr,"self.dataFrames['KNOT_BZ']['TE']",'TE only in Heatingmodels?!')) 
                self.dataFrames['KNOT_BZ']['TE']=pd.Series()     

            # FWVB LFK
            if 'FWVB' in self.dataFrames:
                try:
                    isinstance(self.dataFrames['FWVB']['LFK'],pd.core.series.Series)
                except:
                    logger.debug("{:s}Error: {:s}: {:s}.".format(logStr,"self.dataFrames['FWVB']['LFK']",'LFK not set?!')) 
                    self.dataFrames['FWVB']['LFK']=pd.Series()
                self.dataFrames['FWVB']['LFK'].fillna(value=1,inplace=True)

            # Models with only one Standard LTGR ...
            try:
                isinstance(self.dataFrames['LTGR']['BESCHREIBUNG'],pd.core.series.Series)
            except:
                self.dataFrames['LTGR']['BESCHREIBUNG']=pd.Series()    

            # Models with old DTRO_ROWD                 
            for attrib in ['AUSFALLZEIT','PN','REHABILITATION','REPARATUR','WSTEIG','WTIEFE']:
                 try:
                    isinstance(self.dataFrames['DTRO_ROWD'][attrib],pd.core.series.Series)
                 except:
                    self.dataFrames['DTRO_ROWD'][attrib]=pd.Series()   

            # Models with no CONTs ...
            try:
                isinstance(self.dataFrames['CONT']['LFDNR'],pd.core.series.Series)
            except:
                self.dataFrames['CONT']['LFDNR']=pd.Series()    
            try:
                isinstance(self.dataFrames['CONT']['GRAF'],pd.core.series.Series)
            except:
                self.dataFrames['CONT']['GRAF']=pd.Series()       

            # Models with no PZONs ...
            if not 'PZON' in self.dataFrames: 
                self.dataFrames['PZON']=pd.DataFrame()       
                self.dataFrames['PZON']['NAME']=pd.Series()  
                self.dataFrames['PZON']['pk']=pd.Series()  

            # Models with no STOFs ...
            if not 'STOF' in self.dataFrames: 
                #                                                            BESCHREIBUNG
                self.dataFrames['STOF']=self._constructEmptyDf(['pk','NAME','BESCHREIBUNG']) 

            # Models with no GMIXs ...
            if not 'GMIX' in self.dataFrames: 
                self.dataFrames['GMIX']=self._constructEmptyDf(['pk','NAME']) 
                   
            # empty WBLZ OBJS-BLOBs
            if 'WBLZ' in self.dataFrames.keys():
                self.dataFrames['WBLZ']=self.dataFrames['WBLZ'][pd.notnull(self.dataFrames['WBLZ']['OBJS'])]      
            # empty LAYR OBJS-BLOBs
            if 'LAYR' in self.dataFrames.keys():
                if 'OBJS' in self.dataFrames['LAYR'].columns:
                    self.dataFrames['LAYR']=self.dataFrames['LAYR'][pd.notnull(self.dataFrames['LAYR']['OBJS'])]     
                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)             
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _constructEmptyDf(self,cols=['DummyCol1','DummyCol2']):
        """Constructs an empty df with cols.

        Args:
            * cols: list of colNames

        Returns:
            df: constructed df

        Raises:
            XmError                                       
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            df=pd.DataFrame()       
            for col in cols:
                df[col]=pd.Series()  
             
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)             
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return df

    def getWDirModelDirModelName(self):
        """ Returns (wDir,modelDir,modelName,mx1FileName).

        Returns:            
            (wDir,modelDir,modelName,mx1FileName)

        wDir
            If wDir as given literally in .xmlFile is not a valid Dir 
            or such a wDir relative to .xmlFile-Path exists the wDir relative is returned. 

        mx1FileName
            mx1FileName is assumed to be: .:\...\WD...\B...\V...\BZ...\M... .MX1
            If not existing: .*.MX1 (first match is returned)
            If a suitable mx1File is not existing an INFO-Message is generated.
           
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        result=tuple(['','',''])
        
        try:    
            # wDir literally from Model 
            t=self.dataFrames['SYSTEMKONFIG']
            WDirFromModel=t[t['ID'].astype(int)==1]['WERT'].iloc[0] 

            # such a wDir relative to Modelfile-Path
            head,wDirTail=os.path.split(os.path.abspath(WDirFromModel))
            xmlDirHead,tail=os.path.split(os.path.abspath(self.xmlFile))
            WDirFromModelFilePath=os.path.join(xmlDirHead,wDirTail)
            
            if not os.path.isdir(WDirFromModel) and not os.path.isdir(WDirFromModelFilePath):   
                    logStrFinal="{:s}wDirs {:s} and {:s} both not existing!".format(logStr,WDirFromModel,WDirFromModelFilePath)                          
                    logger.error(logStrFinal)       
                    raise XmError(logStrFinal)  
            elif os.path.isdir(WDirFromModel) and not os.path.isdir(WDirFromModelFilePath):   
                    logStr="{:s}Only wDir {:s} exists.".format(logStr,WDirFromModel)                          
                    logger.debug(logStr)       
                    wDir=wDirFromModel
            elif not os.path.isdir(WDirFromModel) and os.path.isdir(WDirFromModelFilePath):   
                    logStr="{:s}Only wDir {:s} exists.".format(logStr,WDirFromModelFilePath)                          
                    logger.debug(logStr)       
                    wDir=WDirFromModelFilePath
            else: # beide Verzeichnisse existieren ....   
                    if WDirFromModel == WDirFromModelFilePath:
                        pass # der Normalfall
                    else:
                        logStr="{:s}wDirs {:s} and {:s} both are existing.".format(logStr,WDirFromModel,WDirFromModelFilePath)      
                        logger.debug(logStr)  
                        logStr="{:s}wDir {:s} is used.".format(logStr,WDirFromModelFilePath)   
                        logger.debug(logStr)       
                    wDir=WDirFromModelFilePath

            t=self.dataFrames['DATENEBENE']
            B=t[t['TYP'].str.contains('BASIS')]['ORDNERNAME'].iloc[0] 
            V=t[t['TYP'].str.contains('VARIANTE')]['ORDNERNAME'].iloc[0]
            BZ=t[t['TYP'].str.contains('BZ')]['ORDNERNAME'].iloc[0]
            modelDir=os.path.join(B,os.path.join(V,BZ))

            t=self.dataFrames['MODELL']
            modelName=t['BEZEICHNER'].iloc[0]          
  
            mx1FilenamePre=os.path.join(wDir,os.path.join(modelDir,modelName))     
            mx1Filename=mx1FilenamePre+'.MX1' 
            if not os.path.isfile(mx1Filename):                                          
                logger.debug("{:s}This mx1FileName: {:s} does not exist. Trying .*.MX1 ...".format(logStr,mx1Filename))
                mx1FileNames=glob.glob(mx1FilenamePre+'.*'+'.MX1')
                if len(mx1FileNames)==0:
                    logger.info("{:s}Those mx1FileName(s): {:s} also do not exist?!".format(logStr,mx1FilenamePre+'.*'+'.MX1'))  
                else:
                    mx1Filename=mx1FileNames[0]

            result=tuple([wDir,modelDir,modelName,mx1Filename])

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal)       
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return result 

    def getVersion(self,type='BASIS'):
        """ Returns VERSION-String i.e. Sir3S-90-10.

        Args:
            * type: BASIS or VARIANTE or BZ; the DATENEBENEn-TYPe from which the VERSION-String is requested 
     
        Returns:
            * VERSION-String i.e. Sir3S-90-10; Sir3S-90-09 is returned if Attribute VERSION is not available  
        Raises:
            XmError

        >>> xm=xms['OneLPipe']
        >>> vStr=xm.getVersion()
        >>> import re
        >>> m=re.search('Sir(?P<Db3s>[DBdb3Ss]{2})-(?P<Major>\d+)-(?P<Minor>\d+)$',vStr) # i.e. Sir3S-90-10
        >>> int(m.group('Major')[0])
        9
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
                
        try:               
            vStr=None
            t=self.dataFrames['DATENEBENE']
            if 'VERSION' not in t.columns.tolist():
                vStr='Sir3S-90-10'
            else:           
                tType=t[t['TYP'].str.contains(type)]
                vStr=tType['VERSION'].iloc[0] 
                       
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal)       
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return vStr

    def _getvXXXXAsOneString(self,vXXXX=None,start=0,end=-1,dropColList=None,filterColList=None,mapFunc={},sortList=None,fmtFunc={},index=True,header=True):
        """Returns vXXXX-Content as one String (for Doctest-Purposes).

        Args:
            * vXXXX: df=self.dataFrames[vXXXX]
            * start
            * end
            * dropColList
            * filterColList
            * mapFunc: col:func: df[col].map(func)
            * sortList
            * fmtFunc: col:func: passed to df.to_string(formatters=fmtFunc, ...)
            * index
            * header

        Returns:
            * df.to_string(formatters=fmtFunc,index=index,header=header)                
           
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        dfContentAsOneString=None

        df=self.dataFrames[vXXXX]

        # select rows
        if end == -1:
            df=df[start:]
        else:
            df=df[start:end]

        # select cols        
        colList=df.columns.values.tolist()
        if isinstance(dropColList,list):
            colListOut=[col for col in colList if col not in dropColList]
        else:
            colListOut=colList
        df=df.loc[:,colListOut]
        if filterColList!=None:
            df=df.filter(items=filterColList)

        # map cols
        for col,func in mapFunc.items():          
            if col not in df.columns:
                pass
            else:
                df[col]=df[col].map(func)

        # sort 
        if isinstance(sortList,list):
            df=df.sort_values(sortList,ascending=True)    

        try:                 
            dfContentAsOneString=df.to_string(formatters=fmtFunc,index=index,header=header)                                                                            
        except MxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return dfContentAsOneString

    def _vXXXX(self):
        """Creates all Views.

        Views created:
            * BLOB-Data 
                * vLAYR
                * vWBLZ
                * vAGSN u. vAGSN_raw
            * Timeseries
                * vLFKT
                * vQVAR
                * vPVAR
                * vSWVT
            * Signalmodel
                * vRSLW           
            * Miscellanea
                * vRART
            * Hydraulicmodel
                * Nodes
                    * vVKNO: CONT-Nodes (also called Block-Nodes)
                    * vKNOT
                    * pXCorZero, pYCorZero
                * Edges
                    * vROHR: Pipes
                    * vFWVB: Housestations (district heating)    
                * all Edges (all; implemented Edges see vVBEL_edges)
                    * vVBEL
            * Annotations
                * vNRCV
                * vGTXT                       
                    
        Raises:
            XmError                      
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            #BLOB-Data
            self.dataFrames['vLAYR']=self._vLAYR()
            self.dataFrames['vWBLZ']=self._vWBLZ()
            #self.dataFrames['vAGSN']=self._vAGSN()
            #self.dataFrames['vAGSN_raw']=self.dataFrames['vAGSN']

            #timeseries
            self.dataFrames['vLFKT']=self._vLFKT()   
            self.dataFrames['vQVAR']=self._vQVAR()           
            self.dataFrames['vPVAR']=self._vPVAR()           
            self.dataFrames['vSWVT']=self._vSWVT()

            #signalmodel
            self.dataFrames['vRSLW']=self._vRSLW(vSWVT=self.dataFrames['vSWVT']) 
            
            #nodes    
            self.dataFrames['vVKNO']=self._vVKNO()
            self.dataFrames['vKNOT']=self._vKNOT(
                 vVKNO=self.dataFrames['vVKNO']
                ,vQVAR=self.dataFrames['vQVAR']
                ,vPVAR=self.dataFrames['vPVAR']
                ,vLFKT=self.dataFrames['vLFKT']
                )
            #
            vKNOT=self.dataFrames['vKNOT']
            self.pXCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & 
                (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['XKOR'].astype(np.double).min()

            self.pYCorZero=vKNOT[
                (vKNOT['CONT_ID'].astype(int)==1001) 
                & (vKNOT['BESCHREIBUNG'].fillna('').str.startswith('Template Element') == False)]['YKOR'].astype(np.double).min()

            #special edges
            self.dataFrames['vROHR']=self._vROHR(vKNOT=self.dataFrames['vKNOT'])
            self.dataFrames['vFWVB']=self._vFWVB(vKNOT=self.dataFrames['vKNOT']
                                            ,vLFKT=self.dataFrames['vLFKT']
                                            ,vWBLZ=self.dataFrames['vWBLZ']
                                            )                                             

            #all edges
            self.dataFrames['vVBEL']=self._vVBEL(vKNOT=self.dataFrames['vKNOT'])

            self.dataFrames['vAGSN']=self._vAGSN()
            self.dataFrames['vAGSN_raw']=self.dataFrames['vAGSN']

            #miscellanea
            self.dataFrames['vRART']=self._vRART()          

            #annotations
            self.dataFrames['vNRCV']=self._vNRCV()            
            self.dataFrames['vGTXT']=self._vGTXT()

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _vLAYR(self):
        """One row per LAYR and OBJ.
        
        Returns:
            columns           
                LAYR (also called 'Group')
                    * LFDNR
                    * NAME

                    from SIR 3S OBJ BLOB collection:
                        * OBJTYPE: type (i.e.ROHR) of a LAYR OBJ
                        * OBJID: pk (or tk?!) of a LAYR OBJ      
                                 
                LAYR IDs
                    * pk, tk         

                ANNOTATION
                    * nrObjInGroup: Element Nr. in LAYR (LFDNR) - should be 1 otherwise the same OBJ occurs in the same LAYR multiple times               
                    * nrObjtypeInGroup: Element Nr. of OBJTYPE in LAYR (LFDNR)     
                    
                SORTING
                    LFDNR,NAME,OBJTYPE,OBJID       
                    
        Raises:
            XmError                     
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vLAYR=None
            vLAYR=self._OBJS('LAYR')

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
            vLAYR=vLAYR.assign(nrObjInGroup=vLAYR.sort_values(['LFDNR','OBJTYPE','OBJID']).groupby(['LFDNR','OBJID']).cumcount()+1)
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

    def _vWBLZ(self):
        """One row per WBLZ and OBJ.

        Returns:
            columns
                WBLZ
                    * AKTIV            
                    * BESCHREIBUNG
                    * IDIM
                    * NAME

                    from SIR 3S OBJ BLOB collection:
                        * OBJTYPE: type (always KNOT?!) 
                        * OBJID: pk (or tk?!) 
                      
                WBLZ IDs
                    * pk   
                    
                SORTING
                    NAME,pk                                  
                    
        Raises:
            XmError                                
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vWBLZ=None
            vWBLZ=self._OBJS('WBLZ')
          
            vWBLZ=vWBLZ[[
             'AKTIV'            
            ,'BESCHREIBUNG'
            ,'IDIM'
            ,'NAME'
            #from WBLZ's OBJS: 
            ,'OBJTYPE' #type (i.e. KNOT) of a WBLZ OBJ
            ,'OBJID' #pk (or tk?!) of a WBLZ OBJ          
            #IDs (of the WBLZ)
            ,'pk'
            ]]
            vWBLZ.sort_values(['NAME','pk'],ascending=True,inplace=True)
            #reindex:
            vWBLZ=pd.DataFrame(vWBLZ.values,columns=vWBLZ.columns)
          
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

    def _vAGSN(self):
        """One row per AGSN and OBJ.

        Returns:
            columns
                AGSN
                    * LFDNR
                    * NAME
                    * AKTIV
                   
                    * from SIR 3S OBJ BLOB collection:

                        * OBJTYPE: type (i.e.ROHR) 
                        * OBJID: pk (or tk?!)   
                                 
                AGSN IDs
                    * pk, tk   

                Sequence
                    * Model
                        * therefore nrObjIdInAgsn (see ANNOTATION below) should be the realwolrd sequence
                        
                ANNOTATION
                    * nrObjIdInAgsn: lfd.Nr. (in Schnittreihenfolge) Obj. (der Kante) in AGSN (AGSN is defined by LFDNR not by NAME)                      
                    * nrObjIdTypeInAgsn: should be 1 determined by raw data
                        * nrObjIdTypeInAgsn>1 - if any - are not part of the view
                        * the 1st occurance is in the view 
                    * Layer
                        0=undef
                        bei Netztyp 21: 1=VL, 2=RL, 0=undef 
                        wenn keine BN-Trennzeile gefunden wird, wird VL angenommen und gesetzt
                        die BN-Trennzeile wird dem VL (1) zugerechnet
                    * nextNODE: node which is connected by the edge
                        * the cut-direction is defined (per cut and comp) by edge-sequence
                        * the cut node-sequence ist the (longest shortest) path between the nodes of the 1st and last edge                         
                        * in case of 1 edge cut-direction  is edge-definition and cut node-sequence is edge-definition
                        * the nextNODEs are the node-sequence omitting the start-node ... 
                        * ... nextNODE of an edge is the node connected by this edge in cut-direction; so nextNODE might be the i-node (the source-node) of the edge
                        * if edge-direction is cut-direction nextNODE is the k-node (the sink-node) of the edge
                    * compNr
                        * all 1 if all edges in the cut are connected
                        * otherwise the compNr (starting with 1) the edge belongs to
                        * the comp-Sequence is defined by the edge-sequence 
                        * the nodes of the 1st and last edge in cut-definition of the comp are defining the node-Sequence of the (longest shortest) path in the comp 
                    * parallel Edges 
                        * are omitted in the cut-Result; the 1st edge in cut-definition is in the edge
                    * Abzweige
                        * are omitted in the cut-Result
                        * the nodes of the 1st and last edge in cut-definition are defining the node-Sequence of the (longest shortest) path (comp-wise)
                        * only edges implementing this path are in the cut-Result

        Raises:
            XmError             
            
        >>> xmlFile=ms['GPipes']   
        >>> from Xm import Xm
        >>> xm=Xm(xmlFile=xmlFile)
        >>> vAGSN=xm.dataFrames['vAGSN']
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))
           index LFDNR NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0      7    14   LR   101    VENT  5309992331398639768  5625063016896368599  5625063016896368599              1                  1      0       G1      1
        1      8    14   LR   101    ROHR  5244313507655010738  5625063016896368599  5625063016896368599              2                  1      0      GKS      1
        2      9    14   LR   101    VENT  5508684139418025293  5625063016896368599  5625063016896368599              3                  1      0      GKD      1
        3     10    14   LR   101    ROHR  5114681686941855110  5625063016896368599  5625063016896368599              4                  1      0       G3      1
        4     11    14   LR   101    ROHR  4979507900871287244  5625063016896368599  5625063016896368599              5                  1      0       G4      1
        5     12    14   LR   101    VENT  5745097345184516675  5625063016896368599  5625063016896368599              6                  1      0       GR      1
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR-Lücke']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))
           index LFDNR      NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0     13    16  LR-Lücke   101    VENT  5309992331398639768  5630543731618051887  5630543731618051887              1                  1      0       G1      1
        1     14    16  LR-Lücke   101    ROHR  5244313507655010738  5630543731618051887  5630543731618051887              2                  1      0      GKS      1
        2     15    16  LR-Lücke   101    ROHR  5114681686941855110  5630543731618051887  5630543731618051887              3                  1      0       G3      2
        3     16    16  LR-Lücke   101    ROHR  4979507900871287244  5630543731618051887  5630543731618051887              4                  1      0       G4      2
        4     17    16  LR-Lücke   101    VENT  5745097345184516675  5630543731618051887  5630543731618051887              5                  1      0       GR      2
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR-Flansch']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))    
           index LFDNR        NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0     18    18  LR-Flansch   101    VENT  5309992331398639768  5134530907542044265  5134530907542044265              1                  1      0       G1      1
        1     19    18  LR-Flansch   101    ROHR  5244313507655010738  5134530907542044265  5134530907542044265              2                  1      0      GKS      1
        2     20    18  LR-Flansch   101    VENT  5508684139418025293  5134530907542044265  5134530907542044265              3                  1      0      GKD      1
        3     21    18  LR-Flansch   101    ROHR  5114681686941855110  5134530907542044265  5134530907542044265              4                  1      0       G3      1
        4     22    18  LR-Flansch   101    ROHR  4979507900871287244  5134530907542044265  5134530907542044265              5                  1      0       G4      1
        5     24    18  LR-Flansch   101    VENT  5745097345184516675  5134530907542044265  5134530907542044265              7                  1      0       GR      1
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR-Parallel']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))          
           index LFDNR         NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0     25    20  LR-Parallel   101    VENT  5309992331398639768  4694969854935170169  4694969854935170169              1                  1      0       G1      1
        1     26    20  LR-Parallel   101    ROHR  5244313507655010738  4694969854935170169  4694969854935170169              2                  1      0      GKS      1
        2     27    20  LR-Parallel   101    VENT  5116489323526156845  4694969854935170169  4694969854935170169              3                  1      0      GKD      1
        3     29    20  LR-Parallel   101    ROHR  5114681686941855110  4694969854935170169  4694969854935170169              5                  1      0       G3      1
        4     30    20  LR-Parallel   101    ROHR  4979507900871287244  4694969854935170169  4694969854935170169              6                  1      0       G4      1
        5     31    20  LR-Parallel   101    VENT  5745097345184516675  4694969854935170169  4694969854935170169              7                  1      0       GR      1
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vAGSN=None
            vAGSN=self._OBJS('AGSN')
          
            vAGSN=vAGSN[[
             'LFDNR'
             ,'NAME'
             ,'AKTIV'
            #from OBJS
            ,'OBJTYPE' #type (i.e. KNOT) 
            ,'OBJID' #pk (or tk?!) 
            #IDs
            ,'pk','tk'
            ]]
            vAGSN=vAGSN.assign(nrObjIdInAgsn=vAGSN.groupby(['LFDNR']).cumcount()+1) # dieses VBEL-Obj. ist im Schnitt Nr. x
            vAGSN=vAGSN.assign(nrObjIdTypeInAgsn=vAGSN.groupby(['LFDNR','OBJTYPE','OBJID']).cumcount()+1) # dieses VBEL-Obj kommt im Schnitt zum x. Mal vor

            tModell=self.dataFrames['MODELL']
            netzTyp=tModell['NETZTYP'][0] # '21'

            vAGSN['Layer']=0
            if netzTyp == '21':
                #vAGSN['Layer']=-666

                for lfdnr in sorted(vAGSN['LFDNR'].unique()):
                
                    oneAgsn=vAGSN[vAGSN['LFDNR']==lfdnr]
                   
                    dfSplitRow=oneAgsn[oneAgsn['OBJID'].str.endswith('\n')]
                    # Test if empty Dataframe
                    if dfSplitRow.empty:                        
                        logger.debug("{0:s}vAGSN {1:s} has no OBJID\n-Row to seperate SL/RL.".format(logStr,oneAgsn.iloc[0].NAME)) 
                        vAGSN.loc[oneAgsn.index.values[0]:oneAgsn.index.values[-1],'Layer']=1 

                    else:
                        splitRowIdx=dfSplitRow.index.values[0]                                    
    
                        vAGSN.loc[splitRowIdx,'Layer']=1#0
                        vAGSN.loc[oneAgsn.index.values[0]:splitRowIdx-1,'Layer']=1
                        vAGSN.loc[splitRowIdx+1:oneAgsn.index.values[-1],'Layer']=2

                        ObjId=vAGSN.loc[splitRowIdx,'OBJID']
                        vAGSN.loc[splitRowIdx,'OBJID']=ObjId.rstrip('\n')

            df=pd.merge(
                    vAGSN[vAGSN['nrObjIdTypeInAgsn']==1] # mehrfach vorkommende selbe VBEL im selben Schnitt ausschliessen
                   ,self.dataFrames['vVBEL']
                   ,how='left' 
                   ,left_on=['OBJTYPE','OBJID']  
                   ,right_index=True ,suffixes=('', '_y'))
            df.rename(columns={'tk_y':'tk_VBEL'},inplace=True)
            df=df[pd.isnull(df['tk_VBEL']) != True].copy()

            df['nextNODE']=None
            df['compNr']=None
            df['pEdgeNr']=0
            df['SOURCE_i']=df['NAME_i']
            df['SOURCE_k']=df['NAME_k']

            for nr in df['LFDNR'].unique():                
                
                for ly in df[df['LFDNR']==nr]['Layer'].unique():                                        

                    dfSchnitt=df[(df['LFDNR']==nr) & (df['Layer']==ly)]                                      
                    logger.debug("{0:s}Schnitt: {1:s} Nr: {2:s} Layer: {3:s}".format(logStr
                                                                           ,str(dfSchnitt['NAME'].iloc[0])
                                                                           ,str(dfSchnitt['LFDNR'].iloc[0])
                                                                           ,str(dfSchnitt['Layer'].iloc[0])
                                                                          )) 
                    self.dataFrames['dummy']=dfSchnitt
                    logString="{0:s}dfSchnitt: {1:s}".format(logStr,self._getvXXXXAsOneString(vXXXX='dummy'))
                    logger.debug(logString)
                  
                    dfSchnitt=dfSchnitt.reset_index() # stores index as a column
                    GSchnitt=nx.from_pandas_edgelist(dfSchnitt, source='SOURCE_i', target='SOURCE_k', edge_attr=True,create_using=nx.MultiGraph())
                    
                    iComp=0
                    for comp in nx.connected_components(GSchnitt):
                        iComp+=1

                        logger.debug("{0:s}CompNr.: {1:s}".format(logStr,str(iComp))) 
                        
                        GSchnittComp=GSchnitt.subgraph(comp)
                                                
                        # Knoten der ersten Kante                        
                        for u,v, datadict in sorted(GSchnittComp.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                            
                            #logger.debug("{0:s}1st: i: {1:s} (Graph: {2:s}) k:{3:s} (Graph: {4:s})".format(logStr,datadict['NAME_i'],u,datadict['NAME_k'],v)) 
                            sourceKi=datadict['NAME_i']
                            sourceKk=datadict['NAME_k']      
                            break
                        # Knoten der letzten Kante; sowie Ausgabe über alle Kanten
                        ieComp=0
                        for u,v, datadict in sorted(GSchnittComp.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                                                        
                            ieComp+=1
                            if datadict['NAME_i']==u and datadict['NAME_k']==v:
                                GraphStr="="
                            elif datadict['NAME_i']==v and datadict['NAME_k']==u:                                                                                            
                                GraphStr="{0:s}>{1:s}".format(u,v)
                            else:
                                GraphStr="Fehler: Die NX-Kante ist ungl. der SIR 3S Kante?!"
                            logger.debug("{0:s}iComp: {1:d} ieComp: {2:d} idx: {3:d} NX i: {4:s} > NX k:{5:s} (SIR 3S Kantendef.: {6:s})".format(logStr,iComp,ieComp,datadict['index'],u,v,GraphStr)) 
                        #logger.debug("{0:s}Lst: i: {1:s} (Graph: {2:s}) k:{3:s} (Graph: {4:s})".format(logStr,datadict['NAME_i'],u,datadict['NAME_k'],v)) 
                        targetKi=datadict['NAME_i']
                        targetKk=datadict['NAME_k']
                        
                        
                        # laengster Pfad zwischen den Knoten der ersten und letzten Kante (4 Möglichkeiten)
                        nlComp=nx.shortest_path(GSchnittComp,sourceKi,targetKk)
                        nlCompTmp=nx.shortest_path(GSchnittComp,sourceKk,targetKk)
                        if len(nlCompTmp)>len(nlComp):
                            nlComp=nlCompTmp
                        nlCompTmp=nx.shortest_path(GSchnittComp,sourceKi,targetKi)
                        if len(nlCompTmp)>len(nlComp):
                            nlComp=nlCompTmp
                        nlCompTmp=nx.shortest_path(GSchnittComp,sourceKk,targetKi)
                        if len(nlCompTmp)>len(nlComp):
                            nlComp=nlCompTmp        
                        
                        logger.debug("{0:s}Pfad: Start: {1:s} > Ende: {2:s}".format(logStr,nlComp[0],nlComp[-1])) 
                                                
                        # SP-Kanten ermitteln (es koennten Abzweige dabei sein; die sind dann im SP-Graphen nicht enthalten)
                        GSchnittCompSP=GSchnittComp.subgraph(nlComp)
                        # SP-Kanten Ausgabe
                        ieComp=0
                        for u,v, datadict in sorted(GSchnittCompSP.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                                                        
                            ieComp+=1
                            if datadict['NAME_i']==u and datadict['NAME_k']==v:
                                GraphStr="="
                            elif datadict['NAME_i']==v and datadict['NAME_k']==u:                                                                                            
                                GraphStr="{0:s}>{1:s}".format(u,v)
                            else:
                                GraphStr="Fehler: Die NX-Kante ist ungl. der SIR 3S Kante?!"
                            logger.debug("{0:s}iComp: {1:d} ieCompSP: {2:d} idx: {3:d} NX i: {4:s} > NX k:{5:s} (SIR 3S Kantendef.: {6:s})".format(logStr,iComp,ieComp,datadict['index'],u,v,GraphStr)) 

                        # index-Liste der SP-Kanten
                        idxLst=[]
                        for u,v, datadict in sorted(GSchnittCompSP.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                                                        
                            idxLst.append(datadict['index'])
                        
                        # parallele Kanten bis auf eine aus der index-Liste eliminieren
                        idxLstWithoutP=[idx for idx in idxLst]
                        idxLstOnlyP=[]
                        nrOfParallel=[]
                        # For every node in graph
                        for node in GSchnittCompSP.nodes(): 
                            # We look for adjacent nodes
                            for adj_node in GSchnittCompSP[node]: 
                                # If adjacent node has an edge to the first node
                                # Or our graph as several edges from the first to the adjacent node
                                if node in GSchnittCompSP[adj_node] or len(GSchnittCompSP[node][adj_node]) > 1: 
                                    #
                                    GSchnittCompSPParallel=GSchnittCompSP.subgraph([node,adj_node])
                                    ip=1
                                    for u,v, datadict in sorted(GSchnittCompSPParallel.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                                                                                       
                                        if ip>1:
                                            idx=datadict['index']
                                            if idx in idxLstWithoutP:
                                                if datadict['NAME_i']==u and datadict['NAME_k']==v:
                                                    GraphStr="="
                                                elif datadict['NAME_i']==v and datadict['NAME_k']==u:                                                                                            
                                                    GraphStr="{0:s}>{1:s}".format(u,v)
                                                else:
                                                    GraphStr="Fehler: Die NX-Kante ist ungl. der SIR 3S Kante?!"
                                                logger.debug("{0:s}idx: {1:d} parallele Kante: NX i: {2:s} > NX k:{3:s} (SIR 3S Kantendef.: {4:s})".format(logStr,idx,u,v,GraphStr))                                                                                               
                                                idxLstWithoutP.remove(idx)
                                                idxLstOnlyP.append(idx)
                                                nrOfParallel.append(ip-1)                                            
                                        ip+=1                      

                        # compNr-List: Laenge = Anzahl der Kanten  (parallele sind dabei)                                                                        
                        compNr=np.empty(GSchnittCompSP.number_of_edges(),dtype=int) 
                        compNr.fill(iComp)
                                                                           
                        logger.debug("{0:s}Len NodeList (with 1st Node): {1:d}".format(logStr,len(nlComp)))   
                        logger.debug("{0:s}Len CompList                : {1:d}".format(logStr,len(compNr)))         
                        logger.debug("{0:s}Len IdxList                 : {1:d}".format(logStr,len(idxLst)))
                        logger.debug("{0:s}Len IdxListWithoutP         : {1:d}".format(logStr,len(idxLstWithoutP)))   

                        logger.debug("{0:s}NodeList (with 1st Node): {1:s}".format(logStr,str(nlComp)))   
                        logger.debug("{0:s}CompList                : {1:s}".format(logStr,str(compNr)))   
                        logger.debug("{0:s}IdxList                 : {1:s}".format(logStr,str(idxLst)))   
                        logger.debug("{0:s}IdxListWithoutP         : {1:s}".format(logStr,str(idxLstWithoutP)))   

                        df.loc[idxLstWithoutP,'nextNODE']=nlComp[1:]  
                        df.loc[idxLst,'compNr']=compNr
                        df.loc[idxLstOnlyP,'pEdgeNr']=nrOfParallel
                       
            df['pEdgeNr']=df['pEdgeNr'].astype(int)
            df.drop(['SOURCE_i', 'SOURCE_k'], axis=1,inplace=True)

            # Testausgabe
            self.dataFrames['vAGSN_raw']=df[['LFDNR','NAME','OBJTYPE','nrObjIdInAgsn','Layer','NAME_i','NAME_k','L','D','nextNODE','compNr','pEdgeNr']]
            logger.debug("{0:s}df: {1:s}".format(logStr,self._getvXXXXAsOneString(vXXXX='vAGSN_raw',index=True)))

            vAGSN=df[(df['pEdgeNr']==0) & (pd.notnull(df['compNr']))].filter(items=[
                        'LFDNR'
                        ,'NAME'
                        ,'AKTIV'
                        ,'OBJTYPE'
                        ,'OBJID'
                        ,'pk'
                        ,'tk'
                        ,'nrObjIdInAgsn'
                        ,'nrObjIdTypeInAgsn'
                        ,'Layer'
                        ,'nextNODE'
                        ,'compNr'
                        #,'pEdgeNr'
                        ])

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vAGSN,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vAGSN=pd.DataFrame()   
                                                                              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vAGSN

    def _vRART(self):
        """One row per RART.

        Returns:
            columns:
                RART
                    * NAME
                    * BESCHREIBUNG
                    * INDSTD_TXT
                    * INDSTD (numeric)
                    * DWDT
                RART_BZ
                    * WSOSTD
                ID
                    * pk
                References
                    * NAME_KREF1
                    * NAME_KREF2
                    * NAME_SWVT
                    * [NAME_RCPL] - only if RCPLs exist
            
            sequence: Model

        Raises:
            XmError                                
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vRART=None            
        
            sPgrp='(0=aus | 2=Drehzahl | 21=Regelpunktliste Druckseite | 22=Regelpunktliste Saugseite | 41=Netzdruck Druckseite, Sollwert konstant | 43=Netzdruck Druckseite, Sollwert Tabelle | 42=Netzdruck Saugseite, Sollwert konstant | 44=Netzdruck Saugseite, Sollwert Tabelle | 51=Druckerhoehung/-abfall am Stellglied selbst, Sollwert konstant | 54=Druckerhoehung/-abfall am Stellglied selbst, Sollwert Tabelle | 52=Differenzdruck Druckseite, Sollwert konstant | 55=Differenzdruck Druckseite, Sollwert Tabelle | 53=Differenzdruck Saugseite, Sollwert konstant | 56=Differenzdruck Saugseite, Sollwert Tabelle | 62=Mitteldruck Druckseite, Sollwert konstant | 65=Mitteldruck Druckseite, Sollwert Tabelle | 63=Mitteldruck Saugseite, Sollwert konstant | 66=Mitteldruck Saugseite, Sollwert Tabelle | 71=Durchfluss Messstelle, Wirkungsrichtung positiv, Sollwert konstant | 73=Durchfluss Messstelle, Wirkungsrichtung positiv, Sollwert Tabelle | 72=Durchfluss Messstelle, Wirkungsrichtung negativ, Sollwert konstant | 74=Durchfluss Messstelle, Wirkungsrichtung negativ, Sollwert Tabelle)'            
            sRegv='(1002=Stellung | 1021=Regelpunktliste Unterstrom | 1022=Regelpunktliste Oberstrom | 1041=Netzdruck Unterstrom, Sollwert konstant | 1043=Netzdruck Unterstrom, Sollwert Tabelle | 1042=Netzdruck Oberstrom, Sollwert konstant | 1044=Netzdruck Oberstrom, Sollwert Tabelle | 1051=Druckabfall Regelventil, Sollwert konstant | 1054=Druckabfall Regelventil, Sollwert Tabelle | 1052=Differenzdruck Unterstrom, Sollwert konstant | 1055=Differenzdruck Unterstrom, Sollwert Tabelle | 1053=Differenzdruck Oberstrom, Sollwert konstant | 1056=Differenzdruck Oberstrom, Sollwert Tabelle | 1062=Mitteldruck Unterstrom, Sollwert konstant | 1065=Mitteldruck Unterstrom, Sollwert Tabelle | 1063=Mitteldruck Oberstrom, Sollwert konstant | 1066=Mitteldruck Oberstrom, Sollwert Tabelle | 1071=Durchfluss Messstelle, Wirkungsrichtung positiv, Sollwert konstant | 1073=Durchfluss Messstelle, Wirkungsrichtung positiv, Sollwert Tabelle | 1072=Durchfluss Messstelle, Wirkungsrichtung negativ, Sollwert konstant | 1074=Durchfluss Messstelle, Wirkungsrichtung negativ, Sollwert Tabelle)'
            sRegvGas='(1002=Stellung | 1041=Netzdruck, Unterstrom, Sollwert konstant | 1042=Netzdruck, Oberstrom, Sollwert konstant | 1071=Durchfluss Messstelle, Wirkungsrichtung positiv, Sollwert konstant | 1073=Durchfluss Messstelle, Wirkungsrichtung positiv, Sollwert Tabelle)'
            items=sPgrp.strip('()').split(sep='|')+sRegv.strip('()').split(sep='|')+sRegvGas.strip('()').split(sep='|')
            IndstdDct=dict(zip([int(pair[0]) for pair in [item.split(sep='=') for item in items]]
                ,[pair[1].strip()  for pair in [item.split(sep='=') for item in items]]
                     ))
            #logger.debug("{0:s}{1:s}".format(logStr,str(IndstdDct))) 

            vRART=pd.merge(self.dataFrames['RART_BZ'],self.dataFrames['RART'],left_on='fk',right_on='pk',suffixes=['_BZ',''])[['NAME','BESCHREIBUNG'
            ,'INDSTD','DWDT'
            ,'fkKREF1','fkKREF2'
            #BZ
            ,'WSOSTD','fkRCPL', 'fkSWVT','pk']]

            vKnot=self.dataFrames['vKNOT']
            colLst=vRART.columns.tolist()
            colLst.append('NAME_KREF1')
            vRART=pd.merge(vRART,vKnot,left_on='fkKREF1',right_on='pk',suffixes=['','_KREF1'],how='left')[colLst]
            colLst.remove('fkKREF1')
            colLst.append('NAME_KREF2')
            colLst.remove('fkKREF2')
            vRART=pd.merge(vRART,vKnot,left_on='fkKREF2',right_on='pk',suffixes=['','_KREF2'],how='left')[colLst]

            vSwvt=self.dataFrames['vSWVT']
            colLst.append('NAME_SWVT')

              # * W: 1st Value
              #      * W_min
              #      * W_max

            colLst.remove('fkSWVT')
            vRART=pd.merge(vRART,vSwvt,left_on='fkSWVT',right_on='pk',suffixes=['','_SWVT'],how='left')[colLst]

            if 'RCPL' in self.dataFrames:
                tRcpl=self.dataFrames['RCPL']
                colLst.append('NAME_RCPL')
                colLst.remove('fkRCPL')
                vRART=pd.merge(vRART,tRcpl,left_on='fkRCPL',right_on='pk',suffixes=['','_RCPL'],how='left')[colLst]
            else:
                vRART.drop(columns=['fkRCPL'],inplace=True)      

            vRART['INDSTD']=pd.to_numeric(vRART['INDSTD'])                 
            vRART['INDSTD_TXT']=vRART.apply(lambda row: IndstdDct[row.INDSTD] if row.INDSTD in IndstdDct  else -1  , axis=1)
            cols=vRART.columns.tolist()
            cols.pop(cols.index('INDSTD_TXT'))
            cols.insert(cols.index('INDSTD'),'INDSTD_TXT')
            vRART=vRART.reindex(cols,axis="columns")

            #['NAME', 'BESCHREIBUNG', 'INDSTD_TXT', 'INDSTD', 'DWDT', 'WSOSTD', 'pk', 'NAME_KREF1', 'NAME_KREF2', 'NAME_SWVT']

            logger.debug("{0:s}{1:s}".format(logStr,str(vRART.columns.tolist())))
          
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vRART,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vRART=pd.DataFrame()   
                                                                              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vRART

    def _OBJS(self,dfName):
        """Decode a column OBJS (a BLOB containing a SIR 3S OBJ collection).

        Args:
            dfName: Name of a dataFrame with column OBJS
            
            columns used (in self.dataFrames[dfName]):
                * OBJS (BLOB): i.e.: KNOT~4668229590574507160\t...
                * pk: ID (of the row) 
                * None is returned if these columns are missing
                * in this case no changes in column OBJS in self.dataFrames[dfName]

        Returns:
            column OBJS in self.dataFrames[dfName] is decoded
            to 'XXXX~' if OBJS was None 

            dfOBJS: dataFrame with one row per OBJ in OBJS: 
                columns added (compared to self.dataFrames[dfName]):
                    * OBJTYPE
                    * OBJID 
                rows missing (compared to self.dataFrames[dfName]):
                    * rows with OBJS None
        Raises:
            XmError                                
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            dfOBJS=None

            if dfName not in self.dataFrames.keys():
                 logger.debug("{0:s}{1:s} not in dataFrames.keys()".format(logStr,dfName)) 
            else:
                 logger.debug("{0:s}{1:s}     in dataFrames.keys()".format(logStr,dfName)) 

            if 'OBJS' not in self.dataFrames[dfName].columns.tolist():
                 logger.debug("{0:s}column OBJS not in dataFrame!".format(logStr)) 
                 logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
                 return dfOBJS

            if 'pk' not in self.dataFrames[dfName].columns.tolist():
                 logger.debug("{0:s}column pk not in dataFrame!".format(logStr)) 
                 logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
                 return dfOBJS
           
           
            # Spalte OBJS dekodieren; wenn leer ((noch) keine OBJS), dann 'XXXX~'      
            #                                                                   4668229590574507160
            self.dataFrames[dfName].loc[:,'OBJS']=self.dataFrames[dfName]['OBJS'].apply(lambda x: 'XXXX~' if x is None else base64.b64decode(x)).str.decode('utf-8')

            # einzelne OBJS als neuer df
            # ------------------------->           
            sList=[pd.Series(row['pk'],index=row['OBJS'].split('\t'),name='pk_Echo') for index,row in self.dataFrames[dfName].iterrows()]                

            # sList[0]:
            # index:                      pk_Echo 
            # KNOT~4668229590574507160    5403356857783326643
            # XXXX~                       5403356857783326643

            dfOBJS_OBJS=pd.concat(sList).reset_index() # When we reset the index, the old index is added as a column named 'index', and a new sequential index is used
            dfOBJS_OBJS.rename(columns={'index':'ETYPEEID'},inplace=True)
            # dfOBJS_OBJS:
            #	ETYPEEID	              pk_Echo
            # 0	KNOT~4668229590574507160  5403356857783326643
            # 0 XXXX~                     5403356857783326643

            # ETYPEEID Checks als Filter
            dfOBJS_OBJS=dfOBJS_OBJS[dfOBJS_OBJS['ETYPEEID'].notnull()]
            dfOBJS_OBJS=dfOBJS_OBJS[dfOBJS_OBJS['ETYPEEID'].str.len()>5]

            # ETYPEEID: neue Spalten bilden 
            dfOBJS_OBJS['OBJTYPE']=dfOBJS_OBJS['ETYPEEID'].str[:4]
            dfOBJS_OBJS['OBJID']=dfOBJS_OBJS['ETYPEEID'].str[5:]
            # ETYPEEID: loeschen
            dfOBJS_OBJS.drop(['ETYPEEID'],axis=1,inplace=True)
            # dfOBJS_OBJS:
            #	OBJTYPE OBJID 	            pk_Echo
            # 0	KNOT    4668229590574507160	5403356857783326643   
            # <-------------------------                   
            
            # neuer df
            # --------                
            dfOBJS=pd.merge(self.dataFrames[dfName],dfOBJS_OBJS,left_on='pk',right_on='pk_Echo')
            dfOBJS.drop(['pk_Echo'],axis=1,inplace=True)

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(dfOBJS,pd.core.frame.DataFrame):
                pass 
            else:
                pass

            logger.debug(logStrFinal) 
                                                  
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return dfOBJS

    def _vLFKT(self):
        """One row per Loadfactor Timeseries.

        Returns:
            columns
                LFKT
                    * NAME
                    * BESCHREIBUNG
                    * INTPOL
                    * ZEITOPTION
                SERIES
                    * LF: 1st Value
                    * LF_min
                    * LF_max
                LFKT ID
                    * pk

        Raises:
            XmError
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

    def _vNRCV(self):
        """One row per NRCV (NumeRiCal Value).

        Returns:
            columns
                ANNOTATIONS
                    * cRefLfdNr
                CONT
                    * CONT
                    * CONT_ID
                    * CONT_LFDNR
                DP
                    Datapointgroup
                        * DPGR
                    Datapoint
                        * OBJTYPE
                        * fkOBJTYPE
                        * ATTRTYPE                    
                    Datapoint IDs
                        * pk_ROWS
                        * tk_ROWS
                NRCV IDs
                    * pk
                    * tk
                PLot Coordinates
                    * pXYLB: (X,Y): Left,Bottom

        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vNRCV=None
            vNRCV=self.dataFrames['NRCV']

            if 'DPGR_ROWS' in self.dataFrames.keys():
                # 90-09
                vNRCV=vNRCV.merge(self.dataFrames['DPGR_ROWS'],left_on='fkDPGR_ROWS',right_on='pk',suffixes=['_NR','_DR'])                
                vNRCV=vNRCV.merge(self.dataFrames['DPGR'],left_on='fk',right_on='pk',suffixes=['_DR2','_DG'])
            else:
                # 90-10                
                vNRCV=vNRCV.merge(self.dataFrames['DPGR_DPKT'],left_on='fkDPGR_DPKT',right_on='pk',suffixes=['_NR','_DR'])
                vNRCV=vNRCV.merge(self.dataFrames['DPKT'],left_on='fkDPKT',right_on='pk',suffixes=['_NR','_DR'])
                vNRCV=vNRCV.merge(self.dataFrames['DPGR'],left_on='fkDPGR',right_on='pk',suffixes=['_DR2','_DG'])
            
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

    def _vGTXT(self):
        """One row per GTXT (Graphic TeXT).

        Returns:
            columns
                GTXT
                    * GRAFTEXT (the text)
                CONT
                    * CONT
                    * CONT_ID
                    * CONT_LFDNR
                GTXT IDs
                    * pk
                    * tk
                PLot Coordinates
                    * pXYLB: (X,Y): Left,Bottom

        Raises:
            XmError
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

    def _vSWVT(self):
        """One row per Timeseries.

        Returns:
            columns
                SWVT
                    * NAME
                    * BESCHREIBUNG
                    * INTPOL
                    * ZEITOPTION
                SERIES
                    * W: 1st Value
                    * W_min
                    * W_max
                SWVT ID
                    * pk

        Raises:
            XmError
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

    def _vRSLW(self,vSWVT=None):
        """One row per RSLW.

        Args:
            * vSWVT 

        Returns:
            columns
                RSLW
                    * KA
                    * BESCHREIBUNG
                    * INDWBG, INDWNO

                RSLW BZ
                    * INDSLW, SLWKON

                CONT
                    * CONT
                    * ID

                SWVT
                    * SWVT
                    * BESCHREIBUNG_SWVT
                    * INTPOL
                    * ZEITOPTION

                    SERIES
                        * W: 1st Value
                        * W_min
                        * W_max

                RSLW IDs
                    * pk
                    * tk

        Raises:
            XmError
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

    def _vQVAR(self):
        """One row per Timeseries.

        Returns:
            columns
                QVAR
                    * NAME
                    * BESCHREIBUNG
                    * INTPOL
                    * ZEITOPTION
                SERIES
                    * QM: 1st Value
                    * QM_min
                    * QM_max
                QVAR ID
                    * pk

        Raises:
            XmError
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

    def _vPVAR(self):
        """One row per Timeseries.

        Returns:
            columns
                PVAR
                    * NAME
                    * BESCHREIBUNG
                    * INTPOL
                    * ZEITOPTION
                SERIES
                    * PH: 1st Value
                    * PH_min
                    * PH_max
                QVAR ID
                    * pk

        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vPVAR = None
            vPVAR=pd.merge(self.dataFrames['PVAR'],self.dataFrames['PVAR_ROWT'],left_on='pk',right_on='fk')
            vPVAR['ZEIT']=pd.to_numeric(vPVAR['ZEIT']) 
            vPVAR['PH']=pd.to_numeric(vPVAR['PH']) 
            vPVAR['ZEIT_RANG']=vPVAR.groupby(['pk_x'])['ZEIT'].rank(ascending=True)
            #
            vPVAR_gPH=vPVAR.groupby(['pk_x'], as_index=False).agg({'PH':[np.min,np.max]})
            vPVAR_gPH.columns= [tup[0]+tup[1] for tup in zip(vPVAR_gPH.columns.get_level_values(0),vPVAR_gPH.columns.get_level_values(1))]
            vPVAR_gPH.rename(columns={'PHamin':'PH_min','PHamax':'PH_max'},inplace=True)
            #
            vPVAR=pd.merge(vPVAR,vPVAR_gPH,left_on='pk_x',right_on='pk_x')
            #
            vPVAR=vPVAR[vPVAR['ZEIT_RANG']==1]
            #
            vPVAR=vPVAR[['NAME','BESCHREIBUNG','INTPOL','ZEITOPTION','PH','PH_min','PH_max','pk_x']]
            #
            vPVAR.rename(columns={'pk_x':'pk'},inplace=True)
                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise XmError(logStrFinal)               
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vPVAR
   
            
    def _vVKNO(self):
        """One row per Blocknode.

        Returns:
            columns
                * NAME 
                * CONT (Blockname)
                * fkKNOT
                * fkCONT   

        Raises:
            XmError
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

    def _vKNOT(self,vVKNO=None,vQVAR=None,vPVAR=None,vLFKT=None):
        """One row per Node (KNOT).

        Args:
            * vVKNO
            * vQVAR
            * vPVAR
            * vLFKT

        Returns:
            rows
                sequence: Xml

            columns
                KNOT
                    * NAME
                    * BESCHREIBUNG
                    * IDREFERENZ
                CONT
                    * CONT
                    * CONT_ID
                    * CONT_LFDNR
                    * CONT_VKNO (name of the Block/Container for NAME is a Blocknode)
                KNOT 
                    * KTYP
                    * LFAKT (Umrechnungsfaktor) 
                    * QM_EIN
                QVAR
                    * QVAR_NAME
                    * QM, QM_min, QM_max 
                LFKT
                    * LFKT_NAME
                    * LF, LF_min, LF_max 
                PVAR
                    * PVAR_NAME
                    * PH, PH_min, PH_max 
                Zugehoerigkeit
                    * PZON_NAME
                    * FSTF_NAME,STOF_NAME,GMIX_NAME
                    * UTMP_NAME
                2L
                    * 2L_NAME
                    * 2L_KVR
                KNOT 
                    * KVR
                    * TE
                    * TM
                KNOT
                    * XKOR, YKOR, ZKOR
                KNOT IDs
                    * pk, tk
                KNOT: plot-Coordinates
                    * pXCor: X-pXCorZero
                    * pYCor: Y-pYCorZero
        
        Raises:
            XmError
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
                   ,'LFAKT','QM_EIN','fkQVAR','fkLFKT','fkPVAR'   
                   ,'fk2LKNOT','fkFQPS','fkFSTF','fkHYDR','fkPZON','fkUTMP'
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
                   ,'LFAKT','QM_EIN','fkLFKT','fkPVAR'       
                   ,'fk2LKNOT','fkFQPS','fkFSTF','fkHYDR','fkPZON','fkUTMP'
                   ,'QVAR_NAME'
                   ,'QM','QM_min','QM_max'     
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            vKNOT=pd.merge(vKNOT,vLFKT,left_on='fkLFKT',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'LFKT_NAME','pk_x':'pk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'fkPVAR'       
                   ,'fk2LKNOT','fkFQPS','fkFSTF','fkHYDR','fkPZON','fkUTMP'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]
          
            vKNOT=pd.merge(vKNOT,vPVAR,left_on='fkPVAR',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'PVAR_NAME','pk_x':'pk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'fk2LKNOT','fkFQPS','fkFSTF','fkHYDR','fkPZON','fkUTMP'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            vKNOT=pd.merge(vKNOT,self.dataFrames['PZON'],left_on='fkPZON',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','NAME_y':'PZON_NAME','pk_x':'pk','tk_x':'tk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'PZON_NAME'
                   #,'IDIMRA','PKMINRA','PKMAXRA'
                   ,'fk2LKNOT','fkFQPS','fkFSTF','fkHYDR','fkUTMP'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            vKNOT=pd.merge(vKNOT,self.dataFrames['FSTF'],left_on='fkFSTF',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','NAME_y':'FSTF_NAME','pk_x':'pk','tk_x':'tk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'PZON_NAME'
                   #,'IDIMRA','PKMINRA','PKMAXRA'
                   ,'FSTF_NAME'
                   ,'fk2LKNOT','fkFQPS','fkSTOF','fkGMIX','fkHYDR','fkUTMP'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            vKNOT=pd.merge(vKNOT,self.dataFrames['STOF'],left_on='fkSTOF',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','BESCHREIBUNG_x':'BESCHREIBUNG','NAME_y':'STOF_NAME','pk_x':'pk','tk_x':'tk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'PZON_NAME'
                   #,'IDIMRA','PKMINRA','PKMAXRA'
                   ,'FSTF_NAME','STOF_NAME'
                   ,'fk2LKNOT','fkFQPS','fkGMIX','fkHYDR','fkUTMP'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            gMix=self.dataFrames['GMIX']
            vKNOT=pd.merge(vKNOT,gMix[[col for col in gMix.columns.tolist() if col not in ['BESCHREIBUNG']]],left_on='fkGMIX',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','NAME_y':'GMIX_NAME','pk_x':'pk','tk_x':'tk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'PZON_NAME'
                   #,'IDIMRA','PKMINRA','PKMAXRA'
                   ,'FSTF_NAME','STOF_NAME','GMIX_NAME'
                   ,'fk2LKNOT','fkFQPS','fkHYDR','fkUTMP'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            vKNOT=pd.merge(vKNOT,self.dataFrames['UTMP'],left_on='fkUTMP',right_on='pk',how='left')
            vKNOT.rename(columns={'NAME_x':'NAME','NAME_y':'UTMP_NAME','pk_x':'pk','tk_x':'tk'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'PZON_NAME'
                   #,'IDIMRA','PKMINRA','PKMAXRA'
                   ,'FSTF_NAME','STOF_NAME','GMIX_NAME'
                   ,'UTMP_NAME'
                   ,'fk2LKNOT','fkFQPS','fkHYDR'
                   ,'KVR' 
                   ,'TE','TM' 
                   ,'XKOR','YKOR','ZKOR'
                   ,'pk','tk'
                ]]

            vKNOT=pd.merge(vKNOT,self.dataFrames['KNOT'],left_on='fk2LKNOT',right_on='pk',how='left',suffixes=('', '_y'))
            vKNOT.rename(columns={'NAME_y':'2L_NAME','KVR_y':'2L_KVR'},inplace=True)

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
                   ,'LFKT_NAME'
                   ,'LF','LF_min','LF_max'     
                   ,'PVAR_NAME'
                   ,'PH','PH_min','PH_max'     
                   ,'PZON_NAME'
                   #,'IDIMRA','PKMINRA','PKMAXRA'
                   ,'FSTF_NAME','STOF_NAME','GMIX_NAME'
                   ,'UTMP_NAME'
                   ,'2L_NAME','2L_KVR'
                   ,'fkFQPS','fkHYDR'
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

    def _vROHR(self,vKNOT=None):
        """One row per Pipe (ROHR).

        Args:
            vKNOT

        Returns:
            rows
                sequence: Xml

            columns
                ROHR
                    * BESCHREIBUNG
                    * IDREFERENZ
                ROHR
                    * BAUJAHR, HAL
                    * IPLANUNG, KENNUNG
                ROHR
                    * L, LZU, RAU, ZAUS, ZEIN, ZUML
                    * JLAMBS, LAMBDA0
                ROHR
                    * ASOLL, INDSCHALL
                ROHR FW                   
                    * NAME_i_2L
                    * NAME_k_2L
                    * KVR
                DTRO_ROWD
                    * AUSFALLZEIT, DA , DI , DN , KT , PN , REHABILITATION , REPARATUR , S , WSTEIG , WTIEFE
                LTGR
                    * LTGR_NAME, LTGR_BESCHREIBUNG , SICHTBARKEIT , VERLEGEART
                DTRO
                    * DTRO_NAME, DTRO_BESCHREIBUNG, E
                REF
                    * fkSTRASSE, fkSRAT
                ROHR IDs
                    * pk, tk
                ROHR BZ
                    * ITRENN
                    * LECKSTART, LECKEND, LECKMENGE, LECKORT, LECKSTATUS
                Rest
                    * QSVB, ZVLIMPTNZ, KANTENZV
                CONT
                    * CONT
                    * CONT_ID
                    * CONT_LFDNR
                vKNOT
                    KI
                        * NAME_i
                        * KVR_i, TM_i
                        * XKOR_i, YKOR_i, ZKOR_i
                    KK
                        * NAME_k
                        * KVR_k, TM_k
                        * XKOR_k, YKOR_k, ZKOR_k
                    
                    pXCor_i, pYCor_i
                    pXCor_k, pYCor_k
                PLOT
                    * pXCors, pYCors
                    * pWAYPXCors, pWAYPYCors        

        Raises:
            XmError                           
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

            vROHR.rename(columns={'GEOM_x':'GEOM'},inplace=True)         

            vROHR=pd.merge(vROHR,vROHR,left_on='fk2LROHR',right_on='pk',how='left',suffixes=('','_2L'))   

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
                    ,'NAME_i_2L'
                    ,'NAME_k_2L'
                    ,'KVR'                  
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
                   # ...........
                   ,'GEOM'
                            ]]
            
            # WAYP ###
            vROHR['WAYP']=[list() for dummy in vROHR['pk']] # leere Liste von Wegpunkten
            for index,row in vROHR.iterrows():
                if pd.isnull(row.GEOM):                    
                    continue
                geomBytes=base64.b64decode(row.GEOM)
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
                    ,'NAME_i_2L'
                    ,'NAME_k_2L'
                    ,'KVR'
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

    def _vFWVB(self,vKNOT=None,vLFKT=None,vWBLZ=None):
        """One row per DistrictHeatingHousestation (FWVB).

        Args:
            * vKNOT 
            * vLFKT
            * wWBLZ

        Returns:
            columns
                FWVB
                    * BESCHREIBUNG
                    * IDREFERENZ
                    * W0
                    * LFK
                    * W0LFK
                    * TVL0, TRS0
                vLFKT
                    * LFKT
                    * W, W_min, W_max
                FWVB contd.
                    * INDTR, TRSK
                    * VTYP 
                    * DPHAUS, IMBG, IRFV
                FWVB IDs
                    * pk, tk  
                vKNOT
                    Ki
                        * NAME_i
                        * KVR_i, TM_i
                        * XKOR_i, YKOR_i, ZKOR_i
                        * pXCor_i, pYCor_i
                    Kk
                        * NAME_k
                        * KVR_k, TM_i
                        * XKOR_k, YKOR_k, ZKOR_i
                        * pXCor_k, pYCor_i                   
                vCONT
                    * CONT 
                    * CONT_ID
                    * CONT_LFDNR 
                vWBLZ
                    * ['BLZ1','BLZ2',...]
                        list of the WBLZ-Names of the FWVB in alphabetical Order;  
                        empty list, if FWVB is not a WBLZ-Member      
        Raises:
            XmError
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
            vFWVB['DPHAUS']=pd.to_numeric(vFWVB['DPHAUS']) 
            vFWVB['IMBG']=pd.to_numeric(vFWVB['IMBG']) 
            vFWVB['IRFV']=pd.to_numeric(vFWVB['IRFV']) 
            
            #
            vFWVB=pd.merge(vFWVB,vLFKT,left_on='fkLFKT',right_on='pk',how='left')
            #logger.debug("{:s} nach vLFKT: {!s:s}".format(logStr,(vFWVB)))
            #
            vFWVB['W0LFK']  = vFWVB.apply(lambda row: row.LFK    * row.W0   , axis=1)
            vFWVB['W']      = vFWVB.apply(lambda row: row.LF     * row.W0LFK, axis=1)
            vFWVB['W_min']  = vFWVB.apply(lambda row: row.LF_min * row.W0LFK, axis=1)
            vFWVB['W_max']  = vFWVB.apply(lambda row: row.LF_max * row.W0LFK, axis=1)
            #
            vFWVB=vFWVB[[
                    'BESCHREIBUNG_x','IDREFERENZ'
                   ,'W0','LFK','W0LFK','TVL0' ,'TRS0'
                   ,'W','W_min','W_max'
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' 
                   ,'DPHAUS','IMBG' ,'IRFV'
                   ,'pk_x','tk'
                   ,'NAME','BESCHREIBUNG_y'
                   ,'fkKI','fkKK'
                   ,'fkCONT'
                 ]]
            vFWVB.rename(columns={'BESCHREIBUNG_x':'BESCHREIBUNG','pk_x':'pk','NAME':'LFKT'},inplace=True)       
            vFWVB=vFWVB[[
                    #FWVB
                    'BESCHREIBUNG','IDREFERENZ'
                   ,'W0','LFK','W0LFK','TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' 
                   ,'DPHAUS', 'IMBG' ,'IRFV'
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
                   ,'W0','LFK','W0LFK','TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' 
                   ,'DPHAUS','IMBG' ,'IRFV'
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
                   ,'W0','LFK','W0LFK','TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' 
                   ,'DPHAUS','IMBG' ,'IRFV'
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
                   ,'W0','LFK','W0LFK','TVL0' ,'TRS0'
                    #LFKT
                   ,'LFKT'
                   ,'W','W_min','W_max'
                    #FWVB contd.
                   ,'INDTR' ,'TRSK'
                   ,'VTYP' 
                   ,'DPHAUS','IMBG' ,'IRFV'
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


    def _vVBEL(self,vKNOT=None,edges=vVBEL_edges,edgesD=vVBEL_edgesD,indices=['OBJTYPE','pk'],mIdxNames=['OBJTYPE','OBJID']):
        """One row per Edge.

        Args:
            * vKNOT: df 
            * edges: list of strs
            * edgesD: list of strs
            * indices: list of columns which shall be used as MIndex; the columns will be droped; the columns must be delivered by _vVBEL_XXXX
            * mIdxNames: list of names for the indices above

        Returns:
            Edge-df
            returned Edge-df is None if an exception occurs 

            rows:
                * sequence edges: edges
                * sequence within edges: Xml

            Mindices:
                * OBJTYPE: str: 'ROHR','VENT',... [default a MIndex not a column]
                * OBJID [default a MIndex not a column]      
              
            columns:                
                * LAYR
                * L in m (0 if edge <> ROHR)
                * D in mm (NaN if no Diameter could be determined)

            columns:                
                * see _vVBEL_XXXX
                                 
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:    
            # construct 
            vVBEL=None
            vVBEL_UnionList=[]

            for VBEL in edges:
                if VBEL in self.dataFrames:
                    vXXXX=self._vVBEL_XXXX(vKNOT=vKNOT,OBJTYPE=VBEL)
                    if vXXXX is None:
                        pass
                    else:
                        vVBEL_UnionList.append(vXXXX)
            vVBEL=pd.concat(vVBEL_UnionList)

            # MIndices
            arrays=[]
            for col in indices:
                arrays.append(vVBEL[col].tolist())
            tuples = list(zip(*(arrays)))
            index = pd.MultiIndex.from_tuples(tuples,names=mIdxNames)
            vVBEL.drop(indices,axis=1,inplace=True)   
            vVBEL=pd.DataFrame(vVBEL.values,index=index,columns=vVBEL.columns)

            # Gruppenzugeh. ergaenzen
            vVBEL['LAYR']=[list() for dummy in vVBEL['tk']]
            dfLayr=self.dataFrames['vLAYR']
            if not dfLayr.empty:
                dfLayr=dfLayr.rename(columns={'OBJTYPE':'TYPE'})         
                dfLayr=pd.merge(
                    vVBEL
                   ,dfLayr
                   ,how='inner' # nur die VBEL die eine Gruppenzugehoerigkeit haben
                   ,left_index=True 
                   ,right_on=['TYPE','OBJID']               
                   ,suffixes=('', '_y'))[['NAME','TYPE','OBJID','nrObjInGroup','nrObjtypeInGroup']]
                dfLayr=dfLayr[dfLayr.nrObjInGroup <= 1] # pro VBEL und Gruppe nur 1 Zeile

                for index, row in vVBEL.merge(dfLayr.sort_values(by=['NAME','OBJID']),how='left',left_index=True ,right_on=['TYPE','OBJID'],suffixes=('', '_y')).iterrows():                
                    if pd.isnull(row.NAME):
                        continue
                    row.LAYR.append(row.NAME)

            # L ergaenzen
            Rohr=self.dataFrames['ROHR']
            VbelL=vVBEL.join(Rohr.set_index('pk').rename_axis('OBJID', axis='index'),rsuffix='_y')[['L']]            
            vVBEL['L']=VbelL['L'].fillna(0)            

            # D ergaenzen
            # Spalte erzeugen ... 
            vRohr=self.dataFrames['vROHR']
            VbelD=vVBEL.join(vRohr.set_index('pk').rename_axis('OBJID', axis='index'),rsuffix='_y')[['DI']]
            vVBEL['D']=VbelD['DI'] # ... mit ROHR

            # ueber alle ausser ROHR
            for eIdx,edge in enumerate(edges):
                if edge == 'ROHR':
                    continue
                edgeDCol=edgesD[eIdx]
                if edgeDCol=='':
                    continue     
                if edge not in self.dataFrames:
                    continue
                Edge=self.dataFrames[edge]                      
                if edgeDCol not in Edge.columns.tolist():
                    continue
                edgeD=vVBEL.join(Edge.set_index('pk').rename_axis('OBJID', axis='index'),rsuffix='_y',how='inner')[[edgeDCol]]
                vVBEL.loc[[edge],'D']=edgeD.loc[[edge],:].values


            # fehlende Spaltenwerte zuweisen
            #Vent=self.dataFrames['VENT']
            #VentD=vVBEL.join(Vent.set_index('pk'),rsuffix='_y',how='inner')[['DN']]
            #vVBEL.loc[['VENT'],'D']=VentD.loc[['VENT'],:].values

            # Finish
            vVBEL.sort_index(level=0,inplace=True)

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal)    
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return vVBEL     
        
    def _vVBEL_XXXX(self,vKNOT=None,OBJTYPE=None):
        """One row per Edge.

        Args:
            * vKNOT: df 
            * OBJTYPE: str ('ROHR','VENT',...)
                self.dataFrames[OBJTYPE] is used to build with vKNOT the returned Edge-df 

        Returns:
            Edge-df
            None is returned if an exception occurs

            columns:
                * OBJTYPE: str: ROHR,VENT,...
                
                * BESCHREIBUNG
                * IDREFERENZ
                * pk      
                * tk
                
                * NAME_i
                * CONT_i
                * CONT_VKNO_i
                * Z_i
                * pk_i
                * NAME_k
                * CONT_k
                * CONT_VKNO_k
                * Z_k
                * pk_k
                                 
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:        
            
            #'KVR','PZON_NAME', 'FSTF_NAME', 'STOF_NAME', 'GMIX_NAME','UTMP_NAME'



            vXXXX=None

            vXXXX=pd.merge(self.dataFrames[OBJTYPE],vKNOT,left_on='fkKI',right_on='pk',suffixes=('','_i'))            
            vXXXX=vXXXX[['fkKK','BESCHREIBUNG','IDREFERENZ','pk','tk','NAME','CONT','CONT_VKNO','pk_i','ZKOR']]
            vXXXX.rename(columns={'NAME':'NAME_i','CONT':'CONT_i','CONT_VKNO':'CONT_VKNO_i','ZKOR':'Z_i'},inplace=True)

            vXXXX=pd.merge(vXXXX,vKNOT,left_on='fkKK',right_on='pk',suffixes=('','_k'))
            vXXXX=vXXXX[['BESCHREIBUNG','IDREFERENZ','pk','tk','NAME_i','CONT_i','CONT_VKNO_i','Z_i','pk_i','NAME','CONT','CONT_VKNO','pk_k','ZKOR']]
            vXXXX.rename(columns={'NAME':'NAME_k','CONT':'CONT_k','CONT_VKNO':'CONT_VKNO_k','ZKOR':'Z_k'},inplace=True)
            
            vXXXX=vXXXX.assign(OBJTYPE=lambda x: OBJTYPE)
            vXXXX=vXXXX[['OBJTYPE','BESCHREIBUNG','IDREFERENZ','pk','tk','NAME_i','CONT_i','CONT_VKNO_i','Z_i','pk_i','NAME_k','CONT_k','CONT_VKNO_k','Z_k','pk_k']]

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal) 
            vXXXX=None
         
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return vXXXX     

    def MxSync(self,mx=None):
        """Mx: Sir3sID Update in Mx-Object. Xm: NEW 1st Call: vNRCV_Mx1: vNRCV with MX1-Information. Some Xm-Views with MX2-Information (mx2Idx).

        Args:
            mx: Mx-Object
                * If no Mx-Object is given the Mx-Object is constructed.       
                * Notes:

                    * Xm holds no Mx-Object.
                    * Method MxSync can be considered as a Sync between Xm and a particular Mx-Object.
                    * The Sync has to be done before the 1st MxAdd-Call with the Mx-Object.

                    * The Sync-Result is persisted if dfs were read from H5:
                    
                        * xm.ToH5() is called if xm.h5Read is True. 
                        * mx.ToH5() is called (from __Mx1_Sir3sIDUpd) if Sir3sID-Updates occured and mx.h5Read is True. 

        Raises:
            XmError

        >>> xm=xms['LocalHeatingNetwork']
        >>> xm.MxSync()
        """
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if isinstance(mx,Mx.Mx):
                pass
            else:
                (wDir,modelDir,modelName,mx1File)=self.getWDirModelDirModelName()                      
                mx=Mx.Mx(mx1File=mx1File)


            self.__Mx1_Sir3sIDUpd(mx) # Sir3sID

            self.__Mx1_vNRCV(mx) # vNRCV

            self.__Mx2_vKNOT(mx) # vKNOT
            self.__Mx2_vROHR(mx) # vROHR
            self.__Mx2_vFWVB(mx) # vFWVB           
            self.__Mx2_vVBEL(mx) # vVBEL

            if self.h5Read:
                self.ToH5()
                                                       
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                       
            logger.error(logStrFinal) 
                     
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    def __Mx1_Sir3sIDUpd(self,mx):
        """Update NAME1,2 and Sir3sID in mx.mx1Df and mx.df.

        Args:
            mx: Mx-Object

        Notes:
            The following Channels are updated:
                * KNOT
                * WBLZ
                * RXXXX
                * all Channels in vVBEL

            mx.ToH5() is called if Sir3sID-Updates occured and mx.h5Read is True. 

        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:
            # Sir3sID split
            df=mx.mx1Df['Sir3sID'].str.extract(Mx.reSir3sIDcompiled)               
            # Sir3sID reconstruction
            df=df.assign(Sir3sID=lambda df: df.OBJTYPE+'~'+df.NAME1+'~'+df.NAME2+'~'+df.OBJTYPE_PK+'~'+df.ATTRTYPE)

            nOfSir3sIDsUpdated=0
            
            # KNOT
            nOfSir3sIDsUpdated=nOfSir3sIDsUpdated+self.__Mx1_Sir3sIDUpd_ObjTypeNode(mx=mx
                                                                 ,dfUpd=df[ (df['NAME1'].str.len()==0) & (df['OBJTYPE'].isin(['KNOT'])) ]
                                                                 ,dfNAME1=self.dataFrames['KNOT']
                                                                 ,NAME1Col='NAME')
            # WBLZ
            if 'WBLZ' in self.dataFrames.keys():
                nOfSir3sIDsUpdated=nOfSir3sIDsUpdated+self.__Mx1_Sir3sIDUpd_ObjTypeNode(mx=mx
                                                                     ,dfUpd=df[ (df['NAME1'].str.len()==0) & (df['OBJTYPE'].isin(['WBLZ'])) ]
                                                                     ,dfNAME1=self.dataFrames['WBLZ']
                                                                     ,NAME1Col='NAME')
            # RXXXX
            for ObjType in ['RSLW','RMES','RFKT','RTOT','RVGL','RHYS','RINT','RPT1','RADD','RMUL','RDIV','RMIN','RPID','RVGL']:       
                if ObjType in self.dataFrames:
                    nOfSir3sIDsUpdated=nOfSir3sIDsUpdated+self.__Mx1_Sir3sIDUpd_ObjTypeNode(mx=mx
                                                                     ,dfUpd=df[ (df['NAME1'].str.len()==0) & (df['OBJTYPE'].isin([ObjType])) ]
                                                                     ,dfNAME1=self.dataFrames[ObjType]
                                                                     ,NAME1Col='KA')
            
            # VBEL (NAME1,2 und Sir3sID)
            dfUpd=df[ (df['NAME1'].str.len()==0) & (df['OBJTYPE'].isin(vVBEL_edges)) ]
            #logger.debug("{0:s}dfUpd vor Merge: {1:s}.".format(logStr,str(dfUpd)))

            # fuer Col-Auswahl nach Merge
            dfUpdCols=dfUpd.columns.tolist()
            dfUpdCols.append('NAME_i')
            dfUpdCols.append('NAME_k')

            # right (hat die zu mergenden Keys als Index)
            dfVBEL=self.dataFrames['vVBEL']
            
            #logger.debug("{0:s}dfUpd vor Merge: {1:s}.".format(logStr,str(dfUpd)))
            #logger.debug("{0:s}dfVBEL vor Merge: {1:s}.".format(logStr,str(dfVBEL)))
            #logger.debug("{0:s}dfVBEL index vor Merge: {1:s}.".format(logStr,str(dfVBEL.index)))

            dfUpd=pd.merge(
                dfUpd
               ,dfVBEL
               ,how='left' # expected: no NaNs/Nones in Merge-Result
               ,left_on=['OBJTYPE','OBJTYPE_PK'] # diese left Key-Spalten ... 
               ,right_index=True # ... matchen mit den right Indices 
               ,suffixes=('', '_y'))[dfUpdCols]

            #logger.debug("{0:s}dfUpd nach Merge: {1:s}.".format(logStr,str(dfUpd)))

            # calculate Sir3sID Update 
            dfUpd=dfUpd.assign(Sir3sIDUpd=lambda df: df.OBJTYPE+'~'+df.NAME_i+'~'+df.NAME_k+'~'+df.OBJTYPE_PK+'~'+df.ATTRTYPE)
            # iterate over all Sir3sIDs to be updated
            for index, row in dfUpd.iterrows():
                nOfSir3sIDsUpdated=nOfSir3sIDsUpdated+1
                # set Sir3sID to Sir3sIDUpd in mx.mx1Df
                mx.mx1Df.loc[lambda df: df.Sir3sID==row['Sir3sID'],'Sir3sID']=row['Sir3sIDUpd']
                logger.debug("{0:s}Changing Sir3sID {1:s} to {2:s}.".format(logStr,row['Sir3sID'],row['Sir3sIDUpd']))    
                # set NAME1 to NAME_i in mx.mx1Df
                mx.mx1Df.loc[lambda df: df.Sir3sID==row['Sir3sIDUpd'],'NAME1']=row['NAME_i']
                logger.debug("{0:s}Changing NAME1 (now:{1:s}) to {2:s}.".format(logStr,row['NAME1'],row['NAME_i']))    
                # set NAME2 to NAME_k in mx.mx1Df
                mx.mx1Df.loc[lambda df: df.Sir3sID==row['Sir3sIDUpd'],'NAME2']=row['NAME_k']
                logger.debug("{0:s}Changing NAME2 (now:{1:s}) to {2:s}.".format(logStr,row['NAME2'],row['NAME_k']))    
                if isinstance(mx.df,pd.core.frame.DataFrame):  
                    # rename the corresponding col in mx.df
                    mx.df.rename(columns={row['Sir3sID']:row['Sir3sIDUpd']},inplace=True)  
                    logger.debug("{0:s}Changing Col {1:s} to {2:s}.".format(logStr,row['Sir3sID'],row['Sir3sIDUpd']))

            if nOfSir3sIDsUpdated>0 and mx.h5Read:
                mx.ToH5()
                           
        except Exception as e:            
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e)) 
            logger.error(logStrFinal) 
                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    def __Mx1_Sir3sIDUpd_ObjTypeNode(self,mx=None,dfUpd=None,dfNAME1=None,NAME1Col='NAME'):
        """Update Sir3sID and NAME1 in mx.mx1Df and mx.df for Channels in dfUpd.

        Args:
            mx: Mx-Object
            dfUpd: df with OBJTYPE,NAME1,NAME2,OBJTYPE_PK,ATTRTYPE,Sir3sID to be updated
            dfNAME1: df with NAME1-Information
            NAME1Col: col in dfNAME1 with NAME1-Information

        Returns:
            nOfSir3sIDsUpdated

        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:
            nOfSir3sIDsUpdated=0

            dfUpdCols=dfUpd.columns.tolist()
            dfUpdCols.append(NAME1Col)
            dfUpd=pd.merge(
                dfUpd
               ,dfNAME1
               ,how='inner'
               ,left_on='OBJTYPE_PK'
               ,right_on='pk'
               ,suffixes=('', '_y'))[dfUpdCols]
            dfUpd.rename(columns={NAME1Col:'NAME1Col'},inplace=True)
            # calculate Sir3sID Update 
            dfUpd=dfUpd.assign(Sir3sIDUpd=lambda df: df.OBJTYPE+'~'+df.NAME1Col+'~'+df.NAME2+'~'+df.OBJTYPE_PK+'~'+df.ATTRTYPE)

            # iterate over all Sir3sIDs to be updated
            for index, row in dfUpd.iterrows():
                nOfSir3sIDsUpdated=nOfSir3sIDsUpdated+1
                # set Sir3sID to Sir3sIDUpd in mx.mx1Df
                mx.mx1Df.loc[lambda df: df.Sir3sID==row['Sir3sID'],'Sir3sID']=row['Sir3sIDUpd']
                logger.debug("{0:s}Changing Sir3sID {1:s} to {2:s}.".format(logStr,row['Sir3sID'],row['Sir3sIDUpd']))    
                # set NAME1 to NAME1Col in mx.mx1Df
                mx.mx1Df.loc[lambda df: df.Sir3sID==row['Sir3sIDUpd'],'NAME1']=row['NAME1Col']
                logger.debug("{0:s}Changing NAME1 (now:{1:s}) to {2:s}.".format(logStr,row['NAME1'],row['NAME1Col']))    
                if isinstance(mx.df,pd.core.frame.DataFrame):  
                    # rename the corresponding col in mx.df
                    mx.df.rename(columns={row['Sir3sID']:row['Sir3sIDUpd']},inplace=True)  
                    logger.debug("{0:s}Changing Col {1:s} to {2:s}.".format(logStr,row['Sir3sID'],row['Sir3sIDUpd']))
                           
        except Exception as e:            
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e)) 
            logger.error(logStrFinal) 
                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return nOfSir3sIDsUpdated

    def __Mx1_vNRCV(self,mx):
        """vNRCV_Mx1 (vNRCV with Mx1-Information).

        Args:
            mx: Mx-Object

        self.dataFrames['vNRCV_Mx1']
                index
                    * reindex
                FILTERed
                    * existing MX-Channels only
                    * cRefLfdNr: 1st references only 
                SORTed
                    * Sir3sID 
                columns NEW
                    * Sir3sID
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             

            vNRCV_Mx1=None

            #if 'vNRCV' in self.dataFrames.keys():

            vNRCV=self.dataFrames['vNRCV']
            
            if 'fkOBJTYPE' in vNRCV.columns.tolist():

                vNRCV_Mx1=vNRCV.merge(mx.mx1Df,left_on='fkOBJTYPE',right_on='OBJTYPE_PK',suffixes=['_NR','_MX1'])

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

    def __Mx2_vROHR(self,mx):
        """Mx2-Information into vROHR.
        
        Args:
            mx: Mx-Object

        self.dataFrames['vROHR']
                columns NEW
                    * mx2NoPts
                    * mx2Idx
                   
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            xksROHRMx=mx.mx2Df[
            (mx.mx2Df['ObjType'].str.match('ROHR'))
            &
            ~(mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
            ]['Data'].iloc[0] # Liste der IDs in Mx2

            xkTypeMx=mx.mx2Df[
            (mx.mx2Df['ObjType'].str.match('ROHR'))
            &
            ~(mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
            ]['AttrType'].iloc[0]

            vROHR=self.dataFrames['vROHR']
            xksROHRXm=vROHR[xkTypeMx.strip()] # Liste der IDs in vROHR

            mxXkRohrIdx=[xksROHRMx.index(xk) for xk in xksROHRXm] # zugeh. Liste der mx2Idx in vROHR

            ##vROHR['mx2Idx']=pd.Series(mxXkRohrIdx)
            
            nOfPtsROHRMx=mx.mx2Df[
            (mx.mx2Df['ObjType'].str.match('ROHR'))
            &
            (mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
            ]['Data'].iloc[0]  # Liste der NOfPts in Mx2

            nOfPtsROHRMxXk=[nOfPtsROHRMx[mx2Idx] for mx2Idx in mxXkRohrIdx] # zugeh. Liste der NOfPts in vROHR

            
            vROHR['mx2NofPts']=pd.Series(nOfPtsROHRMxXk)#nOfPtsROHRMx)
            vROHR['mx2Idx']=pd.Series(mxXkRohrIdx) # Abschluss mit mx2Idx
            ##
            ####vROHR['mx2Idx']=pd.Series(mxXkRohrIdx)
                                                                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal) 
                          
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      
            self.dataFrames['vROHR']=vROHR     

    def __Mx2_vFWVB(self,mx):
        """Mx2-Information into vFWVB.
        
        Args:
            mx: Mx-Object

        self.dataFrames['vFWVB']
                columns NEW
                    * mx2Idx
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vFWVB=self.dataFrames['vFWVB']

            xksFWVBMx=mx.mx2Df[
            (mx.mx2Df['ObjType'].str.match('FWVB'))
            ]['Data'].iloc[0]

            xkTypeMx=mx.mx2Df[
            (mx.mx2Df['ObjType'].str.match('FWVB'))
            ]['AttrType'].iloc[0]

            xksFWVBXm=vFWVB[xkTypeMx.strip()]
            mxXkFwvbIdx=[xksFWVBMx.index(xk) for xk in xksFWVBXm]

            vFWVB['mx2Idx']=pd.Series(mxXkFwvbIdx)
                                                                               
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.debug(logStrFinal) 
                          
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      
            self.dataFrames['vFWVB']=vFWVB     
            
    def __Mx2_vKNOT(self,mx):
        """Mx2-Information into vKNOT.
        
        Args:
            mx: Mx-Object

        self.dataFrames['vKNOT']
                columns NEW
                    * mx2Idx
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            xksKNOTMx=mx.mx2Df[(mx.mx2Df['ObjType'].str.match('KNOT'))]['Data'].iloc[0]
            xkTypeMx=mx.mx2Df[(mx.mx2Df['ObjType'].str.match('KNOT'))]['AttrType'].iloc[0]
            vKNOT=self.dataFrames['vKNOT']
            xksKNOTXm=vKNOT[xkTypeMx.strip()]
            mxXkKNOTIdx=[xksKNOTMx.index(xk) for xk in xksKNOTXm]
            vKNOT['mx2Idx']=pd.Series(mxXkKNOTIdx)
                                                  
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal) 
                          
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      
            self.dataFrames['vKNOT']=vKNOT     

    def __Mx2_vVBEL(self,mx,edges=vVBEL_edges):
        """Mx2-Information into vVBEL.
        
        Args:
            mx: Mx-Object

        self.dataFrames['vVBEL']:
                columns NEW
                    * mx2Idx                   

                    * Notes:                        
                        * for all edges mx2Idx is taken from mx.mx2Df
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 

            # new col mx2Idx in dfVBEL
            dfVBEL=self.dataFrames['vVBEL']
            dfVBEL=dfVBEL.assign(mx2Idx=lambda x: -1)
            dfVBEL['mx2Idx'].astype('int64',copy=False)

            # all edges
            for edge in [edge for edge in edges]:
                 try:                     
                     xksEDGEMx=mx.mx2Df[
                                (mx.mx2Df['ObjType'].str.match(edge))
                         ]['Data'].iloc[0]

                     xkTypeMx=mx.mx2Df[
                                (mx.mx2Df['ObjType'].str.match(edge))
                         ]['AttrType'].iloc[0]

                     if xkTypeMx == 'tk':
                        xksEDGEXm=dfVBEL.loc[(edge,),xkTypeMx]
                     else:
                        # pk
                        xksEDGEXm=dfVBEL.loc[(edge,),:].index

                     logger.debug("{0:s}{1:s}: xkTypeMx: {2:s}".format(logStr,edge,xkTypeMx))   
                     logger.debug("{0:s}{1:s}: xksEDGEXm: {2:s}".format(logStr,edge,str(xksEDGEXm.values.tolist())))   
                     logger.debug("{0:s}{1:s}: xksEDGEMx: {2:s}".format(logStr,edge,str(xksEDGEMx)))      
                                      
                     mxXkEDGEIdx=[xksEDGEMx.index(tk) for tk in xksEDGEXm]
                     
                     dfVBEL.loc[(edge,),'mx2Idx']=mxXkEDGEIdx

                 except Exception as e:
                    logStrEdge="{:s}Exception: Line: {:d}: {!s:s}: {:s}: mx2Idx for {:s} failed. mx2Idx = -1.".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e),edge)            
                    logger.debug(logStrEdge) 
                                                                                                               
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
            logger.error(logStrFinal) 
                          
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            self.dataFrames['vVBEL']=dfVBEL

    def MxAdd(self,mx=None,timeReq=None):
        """Add MX-Resultcolumns to some Xm-Views.  NEW 1st Call: vROHRVecResults: vNRCV with MX1-Information.

        Args:
            mx: Mx-Object
                * If no Mx-Object is given the Mx-Object is constructed.    
                
            timeReq:
                * TIMESTAMP 
                * if None 1st TIME in Mx is used

        Views with MX2-Results added:            
            * in the Xm-Views below col mx2Idx must exist 
            * mx2Idx is considered to be the last of the Model-cols
            * right from mx2Idx Result-cols are added if not already existing
            * already existing Result-cols are overwritten
            * mx2Idx-Views:
                * vKNOT (KNOT...) 
                * vROHR (ROHR...) - only Non-VEC-Channel-Results are added
                * vFWVB (FWVB...)
                * vVBEL (KNOT..._i and KNOT..._k and Q)

            * NEW 1st Call:
            * vROHRVecResults: VEC-Channel-Results for Pipe-Interior-Pts (IPts):
                * pk
                * mx2Idx
                * IptIdx: S,0,...,E - Interior Point Index; S=Start EdgeDefNode, E=End EdgeDefNode, 0=1st Ipt in EdgeDefDirection
                * one column per VEC-Channel

            * vAGSN
                * from vVBEL: KNOT..._i and KNOT..._k and Q
                * from vROHRVecResults: vecResults
                * Topology:
                    * nextNODE                   
                    * IptIdx                    
                * Geometry:
                    * dx                       
                    * x                        
                    * xVbel      
                    * Z (the corresponding Z_i, Z_k and ZVEC are droped)
                * Results:
                    * Q: from Q before and QMVEC for PIPEs; in Schnittrichtung; QMVEC is droped
                    * from KNOT...#_i, KNOT...#_k and #VEC:
                        * #1
                        * #2
                        * ...
                        the correspondig 3 columns (2 #KNOT, 1 #VEC) are droped
        Notes:
            * The Add-Result is persisted if df were read from H5:        
                        * xm.ToH5() is called if xm.h5Read is True.           

        Raises:
            XmError

        >>> xm=xms['LocalHeatingNetwork']
        >>> xm.MxSync()
        >>> xm.MxAdd()
        >>> print(xm._getvXXXXAsOneString(vXXXX='vROHRVecResults',filterColList=['mx2Idx','IptIdx','ROHR~*~*~*~SVEC'],index=True))
            mx2Idx IptIdx  ROHR~*~*~*~SVEC
        0        0      S         0.000000
        1        0      E        88.019997
        2        1      S         0.000000
        3        1      E       405.959991
        4        2      S         0.000000
        5        2      E        83.550003
        6        3      S         0.000000
        7        3      E        88.019997
        8        5      S         0.000000
        9        5      E       195.529999
        10       7      S         0.000000
        11       7      E       109.769997
        12       8      S         0.000000
        13       8      E        76.400002
        14       9      S         0.000000
        15       9      E        83.550003
        16      10      S         0.000000
        17      10      E       164.910004
        18      11      S         0.000000
        19      11      E       195.529999
        20      12      S         0.000000
        21      12      E       405.959991
        22      13      S         0.000000
        23      13      E       164.910004
        24      14      S         0.000000
        25      14      E       109.769997
        26      15      S         0.000000
        27      15      E        76.400002
        28       4      S         0.000000
        29       4      E        73.419998
        30       6      S         0.000000
        31       6      E        68.599998
        >>> xm=xms['GPipes']
        >>> xm.MxSync()
        >>> xm.MxAdd()
        >>> xm.MxAdd() # test 2nd Call
        >>> vAGSN=xm.dataFrames['vAGSN']
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR']
        >>> xm.dataFrames['schnitt']=schnitt
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',filterColList=['OBJTYPE','NAME_i','NAME_k','IptIdx','nextNODE','x','PH'],index=True))
            OBJTYPE NAME_i NAME_k IptIdx nextNODE         x       PH
        79     VENT     GL     G1      S       G1       0.0       40
        80     VENT     GL     G1      E       G1       0.0   39.974
        81     ROHR     G1    GKS      S      GKS       0.0   39.974
        82     ROHR     G1    GKS      0      GKS    5000.0  39.4534
        83     ROHR     G1    GKS      1      GKS   10000.0  38.9255
        84     ROHR     G1    GKS      2      GKS   15000.0  38.3903
        85     ROHR     G1    GKS      3      GKS   20000.0  37.8474
        86     ROHR     G1    GKS      4      GKS   25000.0  37.2964
        87     ROHR     G1    GKS      5      GKS   30000.0   36.737
        88     ROHR     G1    GKS      6      GKS   35000.0  36.1689
        89     ROHR     G1    GKS      7      GKS   40000.0  35.5915
        90     ROHR     G1    GKS      8      GKS   45000.0  35.0044
        91     ROHR     G1    GKS      9      GKS   50000.0  34.4071
        92     ROHR     G1    GKS     10      GKS   55000.0  33.7991
        93     ROHR     G1    GKS     11      GKS   60000.0  33.1799
        94     ROHR     G1    GKS     12      GKS   65000.0  32.5486
        95     ROHR     G1    GKS     13      GKS   70000.0  31.9048
        96     ROHR     G1    GKS     14      GKS   75000.0  31.2475
        97     ROHR     G1    GKS     15      GKS   80000.0  30.5759
        98     ROHR     G1    GKS     16      GKS   85000.0  29.8891
        99     ROHR     G1    GKS     17      GKS   90000.0  29.1859
        100    ROHR     G1    GKS     18      GKS   95000.0  28.4653
        101    ROHR     G1    GKS     19      GKS  100000.0  27.7258
        102    ROHR     G1    GKS     20      GKS  105000.0  26.9659
        103    ROHR     G1    GKS     21      GKS  110000.0  26.1838
        104    ROHR     G1    GKS     22      GKS  115000.0  25.3776
        105    ROHR     G1    GKS     23      GKS  120000.0  24.5449
        106    ROHR     G1    GKS     24      GKS  125000.0  23.6829
        107    ROHR     G1    GKS     25      GKS  130000.0  22.7884
        108    ROHR     G1    GKS     26      GKS  135000.0  21.8575
        109    ROHR     G1    GKS     27      GKS  140000.0  20.8855
        110    ROHR     G1    GKS     28      GKS  145000.0  19.8664
        111    ROHR     G1    GKS     29      GKS  150000.0  18.7928
        112    ROHR     G1    GKS     30      GKS  155000.0  17.6551
        113    ROHR     G1    GKS      E      GKS  160000.0  16.4405
        114    VENT    GKS    GKD      S      GKD  160000.0  16.4404
        115    VENT    GKS    GKD      E      GKD  160000.0  16.3758
        116    ROHR    GKD     G3      S       G3  160000.0  16.3758
        117    ROHR    GKD     G3      0       G3  165000.0  15.0583
        118    ROHR    GKD     G3      E       G3  170000.0  13.6122
        119    ROHR     G4     G3      E       G4  170000.0  13.6122
        120    ROHR     G4     G3      0       G4  175000.0  11.9873
        121    ROHR     G4     G3      S       G4  180000.0  10.1062
        122    VENT     G4     GR      S       GR  180000.0  10.1062
        123    VENT     G4     GR      E       GR  180000.0       10
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            if isinstance(mx,Mx.Mx):
                pass

            else:
                (wDir,modelDir,modelName,mx1File)=self.getWDirModelDirModelName()                      
                mx=Mx.Mx(mx1File=mx1File)
            
            if 'vNRCV_Mx1' not in self.dataFrames:
                self.MxSync(mx=mx)

            if timeReq==None:
                timeReq=mx.df.index[0]

            mxVecsFileData=mx.getMxsVecsFileData(timesReq=[timeReq])[0] # 1 Zeit, alle Spalten, in den Zellen stehen die Vektoren als Tuple 

            vKNOT=self.__MxAddForOneDf(dfTarget=self.dataFrames['vKNOT']
                                      ,dfSource=mxVecsFileData.filter(regex='^KNOT'),testStr='KNOT')
            vROHR=self.dataFrames['vROHR']
            vROHR=self.__MxAddForOneDf(dfTarget=vROHR
                                      ,dfSource=mxVecsFileData.filter(regex='^ROHR').filter(regex='^(?!.*VEC)'),testStr='ROHR')

            vFWVB=self.dataFrames['vFWVB']
            if 'mx2Idx' in vFWVB.columns.tolist():
                vFWVB=self.__MxAddForOneDf(dfTarget=vFWVB #self.dataFrames['vFWVB']
                                          ,dfSource=mxVecsFileData.filter(regex='^FWVB'),testStr='FWVB')
           
            self.dataFrames['vKNOT']=vKNOT
            self.dataFrames['vROHR']=vROHR
            self.dataFrames['vFWVB']=vFWVB

            #vVBEL - Knoten
            vKNOT=self.dataFrames['vKNOT']
            vVBEL=self.dataFrames['vVBEL']

            vVBELCols=vVBEL.columns.tolist()
            mx2IdxColVBELIdx=vVBELCols.index('mx2Idx')
            vKNOTCols=vKNOT.columns.tolist()
            mx2IdxColKNOTIdx=vKNOTCols.index('mx2Idx')

            knotResultCols=vKNOTCols[mx2IdxColKNOTIdx+1:]
            vbelModelCols=vVBELCols[:mx2IdxColVBELIdx+1]

            knotResultColsi=[col+'_i' for col in knotResultCols]
            knotResultColsk=[col+'_k' for col in knotResultCols]

            knotResultColsiRenameDct={}
            knotResultColskRenameDct={}
            for idx,col in enumerate(knotResultCols):
                knotResultColsiRenameDct[col]=knotResultColsi[idx]
                knotResultColskRenameDct[col]=knotResultColsk[idx]

            df=pd.merge(vVBEL.loc[:,vbelModelCols],vKNOT,left_on='pk_i',right_on='pk',suffixes=['','_i']).filter(items=vbelModelCols+knotResultCols)
            df.rename(columns=knotResultColsiRenameDct,inplace=True)
            
            df=pd.merge(df,vKNOT,left_on='pk_k',right_on='pk',suffixes=['','_k']).filter(items=vbelModelCols+knotResultColsi+knotResultCols)
            df.rename(columns=knotResultColskRenameDct,inplace=True)

            # merge again for correct alignment
            df=pd.merge(vVBEL.loc[:,vbelModelCols],df.filter(items=['tk','pk_i','pk_k']+knotResultColsi+knotResultColsk),on=['tk','pk_i','pk_k']).filter(items=vbelModelCols+knotResultColsi+knotResultColsk)
            dfResultColsOnly=df.filter(knotResultColsi+knotResultColsk)

            if dfResultColsOnly.columns.isin(vVBELCols).all():
                pass
            else:
                if not dfResultColsOnly.columns.isin(vVBELCols).any():
                    # no col to be added exist
                    for col in dfResultColsOnly:
                        vVBEL[col]=None
                else:
                    # only some cols to be added exist?!       
                    logStringFinal="{0:s}Some but - not all! - cols from dfResultColsOnly exist in dfTarget vVBEL: existing: {1:s} not existing: {2:s}".format(logStr
                                                    ,str(list(set(vVBELCols) & set(dfResultColsOnly)))
                                                    ,str(list(set(dfResultColsOnly) - set(vVBELCols)))
                                                    )             
                    logger.error(logStringFinal) 
                    raise XmError(logStringFinal)

            shapeLeft=vVBEL.loc[:,knotResultColsi+knotResultColsk].shape 
            shapeRight=dfResultColsOnly.shape
            if shapeLeft != shapeRight:
                logStringFinal="{0:s}Alignment Mismatch: shapeLeft vVBEL: {1:s} <> shapeRight df: {2:s}".format(logStr
                                                    ,str(shapeLeft)
                                                    ,str(shapeRight)
                                                    )
                logger.error(logStringFinal) 
                raise XmError(logStringFinal)

            vVBEL.loc[:,knotResultColsi+knotResultColsk]=dfResultColsOnly.values


            #vVBEL - Q
            vVBEL['Q']=None 

            for idx,vbel in enumerate(vVBEL_edges):
                try:
                    df=vVBEL.loc[vbel] 
                except KeyError:
                    continue # VBEL nicht in Modell 
    
                #DataFrame: 1 Zeit, Spalte(n), in den Zelle stehen die Werte als Tuple 
                if vbel != 'ROHR':
                    dfQ=mxVecsFileData.filter(regex='~'+vVBEL_edgesQ[idx]+'$').filter(regex='^'+vbel)
                else:
                    dfQ=mxVecsFileData.filter(regex='~'+vVBEL_edgesQ[idx]+'$').filter(regex='^'+vbel).filter(regex='^(?!.*VEC)')
                shape=dfQ.shape
    
                if shape[1]==0:
                    continue # Spalte nicht in MX2
                if shape[1]>1:
                    continue # mehr als matchende Spalte in MX2?!

                colName=dfQ.columns.tolist()[0]
                vVBEL=self.__MxAddForOneDf(dfTarget=vVBEL,dfSource=dfQ.rename(columns={colName:'Q'}),multiIndexKey=vbel,testStr='vVBEL_'+vbel)

                #logger.debug("{0:s}vVBEL Liste: {1:s}".format(logStr,str(vVBEL.columns.tolist())))  

            self.dataFrames['vVBEL']=vVBEL

            #VEC
            reExpNegLookAhead='(?P<ObjType>\S+)~(?P<Name_i>\S*)~(?P<Name_k>\S*)~(?!\d+)(?P<ObjId>[\*\d]*)~(?P<ChannelType>\S+)'
            dfSource=mxVecsFileData.filter(regex='(VEC$)').filter(regex='(^ROHR)').filter(regex=reExpNegLookAhead)
            dct={}
            for col in dfSource.columns.tolist():
                            #eine Spalte eines Frames liefert eine Series ...
                            #2004-09-22 08:30:00+00:00  (-8.509474754333496,...)
                            #Name: ROHR~*~*~*~QMAV
                            vecsFileDataOneCol=dfSource[col]
                                
                            #erster Wert (erste Zeile) der Series:
                            #Tuple:
                            #(-8.509474754333496,...)
                            vecsFileDataOneColResult=vecsFileDataOneCol[0]
    
                            #Series aus Tuple
                            vecsFileDataOneColResultSeries=pd.Series(vecsFileDataOneColResult)
                
                            #Series merken
                            dct[col]=vecsFileDataOneColResultSeries
               
            #DataFrame aus Dct aus Series
            vROHRVecResults=pd.DataFrame(dct)  
            
            colsToBeAdded=vROHRVecResults.columns.tolist()
            colsMaybeAlreadyAdded=mxVecsFileData.filter(regex='(VEC$)').filter(regex='(^ROHR)').filter(regex=reExpNegLookAhead).columns.tolist()
            #.filter(regex='^ROHR').filter(regex='^(?!.*VEC)')
            #.columns.tolist()
            colsInTarget=vROHR.columns.tolist()
            colsInTargetNet=list(set(colsInTarget)-set(colsToBeAdded)-set(colsMaybeAlreadyAdded))
            colsInTargetNet=[col for col in colsInTarget if col in colsInTargetNet] # preserve the original col-Sequence


            rVecMx2Idx=[] 
            IptIdx=[] 

            for row in vROHR.sort_values(['mx2Idx']).itertuples(): # Mx2-Records sind in Mx2-Reihenfolge und muessen auch so annotiert werden ...
                oneVecIdx=np.empty(row.mx2NofPts,dtype=int) 
                oneVecIdx.fill(row.mx2Idx)                
                rVecMx2Idx.extend(oneVecIdx)
    
                oneLfdNrIdx=['S']
                if row.mx2NofPts>2:                    
                    oneLfdNrIdx.extend(np.arange(row.mx2NofPts-2,dtype=int))
                oneLfdNrIdx.append('E')

                IptIdx.extend(oneLfdNrIdx)
            vROHRVecResults['mx2Idx']=rVecMx2Idx
            vROHRVecResults['IptIdx']=IptIdx  
            vROHRVecResults=vROHRVecResults[['mx2Idx']+['IptIdx']+colsToBeAdded]

            dfMerge=pd.merge(vROHR.filter(items=colsInTargetNet),vROHRVecResults,how='inner',left_on='mx2Idx',right_on='mx2Idx')        
            #logString="{0:s}The cols from dfMerge: {1:s}".format(logStr,str(dfMerge.columns.tolist()))
            #logger.debug(logString)
            vROHRVecResults=dfMerge[['pk']+['mx2Idx']+['IptIdx']+colsToBeAdded]

            self.dataFrames['vROHRVecResults']=vROHRVecResults

            #vAGSN
            vAGSN=self.dataFrames['vAGSN_raw']
            ##logString="{0:s}The shape from vAGSN {1:s}: The cols: {2:s}".format(logStr,str(vAGSN.shape),str(vAGSN.columns.tolist()))
            ##logger.debug(logString)
            ##logString="{0:s}vAGSN_raw: {1:s}".format(logStr,self._getvXXXXAsOneString(vXXXX='vAGSN_raw'))
            ##logger.debug(logString)
           
            vAGSN=pd.merge(
                    vAGSN
                   ,vVBEL
                   ,how='left' 
                   ,left_on=['OBJTYPE','OBJID']  
                   ,right_index=True ,suffixes=('', '_y'))
            vAGSN.rename(columns={'tk_y':'tk_VBEL'},inplace=True)

            ##self.dataFrames['dummy']=vAGSN
            ##logString="{0:s}vAGSN_merge: {1:s}".format(logStr,self._getvXXXXAsOneString(vXXXX='dummy'))
            ##logger.debug(logString)
           
            df=vAGSN[pd.isnull(vAGSN['tk_VBEL']) != True].copy()
            
            # mit S E verdoppeln 
            ik = {'ik_tmp': ['S', 'E']}
            dfIk = pd.DataFrame(data=ik)
            dfIk['key_tmp'] = 0
            df['key_tmp'] = 0
            df=pd.merge(df,dfIk,on='key_tmp',how='outer')

            # Vecs ergaenzen
            df=pd.merge(df,vROHRVecResults,how='left',left_on='OBJID',right_on='pk',suffixes=['','_tmp'])
            # ROHRE mit E loeschen
            df=df[(df.OBJTYPE != 'ROHR') | ((df.OBJTYPE == 'ROHR') & (df.ik_tmp=='S'))]
            df['IptIdx']=df.apply(lambda row: row.IptIdx if row.OBJTYPE=='ROHR' else row.ik_tmp,axis=1)

            if 'ROHR~*~*~*~SVEC' not in df.columns.tolist():
                df=vAGSN[pd.isnull(vAGSN['tk_VBEL']) != True].copy()
            else:
                # x
                df['dx']=df.groupby(['LFDNR','OBJID','Layer'])['ROHR~*~*~*~SVEC'].shift(0)-df.groupby(['LFDNR','OBJID','Layer'])['ROHR~*~*~*~SVEC'].shift(1)
                df['dx']=df.apply(lambda row: 0 if row.OBJTYPE=='ROHR' and  pd.isnull(row.dx) else row.dx,axis=1)
                df['dx']=df.apply(lambda row: 0 if row.OBJTYPE!='ROHR' and  pd.isnull(row.dx) and row.IptIdx=='S' else row.dx,axis=1)
                df['dx']=df.apply(lambda row: 0 if row.OBJTYPE!='ROHR' and  pd.isnull(row.dx) and row.IptIdx=='E' else row.dx,axis=1)
                df['x']=df.groupby(['LFDNR','Layer'])['dx'].cumsum()                

                tLnet=df.groupby(['LFDNR','Layer'])['dx'].sum()
                tLnet=tLnet.reset_index()
                tLnet.rename(columns={'dx':'tLnet_tmp'},inplace=True)
                df=pd.merge(df,tLnet,how='inner',on=['LFDNR','Layer'],suffixes=['','_tmp'])

                df['dx_tmp']=df.apply(lambda row: row.tLnet_tmp*0.01 if row.OBJTYPE!='ROHR' and row.IptIdx=='E' else row.dx,axis=1)

                df['xVbel']=df.groupby(['LFDNR','Layer'])['dx_tmp'].cumsum()

                # alle _tmp loeschen
                df=df.filter(items=[col for col in df.columns.tolist() if re.search('_tmp$',col) == None])

                # cols belegen
                kiCols=[col for col in df.columns.tolist() if re.search('^(?P<Pre>KNOT~\*~\*~\*~)(?P<Channel>[a-zA-Z_]+)(?P<Post>_i$)',col) != None]          
                if 'KNOT~*~*~*~QM_i' in kiCols:
                    kiCols.remove('KNOT~*~*~*~QM_i')
                mos=[re.search('^(?P<Pre>KNOT~\*~\*~\*~)(?P<Channel>[a-zA-Z_]+)(?P<Post>_i$)',col) for col in kiCols]
                cols=[mo.group('Pre')+mo.group('Channel') for mo in mos]
                kkCols=[col+'_k' for col in cols]
                vecCols=['ROHR~*~*~*~'+mo.group('Channel')+'VEC' for mo in mos]
                kiColsEff=[]
                for kiCol,kkCol,col,vecCol in zip(kiCols,kkCols,cols,vecCols):
                    if vecCol in df.columns.tolist():
                        kiColsEff.append(kiCol)
                ###kiColsEff
                mos=[re.search('^(?P<Pre>KNOT~\*~\*~\*~)(?P<Channel>[a-zA-Z_]+)(?P<Post>_i$)',col) for col in kiColsEff]
                cols=[mo.group('Pre')+mo.group('Channel') for mo in mos]
                channels=[mo.group('Channel') for mo in mos]
                kkCols=[col+'_k' for col in cols]
                vecCols=['ROHR~*~*~*~'+mo.group('Channel')+'VEC' for mo in mos]
                if 'ROHR~*~*~*~ZVEC' in df.columns.tolist():
                    kiColsEff.append('Z_i')
                    kkCols.append('Z_k')
                    channels.append('Z')
                    vecCols.append('ROHR~*~*~*~ZVEC')
                for channel in channels:
                    df[channel]=None

                for nr in df['LFDNR'].unique():
                    for ly in df[df['LFDNR']==nr]['Layer'].unique():
                        dfLy=df[(df['LFDNR']==nr) & (df['Layer']==ly)]
        
                        logger.debug("{0:s}Schnitt: {1:s} Layer: {2:s}".format(logStr
                                                                               ,str(dfLy['NAME'].iloc[0])
                                                                               ,str(dfLy['Layer'].iloc[0])
                                                                              )) 
                        grouped = dfLy.groupby(['OBJTYPE','OBJID'])
                        for name, group in grouped:
                            OBJTYPE,OBJID=name
                            si=df.loc[group.index[0],:]
                            sk=df.loc[group.index[-1],:]
                            logger.debug("{0:s}OBJTYPE: {1:s} OBJID: {2:s} NAME_i: {3:s} NAME_k: {4:s}".format(logStr
                                                                               ,OBJTYPE
                                                                               ,OBJID
                                                                               ,str(si['NAME_i'])
                                                                               ,str(si['NAME_k'])
                                                                              ))             
            
                            for kiCol,kkCol,col,vecCol in zip(kiColsEff,kkCols,channels,vecCols):                                            
                                 try:
                                    if OBJTYPE == 'ROHR':
                                        df.loc[group.index,col]=df.loc[group.index,vecCol].values
                                    else:
                                        df.loc[group.index[0],col]=si[kiCol]
                                        df.loc[group.index[-1],col]=sk[kkCol]
                   
                                 except:
                                    pass

                for kiCol,kkCol,vecCol in zip(kiColsEff,kkCols,vecCols):
                    df.drop([kiCol], axis=1, inplace=True)
                    df.drop([kkCol], axis=1, inplace=True)
                    df.drop([vecCol], axis=1, inplace=True)

                # rows ggf. invertieren        
                for nr in df['LFDNR'].unique():                
                    for ly in df[df['LFDNR']==nr]['Layer'].unique():                    
                        dfLy=df[(df['LFDNR']==nr) & (df['Layer']==ly)]
                        grouped = dfLy.groupby(['OBJTYPE','OBJID'])
                        for name, group in grouped:
                            s=df.loc[group.index[0],:]                       
                            if s.NAME_k == s.nextNODE:    
                                f=1.
                            else:    
                                f=-1.
                                df.loc[group.index,:]=group[::-1].values     
                                # x zurueck
                                df.loc[group.index,'x']=df.loc[group.index,'x'][::-1].values
                                df.loc[group.index,'xVbel']=df.loc[group.index,'xVbel'][::-1].values
                        
                            if s.OBJTYPE == 'ROHR':
                                try:
                                    df.loc[group.index,'Q']=df.loc[group.index,'ROHR~*~*~*~QMVEC'].values
                                except:
                                    pass
                        
                            #Q ggf. drehen
                            df.loc[group.index,'Q']*=f       

                if 'ROHR~*~*~*~QMVEC' in df.columns.tolist():
                    df.drop(['ROHR~*~*~*~QMVEC'], axis=1, inplace=True)

            self.dataFrames['vAGSN']=df

            if self.h5Read:
                self.ToH5()          
                                                  
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                       
            logger.error(logStrFinal) 
                     
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  

    def __MxAddForOneDf(self,dfTarget=None,dfSource=None,multiIndexKey=None,testStr='testStr'):
        """Add MX2-Resultdata from dfSource as cols to dfTarget.

        Args:
            dfTarget: df with col mx2Idx
            dfSource: df with mx2Idx-corresponding index and cols (containing MX2-Resultdata) to be added
            multiIndexKey: value for 1st Index if dfTarget is Multiindexed - i.e. 'XXXX'

        Notes:
            * all cols from dfSource are added at the end of dfTarget in dfSource-sequence
            * the cols can already exist in dfTarget
            * if so, _all cols must already exist ...
            * ... the dfTarget-sequence should but must be not necessary the dfSource-sequence 
            
        Returns:
            dfTarget
            
        Raises:
            XmError
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            # maybe the cols are already added in previous calls: otherwise: construct them ... 
            colsToBeAdded=dfSource.columns.tolist()
            colsInTarget=dfTarget.columns.tolist()
            colsInTargetNet=list(set(colsInTarget)-set(colsToBeAdded))
            colsInTargetNet=[col for col in colsInTarget if col in colsInTargetNet] # preserve the original col-Sequence

            if dfSource.columns.isin(colsInTarget).all():
                pass
            else:
                if not dfSource.columns.isin(colsInTarget).any():
                    # no col to be added exista
                    logString="{0:s}None of the cols from dfSource exist in dfTarget: {1:s}".format(logStr,str(colsToBeAdded))
                    logger.debug(logString)
                    for col in colsToBeAdded:
                        dfTarget[col]=None                                           
                else:
                    # only some cols to be added exists?!       
                    logStringFinal="{0:s}Some but - not all! - cols from dfSource exist in dfTarget: existing: {1:s} not existing: {2:s}".format(logStr
                                                    ,str(list(set(colsInTarget) & set(colsToBeAdded)))
                                                    ,str(list(set(colsToBeAdded) - set(colsInTarget)))
                                                    )             
                    logger.error(logStringFinal) 
                    raise XmError(logStringFinal)

            dct={}          
            for col in colsToBeAdded:
                #eine Spalte eines Frames liefert eine Series ...
                #2004-09-22 08:30:00+00:00  (-8.509474754333496,...)
                #Name: ROHR~*~*~*~QMAV
                vecsFileDataOneCol=dfSource[col]
                
                
                #erster Wert der Series:
                #Tuple:
                #(-8.509474754333496,...)
                vecsFileDataOneColResult=vecsFileDataOneCol[0]
    
                #Series aus Tuple
                vecsFileDataOneColResultSeries=pd.Series(vecsFileDataOneColResult)
                
                #Series merken
                dct[col]=vecsFileDataOneColResultSeries
            #DataFrame aus Dct aus Series
            dfMx2Idx=pd.DataFrame(dct)            
                     
            if multiIndexKey != None:
                ###dfMx2Idx.to_excel(testStr+'_dfMx2Idx'+'_multiIndexKey'+'.xlsx')
                ###dfTarget.loc[[multiIndexKey]].filter(items=colsInTargetNet).to_excel(testStr+'_dfTarget'+'_multiIndexKey'+'.xlsx')
                dfMerge=pd.merge(dfTarget.loc[[multiIndexKey]].filter(items=colsInTargetNet),dfMx2Idx,how='inner',left_on='mx2Idx',right_index=True)            
                #logger.debug("{0:s}dfMerge: {1:s}".format(logStr,str(dfMerge)))
                ###dfMerge.filter(items=['mx2Idx','L','NAME_i','NAME_k','Q']).to_excel(testStr+'_dfMerge'+'_multiIndexKey'+'.xlsx')
                # check alignment ...
                shapeLeft=dfTarget.loc[[multiIndexKey],colsToBeAdded].shape
                shapeRight=dfMerge[colsToBeAdded].shape
                if shapeLeft != shapeRight:
                    logStringFinal="{0:s}Alignment Mismatch: shapeLeft dfTarget: {1:s} <> shapeRight dfMerge: {2:s}".format(logStr
                                                    ,str(shapeLeft)
                                                    ,str(shapeRight)
                                                    )
                    logger.error(logStringFinal) 
                    raise XmError(logStringFinal)
                dfTarget.loc[[multiIndexKey],colsToBeAdded]=dfMerge.filter(colsToBeAdded).values    

            else:
                dfMerge=pd.merge(dfTarget.filter(items=colsInTargetNet),dfMx2Idx,how='inner',left_on='mx2Idx',right_index=True)        
                ###logger.debug("{0:s}dfMerge: {1:s}".format(logStr,str(dfMerge)))
                ###dfMerge.to_excel(testStr+'_dfMerge'+'.xlsx')
                # check alignment ...
                shapeLeft=dfTarget.loc[:,colsToBeAdded].shape
                shapeRight=dfMerge[colsToBeAdded].shape
                if shapeLeft != shapeRight:
                    logStringFinal="{0:s}Alignment Mismatch: shapeLeft dfTarget: {1:s} <> shapeRight dfMerge: {2:s}".format(logStr
                                                    ,str(shapeLeft)
                                                    ,str(shapeRight)
                                                    )
                    logger.error(logStringFinal) 
                    raise XmError(logStringFinal)
                else:
                    dfTarget.loc[:,colsToBeAdded]=dfMerge[colsToBeAdded].values
                ###if testStr=='ROHR':                    
                    ###dfTarget.filter(items=['L','KVR','NAME_i','NAME_k','ROHR~*~*~*~QMAV']).to_excel(testStr+'_dfTarget'+'_multiIndexKey'+'.xlsx')
                ###logger.debug("{0:s}dfTarget: {1:s}".format(logStr,str(dfTarget)))
                   
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))                       
            logger.error(logStrFinal) 
                     
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
            return dfTarget

def setUpFct(dto):
        """
        """

        logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:      
            testDir=dto.globs['testDir']
            dotResolution=dto.globs['dotResolution']
            h5File=os.path.join(os.path.join(path,testDir),'OneLPipe.h5')       
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
        group.add_argument("-v","--verbose", help="Debug Messages On: -v (default): logging.DEBUG", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off: -q: logging.ERROR", action="store_true",default=False)        
                                 
        parser.add_argument("-m","--moduleTest", help="execute the Module's Doctest On/Off: -m 1 (default)", action="store",default='1')      
        parser.add_argument("-s","--singleTest", help="execute single Doctest: -s Xm: Doctest names matching Xm are executed", action="append",default=[])        

        parser.add_argument('--testDir',type=str,default='testdata',help="value for global 'testDir' i.e. testdata")     
        
        args = parser.parse_args()

        if args.verbose:  # default         
            logger.setLevel(logging.DEBUG)  
        if args.quiet:    # Debug Messages are turned Off
            logger.setLevel(logging.ERROR)  
            args.verbose=False
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        if args.moduleTest == '1':
            dtFinder=doctest.DocTestFinder(recurse=False,verbose=args.verbose) # recurse = False findet nur den Modultest
            suite=doctest.DocTestSuite(test_finder=dtFinder #,setUp=setUpFct
                                   ,globs={'testDir':args.testDir                                          
                                           })   
            unittest.TextTestRunner().run(suite)
        
        xms={}   
        modelFiles={}
        if len(args.singleTest)>0:
            for testModel in ['OneLPipe','LocalHeatingNetwork','GPipes']:
                h5File=os.path.join(os.path.join('.',args.testDir),testModel+'.h5')
                if os.path.exists(h5File):                        
                    os.remove(h5File)
                xmlFile=os.path.join(os.path.join('.',args.testDir),testModel+'.XML')
                modelFiles[testModel]=xmlFile
                xm=Xm(xmlFile=xmlFile)
                xms[testModel]=xm

            dtFinder=doctest.DocTestFinder(verbose=args.verbose)
            dtRunner=doctest.DocTestRunner(verbose=args.verbose) 
            dTests=dtFinder.find(Xm,globs={'testDir':args.testDir                                       
                                           ,'xms':xms
                                           ,'ms':modelFiles}) 
            for test in dTests:
                for expr in args.singleTest:
                    if re.search(expr,test.name) != None:                    
                        logger.debug("{0:s}{1:s}: {2:s} ...".format(logStr,'Running Test: ',test.name)) 
                        dtRunner.run(test)
                        break

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


