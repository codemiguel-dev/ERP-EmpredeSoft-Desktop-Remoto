from PyQt5.QtCore import QObject
from model.modelprovider import ProviderModel

class ProviderController:

    def __init__(self, view):
        self.model = ProviderModel()
        self.view = view

    def register_provider(self, name, bunisessocial, linksocial, address, email, phone):
        return self.model.register_provider(name, bunisessocial, linksocial, address, email, phone)

    def users_data_changed(self):
        # Notificar a la vista (a través de señales) cuando los datos cambian
        pass

    def get_providers(self):
        return self.model.get_providers()

    def get_user_data(self, user_key):
        return self.model.get_user_data(user_key)

    def get_users_count(self):
        return self.model.get_users_count()

    def update_provider(self, uid, name, bunisessocial, linksocial, address, email, phone):
        return self.model.update_provider(uid, name, bunisessocial, linksocial, address, email, phone)

    def delete_provider(self, uid):
        return self.model.delete_provider(uid)
