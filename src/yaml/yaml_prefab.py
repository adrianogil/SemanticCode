import os, sys

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

# print(__path__)

if __path__ not in sys.path:
    sys.path.insert(0, __path__)

from yaml_element import YamlElement

class YamlPrefab(YamlElement):
    guid = ''
    target_id = ''

    game_object = None
    transform = None

    # def __init__(self, gameobject_name, definition_line):
    #     super(YamlPrefab, self).__init__(gameobject_name, definition_line)
    # def print_outline(self):
    #     object_outline = '<a href="' + str(self.definition_line) + '">Prefab ' + \
    #                                 self.gameobject_name + '</a>'
    #     return object_outline

# Variables used to compoung YamlGameObject
current_go_id = ''
current_go_line = 0
go_instance = None

#Prefab detection
if last_line.find('--- !u!') != -1 and line.find("Prefab") != -1:
    current_prefab_id = last_line[14:-1]
    current_prefab_line = i
    found_prefab = True

if found_prefab and line.find("target: {") != -1:
    start_prefab_guid = 0
    end_prefab_guid = 0
    for l in range(20, line_size):
        if line[l-6:l].find("guid: ") != -1:
            start_prefab_guid = l
        if start_prefab_guid > 0 and line[l] == ",":
            end_prefab_guid = l
            break
    current_prefab_guid = line[start_prefab_guid:end_prefab_guid]
    # print("found prefab with guid: " + current_prefab_guid)
    if current_prefab_guid in parse_data['yaml']['filenames_by_guid']:
        prefab_filename = parse_data['yaml']['filenames_by_guid'][current_prefab_guid]
        # outline_data.append(YamlPrefab(prefab_filename, current_prefab_line))
    found_prefab = False
    current_prefab_line = 0
    current_prefab_id = ''
    current_prefab_guid = ''

def is_start_of_yaml_section(line):
    return line.find("GameObject") != -1

def on_yaml_section_start(line, line_number):
    current_go_id = line[10:-1]
    current_go_line = line_number
    go_instance = None

def parse_line(line, file_data):
    if line.find("m_Name") != -1:
        gameobject_name = line[9:-1]
        file_data['gameobject_name_by_id'][current_go_id] = gameobject_name
        file_data['row_by_id'][current_go_id] = current_go_line

        go_instance = YamlGameObject(gameobject_name, current_go_line)
        go_instance.yaml_id = current_go_id

    return file_data

def on_yaml_section_finish():
    return go_instance