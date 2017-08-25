
class CSharpClassParamMethod:

    def __init__(self, csharp_param_name, method_id):
        self.param_name = csharp_param_name
        self.param_type = ''
        self.param_default_value = ''
        self.method_id = method_id

    def add_entity(self, parser):
        self.parser = parser
        entity = parser.symbols.create_symbolic_entity(parser.get_file_path())
        entity.add_value('csharp_type', 'class_method_param')
        entity.add_value('method_id', self.method_id)
        entity.add_value('param_name', self.param_name)
        entity.add_value('param_type', self.param_type)
        entity.add_value('param_default_value', self.param_default_value)
        parser.symbols.add_entity(entity)
        self.class_entity = entity

# class_region = (token_start, token_end) of enclosure class
def parse_tokens(parser, class_region, method_id):
    tokens_data = parser.tokens_data
    tokens = tokens_data['tokens']
    enclosure_position = tokens_data['enclosure_tokens']

    params_data = []

    start_region = class_region[0]
    end_region = class_region[1]

    t = start_region

    start_method_pos = -1

    parameter_type = ''
    parameter_name = ''
    parameter_default_value = ''

    parameter_type_found = False
    parameter_name_found = False
    expected_default_value = False

    number_of_parameters = 0

    def create_method_instance(t):
        param_instance = CSharpClassParamMethod(parameter_name, method_id)
        param_instance.param_type = parameter_type
        param_instance.param_default_value = parameter_default_value

        param_instance.add_entity(parser)

    while t < end_region:

        if tokens[t] == ',':
            # New parameter
            print('\t - parameter ' + parameter_name + " with type " + parameter_type)
            create_method_instance(t)
            parameter_type = ''
            parameter_name = ''
            parameter_default_value = ''

            parameter_type_found = False
            parameter_name_found = False
            expected_default_value = False
        elif expected_default_value:
            parameter_default_value = parameter_default_value + tokens[t]
        elif parameter_name_found and tokens[t] == '=':
            expected_default_value = True
        elif parameter_type_found:
            parameter_name = tokens[t]
            parameter_name_found = True
        else:
            start_method_pos = t
            number_of_parameters = number_of_parameters + 1
            parameter_type = tokens[t]
            parameter_type_found = True

        t = t + 1

    if number_of_parameters > 0:
        print('\t - parameter ' + parameter_name + " with type " + parameter_type)
        create_method_instance(t)

