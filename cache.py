import json


class CacheManager(object):
    """
    The purpose of this class is to manage the cache of the mirroring by editing the cache file for the mirrors.

    Saves the data mirrors on the file as a json string.
    """
    def __init__(self, fastest_mirrors, cache_size=20):
        self._fastest_mirrors = fastest_mirrors
        self._cache_size = cache_size
        self._cache_mirrors = {
            mirror: time for (mirror, time), _ in zip(self._fastest_mirrors.items(), range(self._cache_size))
        }

    @property
    def cache_mirrors(self):
        return self._cache_mirrors

    @cache_mirrors.setter
    def cache_mirrors(self, cache_mirrors):
        self._cache_mirrors = cache_mirrors

    def save(self):
        """
        Saves the best mirrors into the cache according to the cache size.
        """
        with open('mirrors_list', 'w') as file:
            file.write(json.dumps(self._cache_mirrors))

    def load(self):
        """
        Loads the cache mirrors json from a file.
        """
        with open('mirrors_list', 'r') as file:
            self._cache_mirrors = json.load(file)


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
