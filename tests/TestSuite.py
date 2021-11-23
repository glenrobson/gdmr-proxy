#!/usr/local/bin/python3
import unittest
import TestRedirect
import os
import sys

def suite():
    tests = []
    tests.append(unittest.TestLoader().loadTestsFromTestCase(TestRedirect.TestRedirect))
    return  unittest.TestSuite(tests)

if __name__ == '__main__':
    baseurl = 'http://0.0.0.0'
    desturl = baseurl
    if len(sys.argv) > 1:
        baseurl = sys.argv[1]
        desturl = baseurl
        if len(sys.argv) > 2:
            desturl = sys.argv[2]

    os.environ["baseurl"] = baseurl
    os.environ["desturl"] = desturl

    mySuit=suite()

    runner=unittest.TextTestRunner()
    result = runner.run(mySuit)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
        
