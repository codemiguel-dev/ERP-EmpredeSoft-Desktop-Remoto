# controllerlogin.py

from PyQt5.QtWidgets import QMessageBox
from view.admin.viewdashboard import MiAppAdmin
from view.standar.viewdashboard import MiApp  # Importa la nueva ventana
from model.modeluser import UserModel

class LoginController:
    def __init__(self, view):
        self.model = UserModel()
        self.view = view

    def verify_credentials(self):
        username = self.view.lineEdit1.text()
        password = self.view.lineEdit2.text()

        if not username or not password:
            QMessageBox.warning(self.view, "Advertencia", "Ambos campos deben ser llenados.")
            return

        uid, role, name, email, password, image = self.model.verify_user(username, password)

        if role:
            QMessageBox.information(self.view, "Info", f"Login exitoso! Rol: {role}")
            self.open_dashboard(uid, role, name, email, password, image)
        else:
            QMessageBox.warning(self.view, "Warning", "Fallo al iniciar sesión. Usuario o contraseña incorrecta")


    def open_dashboard(self, uid, role, name, email, password, image):
        if role == 'Administrador':
            self.dashboard_view_admin = MiAppAdmin(uid, role, name, email, password, image)
            self.dashboard_view_admin.show()
        elif role == 'Estándar':
            self.dashboard_view = MiApp()
            self.dashboard_view.show()
        else:
            QMessageBox.warning(self.view, "Warning", "Rol desconocido.")