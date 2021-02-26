import abc


class Parser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse_mirrors(self):
        pass

    @abc.abstractmethod
    def switch_to_fastest_mirror(self, upstream_package_file_path, mirror):
        pass
