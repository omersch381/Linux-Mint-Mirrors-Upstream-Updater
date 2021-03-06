import sys

from arch_parser import ArchParser
from config import Config
from fedora_parser import FedoraParser
from logger import Logger
from mint_parser import MintParser
from constants import *

logger = Logger(__name__)
logger = logger.logger


def get_parser_from_config(config):
    """Gets the parser from the config file.

    :param config: the user's configuration preferences.

    :returns parser: a pointer to the required parser with its parameters:
            mirrors_url - the url which we will get the upstream mirrors from.
            upstream_mirrors_location - the path of the upstream mirrors file.
    """

    if config[DEFAULT][OPERATING_SYSTEM] == FEDORA_PARSER:
        logger.debug(f'Returning {FEDORA_PARSER} parser from ' + __name__)
        return FedoraParser()

    if config[DEFAULT][OPERATING_SYSTEM] == ARCH_PARSER:
        parser = ArchParser
    elif config[DEFAULT][OPERATING_SYSTEM] == MINT_PARSER:
        parser = MintParser
    else:
        exit_parser()

    mirrors_url = config[DEFAULT][MIRRORS_URL]
    upstream_mirrors_location = config[DEFAULT][UPSTREAM_MIRRORS_LOCATION]

    logger.debug(f'Returning {parser} parser from ' + __name__ + f' with {mirrors_url} as the'
                                                                 f' mirrors url and as {upstream_mirrors_location} '
                                                                 f'as the upstream mirrors location')
    return parser(mirrors_url, upstream_mirrors_location)


def get_parser_from_cli(provided_parser, url, upstream_location):
    """Gets the parser from the command line.

    This function gets the parser by the command the user have entered.

    :param provided_parser: the parser the user chose.
    :param url: the default url for the upstream mirrors (being
        taken from the default values file)
    :param upstream_location: the upstream mirrors file path. Might be
        taken from the default values file or overridden by the user.
    :returns parser/provided_parser: the parser the user chose.

    Ex for a cli command: python mirrors_manager.py --parser arch --mirrors_location PATH
    """

    if 'None' in url:  # Fedora
        logger.debug(f'Returning {provided_parser} parser from ' + __name__)
        return provided_parser()
    if upstream_location:  # if the user chooses a different mirror location
        parser = provided_parser(url, upstream_location)
    else:
        parser = provided_parser(url)

    logger.debug('Returning {parser_name} parser from ' + __name__.format(parser_name=parser.name))
    return parser


def exit_parser():
    print('Please insert a valid operation system which we support. For further details, please '
          'take a look at our README file.')
    logger.debug('Exit with exit_parser')
    sys.exit()


def get_parser_and_scan_type(args):
    """Gets parser and scan type.

    This function get the parser by either the config file (if flag "-c" or
    "--config" specified), or by the cli command.
    A supported parser has to be specified in at least one of the options.

    :param args: the arguments the user have entered in the command line.
    :returns parser, scan_type: the parser the user has chosen and the scan_type.
        If the user didn't choose daily_scan explicitly, it returns a full_scan.
    """

    config = Config()

    if args.config or config.all_configurations_are_valid() is False:
        config.start_config()
        parser = get_parser_from_config(config.config)
        scan_type = FULL_SCAN if parser.name not in PARSERS_WHICH_NOT_REQUIRE_PING else None
        return parser, scan_type

    else:
        # Parser handling - we get the parser from the user
        parser = get_parser_from_config(config.config) if not args.parser else args.parser

        if parser.name == MINT_PARSER:
            provided_parser = MintParser
            provided_section = MINT_SECTION
        elif parser.name == ARCH_PARSER:
            provided_parser = ArchParser
            provided_section = ARCH_SECTION
        elif parser.name == FEDORA_PARSER:
            provided_parser = FedoraParser
            provided_section = FEDORA_SECTION
        else:
            exit_parser()

        if args.mirrors_location:
            upstream_location = args.mirrors_location
        else:
            upstream_location = config.get_default_value_of(provided_section, UPSTREAM_MIRRORS_LOCATION)
        logger.debug(f'Upstream mirrors location is {upstream_location}')

        parser = get_parser_from_cli(provided_parser=provided_parser,
                                     url=config.get_default_value_of(provided_section, MIRRORS_URL),
                                     upstream_location=upstream_location)

        # Scan type handling
        scan_type = None
        if args.scan_type:  # If the user provided an explicit scan_type param
            scan_type = DAILY_SCAN if args.scan_type.lower() in ['daily_scan', 'daily scan'] else FULL_SCAN

        else:  # If they didn't provide an explicit scan_type param
            full_scan_frequency = config.get_config_of(DEFAULT, FULL_SCAN_FREQUENCY)
            num_of_runs_since_full_scan = config.get_config_of(DEFAULT, NUM_OF_RUNS_SINCE_FULL_SCAN)

            if int(num_of_runs_since_full_scan) >= int(full_scan_frequency):
                scan_type = FULL_SCAN
                config.change_config_value(DEFAULT, NUM_OF_RUNS_SINCE_FULL_SCAN, "0")

        if not scan_type and parser.name not in PARSERS_WHICH_NOT_REQUIRE_PING:
            scan_type = DAILY_SCAN

        logger.debug(f'Scan type is {scan_type}')
        return parser, scan_type
