Releases
========

Welcome to the Releases page! Here, you can keep up with the additions and fixes that come with new releases.

90.14.51.0.dev1
---------------

- **Fix**: Publication is done via pyproject.toml
- Releases 90.14.47.0.dev1 to 90.14.50.0.dev1 are not useable due to issues that arose concerning the change of the deployment process.
- Latest functional changes from 90.14.47.0.dev1 are now working

90.14.47.0.dev1
---------------

**Changed**: 

- Publication is done via pyproject.toml instead of setup.py from this version on
- setup.py Repo/Documentation Link changed to GitHub-Team Account
- V3_ROHR col MAV: changed from abs. STAT av. Flow kg/s to STAT av. Flow kg/
- Example 8

**New**: 

- V3_VBEL has new col: M: STAT Flow kg/s
- dxAndMxHelperFcts.readDxAndMx() has new param SirCalcExePath to specify SirCalc.exe used for calculations with maxRecords<0

90.14.46.0.dev1
---------------

**New**: 

- V3_KNOT has new cols: T (Temperature in °C) and M (ext. Flow in kg/s)
- V3_ROHR has new cols: MAV (av. Flow in kg/s) and LAMBDA

**Fix**:

- m.GSig: nx.shortest_path(m.GSig,node): paths with RUES transitions were not found because ...
- ... because in mx.dx.dataFrames['V3_RVBEL'] edges with RUES as source node were not replaced by the RUES source node 
- Dx.py ln 1592: logger.debug(f"dfVBEL before edge loop:\n{df}") => logger.debug(f"dfVBEL before edge loop:\n{dfVBEL}")
- m.GSig: concatenation of transition symbols (of RUES) resulted in GSig not being constructed
- readDxAndMx: mxsVecsResults2MxDf: Mix of OBJTYPEs (i.e. KNOT and ROHR) was not implemented 
- _gdfs: empty gdf_ROHR was not checked

90.14.45.0.dev1
---------------

**Fix**:

- Importing issue of ncd.py fixed

90.14.44.0.dev1
---------------

**New**: 

- Documentation and Repository page both included as links in setup.py

- V3_KNOT has new col srcvector for source spectrum (Quellspektrum)
 
- ncd.plot_src_spectrum() function for plotting source spectrum as a network color diagram with ncd.mix_colors() and ncd.convert_to_hex() as helper functions

**Fix**:

- Mx.reSir3sID: blank in node name (in dst node name of edges) is now handled correct

90.14.43.0.dev1
---------------

**Fix**:

- V3_AGSNVEC: Changes from 90.14.42.0.dev1 dont cause issues with _end, _min, _max columns anymore

- self.dfAGSN = dxDecodeObjsData.Agsn(self.dx) in dxAndMxHelperFcts put in try/except to prevent reading stop in case of an issue with the called function. Proper fix of this function still to be done.

90.14.42.0.dev1
---------------

**New**: 

- V3_AGSNVEC: additional cols _n_1,2,3,... derived from mxsVecsResults2MxDfVecAggs=[idxt1,idxt2,idxt3,...,-1]; _1,_2,_3,... corresponds to sorted([idxt1,idxt2,idxt3,...])

90.14.41.0.dev1
---------------

**Fix**:

- 'QM'-Error fixed: tuple col index like ('STAT', 'QM', Timestamp('2023-02-12 23:00:00'), Timestamp('2023-02-12 23:00:00')) might be interpreted as multiindex depending on local versions of python and pandas. To fix this, tuple converted to string.

**Changed:**

dxAndMxHelperFcts.dxWithMx._G: refactoring as function; documentation


90.14.40.0.dev1
---------------

Reupload of 90.14.39.0.dev1 due to higher required setuptools version (compatibility with PEP 625)

90.14.39.0.dev1
---------------

**Changed:**

- Packages necessary for Examples but not for PT3S itself are from now on not included in PT3S releases but instead installed in each Example. In setup.py these packages are commented away. Same applies for packages necessary for documentaion generation. Their installion is described in Section For Developers.

- Example1
    - 'selenium'
    - 'Pillow'
- Example2
    - 'ipywidgets'
    - 'bokeh'
    - 'ipython'
- Example3    
- Example4
    - 'cykhash'
    - 'pyrobuf'
    - 'pyrosm'
    - 'osmnx'
    - 'msvc-runtime'
- Example5
    - 'ipython'
- Example6
    - 'ipython'
    - 'yfiles_jupyter_graphs'
- Documentation Generation
    - 'nbsphinx'
    - 'sphinx_copybutton'
    - 'sphinx-rtd-theme'

90.14.38.0.dev1
---------------

**Changend:**

- pyrosm, cykhash, pyrobuf deleted as install_requires (pyrosm issue)

90.14.37.0.dev1
---------------

**New:**

- cykhash, pyrobuf as install_requires

90.14.36.0.dev1
---------------

**New:**

- pyrosm, osmnx, msvc-runtime as install_requires

**Changed:**

- V3_AGSNVEC: new cols: ..._end, ..._min, ..._max
- Example 3
- Docstrings of readDxAndMx and others

90.14.35.0.dev1
---------------

**New:**

- Example 6:
    - This example demonstrates how the NetworkX-Graph created by PT3S can be used with yFiles.

90.14.34.0.dev1
---------------

