import urllib.request as request
from shutil import copyfile

from config import Config
from logger import Logger
from parser import Parser
from bs4 import BeautifulSoup
from constants import *

logger = Logger(__name__)
logger = logger.logger
config = Config()


class MintParser(Parser):
    """This class handles the Mint mirrors.

    It receives a url, sends a get request (similar to wget), parses the html file into mirrors.
    It also switches the default mirror to the fastest.
    """

    def __init__(self, url, upstream_package_file_path=config.get_default_value_of(MINT_SECTION,
                                                                                   UPSTREAM_MIRRORS_LOCATION)):
        self._url = url
        self._upstream_package_file_path = upstream_package_file_path

    @property
    def url(self):
        return self._url

    @property
    def name(self):
        return MINT_PARSER

    def parse_mirrors(self):
        """Gets the mirrors and parses them.

        This method gets the Mint upstream mirrors with an http request and
        parses the html into list of mirrors.

        :returns (list): parsed_mirrors
        """

        html_content = request.urlopen(self._url)

        soup = BeautifulSoup(html_content, 'html.parser')

        list_of_objects = soup.find_all('td')

        list_of_objects = [html_object for html_object in list_of_objects if "http" in str(html_object) and
                           'a href' not in str(html_object)]

        parsed_mirrors = [str(html_object).split('/')[2] for html_object in list_of_objects]
        logger.debug(f'The mirrors we parsed are:\n{parsed_mirrors}')

        return parsed_mirrors

    def switch_to_fastest_mirror(self, mirror):
        """Switches to fastest mirror.

        This method gets the fastest mirror, backs up the upstream mirrors file and puts the
        fastest mirror as the default mirror.

        :param mirror: the fastest mirror which was returned from our pinger.
        """

        # Saving a backup of the configuration file
        copyfile(self._upstream_package_file_path, self._upstream_package_file_path + '.bak')
        logger.debug('Original upstream file was at ' + self._upstream_package_file_path)
        logger.debug('Upstream file was backed up at ' + self._upstream_package_file_path + '.bak')

        with open(self._upstream_package_file_path, 'r') as file:
            filedata = file.read()

        with open(self._upstream_package_file_path, 'w') as file:
            for line in filedata.splitlines():
                if 'upstream import backport' in line:
                    words = line.split()
                    old_mirror = ''
                    for word in words:
                        if 'http' in word:
                            old_mirror = word
                    mirror = 'http://' + mirror
                    line = line.replace(old_mirror, mirror) + '\n'
                    file.write(line)
                    continue
                line += '\n'
                file.write(line)
