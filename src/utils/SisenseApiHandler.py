import json

import requests

from src.utils.Authenticator import Authenticator
from src.utils.Utilities import Utilities


class SisenseApiHandler:

    def __init__(self):
        self.util = Utilities()
        self.auth = Authenticator()
        self.token = self.auth.get_token()

    def get(self, dashboard_id, widget_id):
        widget_jaql = {}
        try:
            url = SisenseApiHandler.get_widget_jaql_endpoint(self, dashboard_id, widget_id)
            headers = {"Authorization": "Bearer " + str(self.token),
                       'Content-Type': 'application/json'}
            response = requests.get(url, headers=headers)
            self.assert_response_status_code(response.status_code)
            parsed_response = response.json()
            panels = parsed_response['metadata']['panels']
            widget_jaql['metadata'] = self.frame_jaql(panels)
        except requests.exceptions.RequestException as err:
            print('Error Occurred while GET request!' + str(err))
        return widget_jaql

    def post(self, data_source, payload):
        act_dict = {}
        try:
            url = SisenseApiHandler.get_endpoint(self, data_source)
            headers = {"Authorization": "Bearer " + str(self.token),
                       'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            self.assert_response_status_code(response.status_code)
            act_dict = self.response_parser(response)
        except requests.exceptions.RequestException as err:
            print('Error Occurred while POST request!' + str(err))
        return act_dict

    def response_parser(self, response):
        response = response.json()
        headers = response['headers']
        values = response['values']
        list_output = []
        for idx, value in enumerate(values):
            resp = {}
            if type(values[idx]) is list:
                for i, item in enumerate(value):
                    header = self.util.replace_list_of_chars([' ', '-'], '_', headers[i])
                    resp[header.lower()] = self.format_value(str(item['data']))
            else:
                header = self.util.replace_list_of_chars([' ', '-'], '_', headers[idx])
                resp[header.lower()] = self.format_value(str(values[idx]['data']))
            list_output.append(resp)
        return list_output

    def format_value(self, value):
        value = self.util.extract_month(value)
        value = '0' if value == 'N\\A' else value
        return value

    def assert_response_status_code(self, status_code):
        assert (status_code == 200)
        return

    def assert_response_range(self, value, lower_range, upper_range):
        assert (lower_range <= value <= upper_range)
        return

    def get_widget_jaql_endpoint(self, dashboard_id, widget_id):
        return self.auth.get_base_url() + "dashboards/{0}/widgets/{1}".format(dashboard_id, widget_id)

    def get_endpoint(self, data_source):
        return self.auth.get_base_url() + "datasources/{0}/jaql".format(data_source)

    def frame_jaql(self, panels):
        jaql_list = []
        for panel in panels:
            for item in panel['items']:
                if ("disabled" in item and not item['disabled']) or ("disabled" not in item):
                    jaql_list.append({"jaql": item["jaql"]})
        return jaql_list
