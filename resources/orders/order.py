from client import IntegraCommerceClient
from typing import Dict


class Order(IntegraCommerceClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "ihub/orders"

    def create(self, data: Dict):
        return self.api_post(endpoint=f"{self.base_url}/", data=data)

    def get(self, id):
        return self.api_get(endpoint=f"{self.base_url}/{id}")

    def list(self):
        return self.api_get(endpoint=f"{self.base_url}/")  # Weird but Ok

    def approve(self, id, data: Dict):#TODO: Create the Patch request for this one
        return self.api_put(endpoint=f"{self.base_url}/approve/{id}", data=data)

    def cancel(self, id, data: Dict):#TODO: Create the Patch request for this one
        return self.api_put(endpoint=f"{self.base_url}/cancel/{id}", data=data)
    
    def picking(self, id):#TODO: Create the Patch request for this one
        return self.api_put(endpoint=f"{self.base_url}/{id}/picking")
    
    def invoice(self, id, data: Dict):#TODO: Create the Patch request for this one
        return self.api_put(endpoint=f"{self.base_url}/{id}/invoice")

    def dispatch(self, id, data: Dict):#TODO: Create the Patch request for this one
        return self.api_put(endpoint=f"{self.base_url}/{id}/dispatch")

    def deliver(self, id, data: Dict):#TODO: Create the Patch request for this one
        return self.api_put(endpoint=f"{self.base_url}/{id}/deliver")
