from constants.codes import Code


class ReceiverProperty:
    def __init__(self, code: Code, receiver_value: int):  # pragma: no cover
        self.code = code
        self.receiver_value = receiver_value

    def __str__(self):  # pragma: no cover
        return f'<Code: {self.code}  Value: {self.receiver_value}>'
