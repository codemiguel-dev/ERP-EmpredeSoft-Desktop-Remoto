from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from controller.controllerclient import ClientsController

class ClientUpdateForm(QtWidgets.QMainWindow):
    def __init__(self, controller, uid, rut, name, lastname, address, phone, age, email, linksocial, typeclient):
        super(ClientUpdateForm, self).__init__()
        loadUi('design/designUpdateclient.ui', self)

        self.controller = ClientsController(self)
        self.uid = uid

        self.ruttxt = self.findChild(QtWidgets.QLineEdit, 'ruttxt')
        self.nametxt = self.findChild(QtWidgets.QLineEdit, 'nametxt')
        self.lastnametxt = self.findChild(QtWidgets.QLineEdit, 'lastnametxt')
        self.addresstxt = self.findChild(QtWidgets.QLineEdit, 'addresstxt')
        self.phonetxt = self.findChild(QtWidgets.QLineEdit, 'phonetxt')
        self.agetxt = self.findChild(QtWidgets.QLineEdit, 'agetxt')
        self.emailtxt = self.findChild(QtWidgets.QLineEdit, 'emailtxt')
        self.linksocialtxt = self.findChild(QtWidgets.QLineEdit, 'linksocialtxt')
        self.clienttypecombobox = self.findChild(QtWidgets.QComboBox, 'clienttypecombobox')
        self.btn_update_client = self.findChild(QtWidgets.QPushButton, 'btn_update_client')

        self.ruttxt.setText(rut)
        self.nametxt.setText(name)
        self.lastnametxt.setText(lastname)
        self.addresstxt.setText(address)
        self.phonetxt.setText(phone)
        self.agetxt.setText(age)
        self.emailtxt.setText(email)
        self.linksocialtxt.setText(linksocial)
        self.clienttypecombobox.setCurrentText(typeclient)
 

        self.btn_update_client.clicked.connect(self.update_client)

    def update_client(self):
        rut = self.ruttxt.text()
        name = self.nametxt.text()
        lastname = self.lastnametxt.text()
        address = self.addresstxt.text()
        phone = self.phonetxt.text()
        age = self.agetxt.text()
        email = self.emailtxt.text()
        linksocial = self.linksocialtxt.text()
        clienttype = self.clienttypecombobox.currentText()

        if self.controller.update_client(self.uid, rut, name, lastname, address, phone, age, email, linksocial, clienttype):
            QtWidgets.QMessageBox.information(self, "Info", "Usuario actualizado con éxito")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al actualizar el usuario")
        self.close()
