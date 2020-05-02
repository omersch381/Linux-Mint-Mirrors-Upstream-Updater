from bs4 import BeautifulSoup
import urllib.request as request

url = 'https://www.linuxmint.com/mirrors.php'
html_content = request.urlopen(url)
soup = BeautifulSoup(html_content, 'html.parser')
list_of_objects = soup.find_all()
mirrors_starting_index = 0
mirrors_ending_index = 0

for current_object in list_of_objects:
    if 'Repository mirrors' in current_object.text:  # Since in 'Repository mirrors' they start their list of mirrors
        mirrors_starting_index = list_of_objects.index(current_object)
    if 'Donate' in current_object.text:  # Since in 'Donate' word they finish their list of mirrors
        mirrors_ending_index = list_of_objects.index(current_object)

mirrors_general_list = list_of_objects[mirrors_starting_index:mirrors_ending_index]
list_of_mirror_elements = list()
for potential_mirror_element in mirrors_general_list:
    if "http" in potential_mirror_element.text:
        list_of_mirror_elements.append(potential_mirror_element)
list_of_mirror_elements = list_of_mirror_elements[
                          1:]  # They arranged the first element to have all the others in a duplicated way
list_of_mirrors = []
for i, element in enumerate(list_of_mirror_elements):
    if i % 2 == 1:  # Each odd index has the mirror's url of the index before it
        list_of_mirrors.append(element.text)

with open('mirrors_list', 'w') as file_handler:
    for mirror in list_of_mirrors:
        file_handler.write('%s\n' % mirror)
