from PyQt5.QtCore import QObject
from model.modelclient import ClientModel

class ClientsController:

    def __init__(self, view):
        self.model = ClientModel()
        self.view = view

    def register_client(self, rut, name, lastname, address, phone, age, email, linksocial, typeclient):
        return self.model.register_client(rut, name, lastname, address, phone, age, email, linksocial, typeclient)

    def users_data_changed(self):
        # Notificar a la vista (a través de señales) cuando los datos cambian
        pass

    def get_clients(self):
        return self.model.get_clients()

    def get_user_data(self, user_key):
        return self.model.get_user_data(user_key)

    def get_users_count(self):
        return self.model.get_users_count()

    def update_client(self, uid, rut, name, lastname, address, phone, age, email, linksocial, typeclient):
        return self.model.update_client(uid, rut, name, lastname, address, phone, age, email, linksocial, typeclient)

    def delete_client(self, uid):
        return self.model.delete_client(uid)
