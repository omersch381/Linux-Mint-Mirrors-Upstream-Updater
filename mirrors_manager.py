import os
from os import path

from arg_parser import ArgParser
from best_mirrors import FastestMirrors
from cache import CacheManager
from config import Config
from constants import *
from docker_images import build_docker_file
from init import get_parser_and_scan_type
from logger import Logger

logger = Logger(__name__)
logger = logger.logger


class MirrorsManager:

    def __init__(self, args):
        self._args = args
        self._num_of_runs_since_full_scan = 0
        self._parser = None
        self._scan_type = None
        self._config = None
        self._list_of_mirrors = None

    def run(self):
        self._config = Config()
        self._parser, self._scan_type = get_parser_and_scan_type(args=self._args)
        self._parser.parse_mirrors()

        default_cache_size = self._config.get_config_of(CACHE, CACHE_SIZE)

        if self._scan_type == FULL_SCAN:
            self.full_scan(default_cache_size)
        elif self._scan_type == DAILY_SCAN:
            self.daily_scan(default_cache_size)
        elif not self._scan_type:
            self._parser.switch_to_fastest_mirror()  # others, such as None
        else:
            raise RuntimeError('Invalid scan type, exiting...')

        num_of_runs_since_full_scan = self._config.get_config_of(DEFAULT, NUM_OF_RUNS_SINCE_FULL_SCAN)
        next_num_of_runs = int(num_of_runs_since_full_scan) + 1
        self._config.change_config_value(DEFAULT, NUM_OF_RUNS_SINCE_FULL_SCAN, str(next_num_of_runs))

    def _write_mirrors_list_to_file(self, list_of_mirrors_to_write=None):
        """This method writes the final and sorted fastest mirrors to a file.
        """

        if not list_of_mirrors_to_write:
            list_of_mirrors_to_write = self._list_of_mirrors

        with open(MIRRORS_FILE_NAME, 'w') as file_handler:
            file_handler.write(str(list_of_mirrors_to_write))
            logger.debug('Writing the next mirrors to file:\n' + str(list_of_mirrors_to_write))

    def _run_daily(self, list_of_mirrors=None, cache_size=20):
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

        if not list_of_mirrors:
            list_of_mirrors = self._list_of_mirrors

        pinger = FastestMirrors()
        pinger.sort_mirrors_by_ping_avg(mirrors=list_of_mirrors)
        sorted_mirrors = pinger.sorted_mirrors

        cache = CacheManager(fastest_mirrors=pinger, cache_size=cache_size)
        cache.set_cached_mirrors_from_list()
        cache.save()

        self._parser.switch_to_fastest_mirror(mirror=next(iter(cache.cache_mirrors.keys())))
        return sorted_mirrors

    def full_scan(self, cache_size=20):
        """Pings all the upstream mirrors.

        This function uses a provided parser and do the following operations:

                Gets all the upstream mirrors

                Calls run_daily() function to ping and handle post-ping operations.

                Saves all the mirrors to file.

        :param parser: the parser that will be used. (Parser-like class)
        :param cache_size: the size of the mirrors to be saved in cache. (int)
        """

        logger.debug('full scan')
        if hasattr(self._parser, 'list_of_mirrors'):
            list_of_mirrors = self._parser.list_of_mirrors
        # logger.debug('list of mirrors:\n' + list_of_mirrors)
        # TODO oschwart: after testing we should comment the next line and uncomment the previous one
        example_for_testing = ['mirrors.evowise.com']

        self._run_daily(example_for_testing, cache_size=cache_size)

        if hasattr(self._parser, 'list_of_mirrors'):
            self._write_mirrors_list_to_file(example_for_testing)
        # or
        # if list_of_mirrors:
        #     self._write_mirrors_list_to_file(list_of_mirrors)

    def _file_len(self, file_name):
        with open(file_name) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def daily_scan(self, cache_size=20, max_mirror_ping_avg=1.0):
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

        if not path.exists(CACHED_MIRRORS_FILE_NAME) or self._file_len(CACHED_MIRRORS_FILE_NAME) < int(cache_size) / 2:
            logger.debug('There was not a cached mirrors file, or number of cached mirrors'
                         ' entries was less than half of the given cache_size')
            self.full_scan()
        else:
            cache = CacheManager(fastest_mirrors=FastestMirrors(), cache_size=cache_size)
            cache.load(max_mirror_ping_time=max_mirror_ping_avg)
            self._run_daily(cache.cache_mirrors.keys(), cache_size=cache_size)

    def choose_docker_image(self, image_type='mint'):
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

        logger.debug(f'The docker file path was {docker_file_path}, building a docker image of {tag}')
        return build_docker_file(path=docker_file_path, tag=tag)
