Mx
================================

.. automodule:: Mx

.. autoclass:: Mx.Mx
   :members:
   :private-members:

.. autofunction:: Mx.getMicrosecondsFromRefTime

.. autoexception:: Mx.MxError

.. testsetup:: *

   import Mx
   import os

The parrot module is a module about parrots.

Doctest example:

.. doctest::

	>>> mx1File=os.path.join(path,'..\testdata\WDOneLPipe\B1\V0\BZ1\M-1-0-1.MX1')
	>>> mx=Mx(mx1File=mx1File,NoH5Read=True,NoMxsRead=True)
	>>> isinstance(mx.mx1Df,pd.core.frame.DataFrame) # MX1-Content
	False



