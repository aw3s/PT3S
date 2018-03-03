

#import nbformat
#from nbconvert.preprocessors import ExecutePreprocessor
#from nbconvert.preprocessors.execute import CellExecutionError


import matplotlib.pyplot as plt
from matplotlib import colors


class MxTest(unittest.TestCase):
    ###mx1File='./testdata/WDOneLPipe/B1/V0/BZ1/M-1-0-1.MX1'  
    mx1File='testdata\WDOneLPipe\B1\V0\BZ1\M-1-0-1.MX1'
    mx1File='testdata\M-1-0-1.MX1'  
    unpackVectorChannels=False

    channelsNotToBeProcessedSir3sIDRegExp=[
     '(\S+)~(\S+)~(\S+)~(\S+)~*INST*'
#   ,'ALLG~(\S*)~(\S*)~(\S*)~CVERSO'
#   ,'ALLG~(\S*)~(\S*)~(\S*)~SNAPSHOTTYPE' 
#   ,'(\S+)~(\S+)~(\S+)~(\S*)~RART' 
    ,'^ROHR_VRTX' # surprise: not a VectorChannel?!
    ,'^ROHR~(\S+)~(\S+)~(\S*)~QM[I,K]{1}'
    ,'^VENT~(\S+)~(\S+)~(\S*)~OEFFNET'
    ,'^VENT~(\S+)~(\S+)~(\S*)~SCHLIESST'
    ,'^VENT~(\S+)~(\S+)~(\S*)~AUF'
    ,'^VENT~(\S+)~(\S+)~(\S*)~ZU'
    ,'^KNOT~(\S+)~(\S*)~(\S*)~T'
    ,'^KNOT~(\S+)~(\S*)~(\S*)~PDAMPF'
    ,'^KNOT~(\S+)~(\S*)~(\S*)~RHO'
    ,'^PUMP'
    ,'^PGRP'
    ,'^R\S+~(\S+)~(\S*)~(\S*)~X\S+'
    ]
    #channelsNotToBeProcessedSir3sIDRegExp=[]

    mxObjectCreated=False    
    mx=None  

    h5File='./testdata/WDOneLPipe/B1/V0/BZ1/M-1-0-1.h5'  
    h5File='./testdata/M-1-0-1.h5'  
    h5Key='/testdata/WDOneLPipe/B1/V0/BZ1/M_1_0_1'  
    h5Key='/testdata/M_1_0_1'  


    nbFile='./nb/MxWithPandas.ipynb'

