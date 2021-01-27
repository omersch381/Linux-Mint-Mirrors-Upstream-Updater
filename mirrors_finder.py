from arg_parser import ArgParser
from mint_parser import MintParser
from best_mirrors import FastestMirrors


def write_mirrors_list_to_file(given_list_of_mirrors):
    """This method writes the final and sorted fastest mirrors to a file.

    :param given_list_of_mirrors: The sorted mirrors that we have found.
    """

    with open('mirrors_list', 'w') as file_handler:
        for mirror in given_list_of_mirrors:
            file_handler.write('%s\n' % mirror)


def get_less_mirrors():
    with open('small_mirror_list', 'r') as file_handler:
        mirrors = file_handler.readlines()
        return mirrors

# args = ArgParser().parse_args()
# mint_parser = MintParser(url=args.url)

# For testing only. In any other case, just comment the next 2 lines
# and uncomment the previous 2 lines.
url = 'https://www.linuxmint.com/mirrors.php'
parser = MintParser(url=url)

#list_of_mirrors = parser.parse_mirrors()

list_of_mirrors = get_less_mirrors()

pinger = FastestMirrors(list_of_mirrors)
sorted_mirrors = pinger.sorted_mirrors

print(sorted_mirrors)

write_mirrors_list_to_file(sorted_mirrors)
