from os import listdir
from os.path import isfile, join


class Utilities:
    report = "report.html"

    @classmethod
    def get_list_of_all_files(cls, folder_name):
        files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
        return files

    @classmethod
    def assert_response_status_code(cls, status_code):
        assert (status_code == 200)
        return

    @classmethod
    def assert_response_range(cls, value, lower_range, upper_range):
        assert (lower_range <= value <= upper_range)
        return

    @classmethod
    def read_file(cls, folder_name, dashboard, file_name, extension):
        file_name = folder_name + "/" + dashboard + "/" + file_name + extension
        file = open(file_name, 'r')
        urls = file.read().splitlines()
        return urls

    @classmethod
    def round_off(cls, text):
        if '.' in text:
            return str(round(float(text), 3)) if text.replace('.', '').isdigit() else text
        else:
            return text
