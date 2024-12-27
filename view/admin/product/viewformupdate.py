from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from controller.controllerproduct import ProductsController

class ProductUpdateForm(QtWidgets.QMainWindow):
    def __init__(self, controller, uid,  name, stock, category, purchase_price, sale_price, name_provider):
        super(ProductUpdateForm, self).__init__()
        loadUi('design/designUpdateproduct.ui', self)

        self.controller = ProductsController(self)
        self.uid = uid

        self.nametxt = self.findChild(QtWidgets.QLineEdit, 'nametxt')
        self.stocktxt = self.findChild(QtWidgets.QLineEdit, 'stocktxt')
        self.categotrytxt = self.findChild(QtWidgets.QLineEdit, 'categorytxt')
        self.purchasepricetxt = self.findChild(QtWidgets.QLineEdit, 'purchasepricetxt')
        self.salepricetxt = self.findChild(QtWidgets.QLineEdit, 'salepricetxt')
        self.nameprovidertxt = self.findChild(QtWidgets.QLineEdit, 'nameprovidertxt')

        self.nametxt.setText(name)
        self.stocktxt.setText(stock)
        self.categotrytxt .setText(category)
        self.purchasepricetxt.setText(purchase_price)
        self.salepricetxt.setText(sale_price)
        self.nameprovidertxt .setText(name_provider)
 

        self.btn_update_client.clicked.connect(self.update_product)

    def update_product(self):
        name = self.nametxt.text()
        stock = self.stocktxt.text()
        category = self.categotrytxt.text()
        purchase_price = self.purchasepricetxt.text()
        sale_price = self.salepricetxt.text()
        name_provider = self.nameprovidertxt.text()

        if self.controller.update_product(self.uid, name, stock, category, purchase_price, sale_price, name_provider):
            QtWidgets.QMessageBox.information(self, "Info", "Usuario actualizado con éxito")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al actualizar el usuario")
        self.close()
