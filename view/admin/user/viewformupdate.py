from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from controller.controlleruser import UsersController

class UpdateForm(QtWidgets.QMainWindow):
    def __init__(self, controller, uid, name, email, role, password):
        super(UpdateForm, self).__init__()
        loadUi('design/designUpdateuser.ui', self)

        self.controller = UsersController(self)
        self.uid = uid

        self.nametxt = self.findChild(QtWidgets.QLineEdit, 'nametxt')
        self.emailtxt = self.findChild(QtWidgets.QLineEdit, 'emailtxt')
        self.passwordtxt = self.findChild(QtWidgets.QLineEdit, 'passwordtxt')
        self.comboboxrole = self.findChild(QtWidgets.QComboBox, 'comboboxrole')
        self.btn_update_bd = self.findChild(QtWidgets.QPushButton, 'btn_update_bd')

        self.nametxt.setText(name)
        self.emailtxt.setText(email)
        self.comboboxrole.setCurrentText(role)

        self.btn_update_bd.clicked.connect(self.update_user)

    def update_user(self):
        name = self.nametxt.text()
        email = self.emailtxt.text()
        password = self.passwordtxt.text()
        role = self.comboboxrole.currentText()

        if self.controller.update_user(self.uid, name, email, role, password):
            QtWidgets.QMessageBox.information(self, "Info", "Usuario actualizado con éxito")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al actualizar el usuario")
        self.close()
