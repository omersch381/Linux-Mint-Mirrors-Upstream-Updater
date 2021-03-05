import os
from os import path

from arg_parser import ArgParser
from best_mirrors import FastestMirrors
from cache import CacheManager
from constants import *
from docker_images import build_docker_file
from init import get_parser_and_scan_type
from logger import Logger

logger = Logger(__name__)
logger = logger.logger


def write_mirrors_list_to_file(given_list_of_mirrors):
    """This method writes the final and sorted fastest mirrors to a file.

    :param given_list_of_mirrors: The sorted mirrors that we have found.
    """

    with open('mirrors_list', 'w') as file_handler:
        file_handler.write(str(given_list_of_mirrors))


def run_daily(parser, list_of_mirrors, cache_size=20):
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

    logger.debug('run daily')
    pinger = FastestMirrors()
    pinger.sort_mirrors_by_ping_avg(mirrors=list_of_mirrors)
    sorted_mirrors = pinger.sorted_mirrors

    cache = CacheManager(fastest_mirrors=pinger, cache_size=cache_size)
    cache.set_cached_mirrors_from_list()
    cache.save()

    parser.switch_to_fastest_mirror(mirror=next(iter(cache.cache_mirrors.keys())))
    return sorted_mirrors


def full_scan(parser, cache_size=20):
    """Pings all the upstream mirrors.

    This function uses a provided parser and do the following operations:

            Gets all the upstream mirrors

            Calls run_daily() function to ping and handle post-ping operations.

            Saves all the mirrors to file.

    :param parser: the parser that will be used. (Parser-like class)
    :param cache_size: the size of the mirrors to be saved in cache. (int)
    """

    logger.debug('full scan')

    list_of_mirrors = parser.parse_mirrors()
    # after testing we should comment the next line and uncomment the previous one
    example_for_testing = ['mirrors.evowise.com']

    run_daily(parser, example_for_testing, cache_size=cache_size)

    # write_mirrors_list_to_file(run_daily(example_for_testing, cache_size=20))
    # or
    # write_mirrors_list_to_file(run_daily(list_of_mirrors, cache_size=20))


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def daily_scan(parser, cache_size=20, max_mirror_ping_avg=1.0):
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

    logger.debug('daily scan')

    if not path.exists('cached_mirrors') or file_len('cached_mirrors') < cache_size / 2:
        full_scan()
    else:
        cache = CacheManager(fastest_mirrors=FastestMirrors(), cache_size=cache_size)
        cache.load(max_mirror_ping_time=max_mirror_ping_avg)
        run_daily(parser, cache.cache_mirrors.keys(), cache_size=cache_size)


def choose_docker_image(image_type='mint'):
    """
    Chooses a docker file to build & builds it.

    Note: After executing this function we will have an image with our project inside every container that is built
            with this image.

    this function execution is similar to the following command for example (executed from our project dir):
        docker build -f docker_files/mint/Dockerfile . -t <name of our tag>

    Args:
        image_type (str): the image type, e.g.: one of [arch, fedora, mint]
    """
    working_dir = path.abspath(os.getcwd())
    docker_file_path = f"{working_dir}/docker_files"

    if image_type == MINT_PARSER:
        docker_file_path = f"{docker_file_path}/{MINT_PARSER}/Dockerfile"
        tag = MINT_PARSER
    elif image_type == FEDORA_PARSER:
        docker_file_path = f"{docker_file_path}/{FEDORA_PARSER}/Dockerfile"
        tag = FEDORA_PARSER
    else:
        docker_file_path = f"{docker_file_path}/{ARCH_PARSER}/Dockerfile"
        tag = ARCH_PARSER

    return build_docker_file(path=docker_file_path, tag=tag)


args = ArgParser().parse_args()

parser, scan_type = get_parser_and_scan_type(args=args)

if scan_type == FULL_SCAN:
    full_scan(parser=parser)
else:
    daily_scan(parser=parser)
