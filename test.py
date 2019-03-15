"""
XXX

"""

import warnings # 3.6
#...\Anaconda3\lib\site-packages\h5py\__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
#   from ._conv import register_converters as _register_converters
#...\PT3S\Mx.py:1: FutureWarning: pandas.tslib is deprecated and will be removed in a future version.
#   You can access Timestamp as pandas.Timestamp
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import sys

import logging
logger = logging.getLogger('PT3S')  

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
import re

if __name__ == "__main__":
    """
    XXX
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
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
                                      
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
        parser.add_argument("-s","--singleTest", help="execute single Doctest: -s Xm: Doctest names matching Xm are executed", action="append",default=[])        

        args = parser.parse_args()

        if args.verbose:  # default         
            logger.setLevel(logging.DEBUG)  
        if args.quiet:    # Debug Messages are turned Off
            logger.setLevel(logging.ERROR)  
            args.verbose=False
                                            
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'testDir: ',args.testDir)) 

        if args.dotResolution == 'NONE':
            args.dotResolution=''

        try:
            from PT3S import Mx, Xm, Rm
        except ImportError:
            logger.debug("{0:s}{1:s}".format("test: from PT3S import Mx, Xm, Rm: ImportError: ","trying import Mx, Xm, Rm ..."))  
            import Mx, Xm, Rm

        if args.moduleTest == '1':
            # as unittests
            logger.info("{0:s}{1:s}{2:s}".format(logStr,'Start unittests (by DocTestSuite...). testDir: ',args.testDir)) 

            dtFinder=doctest.DocTestFinder(recurse=False,verbose=args.verbose) # recurse = False findet nur den Modultest


            suite=doctest.DocTestSuite(Mx,test_finder=dtFinder #,setUp=setUpFct
                                   ,globs={'testDir':args.testDir
                                           ,'dotResolution':args.dotResolution
                                           })   
            unittest.TextTestRunner().run(suite)

            suite=doctest.DocTestSuite(Xm,test_finder=dtFinder #,setUp=setUpFct
                                   ,globs={'testDir':args.testDir
                                           ,'dotResolution':args.dotResolution
                                           })   
            unittest.TextTestRunner().run(suite)

            suite=doctest.DocTestSuite(Rm,test_finder=dtFinder #,setUp=setUpFct
                                   ,globs={'testDir':args.testDir
                                           ,'dotResolution':args.dotResolution
                                           })   
            unittest.TextTestRunner().run(suite)
                      
            # as doctests
            logger.info("{0:s}{1:s}{2:s}".format(logStr,'Start doctests. testDir: ',args.testDir)) 

            dtRunner=doctest.DocTestRunner(verbose=False) 

            dTests=dtFinder.find(Mx,globs={'testDir':args.testDir,'dotResolution':args.dotResolution}) 
            dtRunner.run(dTests[0])

            dTests=dtFinder.find(Xm,globs={'testDir':args.testDir,'dotResolution':args.dotResolution})
            dtRunner.run(dTests[0])

            dTests=dtFinder.find(Rm,globs={'testDir':args.testDir,'dotResolution':args.dotResolution}) 
            dtRunner.run(dTests[0])

        if len(args.singleTest)>0:
            testModels=['OneLPipe','LocalHeatingNetwork','GPipes']
            mxs={} 
            for testModel in testModels:
                mx1File=os.path.join('.',os.path.join(args.testDir,'WD'+testModel+'\B1\V0\BZ1\M-1-0-1'+args.dotResolution+'.MX1')) 
                mx=Mx.Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)                                
                mxs[testModel]=mx

            xms={}   
            for testModel in testModels:
                h5File=os.path.join(os.path.join('.',args.testDir),testModel+'.h5')
                if os.path.exists(h5File):                        
                    os.remove(h5File)
                xmlFile=os.path.join(os.path.join('.',args.testDir),testModel+'.XML')
                xm=Xm.Xm(xmlFile=xmlFile)
                xms[testModel]=xm

            dtFinder=doctest.DocTestFinder(verbose=args.verbose)
            dtRunner=doctest.DocTestRunner(verbose=args.verbose) 
            dTests=dtFinder.find(Mx,globs={'testDir':args.testDir
                                          ,'dotResolution':args.dotResolution
                                           ,'mxs':mxs
                                           ,'xms':xms}) 
            dTests.extend(dtFinder.find(Xm,globs={'testDir':args.testDir
                                          ,'dotResolution':args.dotResolution
                                           ,'mxs':mxs
                                           ,'xms':xms})) 

            for test in dTests:
                for expr in args.singleTest:
                    if re.search(expr,test.name) != None:                    
                        logger.debug("{0:s}{1:s}: {2:s} ...".format(logStr,'Running Test: ',test.name)) 
                        dtRunner.run(test)
                        break

            for testModel in testModels:                                           
                mx=mxs[testModel]

                if os.path.exists(mx.h5File):                        
                   os.remove(mx.h5File)
                metadataFile=mx.h5File+'.metadata'
                if os.path.exists(metadataFile):                        
                   os.remove(metadataFile)
                if os.path.exists(mx.mxsZipFile):                        
                   os.remove(mx.mxsZipFile)
                mxsDumpFile=mx.mxsFile+'.dump'
                if os.path.exists(mxsDumpFile):                        
                   os.remove(mxsDumpFile)
                if os.path.exists(mx.h5FileVecs):                        
                   os.remove(mx.h5FileVecs)
        
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

