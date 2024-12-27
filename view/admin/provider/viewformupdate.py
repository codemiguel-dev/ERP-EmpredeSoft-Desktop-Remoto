from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from controller.controllerprovider import ProviderController

class ProviderUpdateForm(QtWidgets.QMainWindow):
    def __init__(self, controller, uid, name, bunisessocial, linksocial, address, email, phone):
        super(ProviderUpdateForm, self).__init__()
        loadUi('design/designUpdateprovider.ui', self)

        self.controller = ProviderController(self)
        self.uid = uid

        self.nametxt = self.findChild(QtWidgets.QLineEdit, 'nametxt')
        self.bunisessocialtxt = self.findChild(QtWidgets.QLineEdit, 'bunisessocialtxt')
        self.linksocialtxt = self.findChild(QtWidgets.QLineEdit, 'linksocialtxt')
        self.addresstxt = self.findChild(QtWidgets.QLineEdit, 'addresstxt')
        self.emailtxt = self.findChild(QtWidgets.QLineEdit, 'emailtxt')
        self.phonetxt = self.findChild(QtWidgets.QLineEdit, 'phonetxt')

        self.nametxt.setText(name)
        self.bunisessocialtxt.setText(bunisessocial)
        self.linksocialtxt.setText(linksocial)
        self.addresstxt.setText(address)
        self.emailtxt.setText(email)
        self.phonetxt.setText(phone)
 

        self.btn_update_provider.clicked.connect(self.update_provider)

    def update_provider(self):
        name = self.nametxt.text()
        bunisessocial = self.bunisessocialtxt.text()
        linksocial = self.linksocialtxt.text()
        address = self.addresstxt.text()
        email = self.emailtxt.text()
        phone = self.phonetxt.text()
        
        if self.controller.update_provider(self.uid, name, bunisessocial, linksocial, address, email, phone):
            QtWidgets.QMessageBox.information(self, "Info", "Usuario actualizado con éxito")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al actualizar el usuario")
        self.close()
 