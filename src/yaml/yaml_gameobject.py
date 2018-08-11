import os, sys

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

# print(__path__)

if __path__ not in sys.path:
    sys.path.insert(0, __path__)

from yaml_element import YamlElement

class YamlGameObject(YamlElement):
    def __init__(self, gameobject_name, definition_line):
        super(YamlGameObject, self).__init__()
        self.gameobject_name = gameobject_name
        self.definition_line = definition_line
        # self.gameobject_name = ''
        # self.definition_line = 0
        self.transform = None
        self.components = []

    def add_component(self, component):
        self.components.append(component)
        component.game_object = self

    def print_outline(self, prefix=''):
        # print(self.gameobject_name)
        object_outline = '<a href="' + str(self.definition_line) + '">' + prefix + ' GameObject ' + \
                                    self.gameobject_name + '</a>'
        # print(object_outline)
        for component in self.components:
            object_outline = object_outline + "<br>" +  prefix + component.print_outline()

        if self.transform != None:
            # print(self.transform.yaml_id)
            for c in self.transform.children:
                if c.game_object != None:
                    object_outline = object_outline + "<br>" +  c.game_object.print_outline(prefix + '-')
                    # object_outline = object_outline + "<br>\n" +  c.game_object.yaml_id
        return object_outline

# Variables used to compoung YamlGameObject
class GameObjectYamlParser:

    def __init__(self):
        self.current_go_id = ''
        self.current_go_line = 0
        self.go_instance = None
        self.gameobject_name = ''

    def is_start_of_yaml_section(self, line):
        self.current_go_id = ''
        self.current_go_line = 0
        self.go_instance = None

        return line.find("GameObject") != -1

    def on_yaml_section_start(self, line, line_number):
        self.current_go_id = line[10:-1]
        self.current_go_line = line_number
        self.go_instance = None

    def parse_line(self, line, file_data):
        if line.find("m_Name") != -1:
            self.gameobject_name = line[9:-1]
            file_data['gameobject_name_by_id'][self.current_go_id] = self.gameobject_name
            file_data['row_by_id'][self.current_go_id] = self.current_go_line

            self.go_instance = YamlGameObject(self.gameobject_name, self.current_go_line)
            self.go_instance.yaml_id = self.current_go_id

        return file_data

    def on_yaml_section_finish(self):
        return self.go_instance

# if found_go and line.find("m_PrefabParentObject:") != -1 and line.find("m_PrefabParentObject: {fileID: 0}") == -1:
        #     guid = ''
        #     found_guid = False
        #     for l in range(21, line_size):