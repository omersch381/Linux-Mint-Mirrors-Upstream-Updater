from pythonping import ping


class FastestMirrors(object):
    """
    This class produces the best mirrors available sorted according to their ping average time.

    Attributes:
        _mirrors (list): a list of mirrors.
        _sorted_mirrors (dict): a sorted dict of mirrors
    """
    def __init__(self, mirrors):
        self._mirrors = mirrors
        self._sorted_mirrors = self._get_best_mirrors_by_ping_avg()

    @property
    def sorted_mirrors(self):
        return self._sorted_mirrors

    def _get_best_mirrors_by_ping_avg(self):
        """
        Finds the best mirrors and sorts them according to their average ping time, ignores broken mirrors.

        Returns:
            dict: a sorted dict with the best mirrors by their average ping time.

        Example:
            self._mirrors = ['walla.co.il', 'ynet.co.il', 'google.com', 'blablabla.something.com'] -------------------->

            {'walla.co.il': 0.004660946549847722, 'ynet.co.il': 0.05771557008847594, 'google.com': 0.05773383192718029}
        """
        mirrors_ping_average = {}

        for mirror in self._mirrors:
            try:
                ping_response = ping(target=mirror)
                mirrors_ping_average[mirror] = ping_response.rtt_avg
            except RuntimeError:  # means that mirror cannot be reached or broken.
                pass

        return {
            mirror: mirrors_ping_average[mirror] for mirror in sorted(
                mirrors_ping_average, key=mirrors_ping_average.get
            )
        }
