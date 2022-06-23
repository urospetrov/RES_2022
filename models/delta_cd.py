from models.collection_description import CollectionDescription


class DeltaCD:
    def __init__(self, add: list[CollectionDescription], update: list[CollectionDescription]):  # pragma: no cover
        self.add = add
        self.update = update
