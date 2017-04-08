class SymbolicData

    def __init__(self):
        self.data = {'entities' : {} }
        self.total_entities = 0

    def add_entity(self, entity):
        entity.id = self.total_entities
        self.data['entities'][self.total_entities] = entity
        self.total_entities = self.total_entities + 1

    def update_entity(self, entity):
        self.data['entities'][entity.id] = entity

    def get_entity(self, id):
        return self.data['entities'][id]

