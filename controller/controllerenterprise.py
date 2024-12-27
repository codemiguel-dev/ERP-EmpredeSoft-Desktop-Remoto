from PyQt5.QtCore import QObject
from model.modelenterprise import EnterpriseModel

class EnterpriseController:

    def __init__(self, view):
        self.model = EnterpriseModel()
        self.view = view

    def register_enterpise(self, name, email, address, phone, image):
        return self.model.register_enterprise(name, email, address, phone, image)

    def get_enterprise(self):
        return self.model.get_enterprise()
    
    def delete_enterprise(self, uid):
        return self.model.delete_enterprise(uid)