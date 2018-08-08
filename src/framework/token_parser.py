import sys, os
import codecs

from default_parser_behavior import DefaultParseBehavior

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

class TokenParser(object):

    def __init__(self, parse_behavior = None):
        if parse_behavior == None:
            self.parse_behavior = DefaultParseBehavior()
        else:
            self.parse_behavior = parse_behavior
        self.reset_token_data()

    def parse_file(self, csharp_file):
        with codecs.open(csharp_file, encoding="utf-8-sig", errors='ignore') as f:
            content = f.readlines()

        return self.parse_content(content)

    def parse_content(self, content):
        '''
            Return tokenized data
                - Tokens
                - Tokens category
                - Enclosure tokens
                - Tokens location
        '''
        self.reset_token_data()
        self.parse_tokens(content)
        self.get_enclosure_elements()

        token_data = { "tokens" : self.tokens, \
                      'tokens_category' : self.tokens_category, \
                      'enclosure_tokens' : self.enclosure_tokens, \
                      'tokens_position': self.tokens_location}

        return token_data


    def parse_tokens(self, content):
        p = self.parse_behavior

        total_lines = len(content)

        current_token = ''
        token_start = (-1,-1)
        token_end = (0,0)

        inside_string = False
        string_element = ''
        start_string_pos = (0,0)
        end_string_pos = (0,0)

        inside_stream_comments = False
        start_stream_comments = (0,0)
        end_stream_comments = (0,0)
        stream_comment = ''

        for i in range(0, total_lines):
            line_size = len(content[i])

            for j in range(0, line_size):
                if not inside_string and not inside_stream_comments and \
                        p.is_inside_stream_comment(content[i], j):
                    inside_stream_comments = True
                    start_stream_comments = (i,j)
                    stream_comment = content[i][j]
                elif inside_stream_comments and \
                        p.is_outside_stream_comment(content[i], j):
                    inside_stream_comments = False
                    stream_comment = stream_comment + content[i][j]

                    end_stream_comments = (i,j)
                    token_location = (start_stream_comments, end_stream_comments)
                    self.add_token_data(stream_comment, token_location, TokenCategory.Comment)

                    stream_comment = ''

                elif inside_stream_comments:
                    stream_comment = stream_comment + content[i][j]
                    continue
                elif inside_string and not p.is_escaped_string_element(content[i], j) and \
                     content[i][j] == string_element:
                    inside_string = False
                    string_element = ''

                    end_string_pos = (i,j)
                    token_location = (start_string_pos, end_string_pos)
                    self.add_token_data(current_token, token_location, TokenCategory.String)

                    current_token = ''
                elif not inside_string and not p.is_escaped_string_element(content[i], j) and \
                         (content[i][j] == "\"" or content[i][j] == "\'"):
                    inside_string = True
                    string_element = content[i][j]
                    start_string_pos = (i,j)
                elif not inside_string and p.is_inside_inline_comment(content[i], j):
                    token_location = ((i,j), (i, line_size-1))
                    self.add_token_data(content[i][j:line_size], token_location, TokenCategory.Comment)
                    break
                elif not inside_string and p.is_empty(content[i][j]):
                    if current_token != '':
                        if token_start[0] == 1 or token_start[1] == -1:
                            token_start = (i,j)
                        token_end = (i,j)
                        token_location = (token_start, token_end)
                        self.add_token_data(current_token, token_location, TokenCategory.Code)
                        current_token = ''
                        token_start = (-1,-1)
                elif not inside_string and p.is_special_token(content[i][j]):
                    if current_token != '':
                        self.add_token_data(current_token, (token_start,(i,j-1)), TokenCategory.Code)
                        token_start = (i,j)
                        current_token = ''
                    self.add_token_data("" + content[i][j], ((i,j),(i,j)), TokenCategory.Code)
                    token_start = (-1,-1)
                else:
                    if token_start[0] == 1 or token_start[1] == -1:
                        token_start = (i,j)
                    current_token = current_token + content[i][j]

    def reset_token_data(self):
        self.tokens = []
        self.tokens_category = []
        self.tokens_location = []
        self.enclosure_tokens = []

    def add_token_data(self, token, token_location, token_category):
        # print('add_token_data ' + token + ' with location ' + str(token_location))

        self.tokens.append(token)
        self.tokens_category.append(token_category)
        self.tokens_location.append(token_location)

    def get_enclosure_elements(self):
        p = self.parse_behavior
        total_tokens = len(self.tokens)

        # print(tokens)
        enclosure_position = []
        enclosure_elements = {}
        opposite_enclosure = {'}':'{', ')':'(', ']':'[', '\'':'\'', '\"':'\"' }

        for t in range(0, total_tokens):
            enclosure_position.append(-1)

            if p.is_opening_element(self.tokens[t], self.tokens_category[t]):
                if self.tokens[t] in enclosure_elements:
                    list = enclosure_elements[self.tokens[t]]
                    list.append(t)
                    enclosure_elements[self.tokens[t]] = list
                else:
                    enclosure_elements[self.tokens[t]] = [t]
            elif p.is_enclosure_element(self.tokens[t], self.tokens_category[t]):
                if opposite_enclosure[self.tokens[t]] in enclosure_elements:
                    list = enclosure_elements[opposite_enclosure[self.tokens[t]]]
                    pos = list.pop()
                    enclosure_elements[opposite_enclosure[self.tokens[t]]] = list
                    enclosure_position[pos] = t
                    enclosure_position[t] = pos
                    # print('Match ' + tokens[pos] + " and " + tokens[t])
        self.enclosure_tokens = enclosure_position