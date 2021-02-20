from functools import cache

from arg_parser import ArgParser
from cache import CacheManager
from config import Config
from mint_parser import MintParser
from best_mirrors import FastestMirrors

from os import path


def write_mirrors_list_to_file(given_list_of_mirrors):
    """This method writes the final and sorted fastest mirrors to a file.

    :param given_list_of_mirrors: The sorted mirrors that we have found.
    """

    with open('mirrors_list', 'w') as file_handler:
        file_handler.write(str(given_list_of_mirrors))


# config = Config()

# args = ArgParser().parse_args()
# parser = get_parser(args.parser)

# For testing only. In any other case, just comment the next 2 lines
# and uncomment the previous 2 lines.
url = 'https://www.linuxmint.com/mirrors.php'
parser = MintParser(url=url)


def run_daily(list_of_mirrors, cache_size=20):
    """Pings the provided mirrors and handles post-ping operations.

    This function pings the provided operations and
    handles the following post-ping operations:
        Saves to cache: the cache will be used on daily scans.

        Adds to blacklist: mirrors that will be added to blacklist
        will not be pinged on daily scans.

        Switches to fastest mirror: sets the fastest mirror as the
        default upstream mirror.

    :param list_of_mirrors: the mirrors that should be pinged. (list)
    :param cache_size: the size of the mirrors to be saved in cache. (int)
    :returns sorted_mirrors: the result of the ping operation. (dict)
    """

    pinger = FastestMirrors(list_of_mirrors)
    sorted_mirrors = pinger.sorted_mirrors

    cache = CacheManager(cache_size=cache_size)
    cache.set_cached_mirrors_from_list(sorted_mirrors)
    cache.save()

    # blacklist.....
    # ....
    # ....

    # parser.switch_to_fastest_mirror(
    #     upstream_package_file_path='/etc/apt/sources.list.d/official-package-repositories.list',
    #     mirror='mirrors.evowise.com')
    return sorted_mirrors


def full_scan(cache_size=20):
    """Pings all the upstream mirrors.

    This function uses a provided parser and do the following operations:

            Gets all the upstream mirrors

            Calls run_daily() function to ping and handle post-ping operations.

            Saves all the mirrors to file.

    :param parser: the parser that will be used. (Parser-like class)
    :param cache_size: the size of the mirrors to be saved in cache. (int)
    """

    # NOTE: we still don't get the parser from the user as we didn't implement the
    # Argparser fully, but it will be implemented soon.

    list_of_mirrors = parser.parse_mirrors()

    # after testing we should comment the next line and uncomment the previous one
    example_for_testing = ['mirrors.evowise.com', 'mirrors.layeronline.com', 'muug.ca', 'mirror.scd31.com',
                           'mirror.csclub.uwaterloo.ca', 'mirrors.advancedhosters.com']

    run_daily(example_for_testing, cache_size=20)

    # write_mirrors_list_to_file(run_daily(example_for_testing, cache_size=20))
    # or
    # write_mirrors_list_to_file(run_daily(list_of_mirrors, cache_size=20))


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def daily_scan(cache_size=20):
    """Pings the cache file and handles post-ping operations.

    This function loads the cached mirrors from the cache file
    and do the following operations:

            Calls run_daily() function to ping and handle post-ping operations.

            Saves all the mirrors to file.

    In case there is no cache file or the cache file contains less mirrors than
    the half of the provided cache size, it calls a full run again.

    :param parser: the parser that will be used. (Parser-like class)
    :param cache_size: the size of the mirrors to be saved in cache. (int)
    """

    # NOTE: we still don't get the parser from the user as we didn't implement the
    # Argparser fully, but it will be implemented soon.

    if not path.exists('cached_mirrors') or file_len('cached_mirrors') < cache_size / 2:
        full_scan()
    else:
        cache = CacheManager(cache_size=cache_size)
        cache.load()
        run_daily(cache.cache_mirrors.keys(), cache_size=cache_size)


daily_scan()
