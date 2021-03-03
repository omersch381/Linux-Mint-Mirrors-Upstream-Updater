from pythonping import ping


class FastestMirrors(object):
    """
    This class produces the best mirrors available sorted according to their ping average time.

    Attributes:
        _sorted_mirrors (dict): a sorted dict of mirrors
    """

    def __init__(self):
        self._sorted_mirrors = None

    @property
    def sorted_mirrors(self):
        return self._sorted_mirrors

    def sort_mirrors_by_ping_avg(self, mirrors):
        """
        Finds the best mirrors and sorts them according to their average ping time, ignores broken mirrors.

        Args:
            mirrors (list[str]): a list of mirrors

        Example:
            mirrors = ['walla.co.il', 'ynet.co.il', 'google.com', 'blablabla.something.com'] -------------------->

            {'walla.co.il': 0.004660946549847722, 'ynet.co.il': 0.05771557008847594, 'google.com': 0.05773383192718029}
        """
        mirrors_ping_average = {}
        fastest_mirror_pinging_time = 2

        for mirror in mirrors:
            try:
                print('Pinging {mirror}... '.format(mirror=mirror), end='')
                ping_response = ping(target=mirror)
                mirrors_ping_average[mirror] = ping_response.rtt_avg
                print('took {avg_pinging_time} seconds.'.format(avg_pinging_time=mirrors_ping_average[mirror]))
                if fastest_mirror_pinging_time > mirrors_ping_average[mirror]:
                    fastest_mirror_pinging_time = mirrors_ping_average[mirror]
                    print('{new_fastest_mirror} is the fastest mirror so far!'.format(
                        new_fastest_mirror=mirror))

            except RuntimeError:  # means that mirror cannot be reached or broken.
                pass

        self._sorted_mirrors = {
            mirror: mirrors_ping_average[mirror] for mirror in sorted(
                mirrors_ping_average, key=mirrors_ping_average.get
            )
        }