class MxTest01InitMx1False(unittest.TestCase):

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01__init__FileNotFoundError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="Mx(mx1File='./testdata/None.MX1')"):
                Mx(mx1File='./testdata/None.MX1')
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_02__init__OsError(self):     
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="Mx(mx1File=666)"):
                Mx(mx1File=666)
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_03__init__TypeError(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        with self.assertLogs(logger=logger,level='ERROR')as cm:     
            with self.assertRaises(MxError,msg="Mx()"):
                Mx()
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_04__init__ParseError(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        with self.assertLogs(logger=logger,level='ERROR')as cm:     
            with self.assertRaises(MxError,msg="Mx(mx1File='./testdata/M-1-0-1.txt')"):
                Mx(mx1File='./testdata/M-1-0-1.txt')  
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
        
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxTest02InitMx1(unittest.TestCase):

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01__init__mx1(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='DEBUG') as cm:                                               
            MxTest.mx=Mx(mx1File=MxTest.mx1File,unpackVectorChannels=MxTest.unpackVectorChannels,channelsNotToBeProcessedSir3sIDRegExp=MxTest.channelsNotToBeProcessedSir3sIDRegExp)     
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
 
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxTest03AssignMxsFalse(unittest.TestCase):
             
    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))                 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01_initMxsZip_FileNotFoundError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/None.ZIP')"):
                MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/None.ZIP')                              
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_02_initMxsZip_OsError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="MxTest.mx.setResultsToMxsZipfile(mxsZipFile=666)"):
                MxTest.mx.setResultsToMxsZipfile(mxsZipFile=666)                              
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   

    def test_03_initMxsZip_ZipError(self):    
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)  
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='ERROR') as cm:
            with self.assertRaises(MxError,msg="MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/M-1-0-1.txt')"):
                MxTest.mx.setResultsToMxsZipfile(mxsZipFile='./testdata/M-1-0-1.txt')                              
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
        
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxTest04AssignMxs(unittest.TestCase):

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))                         
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01_setResultsToMxsZipfile(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))         
        with self.assertLogs(logger=logger,level='DEBUG') as cm:                 
            MxTest.mx.setResultsToMxsZipfile()
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
       
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxTest05WriteH5(unittest.TestCase):

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_01_wrtResultsToH5File(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))     
        
        wD,base,ext = MxTest.mx.getMx1FilenameSplit()
        h5Filename=wD+os.path.sep+base+'.'+'h5'   
        if os.path.exists(h5Filename):                        
            logger.debug("{0:s}{1:s}: Delete ...".format(logStr,h5Filename))     
            os.remove(h5Filename)

        MxTest.mx.wrtResultsToH5File()

        self.assertTrue(os.path.exists(h5Filename),msg='os.path.exists({0!s})'.format(h5Filename))        

        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
        
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxTest07InitH5(unittest.TestCase):

    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     


    def test_21__init__h5(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))   

        with pd.HDFStore(MxTest.h5File) as h5Store:
        
                # key correct?
                keys=h5Store.keys()
                h5Key=keys[0]
                self.assertEqual(h5Key,MxTest.h5Key,msg='h5Key <> {0:s}'.format(MxTest.h5Key))

                # reference to MX1-File correct?
                metadata=h5Store.get_storer(h5Key).attrs.metadata
                mx1File=metadata['relPath2Mx1FromCurDir']
                self.assertEqual(mx1File,MxTest.mx1File,msg="metadata['relPath2Mx1FromCurDir'] <> {0:s}".format(MxTest.mx1File))

                # MX1-File existing?
                self.assertTrue(os.path.exists(mx1File))

        with self.assertLogs(logger=logger,level='DEBUG') as cm:                                
            MxTest.mx=Mx(h5File=MxTest.h5File)
                     
        logger.debug("{0:s}{1!s}".format(logStr,cm.output))   
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
        
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
        
class MxTest10Nb(unittest.TestCase):
    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def test_MxWithPandas(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))   
        
        with open(MxTest.nbFile) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')

        try:
            logger.debug("{0:s}Notebook: {1:s} ...".format(logStr,MxTest.nbFile))   
            ep.preprocess(nb, {'metadata': {'path': '.'}})
        except CellExecutionError:
            self.fail("{0:s}: CellExecutionError".format(MxTest.nbFile))
        else:
            logger.debug("{0:s}Notebook: {1:s} ... done without CellExecutionErrors. Save Notebook ...".format(logStr,MxTest.nbFile))   
            with open(MxTest.nbFile, 'wt') as f:
                nbformat.write(nb, f)
            logger.debug("{0:s}Notebook: {1:s} ... done without CellExecutionErrors. Save Notebook ... Done.".format(logStr,MxTest.nbFile))   
                     
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

