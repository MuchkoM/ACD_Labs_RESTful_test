import copy


class Sorter:

    def sort(self, data):
        sorted_data = copy.deepcopy(data)
        sorted_data.sort()
        return sorted_data
