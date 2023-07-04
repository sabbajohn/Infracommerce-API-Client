from client import IntegraCommerceClient


class Resource(IntegraCommerceClient):
    def __init__(self, endpoint_base: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = f"catalog/admin/{endpoint_base}"

    def create(self, data: Dict):
        return self.api_post(endpoint=self.base_url, data=data)

    def get(self, id):
        return self.api_get(endpoint=f"{self.base_url}/{id}")

    def list(self):
        return self.api_get(endpoint=self.base_url)

    def update(self, id, data: Dict):
        return self.api_put(endpoint=f"{self.base_url}/{id}", data=data)
