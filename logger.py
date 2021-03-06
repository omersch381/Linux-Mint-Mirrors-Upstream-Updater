import logging


class Logger:
    """Handles logging.
    """

    def __init__(self, class_name):
        self._logger = logging.getLogger(class_name)
        self._get_logger()

    def _get_logger(self):
        self._logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('mirrors_manager.log')
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    @property
    def logger(self):
        return self._logger
