import json


class CacheManager(object):
    """
    The purpose of this class is to manage the cache of the mirroring by editing the cache file for the mirrors.

    Saves the data mirrors on the file as a json string.
    """

    # class attributes
    cache_file_name = 'cached_mirrors'

    def __init__(self, fastest_mirrors, cache_size=20):
        """
        Args:
            fastest_mirrors (FastestMirrors): it should be the entire object because when we
            load the cache we need to try and ping all the mirrors again to make sure they are valid.
        """
        self._fastest_mirrors = fastest_mirrors
        self._cache_size = cache_size
        self._cache_mirrors = None

    @property
    def cache_mirrors(self):
        return self._cache_mirrors

    @cache_mirrors.setter
    def cache_mirrors(self, cache_mirrors):
        self._cache_mirrors = cache_mirrors

    def set_cached_mirrors_from_list(self):
        """
        Sets the cached mirrors using the fastest mirror object sorted mirrors.
        """
        self._cache_mirrors = {
            mirror: time for (mirror, time), _ in zip(
                self._fastest_mirrors.sorted_mirrors.items(), range(self._cache_size)
            )
        }

    def save(self):
        """
        Saves the best mirrors into the cache according to the cache size.
        """
        with open(self.cache_file_name, 'w') as file:
            file.write(json.dumps(self._cache_mirrors))

    def load(self, max_mirror_ping_time):
        """
        Loads the cache mirrors json from a file.
        Excludes mirrors that cannot be pinged or slow mirrors.

        Args:
            max_mirror_ping_time (float): indicate what is the maximum ping time for a mirror to be valid.
        """
        with open(self.cache_file_name, 'r') as file:
            self._cache_mirrors = json.load(file)

        valid_mirrors = {}
        self._fastest_mirrors.sort_mirrors_by_ping_avg(mirrors=[mirror for mirror in self._cache_mirrors.keys()])

        for mirror, avg_ping in self._fastest_mirrors.sorted_mirrors:
            if avg_ping <= max_mirror_ping_time:
                valid_mirrors[mirror] = avg_ping

        self._cache_mirrors = valid_mirrors


# example to save & load.
# cache = CacheManager(
#     fastest_mirrors={
#         'walla.co.il': 0.004660946549847722, 'ynet.co.il': 0.05771557008847594, 'google.com': 0.05773383192718029
#     },
#     cache_size=2
# )
# cache.save()
# cache.load()
# print(cache.cache_mirrors)
