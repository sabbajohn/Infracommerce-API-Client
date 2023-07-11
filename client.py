import os
import json
import requests
import logging
from json import JSONDecodeError
from datetime import timedelta
from typing import Optional, Dict, List


logger = logging.getLogger(__name__)


class Response:
    def __init__(self, data=None, status=200, message=None):
        self.data = data
        self.status = status
        self.message = message

    def to_dict(self):
        return {"data": self.data, "status": self.status, "message": self.message}

    def to_json(self):
        return json.dumps(self.to_dict())


class IntegraCommerceClient:
    def __init__(self):
        self.__api_key = os.environ.get("INTEGRA_API_KEY", "")
        self.__jwt = os.environ.get("INTEGRA_JWT", "")
        self.__url_base = os.environ.get(
            "INTEGRA_URL_BASE", "stoplight.io/mocks/infrashop/api-integration/116750859"
        )

    def handle_api_error(self, response):
        if response.status_code != 200:
            raise Exception("API Error: {}".format(response.status_code))

    def api_post(self, endpoint, data):
        url = f"https://{self.__url_base}/{endpoint}"
        response = requests.post(url, json=data, headers={})
        self.handle_api_error(response)
        return response

    def api_put(self, endpoint, data):
        url = f"https://{self.__url_base}/{endpoint}"
        response = requests.post(url, json=data, headers={})
        self.handle_api_error(response)
        return response.json()

    def api_get(self, endpoint):
        url = f"https://{self.__url_base}/{endpoint}"
        response = requests.get(url, headers={})
        self.handle_api_error(response)
        return response.json()

    def api_patch(self, endpoint, data):
        url = f"https://{self.__url_base}/{endpoint}"
        response = requests.post(url, json=data, headers={})
        self.handle_api_error(response)
        return response.json()
