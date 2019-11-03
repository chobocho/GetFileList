import unittest
import os
import sys

sys.path.append("..\\src")
import fileutil

class TestSimpleGui(unittest.TestCase):
    def test_getMyHash(self):
        fileutil.getMyHash("test.bat")

if __name__ == '__main__':
    unittest.main()