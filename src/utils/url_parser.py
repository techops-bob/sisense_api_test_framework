import requests
from src.utils.authenticator import Authenticator


class UrlParser:
    def __init__(self):
        self.authenticator = Authenticator()

    def check_url(self, url, payload, values):
        requests.adapters.DEFAULT_RETRIES = 5
        result = self.authenticator.post_request(url, payload, values)
        return result
