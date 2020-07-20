import json

from src.utils.SisenseApiHandler import SisenseApiHandler
from src.utils.Utilities import Utilities


class JaqlConstructor:
    filter_mapping = json.load(open("resources/filter_mapping.json", 'r'))

    def __init__(self):
        self.util = Utilities()
        self.widget_jaql = {}

    # Get value and filter condition from test data file
    def construct_test_data(self, test_data):
        test_data_dict = {}
        for k, v in test_data.items():
            test_data_dict[k] = {'Values': v['Values'], 'FilterCond': v['FilterCond']}
        return test_data_dict

    def append_test_data_in_jaql(self, filter_name, values):
        filter_json = json.load(open("resources/filter_template.json", 'r'))
        if 'date' in filter_name.lower():
            filter_json['jaql']['level'] = 'days'
            filter_json['jaql']['firstday'] = 'mon'
        (table, column) = JaqlConstructor.filter_mapping[filter_name].split('.')
        filter_json['jaql']['table'] = table
        filter_json['jaql']['column'] = column
        filter_json['jaql']['dim'] = "[{0}]".format(JaqlConstructor.filter_mapping[filter_name])

        test_data = values['Values']
        filter_cond = values['FilterCond']
        if len(filter_cond) > 1:
            if 'all' not in test_data and '' != test_data[0].strip():
                for i in range(len(filter_cond)):
                    filter_json['jaql']['filter'][filter_cond[i]] = test_data[i]
            else:
                filter_json['jaql']['filter']['all'] = 'true'
        else:
            if 'all' not in test_data and '' != test_data[0].strip():
                filter_json['jaql']['filter'][filter_cond[0]] = test_data
            else:
                filter_json['jaql']['filter']['all'] = 'true'
        self.widget_jaql['metadata'].append(filter_json)

    def construct_jaql(self, dashboard_widget_mapping, widget, test_data):
        self.get_widget_jaql(dashboard_widget_mapping, widget)
        constructed_test_data = self.construct_test_data(test_data)
        for k, v in constructed_test_data.items():
            self.append_test_data_in_jaql(k, v)
        return self.widget_jaql

    def get_widget_jaql(self, dashboard_widget_mapping, widget):
        self.widget_jaql = SisenseApiHandler().get(dashboard_widget_mapping['dashboard_id'],
                                                   dashboard_widget_mapping[widget])