class MxTest11Pdf(unittest.TestCase):
    def setUp(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
         
    def test_MxWithPandas(self):  
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))   
        

        # del pdf
        root, ext = os.path.splitext(MxTest.nbFile)
        pdfFile=root+'.'+'pdf'   
        if os.path.exists(pdfFile):                        
            logger.debug("{0:s}{1:s}: Delete ...".format(logStr,pdfFile))     
            os.remove(pdfFile)

        # gen pdf
        cmd="jupyter nbconvert --to pdf {0:s} --template ./nb/PT3S.tplx".format(MxTest.nbFile)
        logger.debug("{0:s}cmd=".format(logStr,cmd))  
        subprocess.call(cmd) 

        self.assertTrue(os.path.exists(pdfFile),msg='os.path.exists({0!s})'.format(pdfFile))        
       
                     
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            
    def tearDown(self):
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     




        parser.add_argument('--x','--mx1File',type=str, help='.mx1 File (default: ./testdata/M-1-0-1.MX1)',default='./testdata/M-1-0-1.MX1')  

        group = parser.add_mutually_exclusive_group()                
        group.add_argument('--z','--mxsZipFile',type=str, help='parse .zip File (default: ./testdata/M-1-0-1.ZIP)',default='./testdata/M-1-0-1.ZIP')  
        group.add_argument('--s','--mxsFile',type=str, help='parse .mxs File (default: ./testdata/M-1-0-1.MXS)',default='./testdata/M-1-0-1.MXS')  
        group.add_argument('-a',help='parse all .mxs Files in MX1-Directory - NIY',action="store_true",default=False)    
        group.add_argument('--r','--regExp',type=str,help='parse all Files (.mxs, .zip) in MX1-Directory matching RegExp - NIY',default=False)   
        
        group = parser.add_mutually_exclusive_group()                   
        group.add_argument("-u","--unittest", help="Perform Mx-Unittests", action="store_true",default=True)   
        group.add_argument("-d","--unittestDoc", help="Perform Mx-Unittests: Doc only", action="store_true",default=False)   
        group.add_argument("-n","--unittestNb", help="Perform Mx-Unittests: Nb (run Notebooks) only", action="store_true",default=False)   
        group.add_argument("-p","--unittestPdf", help="Perform Mx-Unittests: Pdf (gen Pdf) only", action="store_true",default=False)   

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")                  
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        suite=None
        if args.unittestPdf:      
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(MxTest11Pdf)          
        elif args.unittestNb:      
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(MxTest10Nb)                                      
        elif args.unittestDoc:            
            #doctest.testmod()
            suite=doctest.DocTestSuite()                                    
        elif args.unittest:
            suite =        unittest.defaultTestLoader.loadTestsFromTestCase(MxTest01InitMx1False)
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(MxTest02InitMx1))
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(MxTest03AssignMxsFalse))
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(MxTest04AssignMxs))
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(MxTest05WriteH5))
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(MxTest07InitH5))
        
        if suite != None:
            unittest.TextTestRunner().run(suite)  


        #head,tail = os.path.split(__file__)
        #file,ext = os.path.splitext(tail)
        #logFileName = os.path.normpath(os.path.join(head,os.path.normpath('./testresults'))) 
        #logFileName = os.path.join(logFileName,file + '.log') 

        #parser.add_argument('--x','--XmlFile',type=str, help='.xml File'
        #                    #,default='./testdata/FW.XML'
        #                    ) 
        
        







