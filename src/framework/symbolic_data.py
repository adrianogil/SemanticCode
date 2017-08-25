class SymbolicEntity:
    def __init__(self):
        self.id = -1
        self.dict = {'id' : -1 }

    def set_id(self, new_id):
        self.id = new_id
        self.dict['id'] = new_id

    def add_value(self, key, value):
        self.dict[key] = value

    def get_value(self, key, value):
        return self.dict[key]

    def to_dict(self):
        return self.dict

class SymbolicData:

    def __init__(self):
        self.data = {'entities' : {} }
        self.total_entities = 0

    def create_symbolic_entity(self, file_path):
        entity = SymbolicEntity()
        entity.add_value('source_file', file_path)

        return entity

    def add_entity(self, entity):
        if entity.id == -1:
            entity.set_id(self.total_entities)
            self.total_entities = self.total_entities + 1

        self.data['entities'][entity.id] = entity.to_dict()

        print('add_entity ' + str(entity.to_dict()))

    def get_entity(self, id):
        return self.data['entities'][id]



