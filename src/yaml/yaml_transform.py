import os, sys

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

# print(__path__)

if __path__ not in sys.path:
    sys.path.insert(0, __path__)

from yaml_element import YamlElement
import yaml_utils

class YamlTransform(YamlElement):

    def __init__(self):
        super(YamlTransform, self).__init__()
        self.go_id = ''
        self.definition_line = 0
        self.children_ids = []
        self.game_object = None
        self.children = []
        self.parent = None
        self.is_rect_transform = False

    def add_child(self, child_transform):
        self.children.append(child_transform)
        child_transform.parent = self

class TransformYamlParser:
    def __init__(self):
        # Variables used to compoung YamlTransform
        # print('TransformYamlParser::__init__')
        self.current_transform_id = ''
        self.current_transform_line = 0
        self.transform_go_id = ""
        self.transform_children_id = []
        self.found_transform_children_property = False
        self.is_rect_transform = False

    def is_start_of_yaml_section(self, line):
        # print('TransformYamlParser::is_start_of_yaml_section - ' + str(line))
        if line.find("RectTransform") != -1:
            self.is_rect_transform = True
            return True

        if line.find("Transform") != -1:
            self.is_rect_transform = False
            return True

        return False

    def on_yaml_section_start(self, line, line_number):
        if self.is_rect_transform:
            self.current_transform_id = line[12:-1]
            print('TransformYamlParser::on_yaml_section_start - current_transform_id ' + self.current_transform_id)
        else:
            self.current_transform_id = line[10:-1]
        self.current_transform_line = line_number
        self.transform_go_id = ""
        self.transform_children_id = []


    def parse_line(self, line, file_data):
        line_size = len(line)
        if line.find("m_GameObject: {fileID: ") != -1:
            self.transform_go_id = yaml_utils.identify_game_object_id(line)
            # print('TransformYamlParser::parse_line - transform_go_id ' + self.transform_go_id)
            file_data['transform_id_by_gameobject_id'][self.transform_go_id] = self.current_transform_id
            file_data['gameobject_id_by_transform_id'][self.current_transform_id] = self.transform_go_id
            file_data['row_by_id'][self.current_transform_id] = self.current_transform_line
        if not self.found_transform_children_property and \
           line.find("m_Children:") != -1 and line.find("m_Children: []") == -1:
            self.found_transform_children_property = True
            self.transform_children_id = []
        elif self.found_transform_children_property and (line.find("- {fileID: ") == -1 or line.find("m_Father:") != -1):
            self.found_transform_children_property = False
        elif self.found_transform_children_property:
            start_child_id = 0
            end_child_id = 0
            for l in range(13, line_size):
                if line[l-13:l].find("  - {fileID: ") != -1:
                    start_child_id = l
                if start_child_id > 0 and line[l] == "}":
                    end_child_id = l
                    break
            # Add a child to current transform
            self.transform_children_id.append(line[start_child_id:end_child_id])
        return file_data

    def on_yaml_section_finish(self):
        transform = YamlTransform()
        transform.yaml_id = self.current_transform_id
        transform.go_id = self.transform_go_id
        transform.definition_line = self.current_transform_line
        transform.children_ids = self.transform_children_id
        transform.is_rect_transform = self.is_rect_transform
        return transform