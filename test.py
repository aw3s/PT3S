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

if __name__ == "__main__":
    """
    XXX
    """

    try:              
        
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
        parser.add_argument('--dotResolution',type=str,default='',help="value for global 'dotResolution' i.e. .1")
                                 
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

        try:
            from PT3S import Mx, Xm, Rm
        except ImportError:
            logger.debug("{0:s}{1:s}".format("test: from PT3S import Mx, Xm, Rm: ImportError: ","trying import Mx, Xm, Rm ..."))  
            import Mx, Xm, Rm

        if args.moduleTest == '1':
            # as unittests
            logger.info("{0:s}{1:s}{2:s}".format(logStr,'Start unittests (by DocTestSuite...). testDir: ',args.testDir)) 
        
               
            unittest.TextTestRunner().run(doctest.DocTestSuite(Mx,globs={'testDir':args.testDir,'dotResolution':args.dotResolution}))  
        
            dtFinder=doctest.DocTestFinder(recurse=False) # recurse = False findet nur den Modultest 
            unittest.TextTestRunner().run(doctest.DocTestSuite(Xm,test_finder=dtFinder,globs={'testDir':args.testDir,'dotResolution':args.dotResolution})) 
        
            unittest.TextTestRunner().run(doctest.DocTestSuite(Rm,globs={'testDir':args.testDir,'dotResolution':args.dotResolution}))

            # as doctests
            logger.info("{0:s}{1:s}{2:s}".format(logStr,'Start doctests. testDir: ',args.testDir)) 

            dtFinder=doctest.DocTestFinder(verbose=False)
            dtRunner=doctest.DocTestRunner(verbose=False) 

            dTests=dtFinder.find(Mx,globs={'testDir':args.testDir,'dotResolution':args.dotResolution}) 
            dtRunner.run(dTests[0])

            dTests=doctest.DocTestFinder(verbose=False,recurse=False).find(Xm,globs={'testDir':args.testDir,'dotResolution':args.dotResolution})
            dtRunner.run(dTests[0])

            dTests=dtFinder.find(Rm,globs={'testDir':args.testDir,'dotResolution':args.dotResolution}) 
            dtRunner.run(dTests[0])
        
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

