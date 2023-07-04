from resources import Resource
from typing import List


class _Attribute(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("catalog/admin/","attributes", *args, **kwargs)

    def list_by_category(self, id):
        return self.api_get(endpoint=f"{self.base_url}/listByCategoryId/{id}")


class _Sku(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("catalog/admin/","skus", *args, **kwargs)

    def list(self):
        return self.api_get(endpoint=f"{self.base_url}")

    def get_fiscal_sku_list(self, sku_list: List[str]):
        skus = ",".join(sku_list)
        return self.api_get(endpoint=f"{self.base_url}/fiscal/{skus}")


class Product(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__("catalog/admin/","products", *args, **kwargs)
        self.Sku = _Sku()
        self.Attribute = _Attribute()
