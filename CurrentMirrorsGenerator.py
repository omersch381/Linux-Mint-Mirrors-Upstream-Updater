class CurrentMirrorsGenerator:  
    def __init__(self, list_of_objects):
        self.mirrors_starting_index = -1
        self.mirrors_ending_index = -1
        self.list_of_objects = list_of_objects

    def general_function(self):
        self.mirrors_starting_index, self.mirrors_ending_index = self.get_mirrors_indices(self.list_of_objects)
        mirrors_general_list = self.list_of_objects[self.mirrors_starting_index:self.mirrors_ending_index]
        list_of_mirror_elements = []
        for potential_mirror_element in mirrors_general_list:
            if "http" in potential_mirror_element.text:
                list_of_mirror_elements.append(potential_mirror_element)
        # They arranged the first element to have all the others in a duplicated way
        list_of_mirror_elements = list_of_mirror_elements[1:]

        return self.get_list_of_mirrors(list_of_mirror_elements)

    def get_mirrors_indices(given_list, starting_index=0, ending_index=0):
        for current_object in given_list:
            if 'Repository mirrors' in current_object.text:  # Since in 'Repository mirrors' they start their list of mirrors
                starting_index = given_list.index(current_object)
            if 'Donate' in current_object.text:  # Since in 'Donate' word they finish their list of mirrors
                ending_index = given_list.index(current_object)
        return starting_index, ending_index

    def get_list_of_mirrors(self,given_list):
        list_of_mirror_urls = []
        for i, element in enumerate(given_list):
            if i % 2 == 1:  # Each odd index has the mirror's url of the index before it
                list_of_mirror_urls.append(element.text)
        return list_of_mirror_urls