**Fix:**

- install_requires:
    - Remove pyrosm 

90.14.33.0.dev1
---------------

**New:**

- install_requires:
    - pyrosm included for Example4

- ncd.py:
    - new Network Color Diagram module (ncd.py) to replace pNFD.py
    - pNcd_pipes(), pNcd_nodes(): functions to create ncd with customized pipes and nodes

90.14.32.0.dev1
---------------
    
**New:**
    
- dxWithMx:
    - SirCalcXmlFile: SirCalc's Xml-File of the model
    - SirCalcExeFile: SirCalc Executable used to (re-)calculate the model 
    
- dxAndMxHelperFcts.processMxVectorResults(mx,dx,mxsVecsResults2MxDf,mxsVecsResults2MxDfVecAggs)

- Example5 data

90.14.31.0.dev1
---------------

**Changed:**
  
- Dx:
    - update: dfUpd: now optional cols: attribValue, xk, xkValue
    
**New:**
    
- Dx:
    - importFromSIR3S: import data from an other SIR 3S Model

90.14.30.0.dev1
---------------

**Fix:**

- dxDecodeObjsData.Agsn: unnecessary exceptions when there is no data
- dxAndMxHelperFcts.dxWithMx._V3_AGSN: unnecessary exceptions when there is no data
- readDxAndMx: gdfs not available in case of no result data


**Changed:**

- dxWithMx:
    - setLayerContentTo: to Dx
    - dfLAYR: to Dx
    
- Dx:
    - setLayerContentTo: from dxWithMx
    - dfLAYR: from dxWithMx

**New:**
    
- Dx:
    - insert

90.14.29.0.dev1
---------------

**Fix:**

- Example 3: typing error: m.V3_AGSNVec ==> m.V3_AGSNVEC

**New:**

- SdfCsv: from PT3S import sdfCsv: mSdfCsv=sdfCsv.SdfCsv(csvFile): mSdfCsv: Wrapper for a model defined by a SDF-CSV-File

90.14.28.0.dev1
---------------

**Fix:**

- V3_AGSNVEC: Sections with starting pipe with interior points: incorrect x-values ​​in starting pipe

90.14.27.0.dev1
---------------

**Fix:**

- ROT 240801

90.14.26.0.dev1
---------------

**Fix:**

- Example 2 tested
- Example 3 finished
- Example 1,2,3 tested
- Doc-Process reviewed

90.14.25.0.dev1
---------------

**New:**

- readDxAndMx:
    - maxRecords=-1: Use maxRecords=-1 to (re-)calculate the model by SirCalc.

**Fix:**

- Mx:
    - False (non existing) Exception propagation in case of Mx-Read-Failures.

**Changed:**

- Dx:
    - Logging clear out
    
- Mx:
    - Logging clear out
    

90.14.24.0.dev1
---------------

**New:**

- DistrictHeating db3+Mx included in package for Example3

90.14.23.0.dev1
---------------
**Fix:**

- readMx:
    Logging: _Done added

- Selenium as install req

- Examples: XML and Mx1 File included with content, all other result files blank


90.14.22.0.dev1
---------------

90.14.21.0.dev1
---------------
**New:**

- readMx:
    Reads SIR 3S results and returns a Mx object.
    
    Args:
        - rootdire (str): Path to root directory of the Model. The results are read into a Mx object via the mx files.
        - logPathOutputFct (fct, optional, default=os.path.relpath): logPathOutputFct(fileName) is used for logoutput of filenames unless explicitly stated otherwise in the logoutput
    Returns:
        - Results: Mx object:
            - mx.df: pandas-Df ('time curve data') from from SIR 3S' MXS file(s)
            - mx.dfVecAggs: pandas-Df ('vector data') from SIR 3S' MXS file(s)

90.14.20.0.dev1
---------------
- readDxAndMx:
    **Fix:**
        - m is constructed (instead of reading m-pickle) if SIR 3S' dbFile is newer than m-pickle; in previous releases m-pickle was read even if dbFile is newer
    **New:**
        - INFO: if SIR 3S' dbFile is newer than SIR 3S' mxFile; in this case the results are maybe dated or (worse) incompatible to the model 

90.14.19.0.dev1
---------------
**New:**

- SIR 3S db3 and mx files used in Examples are now included in the package.

90.14.18.0.dev1
---------------
- readDxAndMx:
    **New:**
        - mxsVecsResults2MxDfVecAggs: (list, optional, default=None): List of timesteps for SIR 3S' Vector-Results to be included in mx.dfVecAggs.
        - crs: (str, optional, default=None): (=coordinate reference system) Determines crs used in geopandas-Dfs (Possible value:'EPSG:25832'). If None, crs will be read from the dbFile.
- dxWithMx:
    **New:**
        - geopandas-Dfs: gdf_KNOT, gdf_ROHR, gdf_FWVB
        - setLayerContentTo

90.14.17.0.dev1
---------------
- readDxAndMx:
    **New:**
        - preventPklDump: True now forces SIR 3S sources to be read because pickles are deleted if existing before timecheck pickles vs. SIR 3S sources is performed.
        - dxWithMx (readDxAndMx): V3_FWVB: new columns: QM, TI, TK
- Dx:
    **Update:**
        - returns now rowsAffectedTotal
