from os import listdir
from os.path import isfile, join
import datetime
import json
import os
import re


class Utilities:
    data_source = ""
    environment = os.getenv('ENVIRONMENT').upper()
    environment_json = json.load(open("resources/environment.json"))[environment]

    def get_list_of_all_files(self, folder_name):
        files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
        return files

    def read_file(self, folder_name, dashboard, file_name, extension):
        file_name = folder_name + "/" + dashboard + "/" + file_name + extension
        file = open(file_name, 'r')
        urls = file.read().splitlines()
        return urls

    def round_off(self, data):
        try:
            flt_val = float(data)
            return str(round(float(f'{flt_val:f}'), 2))
        except ValueError:
            return data

    def divide_numbers(self, num1, num2):
        return str(float(num1) / float(num2)) if num2 != '0' else '0'

    def replace_list_of_chars(self, char_list, repl_char, text):
        return re.sub('|'.join(sorted(char_list, key=len, reverse=True)), repl_char, text)

    def extract_month(self, text):
        try:
            date = datetime.datetime.strptime(text, '%Y-%m-%dT%H:%M:%S')
            return str(date.month)
        except:
            return text

    def read_file_as_json(self, folder_name, dashboard, widget):
        with open(folder_name + "/" + dashboard + "/" + widget, 'r') as data_file:
            json_object = json.load(data_file)
        return json_object

    def get_test_data(self, dashboard):
        test_data = os.getenv('TEST_DATA') if os.getenv('TEST_DATA') != '' else open("resources/test_data.json").read()
        json_object = json.loads(test_data)
        test_data_list = []
        for curr_data_set in json_object[dashboard]:
            test_data_dict = {}
            if 'Data Source' in curr_data_set:
                self.data_source = curr_data_set['Data Source']
                continue
            for k, v in curr_data_set.items():
                test_data_dict[k] = v
            test_data_list.append(test_data_dict)
        return test_data_list

    def get_dashboards(self):
        dashboards = os.getenv('DASHBOARDS').split(',')
        if len(dashboards) == 0:
            raise Exception("Env Variable[DASHBOARDS] empty!")
        return dashboards

    def get_environment(self):
        if len(Utilities.environment) == 0:
            raise Exception("Env Variable[ENVIRONMENT] empty!")
        return Utilities.environment_json

    def get_dashboard_widget_mapping(self):
        return json.load(open("resources/dashboard_widget_mapping/"+Utilities.environment.lower()+".json"))

    def init_test_data(self, dashboard):
        test_data_lst = self.get_test_data(dashboard)
        data_source = self.data_source
        test_data_out = []
        from src.utils.Comparator import Comparator
        for index in range(len(test_data_lst)):
            comparator = Comparator(data_source, dashboard, test_data_lst[index])
            test_data_out.append((dashboard+"[Test_Data " + str(index+1)+"]", {"attribute": comparator}))
        return test_data_out
