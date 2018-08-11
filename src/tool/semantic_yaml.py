import sys, os

import fnmatch
from os.path import join

sys.path.append('yaml')
import yaml_parser

input_path = sys.argv[1]
# print(input_path)

def print_hierarchy(hierarchy, go_list, level):
    level_str = '├──'
    for i in range(0, level):
        level_str = ' ' + level_str

    if level > 0:
        for i in range(0, 3*level):
            level_str = ' ' + level_str

            # ' ロ'
            # 四

    for h in go_list:
        print(str('') + level_str + ' 四' + h.gameobject_name + ' (' + h.yaml_id + ')')
        if h.transform != None and \
           h.transform.yaml_id in hierarchy:
            print_hierarchy(hierarchy, hierarchy[h.transform.yaml_id], level+1)

def parse_file(file_name):
    yaml_data = yaml_parser.parse_file(file_name)

    game_objects = yaml_data['game_objects']

    hierarchy = {}

    hierarchy[0] = []

    for g in game_objects:
        if g.transform is not None:
            if g.transform.parent == None:
                hierarchy[0].append(g)
            elif g.transform.parent.yaml_id in hierarchy:
                hierarchy[g.transform.parent.yaml_id].append(g)
            else:
                hierarchy[g.transform.parent.yaml_id] = [g]

    print_hierarchy(hierarchy, hierarchy[0], 0)

def parse_project(project_path, file_extension):
    for root, subFolders, files in os.walk(project_path):
        for filename in fnmatch.filter(files, file_extension):
            parse_file(join(root, filename))

if os.path.isdir(input_path):
    print("It can't parse a project right now!")
elif os.path.isfile(input_path):
    parse_file(input_path)
else:
    print("Wrong input" )