#>>> # ---
#>>> # Init with MX1-File
#>>> # ---
#>>> mx1File='testdata\WDOneLPipe\B1\V0\BZ1\M-1-0-1.MX1'
#>>> mx=Mx(mx1File=mx1File)
#>>> # ---
#>>> # exploring after Init ...
#>>> # ---
#>>> len(mx.mxChannels)
#55
#>>> # Bytes unpacked in a single MX-Record:
#>>> mx.bytesUnpacked
#272
#>>> # Bytes in MX-Record:
#>>> MxRecordLength=struct.calcsize(mx.mxRecordStructUnpackFmtString)   
#>>> unpackingRate=mx.bytesUnpacked/MxRecordLength
#>>> # ---
#>>> # Read MXS-ZIP...
#>>> # ---
#>>> pdf=mx.setResultsToMxsZipfile() # returns self.pdf
#>>> type(mx.pdf)
#<class 'pandas.core.frame.DataFrame'>
#>>> # ---
#>>> # Dump to H5...
#>>> # ---
#>>> mx.wrtResultsToH5File()
#>>> # ---
#>>> # Init with H5...
#>>> # ---
#>>> h5File='./testdata/WDOneLPipe/B1/V0/BZ1/M-1-0-1.h5'  
#>>> mx=Mx(h5File=h5File)
#>>> # ---
#>>> # how fast is Init with H5? ...
#>>> # ---
#>>> t=timeit.timeit(stmt="Mx.Mx(h5File='./testdata/WDOneLPipe/B1/V0/BZ1/M-1-0-1.h5')",setup="import Mx",number=1)      
#>>> # t should be < 30s!  


    #def __readMxChannelDefinitions(self):
    #    """
    #    Read the MX-Channel Definitions from the MX1-File.
    #    >self.mxChannels[]
    #    >self.mxChannelsSir3sIDs[]     
    #    """

    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    #    try:
    #        # XML Channel Def 
    #        try:
    #            Mx1Tree = ET.parse(self.mx1File)
    #        except:
    #            logStrFinal="{0:s}mx1File: {1:s}: ET.parse: Error.".format(logStr,self.mx1File)
    #            logger.error(logStrFinal) 
    #            raise MxError(logStrFinal)      

    #        Mx1Root = Mx1Tree.getroot()
    #        self.mxChannels=Mx1Root.findall('XL1')
    #        logger.debug("{0:s}mx1File: {1:s}: MX-Channels={2:d}.".format(logStr,self.mx1File,len(self.mxChannels)))      

    #        # Sir3sID
    #        self.mxChannelsSir3sIDs=[]
    #        for idxChannel,mxChannel in enumerate(self.mxChannels):               
    #            sir3sID=self.__getSir3sID(idxChannel)
    #            self.mxChannelsSir3sIDs.append(sir3sID)

    #        # test if Sir3sID is unique
    #        duplicateSir3sIDs = [item for item, count in collections.Counter(self.mxChannelsSir3sIDs).items() if count > 1]
    #        for duplicateSir3sID in duplicateSir3sIDs:
    #            indices = [i for i, x in enumerate(self.mxChannelsSir3sIDs) if x == duplicateSir3sID]
    #            logger.debug("{0:s}mx1File: {1:s}: Sir3sID: {2:s} is NOT unique! NoOfDuplicates={3:s}.".format(logStr,self.mx1File,duplicateSir3sID,str(indices)))      
                
    #        if len(duplicateSir3sIDs)>0:
    #            logStrFinal="{0:s}mx1File: {1:s}: Sir3sIDs are not unique! Error.".format(logStr,self.mx1File)
    #            logger.error(logStrFinal) 
    #            raise MxError(logStrFinal)      

    #    except MxError:
    #        raise                      
    #    except:
    #        logStrFinal="{0:s}mx1File: {1:s}: Error.".format(logStr,self.mx1File)
    #        logger.error(logStrFinal) 
    #        raise MxError(logStrFinal)                 
    #    else:           
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    #def __evalMxChannelsToBeProcessed(self,unpackVectorChannels,channelsNotToBeProcessedSir3sIDRegExp):
    #    """              
    #    >self.mxChannelsProcessed[]
    #    """

    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    #    try:
                      
    #        # mark Channels to be processed
    #        self.mxChannelsProcessed=[]
    #        # 1st aspect unpackVectorChannels
    #        for idxChannel,mxChannel in enumerate(self.mxChannels):
    #            Sir3sID=self.mxChannelsSir3sIDs[idxChannel]
    #            cDTypeLength=int(mxChannel.get('DATATYPELENGTH'))
    #            cDLength=int(mxChannel.get('DATALENGTH'))
    #            items=int(cDLength/cDTypeLength)
    #            if items>1 and not unpackVectorChannels:
    #                self.mxChannelsProcessed.append(False)
    #                logger.debug("{0:s}MX-Channel: {1:s} will NOT be processed because not unpackVectorChannels matches.".format(logStr,Sir3sID))      
    #            else:
    #                self.mxChannelsProcessed.append(True)

    #        # additional aspect RegExp
    #        channelsNotToBeProcessedSir3sIDRegExpCompiled=[]
    #        for idx, regExp in enumerate(channelsNotToBeProcessedSir3sIDRegExp):
    #            regExpCompiled=re.compile(regExp)
    #            channelsNotToBeProcessedSir3sIDRegExpCompiled.append(regExpCompiled)
            
    #        for idxChannel,Sir3sID in enumerate(self.mxChannelsSir3sIDs):
    #            if not self.mxChannelsProcessed[idxChannel]:
    #                continue
    #            tbProcessed=True
    #            for idxRegExp, regExpCompiled in enumerate(channelsNotToBeProcessedSir3sIDRegExpCompiled):
    #                m=regExpCompiled.search(Sir3sID)
    #                if m != None:
    #                    tbProcessed=False
    #                    logger.debug("{0:s}MX-Channel: {1:s} will NOT be processed because -v regExp {2:s} matches.".format(logStr,Sir3sID,channelsNotToBeProcessedSir3sIDRegExp[idxRegExp]))      
    #                    break
    #            self.mxChannelsProcessed[idxChannel]=tbProcessed

    #        # report
    #        self.__reportMxChannelsProcessed()
           
    #    except:
    #        logStrFinal="{0:s}mx1File: {1:s}: Error.".format(logStr,self.mx1File)
    #        logger.error(logStrFinal) 
    #        raise MxError(logStrFinal)                 
    #    else:           
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    #def __reportMxChannelsProcessed(self):

    #    logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
    #    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    #    try:                      
    #        for idxChannel,Sir3sID in enumerate(self.mxChannelsSir3sIDs):
    #            if self.mxChannelsProcessed[idxChannel]:
    #                logger.debug("{0:s}MX-Channel: {1:s} processed.".format(logStr,Sir3sID))      
    #        idxList = [i for i in range(len(self.mxChannelsProcessed)) if self.mxChannelsProcessed[i]]
    #        logger.debug("{0:s}{1:d} from {2:d} MX-Channels processed (making up {3:06.2f} Channel-%).".format(logStr,len(idxList),len(self.mxChannels),len(idxList)/len(self.mxChannels)*100))            
           
    #    except:
    #        logStrFinal="{0:s}Error.".format(logStr)
    #        logger.error(logStrFinal) 
    #        raise MxError(logStrFinal)                 
    #    else:           
    #        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))          
    
    
    
    
    
    """
SIR 3S Logfile Utilities (short: Lx)
"""

