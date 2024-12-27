# controller_register.py

from PyQt5.QtWidgets import QMessageBox
from model.modeluser import UserModel
from view.standar.viewdashboard import MiApp
import bcrypt
import base64

class RegisterController:
    def __init__(self, view):
        self.model = UserModel()
        self.view = view

    def register_user(self, username, password, email, role):
        if self.model.user_exists(username):
            self.view.show_warning("Advertencia", "El usuario ya existe.")
            return False

        success = self.model.register_user(username, password, email, role)

        if success:
            self.view.show_info("Éxito", "Usuario registrado correctamente.")
            self.open_dashboard()
        else:
            self.view.show_warning("Error", "Error al registrar el usuario.")
        
        return success

        
    
    def open_dashboard(self):
        self.dashboard_view = MiApp()
        self.dashboard_view.show()