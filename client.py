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
        return {
            'data': self.data,
            'status': self.status,
            'message': self.message
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class IntegraCommerceClient():

    def __init__(self, api_key, jwt, url_base="https://stoplight.io/mocks/infrashop/api-integration/116750859"):
        self.api_key = api_key
        self.jwt = jwt
        self.ulr_base = url_base
    
    def handle_api_error(response):
        if response.status_code != 200:
            raise Exception('API Error: {}'.format(response.status_code))
    
    def api_post(url, data, headers=None):
        response = requests.post(url, json=data, headers=headers)
        handle_api_error(response)
        return response.json()
    
    def api_get(url, headers=None):
        response = requests.get(url, headers=headers)
        handle_api_error(response)
        return response.json()
    