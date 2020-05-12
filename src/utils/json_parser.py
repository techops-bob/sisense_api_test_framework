import json
import os

from src.utils.utilities import Utilities


class JsonParser:

    @staticmethod
    def read_file(dashboard, widget):
        with open("payload/" + dashboard + "/" + widget, 'r') as data_file:
            json_object = json.load(data_file)
        return json_object

    @staticmethod
    def write_file(dashboard, widget, json_object):
        with open("payload/" + dashboard + "/" + widget, 'w') as data_file:
            json.dump(json_object, data_file)

    @staticmethod
    def column_name_mapping():
        my_dict = {
            'country': 'Working Country',
            'Reporting_category_1': 'Category',
            'Reporting_category_2': 'Sub-category',
            'subproject_name': 'Sub Project Name',
            'employee_name': 'Employee Name',
            'employee_grade': 'Employee Grade',
            'employee_role': 'Employee Role',
            'office': 'Working Office'
        }
        return my_dict

    @staticmethod
    def append_value_in_json_file(json_object, filter_name, values):
        try:
            lst = []
            for item1 in json_object['metadata']:
                for k1, v1 in item1.items():
                    if type(item1[k1]) == dict:
                        for k2, v2 in item1[k1].items():
                            if k2 == 'title' and item1[k1][k2] == filter_name:
                                if 'filter' in item1[k1]:
                                    if 'all' != values.lower() and values != '' if values is not None else False:
                                        if 'all' in item1[k1]['filter']:
                                            del item1[k1]['filter']['all']
                                        for val in values.split(','):
                                            lst.append(val.strip())
                                        item1[k1]['filter']['members'] = lst
                                        raise StopIteration
                                    elif 'Date' in filter_name:
                                        if os.getenv('from_date').lower() == 'all' or os.getenv('from_date') == '':
                                            del item1[k1]['filter']['from']
                                            del item1[k1]['filter']['to']
                                            item1[k1]['filter']['all'] = 'true'
                                            raise StopIteration
                                        else:
                                            item1[k1]['filter']['from'] = os.getenv('from_date')
                                            item1[k1]['filter']['to'] = os.getenv('to_date')
                                            raise StopIteration
                                    else:
                                        if 'members' in item1[k1]['filter']:
                                            del item1[k1]['filter']['members']
                                        item1[k1]['filter']['all'] = 'true'
                                        raise StopIteration
        except StopIteration:
            pass
        return json_object

    @staticmethod
    def construct_json(dashboard, widget):
        my_dict = JsonParser.column_name_mapping()
        json_object = json.load(open("payload/" + dashboard + "/" + widget, 'r'))
        queries = Utilities.read_file("queries", dashboard, widget.replace('.json', ''), ".txt")
        cols = queries[len(queries) - 1].split(',')
        for col in cols:
            if 'calendar' in col:
                json_object = JsonParser.append_value_in_json_file(json_object, 'Days in Date', None)
            else:
                json_object = JsonParser.append_value_in_json_file(json_object, my_dict[col],
                                                                   os.getenv(col).strip())
        return json_object
