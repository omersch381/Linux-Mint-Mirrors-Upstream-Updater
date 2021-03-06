# Scan types:
FULL_SCAN = 'full scan'
DAILY_SCAN = 'daily scan'

# Parsers:
ARCH_PARSER = 'arch'
FEDORA_PARSER = 'fedora'
MINT_PARSER = 'mint'
ALL_PARSERS = [ARCH_PARSER, FEDORA_PARSER, MINT_PARSER]

# Config.ini section names:
ARCH_SECTION = 'Arch'
BLACKLIST = 'Blacklist'
CACHE = 'Cache'
DEFAULT = 'DEFAULT'
FEDORA_SECTION = 'Fedora'
MINT_SECTION = 'Mint'

# Config.ini fields:
CACHE_SIZE = 'cache_size'
CRONTAB = 'crontab'
CRONTAB_SCHEDULE = 'crontab_schedule'
FULL_SCAN_FREQUENCY = 'full_scans_frequency'
MIRRORS_URL = 'mirrors_url'
NUM_OF_RUNS_SINCE_FULL_SCAN = 'num_of_runs_since_full_scan'
OPERATING_SYSTEM = 'operating_system'
PINGING_TIME_MAX_LIMIT = 'pinging_time_max_limit'
UPSTREAM_MIRRORS_LOCATION = 'upstream_mirrors_location'

# File names:
CACHED_MIRRORS_FILE_NAME = 'cached_mirrors'
CONFIG_FILE_NAME = 'config.ini'
DEFAULT_VALUES_NAME = 'default_values.ini'
MIRRORS_FILE_NAME = 'mirrors_list'

# Other:
PARSERS_WHICH_NOT_REQUIRE_PING = [FEDORA_PARSER]
