from LastRunMirrors import LastRunMirrors
from CurrentMirrorsGenerator import CurrentMirrorsGenerator
from bs4 import BeautifulSoup
import urllib.request as request
from ArgParser import ArgParser


def write_final_list_to_file(given_list_of_mirrors):
    """This method writes the final and sorted fastest mirrors to a file.

    :param given_list_of_mirrors: The sorted mirrors that we have found.
    """

    with open('mirrors_list', 'w') as file_handler:
        for mirror in given_list_of_mirrors:
            file_handler.write('%s\n' % mirror)


def generate_final_list(list_of_mirrors, list_of_mirrors_from_last_run):
    # The mirrors were saved in this format: http://<mirrors-domain>/path
    current_mirrors_list = sorted(mirror.split('/')[2] for mirror in list_of_mirrors)

    # The mirrors were saved as a list of tuples with this format: [(<mirror_name>,<time>),(...)]
    last_mirrors_list = sorted([mirror[0] for mirror in list_of_mirrors_from_last_run])

    new_mirrors_list = list(set(current_mirrors_list) - set(last_mirrors_list))
    # TODO: continue the method - mirrors blacklist, which will be cleared once in every 50 runs


# args = ArgParser().parse_args()
# html_content = request.urlopen(args.url)

# For testing only. In any other case, just comment the next 2 lines
# and uncomment the previous 2 lines.
url = 'https://www.linuxmint.com/mirrors.php'
html_content = request.urlopen(url)

soup = BeautifulSoup(html_content, 'html.parser')

list_of_objects = soup.find_all()

# Each object contains a long string which contains the mirror
linux_mint_mirrors_parser = CurrentMirrorsGenerator(list_of_objects)
current_list_of_mirrors = linux_mint_mirrors_parser.parse_mirrors()

list_of_mirrors_from_last_run = LastRunMirrors().get_list_of_mirrors()

final_list = generate_final_list(current_list_of_mirrors, list_of_mirrors_from_last_run)

write_final_list_to_file(final_list)
