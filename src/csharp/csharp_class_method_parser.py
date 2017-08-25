import csharp_class_method_param_parser
# import csharp_class_method_scope_parser
# from csharp_class_method_scope_parser import CSharpMethodScope

import csharp_utils

class CSharpClassMethod:

    def __init__(self, csharp_method_name, token_pos):
        self.method_name = csharp_method_name
        self.method_type = ''
        self.method_access_level = ''
        self.is_static = False
        self.is_constructor = False
        self.is_override = False
        self.is_virtual = False

        self.params = []
        self.definition_line = 0
        self.scope_children = []
        self.tokens_body = []
        self.variable_instances = []
        self.method_instance = self

    def add_entity(self, parser):
        self.parser = parser
        entity = parser.symbols.create_symbolic_entity(parser.get_file_path())
        entity.add_value('csharp_type', 'class_method')
        entity.add_value('method_name', self.method_name)
        entity.add_value('method_type', self.method_type)
        entity.add_value('method_access_level', self.method_access_level)
        entity.add_value('is_static', self.is_static)
        entity.add_value('is_constructor', self.is_constructor)
        entity.add_value('is_override', self.is_override)
        entity.add_value('is_virtual', self.is_virtual)
        entity.add_value('line_in_file', self.definition_line)
        entity.add_value('class_id', self.class_id)
        parser.symbols.add_entity(entity)
        self.class_entity = entity

    def add_param(self, param_object):
        self.params.append(param_object)
        param_object.method_object = self

    def parse_symbols(self, symbols):
        # print('Parse symbol on method ' + self.method_name)
        csharp_class_method_scope_parser.parse_tokens(self.tokens_body, \
                    (1, len(self.tokens_body['tokens'])-1), self, symbols, self)


# class_region = (token_start, token_end) of enclosure class
def parse_tokens(parser, class_region, class_name, class_entity_id):
    print('csharp_class_method_parser region: ' + str(class_region) + ' and entity id ' + str(class_entity_id))

    tokens_data = parser.tokens_data
    tokens = tokens_data['tokens']
    # semantic_tokens = tokens_data['semantic_tokens']
    token_position = tokens_data['tokens_position']
    enclosure_position = tokens_data['enclosure_tokens']

    method_data = []

    method_access_level = ''
    return_type = 'None'
    method_name = ''
    expected_method = False
    is_static_method = False
    is_constructor = False
    is_override = False
    is_virtual = False

    start_region = class_region[0]
    end_region = class_region[1]

    t = start_region

    start_method_pos = -1

    def create_method_instance(t):
        method_instance = CSharpClassMethod(method_name, start_method_pos)
        method_instance.method_type = return_type
        method_instance.method_access_level = method_access_level
        method_instance.line_in_file = tokens_data['tokens_position'][start_method_pos][0]
        method_instance.definition_line = tokens_data['tokens_position'][start_method_pos][0]
        method_instance.is_static = is_static_method
        method_instance.is_constructor = is_constructor
        method_instance.is_virtual = is_virtual
        method_instance.is_override = is_override
        method_instance.class_id = class_entity_id

        t1 = enclosure_position[t]+2
        t2 = enclosure_position[enclosure_position[t]+1]-1

        enclosure_position_method = []

        # for i in range(t1, t2):
        #     if enclosure_position[i] >= t1:
        #         enclosure_position_method.append(enclosure_position[i]-t1)
        #     else:
        #         enclosure_position_method.append(enclosure_position[i])

        # method_instance.tokens_body = {"tokens" : tokens[t1:t2], \
        #                                "semantic_tokens" : semantic_tokens[t1:t2], \
        #                                "token_position" : token_position[t1:t2], \
        #                                "enclosure_position" : enclosure_position_method }

        # method_data.append(method_instance)

        # for i in range(start_method_pos-1, enclosure_position[enclosure_position[t]+1]):
        #     semantic_tokens[i] = method_instance

        method_instance.add_entity(parser)

        return method_instance.class_entity.id

    while t < end_region:

        if tokens[t] == '(' and tokens[enclosure_position[t]+1] == '{':
            if csharp_utils.is_base_keyword(tokens[t-1]):
                is_constructor = True
                if t > 5 and csharp_utils.is_access_modifier(tokens[t-6]):
                    method_access_level = tokens[t-6]
                start_method_pos = t-6
            elif t > 3 and csharp_utils.is_access_modifier(tokens[t-4]) and csharp_utils.is_static_modifier(tokens[t-3]):
                method_access_level = tokens[t-4]
                is_static_method = True
                start_method_pos = t-4
            elif t > 3 and csharp_utils.is_access_modifier(tokens[t-4]) and csharp_utils.is_virtual_modifier(tokens[t-3]):
                method_access_level = tokens[t-4]
                start_method_pos = t-4
                is_virtual = True
            elif t > 3 and csharp_utils.is_access_modifier(tokens[t-4]) and csharp_utils.is_override_modifier(tokens[t-3]):
                method_access_level = tokens[t-4]
                start_method_pos = t-4
                is_override = True
            elif t > 2 and csharp_utils.is_access_modifier(tokens[t-3]):
                method_access_level = tokens[t-3]
                start_method_pos = t-3
            elif t > 2 and csharp_utils.is_static_modifier(tokens[t-3]):
                method_access_level = 'default'
                is_static_method = True
                start_method_pos = t-3
            else:
                method_access_level = 'default'
                start_method_pos = t-2

            if tokens[t-1] == class_name:
                is_constructor = True

            if not is_constructor:
                return_type = tokens[t-2]
                method_name = tokens[t-1]
            else:
                method_name = 'constructor' #tokens[t-5]

            if is_static_method:
                print('Found static method ' + method_name + " with return type '" + return_type + "' and access level " + method_access_level)
            else:
                print('Found method ' + method_name + " with return type '" + return_type + "' and access level " + method_access_level)

            method_id = create_method_instance(t)
            csharp_class_method_param_parser.parse_tokens(parser, (t+1, enclosure_position[t]), method_id)

            is_static_method = False
            is_constructor = False
            method_type = 'None'
            is_override = False
            is_virtual = False

            t = enclosure_position[enclosure_position[t]+1]+1
        else:
            t = t + 1