import sys

sys.path.append('framework')
import frameworktest

sys.path.append('csharp')
import csharp_parser

def test():
    print('Testing CSharp module')
    testCSharpParser(csharp_parser.BasicCSharpParser())

def testCSharpParser(token_parser):
    print('Testing CSharp Parser')
    t = frameworktest.FrameworkTest(token_parser)
    t.TestAll()