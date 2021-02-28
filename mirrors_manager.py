# from functools import cache
import os
from arch_parser import ArchParser
from arg_parser import ArgParser
from cache import CacheManager
from config import Config
from fedora_parser import FedoraParser
from mint_parser import MintParser
from best_mirrors import FastestMirrors
from docker_images import build_docker_file

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
url = 'https://archlinux.org/mirrorlist/all/'
parser = FedoraParser()
parser.parse_mirrors()


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

    pinger = FastestMirrors()
    pinger.sort_mirrors_by_ping_avg(mirrors=list_of_mirrors)
    sorted_mirrors = pinger.sorted_mirrors

    cache = CacheManager(fastest_mirrors=pinger, cache_size=cache_size)
    cache.set_cached_mirrors_from_list()
    cache.save()

    parser.switch_to_fastest_mirror(mirror=next(iter(cache.cache_mirrors.keys())))
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
    example_for_testing = ['mirrors.evowise.com', 'mirror.rackspace.com', 'mirror.rackspace.com',
                           'mirror.aarnet.edu.au', 'archlinux.mirror.digitalpacific.com.au',
                           'archlinux.mirror.digitalpacific.com.au']

    run_daily(example_for_testing, cache_size=cache_size)

    # write_mirrors_list_to_file(run_daily(example_for_testing, cache_size=20))
    # or
    # write_mirrors_list_to_file(run_daily(list_of_mirrors, cache_size=20))


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def daily_scan(cache_size=20, max_mirror_ping_avg=1.0):
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
        cache = CacheManager(fastest_mirrors=FastestMirrors(), cache_size=cache_size)
        cache.load(max_mirror_ping_time=max_mirror_ping_avg)
        run_daily(cache.cache_mirrors.keys(), cache_size=cache_size)


daily_scan()


def choose_docker_image(image_type='mint'):
    """
    Chooses a docker file to build & builds it.

    Note: After executing this function we will have an image with our project inside every container that is built
            with this image.

    this function execution is similar to the following command for example (executed from our project dir):
        docker build -f docker_files/mint/Dockerfile . -t <name of our tag>

    Args:
        image_type (str): the image type, e.g.: one of [arch, kali, fedora, mint]
    """
    working_dir = path.abspath(os.getcwd())
    docker_file_path = f"{working_dir}/docker_files"

    if image_type == 'mint':
        docker_file_path = f"{docker_file_path}/mint/Dockerfile"
        tag = "mint"
    elif image_type == 'fedora':
        docker_file_path = f"{docker_file_path}/fedora/Dockerfile"
        tag = "fedora"
    elif image_type == 'kali':
        docker_file_path = f"{docker_file_path}/kali/Dockerfile"
        tag = "kali"
    else:
        docker_file_path = f"{docker_file_path}/arch/Dockerfile"
        tag = "arch"

    return build_docker_file(path=docker_file_path, tag=tag)
