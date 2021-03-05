import configparser
import sys
from constants import *


class Config:
    """Configures the user preferences.
    """

    def __init__(self):
        self._config_file_name = CONFING_FILE_NAME
        self._config = configparser.ConfigParser()
        self._default_values = self.load_default_values()

    @property
    def config(self):
        return self._config

    def start_config(self):
        config_type = input('Welcome to Mirrors Manager!\nWould you like to'
                            ' configure all preferences or just the mandatory ones? '
                            '[f/full/m/mandatory/e/exit]\n')
        is_valid = config_type.lower() in ['f', 'full', 'm', 'mandatory', 'e', 'exit']

        while not is_valid:
            config_type = input('\nSorry, this choice was not one of our valid choices.'
                                ' Please choose a valid one:\n'
                                'Would you like to configure all preferences or just the'
                                ' mandatory ones? [f/full/m/mandatory/e/exit]\n')
            is_valid = config_type.lower() in ['f', 'full', 'm', 'mandatory', 'e', 'exit']

        if config_type.lower() in ['full', 'f']:
            self.full_config()
        elif config_type.lower() in ['mandatory', 'm']:
            self.mandatory_config()
        else:
            sys.exit()

        with open(self._config_file_name, 'w') as configfile:
            self._config.write(configfile)

        print('\nLet\'s start pinging....')

    def _handle_cache_size(self):
        cache_size = input('\nWhat should be your cache size? (the number of mirrors '
                           'to be saved in the cache file) [Integer]\n'
                           'Press [s/skip] to assign the default value\n')

        if cache_size.lower() in ['s', 'skip']:
            cache_size = self._default_values[CACHE][CACHE_SIZE]

        self._config[CACHE] = {}
        self._config[CACHE][CACHE_SIZE] = cache_size

    def _handle_pinging_time_max_limit(self):
        pinging_time_max_limit = input('\nWhat should be your pinging time max limit in milliseconds? '
                                       '(if the mirror\'s pinging time exceeds that '
                                       'limit, the mirror enters the blacklist) [integer]\n'
                                       'Press [s/skip] to assign the default value\n')

        if pinging_time_max_limit.lower() in ['s', 'skip']:
            pinging_time_max_limit = self._default_values[BLACKLIST][PINGING_TIME_MAX_LIMIT]

        self._config[BLACKLIST] = {}
        self._config[BLACKLIST][PINGING_TIME_MAX_LIMIT] = pinging_time_max_limit

    def _handle_full_scans_frequency(self):
        full_scans_frequency = input('\nWhat should be the full scans frequency? '
                                     '(every X runs of daily scans, a full scan would run) [integer]\n'
                                     'Press [s/skip] to assign the default value\n')
        if full_scans_frequency.lower() in ['s', 'skip']:
            full_scans_frequency = self._default_values[DEFAULT][FULL_SCAN_FREQUENCY]

        self._config[DEFAULT][FULL_SCAN_FREQUENCY] = full_scans_frequency

    def full_config(self):
        self.mandatory_config()

        self._handle_cache_size()

        self._handle_pinging_time_max_limit()

        self._handle_full_scans_frequency()

    def mandatory_config(self):
        print('\nWe are going to ask you about some preferences regarding mirror managing.')
        print('For further details, please take a look at our README file.\n')
        operating_system = input('What Operating System do you use?\n'
                                 'We support [' + '/'.join(ALL_PARSERS) + '/e/exit]\n')
        operating_system = self._check_operating_system(operating_system)
        if operating_system in ['e', 'exit']:
            sys.exit()

        self._config[DEFAULT][OPERATING_SYSTEM] = operating_system

        # set mirrors_default_location and mirrors_url
        if operating_system.lower() == ARCH_PARSER:
            os_section = ARCH_SECTION
        elif operating_system.lower() == FEDORA_PARSER:
            os_section = FEDORA_SECTION
        else:  # Mint
            os_section = MINT_SECTION

        mirrors_default_location = input('\nWould you like to change the default value of '
                                         'your upstream mirrors file location? [y/yes/n/no]\n')
        if mirrors_default_location.lower() in ['y', 'yes']:
            mirrors_default_location = input('Please enter an absolute path for your '
                                             'upstream mirrors file location:\n')
        else:
            mirrors_default_location = self._default_values[os_section][UPSTREAM_MIRRORS_LOCATION]

        mirrors_url = self._default_values[os_section][MIRRORS_URL]

        self._config[DEFAULT][UPSTREAM_MIRRORS_LOCATION] = mirrors_default_location
        self._config[DEFAULT][MIRRORS_URL] = mirrors_url

    def _check_operating_system(self, operating_system):
        while not operating_system.lower() in ['arch', 'fedora', 'mint', 'e', 'exit']:
            operating_system = input('Sorry, an invalid option was entered, Please try again.\n'
                                     'What Operating System do you use?\n'
                                     'We support [' + '/'.join(ALL_PARSERS) + '/e/exit]\n')
        return operating_system

    def load_config(self):
        self._config.read(self._config_file_name)
        if not self._all_configurations_are_valid() > 0:
            print('We noticed that some of the configurations are invalid.\n'
                  'Please reconfigure.')
            self.start_config()
            self._config.read(self._config_file_name)

    def _all_configurations_are_valid(self):
        # TODO oschwart: implement this method
        raise NotImplementedError

    def load_default_values(self):
        self._default_values = configparser.ConfigParser()
        self._default_values.read(DEFAULT_VALUES_NAME)
        return self._default_values

    def get_default_value_of(self, section, field):
        return self._default_values[section][field]
