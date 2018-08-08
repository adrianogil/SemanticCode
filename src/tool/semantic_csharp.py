import sys, os

import fnmatch
from os.path import join

sys.path.append('csharp')
import csharp_parser

input_path = sys.argv[1]

def parse_file(file_name):
    parser = csharp_parser.BasicCSharpParser()
    tokenized_data = parser.parse_file(file_name)

    classes = tokenized_data['classes']

    for c in classes:
        print(c.class_name)

def parse_project(project_path, file_extension):
    for root, subFolders, files in os.walk(project_path):
        for filename in fnmatch.filter(files, file_extension):
            parse_file(join(root, filename))

if os.path.isdir(input_path):  
    parse_project(input_path, '*.cs')
elif os.path.isfile(input_path):  
    parse_file(input_path) 
else:  
    print("Wrong input" )

# class FrameworkTest:
#     def __init__(self, parser, file_name = '../../test/testparse.cs'):
#         self.parser = parser
#         self.file_name = file_name

#         dir_path = os.path.dirname(os.path.realpath(__file__))
#         self.test_file = os.path.join(dir_path, self.test_file)

#     def TestAll(self):
#         self.TestTokenParse()

#     def TestTokenParse(self):
#         print('--- Start Testing - Token Parse ---')

        

#         print('--- Start End ----- Token Parse ---')

#         return tokenized_data



# def testAllModules():
#     print("----- Testing Start -----")
#     test_framework.test()
#     test_csharp.test()
#     print("----- Testing End -------")


# testAllModules()