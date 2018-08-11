import os, sys
import fnmatch
from os.path import join

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

print(__path__)

if __path__ not in sys.path:
    sys.path.insert(0, __path__)

import yaml_monobehaviour
import yaml_gameobject
import yaml_transform

def parse_file(filename):
    with open(filename) as f:
            content = f.readlines()
    total_lines = len(content)

    yaml_data = get_all_guid_files(filename)

    file_data = {}
    file_data['row_by_id'] = {}
    file_data['gameobject_name_by_id'] = {}
    file_data['transform_id_by_gameobject_id'] = {}
    file_data['gameobject_id_by_transform_id'] = {}

    transform_instances = []
    gameobject_instances = []
    monobehaviour_instances = []
    yaml_instances = []

    outline_data = []

    yaml_elements = [yaml_monobehaviour.MonoBehaviourYamlParser(), \
                     yaml_gameobject.GameObjectYamlParser(), \
                     yaml_transform.TransformYamlParser()]

    current_yaml_section = None

    for i in range(1, total_lines):
        line = content[i]
        last_line = content[i-1]

        if current_yaml_section == None:
            for y in yaml_elements:
                if last_line.find('--- !u!') != -1 and y.is_start_of_yaml_section(line):
                    current_yaml_section = y
                    current_yaml_section.on_yaml_section_start(last_line, i)
                    break
        elif line.find("--- !u!") != -1:
            yaml_instances.append(current_yaml_section.on_yaml_section_finish())
            current_yaml_section = None
        else:
            file_data = current_yaml_section.parse_line(line, file_data)

    for y in yaml_instances:
        if isinstance(y, yaml_gameobject.YamlGameObject):
            gameobject_instances.append(y)
        elif isinstance(y, yaml_transform.YamlTransform):
            transform_instances.append(y)
        elif isinstance(y, yaml_monobehaviour.YamlMonoBehaviour):
            monobehaviour_instances.append(y)

    for t1 in transform_instances:
        # print('Transform: ' + t1.go_id)
        # print(t1.children_ids)
        # print(t1.yaml_id + " has " + str(len(t1.children)) + ' children')
        for c in t1.children_ids:
            for t2 in transform_instances:
                if t1 != t2 and t1.yaml_id != t2.yaml_id and t2.yaml_id == c:
                    # print('Add child ' + t2.yaml_id + " to transform " + t1.yaml_id)
                    t1.add_child(t2)
                    break
        # print(t1.yaml_id + " got " + str(len(t1.children)) + ' children')
        for go in gameobject_instances:
            if go.yaml_id == t1.go_id:
                t1.game_object = go
                go.transform = t1
                # print("Add transform " + t1.yaml_id + " to gameobject " + go.yaml_id)
                break
    for m in monobehaviour_instances:
        for go in gameobject_instances:
            if go.yaml_id == m.go_id:
                go.add_component(m)
                # print("Add component " + m.guid + " to gameobject " + go.yaml_id)
                break
        if m.guid in yaml_data['files_by_guid']:
            m.file_path = yaml_data['files_by_guid'][m.guid]
            m.file_name = yaml_data['filenames_by_guid'][m.guid]
            m.script_name = yaml_data['filenames_by_guid'][m.guid][:-3]
            m.reference_file_path = filename

            if m.script_name in parse_data['symbols']:
                parse_data['symbols'][m.script_name].add_usage(m)

    outline_data = []
    for go in gameobject_instances:
        if go.transform != None and go.transform.parent == None:
            outline_data.append(go)

    file_data['game_objects'] = gameobject_instances
    file_data['transforms'] = transform_instances
    file_data['outline_data'] = outline_data

    parse_data = file_data

    return parse_data

def parse_project(project_path, content_data, file_extension, parse_function, read_content=True):
    for root, subFolders, files in os.walk(project_path):
        for filename in fnmatch.filter(files, file_extension):
            content = ''
            if read_content:
                with open(join(root, filename)) as f:
                    content = f.readlines()
            content_data = parse_function(content, content_data, root, filename, project_path)
    return content_data

def get_guid_from_file(content, yaml_data, root, filename, project_path):
    guid = ''
    for line in content:
        if line.find('guid:') != -1:
            guid = line[6:(len(line)-1)]
    if guid != '':
        # print(filename + ": " + guid)
        yaml_data['files_by_guid'][guid] = join(root, filename)[:-5]
        yaml_data['filenames_by_guid'][guid] = filename[:-5]
        yaml_data['relative_path_by_guid'][guid] = join(root, filename)[len(project_path):-5]
    return yaml_data

def get_all_guid_files(project_path):
    yaml_data = {}

    yaml_data['files_by_guid'] = {}
    yaml_data['filenames_by_guid'] = {}
    yaml_data['relative_path_by_guid'] = {}

    yaml_data = parse_project(project_path, yaml_data, '*.meta', get_guid_from_file)

    return yaml_data

