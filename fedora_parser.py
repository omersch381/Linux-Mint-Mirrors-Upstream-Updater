from shutil import copyfile

from parser import Parser


class FedoraParser(Parser):
    def parse_mirrors(self):
        pass

    def switch_to_fastest_mirror(self, mirror=None, upstream_package_file_path='/etc/dnf/dnf.conf'):
        # Saving a backup of the configuration file
        copyfile(upstream_package_file_path, upstream_package_file_path + '.bak')

        was_fastest_mirror_option_added = False
        with open(upstream_package_file_path, 'r') as file:
            content = file.readlines()
            if 'fastestmirror' in content:
                was_fastest_mirror_option_added = True

        if not was_fastest_mirror_option_added:
            with open(upstream_package_file_path, 'a') as file:
                file.write('fastestmirror=1')
