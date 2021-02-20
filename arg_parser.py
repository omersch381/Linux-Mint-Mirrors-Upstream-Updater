import argparse


class ArgParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser(epilog=
                                               """Scan types might be full scans or daily scans.
                                               A full scan would run over all the mirrors and would
                                               save the fastest (by their average ping time) to
                                                the cache file.
                                                Daily scan would run over the cached mirrors.
                                                More details can be found at the README file.""")
        self._args = None

    def parse_args(self):
        # self._parser.add_argument("url", help="The URL where all the mirrors are located")
        self._parser.add_argument("parser", help="The parser which will get and parse the mirrors.")
        self._parser.add_argument("scan_type", help="The type of the scan."
                                                    " Might be a full scan or a daily scan")
        self._args = self._parser.parse_args()
        return self._args

    @property
    def args(self):
        return self._args
