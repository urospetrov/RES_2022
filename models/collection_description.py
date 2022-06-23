from constants.datasets import Dataset
from models.historical_collection import HistoricalCollection


class CollectionDescription:
    def __init__(self, id: int, dataset: Dataset, historical_collection: HistoricalCollection):  # pragma: no cover
        self.id = id
        self.dataset = dataset
        self.historical_collection = historical_collection
