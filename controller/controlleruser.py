from PyQt5.QtCore import QObject
from model.modeluser import UserModel

class UsersController:

    def __init__(self, view):
        self.model = UserModel()
        self.view = view

    def register_user(self, username, password, email, role):
        return self.model.register_user(username, password, email, role)

    def users_data_changed(self):
        # Notificar a la vista (a través de señales) cuando los datos cambian
        pass

    def get_users(self):
        return self.model.get_users()

    def get_user_data(self, user_key):
        return self.model.get_user_data(user_key)

    def get_users_count(self):
        return self.model.get_users_count()

    def update_user(self, uid, name, email, role,  password):
        return self.model.update_user(uid, name, email, role, password)

    def delete_user(self, uid):
        return self.model.delete_user(uid)
    
    def update_profile(self, uid, name, email, role,  password, image):
        return self.model.update_profile(uid, name, email, role, password, image)
