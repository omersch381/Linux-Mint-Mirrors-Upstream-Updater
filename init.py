import sys

from arch_parser import ArchParser
from config import Config
from fedora_parser import FedoraParser
from mint_parser import MintParser
from constants import *


def get_parser_from_config(config):
    if config[DEFAULT][OPERATING_SYSTEM] == FEDORA_PARSER:
        return FedoraParser()

    if config[DEFAULT][OPERATING_SYSTEM] == ARCH_PARSER:
        parser = ArchParser
    elif config[DEFAULT][OPERATING_SYSTEM] == MINT_PARSER:
        parser = MintParser
    else:
        exit_parser()

    mirrors_url = config[DEFAULT][MIRRORS_URL]
    upstream_mirrors_location = config[DEFAULT][UPSTREAM_MIRRORS_LOCATION]

    return parser(mirrors_url, upstream_mirrors_location)


def get_parser_from_user(provided_parser, url, upstream_location):
    if not url:  # Fedora
        return provided_parser()
    if upstream_location:  # if the user chooses a different mirror location
        parser = provided_parser(url, upstream_location)
    else:
        parser = provided_parser(url)
    return parser


def exit_parser():
    print('Please insert a valid operation system which we support. For further details, please '
          'take a look at our README file.')
    sys.exit()


def get_parser_and_scan_type(args):
    config = Config()

    if args.config:
        config.start_config()
        parser = get_parser_from_config(config.config)
        return parser, FULL_SCAN

    else:  # We get the parser from the user
        if not args.parser:
            exit_parser()

        if args.parser.lower() == MINT_PARSER:
            provided_parser = MintParser
            provided_section = MINT_SECTION
        elif args.parser.lower() == ARCH_PARSER:
            provided_parser = ArchParser
            provided_section = ARCH_SECTION
        elif args.parser.lower() == FEDORA_PARSER:
            provided_parser = FedoraParser
            provided_section = FEDORA_SECTION
        else:
            exit_parser()

        if args.mirrors_location:
            upstream_location = args.mirrors_location
        else:
            upstream_location = config.get_default_value_of(provided_section, UPSTREAM_MIRRORS_LOCATION)

        parser = get_parser_from_user(provided_parser=provided_parser,
                                      url=config.get_default_value_of(provided_section, MIRRORS_URL),
                                      upstream_location=upstream_location)

        if args.scan_type and args.scan_type.lower() in ['daily_scan', 'daily scan']:
            scan_type = DAILY_SCAN
        else:
            scan_type = FULL_SCAN

        return parser, scan_type
