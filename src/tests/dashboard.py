import time

from src.tests.big_query import BigQuery
from src.utils.json_parser import JsonParser
from src.utils.url_parser import UrlParser
from src.utils.utilities import Utilities


class Dashboard:
    @classmethod
    def api_checks_for_dashboard(cls, dashboard):
        # Actual result is the result from Sisense
        # Expected result is the result from bigquery
        start = time.time()
        urls = Utilities.read_file("api_endpoints", dashboard, dashboard, ".txt")
        # Get the number of widgets from the payload folder
        widgets = Utilities.get_list_of_all_files("payload/" + dashboard)
        for url in urls:
            for widget in widgets:
                if '.json' in widget:
                    print("*********** Validating Widget : " + widget.replace('.json', '') + " **********")
                    col_nm = Utilities.read_file("columns", dashboard, widget.replace('.json', ''), ".txt")
                    data = JsonParser().construct_json(dashboard, widget)
                    actual_result = UrlParser().check_url(url, data, col_nm)
                    expected_result = BigQuery().query_result(dashboard, widget, col_nm)
                    Dashboard.assert_equals(expected_result, actual_result, col_nm)
        hours, rem = divmod(time.time() - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Completed in : {:0>2}H:{:0>2}M:{:0>2}S".format(int(hours), int(minutes), int(seconds)))
        return

    @classmethod
    def assert_equals(cls, expected_result, actual_result, col_nm):
        print("Expected Result(BigQuery) : " + str(expected_result.items()))
        print("Actual Result(Sisense) : " + str(actual_result.items()))
        primary_col_nm = [s for s in col_nm if "*" in s]
        primary_col_nm = primary_col_nm[0] if primary_col_nm else col_nm[0]
        for exp_ind in range(len(expected_result[primary_col_nm])):
            act_ind = actual_result[primary_col_nm].index(expected_result[primary_col_nm][exp_ind])
            for col in col_nm:
                if '!' not in col:
                    assert (expected_result[col][exp_ind] == actual_result[col][act_ind])
        print("Assertion Completed")
        return
