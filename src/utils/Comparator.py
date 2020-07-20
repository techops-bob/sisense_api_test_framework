from src.utils.BigQuery import BigQuery
from src.utils.Utilities import Utilities
from src.utils.JaqlConstructor import JaqlConstructor
from src.utils.SisenseApiHandler import SisenseApiHandler


class Comparator:

    def __init__(self, data_source, dashboard, test_data):
        self.data_source = data_source
        self.dashboard = dashboard
        self.test_data = test_data
        self.big_query = BigQuery(test_data)
        self.util = Utilities()
        self.dashboard_widget_mapping = self.util.get_dashboard_widget_mapping()

    def assert_equals(self, expected_value, actual_row, primary_columns, key):
        expected_value = str(self.util.round_off(expected_value))
        actual_value = str(self.util.round_off(actual_row[key]))
        primary_col_val = [actual_row[f] for f in primary_columns] if primary_columns is not None else None
        assert actual_value == expected_value, 'Failed at Row ' + str(primary_col_val) + ' Column [' + key + ']'

    def get_sisense_result(self, widget):
        json_obj = JaqlConstructor().construct_jaql(self.dashboard_widget_mapping[self.dashboard],
                                                    widget, self.test_data)
        return SisenseApiHandler().post(self.data_source, json_obj)

    def get_big_query_result(self, widget):
        query = self.util.read_file('resources/queries', self.dashboard, widget, '.txt')
        return self.big_query.get_query_result(query[0])

    def get_big_query_and_sisense_result(self, widget, primary_column=None):
        actual_result = self.get_sisense_result(widget)
        expected_result = self.get_big_query_result(widget)
        assert len(actual_result) == len(expected_result)
        act_rslt_row = {}
        exp_rslt_row = {}
        if primary_column is not None:
            for exp_ind in range(len(expected_result)):
                for act_ind in range(len(actual_result)):
                    if len(primary_column) == 2:
                        if actual_result[act_ind][primary_column[0]] == expected_result[exp_ind][primary_column[0]] \
                                and actual_result[act_ind][primary_column[1]] == expected_result[exp_ind][primary_column[1]]:
                            act_rslt_row = actual_result[act_ind]
                            exp_rslt_row = expected_result[exp_ind]
                            break
                    elif len(primary_column) == 1:
                        if actual_result[act_ind][primary_column[0]] == expected_result[exp_ind][primary_column[0]]:
                            act_rslt_row = actual_result[act_ind]
                            exp_rslt_row = expected_result[exp_ind]
                            break

        else:
            act_rslt_row = actual_result[0]
            exp_rslt_row = expected_result[0]
        assert bool(act_rslt_row) and bool(exp_rslt_row)
        for key in exp_rslt_row.keys():
            self.assert_equals(exp_rslt_row[key], act_rslt_row, primary_column, key)