import os
import sys
import logging
logger = logging.getLogger(__name__)     
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

import csv

class LxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LxSirOPC():
    """
    SirOPC Logfile Set
    """
    def __init__(self,logFile=None):
        """
        (re-)initialize the set with logFile. 
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
             with open(logFile,'r') as f: 
                pass
             self.logFile=logFile 
             restkey='+'
             delimiter='\t'

             with open(logFile,"r") as csvFile: # 1. Zeile enthaelt die Ueberschrift 
                reader = csv.DictReader(csvFile,delimiter=delimiter,restkey=restkey) # erf. wenn eine Spalte selbst delimiter enthalten kann
                colNames=reader.fieldnames
                dcts = [dct for dct in reader] # alle Zeilen lesen
             
             rows = [[dct[colName] for colName in colNames] for dct in dcts]

             for i, dct in enumerate(dcts):
                if restkey in dct:
                    restValue=dct[restkey]
                    restValueStr = delimiter.join(restValue)
                    rows[i][-1]=rows[i][-1]+delimiter+restValueStr

             index=range(len(rows))
             self.pdf = pd.DataFrame(rows,columns=colNames,index=index)

             logger.debug("{0:s}{1:s}: head(10): {2!s}.".format(logStr,logFile,self.pdf.head(10)))   
             logger.debug("{0:s}{1:s}: describe(): {2!s}.".format(logStr,logFile,self.pdf.describe()))         

             self.__convertColumnData()
                          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def __convertColumnData(self):
        """
        converts:
        #LogTime to datetime
        ProcessTime to datetime
        Value to float64
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
             #LogTime
             self.pdf['#LogTime']=pd.to_datetime(self.pdf['#LogTime'],unit='ms',errors='coerce') # NaT
             self.pdf=self.pdf.dropna()
             #ProcessTime
             self.pdf['ProcessTime']=pd.to_datetime(self.pdf['ProcessTime'],errors='coerce') # NaT
             #Value
             self.pdf.Value=self.pdf.Value.str.replace(',', '.')
             self.pdf.Value=pd.to_numeric(self.pdf.Value,errors='coerce') # NaN 
                          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def getProcessDataToSirCalc(self):
        """
        returns df containing only the ProcessData To SirCalc-Cmds and the following additional Columns:
        TableName;ProcessDay;ProcessTime;Value
        LogDay;LogTime
        ProcessTime is not additional but different from the original ProcessTime (which is stored in Column ProcessTimeOrig)
        the df is sorted by TableName,ProcessDay,ProcessTime
        """ 
 
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        df=None
        try: 
             df=self.pdf[self.pdf['ID'].str.contains('^TABL')]
             df=df.sort_values(by=['ID','ProcessTime','#LogTime'])
             df['TableName']=df['ID'].replace('(TABL~)(\S+)~~~SWVT',r'\2',regex=True)#,inplace=True)
             df['LogDay'], df['LogTime'] = df['#LogTime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]).str.split(' ',1).str
             df = df.rename(columns={'ProcessTime':'ProcessTimeOrig'})
             df['ProcessDay'], df['ProcessTime'] = df['ProcessTimeOrig'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]).str.split(' ',1).str        
             df['TimeNr'] = df.groupby('TableName')['ProcessTimeOrig'].rank(ascending=True,method='dense').astype(int)          
        except LxError:
            raise            
        except:
            logStrFinal="{0:s}Error.".format(logStr)
            logger.error(logStrFinal) 
            raise LxError(logStrFinal)               
        else:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
        finally:
            return df

