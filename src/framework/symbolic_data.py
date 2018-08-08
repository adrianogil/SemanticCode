class SymbolicEntity:
    def __init__(self):
        self.id = -1
        self.dict = {'id' : -1 }
        self.position_in_file = ((-1,-1),(-1,-1))

    def set_id(self, new_id):
        self.id = new_id
        self.dict['id'] = new_id

    def add_value(self, key, value):
        self.dict[key] = value

    def get_value(self, key, value):
        return self.dict[key]

    def to_dict(self):
        return self.dict

    def set_position(self, start, end):
        self.position_in_file = (start, end)

    def is_in_position(self, start, end):
        line_start = self.position_in_file[0][0]
        col_start = self.position_in_file[0][1]

        line_end = self.position_in_file[1][0]
        col_end = self.position_in_file[1][1]

        if line_start == end[0] and col_start < end[1]:
            return True
        elif line_end == start[0] and col_end > start[1]:
            return True
        elif line_start > start[0] and line_start < end[0]:
            return True
        elif line_end > start[0] and line_end > end[0]:
            return True

        return False

class SymbolicData:

    def __init__(self):
        self.data = {'entities' : {} }
        self.total_entities = 0
        self.entities_by_line = {}

    def create_symbolic_entity(self, file_path):
        entity = SymbolicEntity()
        entity.add_value('source_file', file_path)

        return entity


    def get_entities_in_position(self, position_start, position_end):
    # Expects to receive (line, col) as position
        found_entities = []

        line_start = position_start[0]
        line_end = position_end[0]
        for l in xrange(line_start, line_end+1):
            if l in self.entities_by_line:
                for e in self.entities_by_line[l]:
                    if e.is_in_position(position_start, position_end):
                        found_entities.append(e)

        return found_entities


    def add_entity(self, entity):
        if entity.id == -1:
            entity.set_id(self.total_entities)
            self.total_entities = self.total_entities + 1
        line_start = entity.position_in_file[0][0]
        line_end = entity.position_in_file[1][0]

        # print('add_entity - entity_position:  ' + str(entity.position_in_file))
        # print('add_entity - line_start ' + str(line_start) + ' line_end ' + str(line_end))

        if line_start  != -1 and line_end != -1:
            for l in xrange(line_start, line_end+1):
                if l in self.entities_by_line:
                    entity_list = self.entities_by_line[l]
                    entity_list.append([entity])
                    self.entities_by_line[l] = entity_list
                else:
                    self.entities_by_line[l] = [entity]

        self.data['entities'][entity.id] = entity.to_dict()

        # print('add_entity ' + str(entity.to_dict()))

    def get_entity(self, id):
        return self.data['entities'][id]



