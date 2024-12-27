from PyQt5.QtCore import QObject
from model.modelsale import SaleModel

class SalesController:

    def __init__(self, view):
        self.model = SaleModel()
        self.view = view

    def register_sale(self, user, client, product_id, product_image, product_name, product_quantity, product_unit_price, product_total):
        return self.model.register_sale(user, client, product_id, product_image, product_name, product_quantity, product_unit_price, product_total)

    def get_sale(self):
        return self.model.get_sale()

    def delete_sale(self, uids):
        return self.model.delete_sales(uids)
