from PyQt5.QtCore import QObject
from model.modelproduct import ProductModel

class ProductsController:

    def __init__(self, view):
        self.model = ProductModel()
        self.view = view

    def register_product(self, name, stock, category, purchaseprice, saleprice, providername, image_path):
        return self.model.register_product(name, stock, category, purchaseprice, saleprice, providername, image_path)

    def users_data_changed(self):
        # Notificar a la vista (a través de señales) cuando los datos cambian
        pass

    def get_product(self):
        return self.model.get_product()

    def get_user_data(self, user_key):
        return self.model.get_user_data(user_key)

    def get_users_count(self):
        return self.model.get_users_count()

    def update_product(self, uid, name, stock, category, purchase_price, sale_price, name_provider):
        return self.model.update_product(uid, name, stock, category, purchase_price, sale_price, name_provider)

    def delete_product(self, uid):
        return self.model.delete_product(uid)
