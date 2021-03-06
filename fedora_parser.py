from shutil import copyfile

from config import Config
from logger import Logger
from parser import Parser
from constants import *

logger = Logger(__name__)
logger = logger.logger
config = Config()


class FedoraParser(Parser):
    """This class handles the Fedora mirrors.

    As Fedora has a flag, 'fastestmirror', which is already implemented, we simply use it.
    We put that flag in the end of upstream mirrors file.
    """

    def parse_mirrors(self):
        pass

    def switch_to_fastest_mirror(self,
                                 mirror=None,
                                 upstream_package_file_path=config.get_default_value_of(FEDORA_SECTION,
                                                                                        UPSTREAM_MIRRORS_LOCATION)):

        # Saving a backup of the configuration file
        copyfile(upstream_package_file_path, upstream_package_file_path + '.bak')
        logger.debug('Original upstream file was at ' + upstream_package_file_path)
        logger.debug('Upstream file was backed up at ' + upstream_package_file_path + '.bak')

        was_fastest_mirror_option_added = False
        with open(upstream_package_file_path, 'r') as file:
            content = file.readlines()
            if 'fastestmirror' in content:
                was_fastest_mirror_option_added = True

        if not was_fastest_mirror_option_added:
            with open(upstream_package_file_path, 'a') as file:
                file.write('fastestmirror=1')
