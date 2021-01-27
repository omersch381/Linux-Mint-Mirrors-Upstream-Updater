import urllib.request as request
from bs4 import BeautifulSoup


class MintParser:
    """This class gets the Mint mirrors.

    It receives a url, sends a get request (similar to wget), parses the html file into mirrors.
    """

    def __init__(self, url):
        self._url = url

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

    def switch_to_fastest_mirror(self, upstream_package_file_path, mirror):
        with open(upstream_package_file_path, 'r') as file_handler:
            upstream_packages_file = file_handler.readlines()

        for i in range(len(upstream_packages_file)):
            if 'upstream import backport' in upstream_packages_file[i]:
                line = upstream_packages_file[i].split()
                for j in range(len(line)):
                    if 'http' in line[j]:
                        line[j] = 'http://' + mirror
        print(upstream_packages_file)

