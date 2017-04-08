import sys

sys.path.append('framework/test')
import test_framework

sys.path.append('csharp/test')
import test_csharp

def testAllModules():
    print("----- Testing Start -----")
    test_framework.test()
    test_csharp.test()
    print("----- Testing End -------")


testAllModules()