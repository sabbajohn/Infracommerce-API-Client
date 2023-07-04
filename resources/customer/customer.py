from client import IntegraCommerceClient
from typing import Dict


class Customer(IntegraCommerceClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "ihub/customers"

    def create(self, data: Dict):
        return self.api_post(endpoint=f"{self.base_url}/b2b", data=data)

    def get(self, id):
        return self.api_get(endpoint=f"{self.base_url}/{id}/")

    def list(self):
        return self.api_get(endpoint=f"{self.base_url}/list/")  # Weird but Ok

    def create_credit_limit(self, id, data: Dict):
        return self.api_put(endpoint=f"{self.base_url}/{id}/creditLimit", data=data)

    def get_credit_limit(self, id):
        return self.api_get(endpoint=f"{self.base_url}/{id}/creditLimit")
