import sys

sys.path.append('csharp')
import csharp_parser

def test():
    testCSharpParser(csharp_parser.BasicCSharpParser())

def testCSharpParser(token_parser):
    print('Testing CSharp module')