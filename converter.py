class Converter:
    col_det = '\n'
    row_det = '\t'

    def get_data(self, string):
        arr2 = []
        for str_col in string.split(self.col_det):
            str_cells = str_col.split(self.row_det)
            arr2.append(str_cells)
        return arr2

    def get_str(self, arr2):
        str_list = []
        for col in arr2:
            str_list.append(self.row_det.join(col))
        return self.col_det.join(str_list)
