from abc import ABCMeta, abstractmethod


class DCLoad(metaclass=ABCMeta):
    REGEX_ID = "DCLOAD"

    def __init__(self, instrument):
        self.instrument = instrument

    # this is just declaring the methods that the dcload driver must implement
    @abstractmethod
    def idn(self) -> str:
        pass

    @abstractmethod
    def get_identity(self) -> str:
        pass
