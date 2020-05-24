from bs4 import BeautifulSoup
import urllib.request as request
from ArgParser import ArgParser


def get_mirrors_indices(given_list, starting_index=0, ending_index=0):
    for current_object in given_list:
        if 'Repository mirrors' in current_object.text:  # Since in 'Repository mirrors' they start their list of mirrors
            starting_index = given_list.index(current_object)
        if 'Donate' in current_object.text:  # Since in 'Donate' word they finish their list of mirrors
            ending_index = given_list.index(current_object)
    return starting_index, ending_index


def get_list_of_mirrors(given_list):
    list_of_mirror_urls = []
    for i, element in enumerate(given_list):
        if i % 2 == 1:  # Each odd index has the mirror's url of the index before it
            list_of_mirror_urls.append(element.text)
    return list_of_mirror_urls


def write_mirrors_to_file(given_list_of_mirrors):
    with open('mirrors_list', 'w') as file_handler:
        for mirror in given_list_of_mirrors:
            file_handler.write('%s\n' % mirror)


args = ArgParser().parse_args()
html_content = request.urlopen(args.url)
soup = BeautifulSoup(html_content, 'html.parser')
list_of_objects = soup.find_all()

mirrors_starting_index, mirrors_ending_index = get_mirrors_indices(list_of_objects)
mirrors_general_list = list_of_objects[mirrors_starting_index:mirrors_ending_index]

list_of_mirror_elements = []
for potential_mirror_element in mirrors_general_list:
    if "http" in potential_mirror_element.text:
        list_of_mirror_elements.append(potential_mirror_element)

# They arranged the first element to have all the others in a duplicated way
list_of_mirror_elements = list_of_mirror_elements[1:]

list_of_mirrors = get_list_of_mirrors(list_of_mirror_elements)

write_mirrors_to_file(list_of_mirrors)
