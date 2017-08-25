
class TokenCategory:
    '''
        Tokens categories:
        0 - code
        1 - string
        2 - commentary
    '''
    Code = 0
    String = 1
    Comment = 2

class CSharpImporter():
    def __init__(self, csharp_namespace):
        self.imported_namespace = csharp_namespace

    def add_entity(self, parser):
        entity = parser.symbols.create_symbolic_entity(parser.get_file_path())
        entity.add_value('csharp_type', 'importer')
        entity.add_value('namespace', self.imported_namespace)
        parser.symbols.add_entity(entity)

def parse_tokens(parser):
    tokens_data = parser.tokens_data
    print(str(parser.symbols))

    tokens = tokens_data['tokens']
    tokens_category = tokens_data['tokens_category']

    total_tokens = len(tokens)

    inside_using = False
    current_imported_namespace = ''
    importer_tokens = []
    start_using_token_pos = -1

    # print(str(len(tokens)) + ' x ' + str(len(semantic_tokens)))
    # print(tokens)
    # print(semantic_tokens)

    # diff = []

    # for t in range(0, len(semantic_tokens)):
    #     # Can't consider importers inside strings
    #     if semantic_tokens[t] != tokens[t]:
    #          diff.append(str(semantic_tokens[t]) + ' x ' + tokens[t])

    # print(diff)

    for t in range(0, total_tokens):
        # print('Current token: ' + tokens[t])
        # Can't consider importers inside strings
        if tokens_category[t] != TokenCategory.Code:
            continue
        if not inside_using and is_using_token(tokens[t]):
            inside_using = True
            start_using_token_pos = t
            importer_tokens.append(tokens[t])
        elif inside_using and tokens[t] == ';':
            inside_using = False

            importer_tokens.append(tokens[t])
            # print(current_imported_namespace)
            importer_instance = CSharpImporter(current_imported_namespace)
            importer_instance.add_entity(parser)

            # for s in range(start_using_token_pos, t+1):
            #     semantic_tokens[s] = importer_instance

            current_imported_namespace = ''
            start_using_token_pos = -1
            importer_tokens = []
        elif inside_using:
            current_imported_namespace = current_imported_namespace + tokens[t]
            # print('importer - current_imported_namespace: ' + current_imported_namespace)
            importer_tokens.append(tokens[t])

    return tokens_data

def is_using_token(token):
    return len(token) == 5 and \
        token[0] == 'u' and \
        token[1] == 's' and \
        token[2] == 'i' and \
        token[3] == 'n' and \
        token[4] == 'g'

