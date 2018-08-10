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
        if len(sys.argv) > 2:
            is_suitable_class = False
            for b in c.base_info:
                is_suitable_class = is_suitable_class or sys.argv[2] in b
            if is_suitable_class:
                print(c.class_name + ' that inherits from ' + str(c.base_info))
        else:
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