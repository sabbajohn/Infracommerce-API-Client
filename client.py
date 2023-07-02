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
        self.api_key = os.environ.get("INTEGRA_API_KEY", "")
        self.jwt = os.environ.get("INTEGRA_JWT", "")
        self.ulr_base = os.environ.get(
            "INTEGRA_URL_BASE", "stoplight.io/mocks/infrashop/api-integration/116750859"
        )

    def handle_api_error(response):
        if response.status_code != 200:
            raise Exception("API Error: {}".format(response.status_code))

    def api_post(self, endpoint, data):
        url = f"https://{self.url_base}/{endpoint}"
        response = requests.post(url, json=data, headers={})
        self.handle_api_error(response)
        return response.json()

    def api_put(self, endpoint, data):
        url = f"https://{self.url_base}/{endpoint}"
        response = requests.post(url, json=data, headers={})
        self.handle_api_error(response)
        return response.json()

    def api_get(self, endpoint):
        url = f"https://{self.url_base}/{endpoint}"
        response = requests.get(url, headers={})
        self.handle_api_error(response)
        return response.json()

    # REGION BEGIN - Customer methods
    def create_customer(self, data: Dict):
        return self.api_post(endpoint="ihub/customers/b2b", data=data)

    # This one wasn't defined on API docs, but I have faith.
    def get_customer(self, id):
        return self.api_get(endpoint=f"ihub/customers/{id}/")

    def list_customers(self, data: Dict):
        return self.api_get(endpoint="ihub/customers/list/")  # Weird but Ok

    def create_credit_limit(self, id, data: Dict):
        return self.api_put(endpoint=f"ihub/customers/{id}/creditLimit", data=data)

    def get_credit_limit(self, id):
        return self.api_get(endpoint=f"ihub/customers/{id}/creditLimit")

    # REGION END - Customer methods

    # REGION START - Catalog methods

    # SUBREGION START - Brand methods
    def create_brand(self, data: Dict):
        return self.api_post(endpoint="catalog/admin/brands", data=data)

    def get_brand(self, id):
        return self.api_get(endpoint=f"catalog/admin/brands/{id}")

    def list_brands(self):
        return self.api_get(endpoint="catalog/admin/brands")

    def update_brand(self, id, data: Dict):
        return self.api_put(endpoint=f"catalog/admin/brands/{id}", data=data)

    # SUBREGION END - Brand methods

    # SUBREGION START - Category methods
    def create_category(self, data: Dict):
        return self.api_post(endpoint="catalog/admin/categories", data=data)

    def get_category(self, id):
        return self.api_get(endpoint=f"catalog/admin/categories/{id}")

    def list_categories(self):
        return self.api_get(endpoint="catalog/admin/categories")

    def update_category(self, id, data: Dict):
        return self.api_put(endpoint=f"catalog/admin/categories/{id}", data=data)

    # SUBREGION END - Category methods

    # SUBREGION START - Supplier methods
    def create_supplier(self, data: Dict):
        return self.api_post(endpoint="catalog/admin/suppliers", data=data)

    def get_supplier(self, id):
        return self.api_get(endpoint=f"catalog/admin/suppliers/{id}")

    def list_suppliers(self):
        return self.api_get(endpoint="catalog/admin/suppliers")

    def update_supplier(self, id, data: Dict):
        return self.api_put(endpoint=f"catalog/admin/suppliers/{id}", data=data)

    # SUBREGION END - Supplier methods

    # SUBREGION START - Products methods
    def create_product(self, data: Dict):
        return self.api_post(endpoint="catalog/admin/products", data=data)

    def get_product(self, id):
        return self.api_get(endpoint=f"catalog/admin/products/{id}")

    def list_products(self):
        return self.api_get(endpoint="catalog/admin/products")

    def update_product(self, id, data: Dict):
        return self.api_put(endpoint=f"catalog/admin/products/{id}", data=data)

    # SKU
    def create_sku(self, data: Dict):
        return self.api_post(endpoint="catalog/admin/skus", data=data)

    def get_sku(self, id):
        return self.api_get(endpoint=f"catalog/admin/skus/{id}")

    def list_skus(self):
        return self.api_get(endpoint="catalog/admin/skus")

    def update_sku(self, id, data: Dict):
        return self.api_put(endpoint=f"catalog/admin/skus/{id}", data=data)

    def get_fiscal_info_from_sku_list(self, sku_list: List[str]):
        skus = ",".join
        return self.api_get(endpoint=f"catalog/admin/skus/fiscal/{skus}")

    # SKU END
    # ATTRIBUTE
    def create_attribute(self, data: Dict):
        return self.api_post(endpoint="catalog/admin/attributes", data=data)

    def get_attribute(self, id):
        return self.api_get(endpoint=f"catalog/admin/attributes/attributeById/{id}")

    def list_attributes_by_category(self, category_id):
        return self.api_get(
            endpoint=f"catalog/admin/attributes/listByCategoryId/{category_id}"
        )

    def update_attribute(self, id, data: Dict):
        return self.api_put(endpoint=f"catalog/admin/attributes/{id}", data=data)

    # ATTRIBUTE
    # SUBREGION END - Products methods

    # REGION END - Catalog methods
