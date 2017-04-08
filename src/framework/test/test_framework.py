import sys
sys.path.append('framework')
import token_parser

import frameworktest

def test():
    print('Testing Framework module')
    t = frameworktest.FrameworkTest(token_parser.TokenParser())
    t.TestAll()