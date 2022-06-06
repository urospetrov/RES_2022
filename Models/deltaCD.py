from collection_description import CollectionDescription

class DeltaCD:

    def __init__(self, add:list, update:list):
        self.add = add
        self.update = update