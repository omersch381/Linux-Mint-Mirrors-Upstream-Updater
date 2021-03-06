import abc


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_mirrors(self):
        pass

    @property
    def name(self):
        pass

    @abc.abstractmethod
    def switch_to_fastest_mirror(self, mirror):
        pass
