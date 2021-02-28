import urllib.request as request
from shutil import copyfile
from parser import Parser
from bs4 import BeautifulSoup


class MintParser(Parser):
    """This class handles the Mint mirrors.

    It receives a url, sends a get request (similar to wget), parses the html file into mirrors.
    It also switches the default mirror to the fastest.
    """

    def __init__(self, url, upstream_package_file_path='/etc/apt/sources.list.d/official-package-repositories.list'):
        self._url = url
        self._upstream_package_file_path = upstream_package_file_path

    @property
    def url(self):
        return self._url

    def parse_mirrors(self):
        html_content = request.urlopen(self._url)

        soup = BeautifulSoup(html_content, 'html.parser')

        list_of_objects = soup.find_all('td')

        list_of_objects = [html_object for html_object in list_of_objects if "http" in str(html_object) and
                           'a href' not in str(html_object)]

        return [str(html_object).split('/')[2] for html_object in list_of_objects]

    def switch_to_fastest_mirror(self, mirror):
        # Saving a backup of the configuration file
        copyfile(self._upstream_package_file_path, self._upstream_package_file_path + '.bak')

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
