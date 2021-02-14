

class CacheManager(object):
    """
    The purpose of this class is to manage the cache of the mirroring by editing the cache file for the mirrors.
    """
    def __init__(self, fastest_mirrors, cache_size=20):
        self._fastest_mirrors = fastest_mirrors
        self._cache_size = cache_size

    def save(self):
        """
        Saves the fastest mirror list into a file.
        """

        fastest_mirrors_names = []
        for mirror in self._fastest_mirrors.keys():
            if len(fastest_mirrors_names) >= self._cache_size:
                break
            fastest_mirrors_names.append(mirror)

        with open('mirrors_list', 'w') as file:
            for mirror in fastest_mirrors_names:
                file.write(f"{mirror}\n")

    def load(self):
        """
        Loads the fastest mirrors list from a file.

        Returns:
            list[str]: a list of all the fastest mirrors that are currently in the cache.
        """
        mirrors_names = []

        with open('mirrors_list', 'r') as file:
            for mirror in file:
                mirrors_names.append(mirror.strip())
                if len(mirrors_names) >= self._cache_size:
                    return mirrors_names

# example to save a file.
# CacheManager(
#     fastest_mirrors={
#         'walla.co.il': 0.004660946549847722, 'ynet.co.il': 0.05771557008847594, 'google.com': 0.05773383192718029
#     },
#     cache_size=1
# ).save()

# example to load a file
# mirrors = CacheManager(
#     fastest_mirrors={
#         'walla.co.il': 0.004660946549847722, 'ynet.co.il': 0.05771557008847594, 'google.com': 0.05773383192718029
#     },
#     cache_size=2
# ).load()
# print(mirrors)
