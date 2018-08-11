import os, sys

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

# print(__path__)

if __path__ not in sys.path:
    sys.path.insert(0, __path__)

from yaml_element import YamlElement
import yaml_utils

class YamlMonoBehaviour(YamlElement):
    def __init__(self, script_guid, definition_line):
        super(YamlMonoBehaviour, self).__init__()
        self.game_object = None
        self.go_id = ''
        self.definition_line = definition_line
        self.id = ''
        self.guid = script_guid
        self.file_name = ''
        self.file_path = ''
        self.script_name = ''
        self.reference_file_path = ''

    def print_outline(self):
        return 'Component ' + self.file_name

class MonoBehaviourYamlParser:
    def __init__(self):
        # Variables used to compoung YamlMonoBehaviour
        self.current_id = ''
        self.current_line = 0
        self.game_object_id = ''
        self.yaml_object = None

    def is_start_of_yaml_section(self, line):
        return line.find("MonoBehaviour") != -1

    def on_yaml_section_start(self, line, line_number):
        self.current_id = line[12:-1]
        self.current_line = line_number
        self.yaml_object = None

    def parse_line(self, line, file_data):
        if line.find("m_GameObject") != -1:
            self.game_object_id = yaml_utils.identify_game_object_id(line)
        elif line.find("m_Script: {") != -1:
            self.guid = yaml_utils.identify_guid(line)
        return file_data

    def on_yaml_section_finish(self):
        self.yaml_object = YamlMonoBehaviour(self.guid, self.current_line)
        self.yaml_object.go_id = self.game_object_id
        self.yaml_object.id = self.current_id
        return self.yaml_object