import glob


class LastRunMirrors:

    """This class parses the last run's mirrors and uses them for the required operations.

    E.g. sorts them and divide the slowest of them in the blacklist.
    E.g. uses/sets the closest mirrors as cache.
    It has a variable: black_list_threshold, where every <threshold> times the cache
    and the blacklist are being reset.
    """

    def __init__(self):
        self._black_list_threshold = 20

    def get_list_of_mirrors(self):
        # If black_list_iteration is less than the black_list_threshold, then we keep our cache.
        # Else, we will delete the cache.
        black_list_iteration, black_list = self.handle_black_list()

        last_log_filename = [file for file in glob.glob("log_file")]
        if len(last_log_filename) > 1:
            # Running the algorithm again will remove all the log files and will create a new one
            print("Please run the algorithm again. Exiting...")
            exit()

        with open(last_log_filename[0], 'r') as file_handler:
            content = file_handler.readlines()

        mirrors_index = self.get_starting_line_of_mirrors(content)  # The file starts with some information which is not mirrors urls
        content = content[mirrors_index:]

        total_mirrors_list = []
        for current_sentence in content:
            if 'has an average time of' not in current_sentence:
                continue
            current_sentence_list = current_sentence.split()
            mirror_name = current_sentence_list[0]
            time_it_took = float(current_sentence_list[-2])
            total_mirrors_list.append((mirror_name, time_it_took))
        total_mirrors_list = sorted(total_mirrors_list, key=lambda mirror: mirror[1])
        return total_mirrors_list

    def get_starting_line_of_mirrors(self, content):
        for line, index in enumerate(content):
            if line == '---':
                return index + 1

    def handle_black_list():
        pass
