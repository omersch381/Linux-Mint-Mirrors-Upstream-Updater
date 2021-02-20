import configparser
import sys


class Config:
    """Configures the user preferences.
    """

    def __init__(self):
        self._config_file_name = 'config.ini'
        self._config = configparser.ConfigParser()
        self._default_values = self._load_default_values()
        self.start_config()

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
            cache_size = self._default_values['Cache']['cache_size']

        self._config['Cache'] = {}
        self._config['Cache']['cache_size'] = cache_size

    def _handle_pinging_time_max_limit(self):
        pinging_time_max_limit = input('\nWhat should be your pinging time max limit in milliseconds? '
                                       '(if the mirror\'s pinging time exceeds that '
                                       'limit, the mirror enters the blacklist) [integer]\n'
                                       'Press [s/skip] to assign the default value\n')

        if pinging_time_max_limit.lower() in ['s', 'skip']:
            pinging_time_max_limit = self._default_values['Blacklist']['pinging_time_max_limit']

        self._config['Blacklist'] = {}
        self._config['Blacklist']['pinging_time_max_limit'] = pinging_time_max_limit

    def _handle_full_scans_frequency(self):
        full_scans_frequency = input('\nWhat should be the full scans frequency? '
                                     '(every X runs of daily scans, a full scan would run) [integer]\n'
                                     'Press [s/skip] to assign the default value\n')
        if full_scans_frequency.lower() in ['s', 'skip']:
            full_scans_frequency = self._default_values['DEFAULT']['full_scans_frequency']

        self._config['DEFAULT']['full_scans_frequency'] = full_scans_frequency

    def full_config(self):
        self.mandatory_config()

        self._handle_cache_size()

        self._handle_pinging_time_max_limit()

        self._handle_full_scans_frequency()

    def mandatory_config(self):
        print('\nWe are going to ask you about some preferences regarding mirror managing.')
        print('For further details, please take a look at our README file.\n')
        # TODO oschwart: change the [Arch/Kali...] to constants
        operating_system = input('What Operating System do you use?\n'
                                 'We support [' + 'Arch/Kali/Fedora/Mint' + '/e/exit]\n')
        self._check_operating_system(operating_system)
        if operating_system in ['e', 'exit']:
            sys.exit()

        self._config['DEFAULT']['Operating System'] = operating_system

        mirrors_default_location = input('\nWould you like to change the default value of '
                                         'your upstream mirrors location? [y/yes/n/no]\n')
        if mirrors_default_location.lower() in ['y', 'yes']:
            mirrors_default_location = input('Please enter an absolute path for your '
                                             'upstream mirrors location:\n')
        else:
            # TODO oschwart: choose the default location that the parser has
            mirrors_default_location = 'TODO'
            pass
        self._config['DEFAULT']['Upstream Mirrors Location'] = mirrors_default_location

    def _check_operating_system(self, operating_system):
        # TODO oschwart: change the [Arch/Kali...] to constants
        while not operating_system.lower() in ['arch', 'kali', 'fedora', 'mint', 'e', 'exit']:
            operating_system = input('Sorry, an invalid option was entered, Please try again.\n'
                                     'What Operating System do you use?\n'
                                     'We support [' + 'Arch/Kali/Fedora/Mint' + '/e/exit]\n')

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

    def _load_default_values(self):
        self._default_values = configparser.ConfigParser()
        self._default_values.read('default_values.ini')
        return self._default_values
