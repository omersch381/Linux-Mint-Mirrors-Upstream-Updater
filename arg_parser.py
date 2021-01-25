import argparse


class ArgParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._args = None

    def parse_args(self):
        self._parser.add_argument("url", help="The URL where all the mirrors are located")
        self._args = self._parser.parse_args()
        return self._args

    @property
    def args(self):
        return self._args
