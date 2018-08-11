
def identify_game_object_id(line):
    if line.find("m_GameObject: {fileID: ") != -1:
        start_go_id = -1
        end_go_id = 0
        line_size = len(line)
        for l in range(8, line_size):
            if line[l-8:l].find('fileID: ') != -1:
                start_go_id = l
            elif start_go_id > 0 and (line[l] == '}' or line[l] == ','):
                end_go_id = l
                return line[start_go_id:end_go_id]
    return ''

# Get GUID from line
def identify_guid(line):
    if line.find(" guid: ") != -1:
        start_guid = -1
        end_guid = 0
        line_size = len(line)
        for l in range(7, line_size):
            if line[l-7:l].find(' guid: ') != -1:
                start_guid = l
            elif start_guid > 0 and (line[l] == '}' or line[l] == ','):
                end_guid = l
                guid = line[start_guid:end_guid]
                # print('yaml_utils::identify_guid - ' + guid)
                return guid
    return ''