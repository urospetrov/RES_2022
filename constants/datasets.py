from constants.codes import *


class Dataset(Enum):
    Dataset_1 = (Code.CODE_ANALOG, Code.CODE_DIGITAL)
    Dataset_2 = (Code.CODE_CUSTOM, Code.CODE_LIMITSET)
    Dataset_3 = (Code.CODE_SINGLENOE, Code.CODE_MULTIPLENODE)
    Dataset_4 = (Code.CODE_CONSUMER, Code.CODE_SOURCE)
