import os
from collections import defaultdict

import requests
import json
from src.utils.utilities import Utilities


class Authenticator:

    def __init__(self):
        # user credentials
        self.user_credential = self.get_user_credentials()
        self.auth_url = self.get_auth_url()
        self.token = self.get_token()

    @staticmethod
    def get_auth_url():
        auth_url = os.getenv('auth_url')
        return auth_url

    @staticmethod
    def get_user_credentials():
        user_credential = {'user_name': os.getenv('sisense_username'), 'password': os.getenv('sisense_password')}
        return user_credential

    def get_token(self):
        # Gets Authorization token to use in other requests.
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = json.dumps({'username': self.user_credential['user_name'], 'password': self.user_credential['password']})
        r = requests.post(self.auth_url, data=body, headers=headers)
        json_data = r.json()
        token = str(json_data['access_token'])
        return token

    def post_request(self, url, payload, col_nm):
        try:
            headers = {"Authorization": "Bearer " + str(self.token),
                       'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            Utilities.assert_response_status_code(response.status_code)
            my_dict = defaultdict(list)
            for key, value in response.json().items():
                if key == "values":
                    for lst_of_val in value:
                        if type(lst_of_val) == list:
                            if len(col_nm) == len(lst_of_val):
                                for val in range(len(col_nm)):
                                    data = Utilities.round_off(str(lst_of_val[val]['text']))
                                    my_dict[col_nm[val].replace('!', '')].append(data.replace('N\\A', '0'))
                        else:
                            data = Utilities.round_off(str(value[0]['text']))
                            my_dict[col_nm[0]].append(data.replace('N\\A', '0'))
        except requests.exceptions.RequestException as err:
            print('Error in URL : ' + url)
            print(response.text.encode('utf8'))
            print("OOps: Something Else", err)
        return my_dict
