import os
import sys
import unittest
import logging

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_DIR + '/libs')

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)-5s | %(name)-23s | %(funcName)-13s | %(message)s"
)

if __name__ == '__main__':
    from tests.decorator_utils import *
    from tests.pathext import *
    from tests.events import *
    from tests.bintools import *

    from syncall_tests import *

    unittest.main()
