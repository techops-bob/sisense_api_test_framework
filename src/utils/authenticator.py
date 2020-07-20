import os
import requests
import json

from src.utils.Utilities import Utilities


class Authenticator:

    def __init__(self):
        self.user_credential = self.get_user_credentials()
        self.auth_url = self.get_auth_url()

    def get_base_url(self):
        return "https://{0}/api/".format(Utilities().get_environment())

    def get_auth_url(self):
        auth_url = self.get_base_url()+"v1/authentication/login"
        return auth_url

    def get_user_credentials(self):
        user_credential = {'user_name': os.getenv('SISENSE_USERNAME'),
                           'password': os.getenv('SISENSE_PASSWORD')}
        return user_credential

    def get_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = json.dumps({'username': self.user_credential['user_name'], 'password': self.user_credential['password']})
        r = requests.post(self.auth_url, data=body, headers=headers)
        json_data = r.json()
        token = str(json_data['access_token'])
        return token