if __name__ == "__main__":
    """
    Run Lx-Stuff or/and perform Lx-Unittests.
    """

    try:              
        # Logfile
        head,tail = os.path.split(__file__)
        file,ext = os.path.splitext(tail)
        logFileName = os.path.normpath(os.path.join(head,os.path.normpath('./testresults'))) 
        logFileName = os.path.join(logFileName,file + '.log') 
        
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
        parser = argparse.ArgumentParser(description='Run Lx-Stuff or/and perform Lx-Unittests.'
        ,epilog='''
        UsageExample#1: (without parameter): -v --x ./testdata/20171103__000001.log   
        '''                                 
        )
        parser.add_argument('--x','--logFile',type=str, help='.log File (default: ./testdata/20171103__000001.log)',default='./testdata/20171103__000001.log')  

        group = parser.add_mutually_exclusive_group()                                
        group.add_argument("-v","--verbose", help="Debug Messages On", action="store_true",default=True)      
        group.add_argument("-q","--quiet", help="Debug Messages Off", action="store_true")                  
        args = parser.parse_args()

        if args.verbose:           
            logger.setLevel(logging.DEBUG)     
        else:            
            logger.setLevel(logging.ERROR)  
                      
        logger.debug("{0:s}{1:s}{2:s}".format(logStr,'Start. Argumente:',str(sys.argv))) 

        lx=LxSirOPC(args.x)

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

        .pypirc
   
        [pypi]
username = PT3S
password = PythonTools3S
