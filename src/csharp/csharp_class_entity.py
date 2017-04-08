class CSharpClassEntity():

    def __init__(self, csharp_class_name, tokens, token_pos):
        super(CSharpClass, self).__init__('class', tokens, token_pos)
        self.namespace = ''
        self.class_name = csharp_class_name
        self.symbol_name = csharp_class_name
        self.base_info = []
        self.inherited_by = []
        self.methods_data = []
        self.fields_data = []
        self.properties_data = []
        self.usage = []
        self.file_name = ''
        self.project_path = ''
        self.referenced = []