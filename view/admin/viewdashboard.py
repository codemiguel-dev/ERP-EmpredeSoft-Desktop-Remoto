import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLineEdit, QSizeGrip, QApplication, QPushButton, QLabel, QCheckBox, QWidget, QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QRectF  # Importa el módulo Qt
from controller.controlleruser import UsersController
from controller.controllerclient import ClientsController
from controller.controllerprovider import ProviderController
from controller.controllerenterprise import EnterpriseController
from controller.controllerproduct import ProductsController
from controller.controllersale import SalesController
from view.admin.user.viewformupdate import UpdateForm
from view.admin.user.viewformadd import RegisterForm
from view.admin.client.viewformadd import RegisterFormClient
from view.admin.client.viewformupdate import ClientUpdateForm
from view.admin.provider.viewformadd import RegisterFormProvider
from view.admin.provider.viewformupdate import ProviderUpdateForm
from view.admin.product.viewformadd import RegisterFormProduct
from view.admin.product.viewformupdate import ProductUpdateForm
from view.admin.sale.viewformadd import RegisterFormSale

class MiAppAdmin(QtWidgets.QMainWindow):
    def __init__(self, uid, role, name, email, password, image):
        super(MiAppAdmin, self).__init__()
        self.role = role  # Guardar la variable role
        loadUi('design/dashboard_admin.ui', self)
    
        # Configurar íconos de botones
        self.icons()

        self.labe_role.setText(f"Bienvenido {self.role}")

        self.table_sale.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.table_sale.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)


        self.show_profile(uid, role, name, email, password, image)
        
        # Eliminar barra de título y hacer la ventana translúcida
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        # Configurar SizeGrip para redimensionar la ventana
        self.gripSize = 5
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Mover ventana con click y arrastre en la barra superior
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.menu_access()

        self.btn_save_enterprise.clicked.connect(self.register_enterpise)
        self.btn_add_image.clicked.connect(self.add_image_enterprise)
        self.btn_update_enterprise.clicked.connect(self.update_enterprise)
        self.btn_delete_enterprise.clicked.connect(self.delete_enterprise)

        # Control de botones de la barra de títulos
        self.btn_enterprise.clicked.connect(self.mover_menu_enterprise)
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_restaurar.hide()

        # Conectar botón de usuarios
        self.buttom_update.clicked.connect(self.update_users)
        self.buttomUpdateUser.clicked.connect(self.show_users)
        self.buttom_add_user.clicked.connect(self.add_user)
        self.buttom_delete.clicked.connect(self.delete_users)

        #conectar botón de cliente
        self.btn_add_client.clicked.connect(self.add_client)
        self.btn_update_table_client.clicked.connect(self.show_clients)
        self.btn_update_client.clicked.connect(self.update_client)
        self.btn_delete_client.clicked.connect(self.delete_client)

        #conectar botón de proveedor
        self.btn_add_provider.clicked.connect(self.add_provider)
        self.btn_update_table_provider.clicked.connect(self.show_providers)
        self.btn_update_provider.clicked.connect(self.update_provider)
        self.btn_delete_provider.clicked.connect(self.delete_provider)

        self.btn_users.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.start_user()))

        self.btn_add_product.clicked.connect(self.from_add_product)
        self.btn_update_table_product.clicked.connect(self.show_product)
        self.btn_update_product.clicked.connect(self.update_product)
        self.btn_delete_product.clicked.connect(self.delete_product)

        self.btn_add_sale.clicked.connect(self.add_sale)
        self.btn_update_table_sale.clicked.connect(self.show_sales)
        self.btn_delete_sale.clicked.connect(self.delete_sale)

        self.btn_image_user.clicked.connect(self.add_image_user)
        self.btn_update_profile.clicked.connect(self.update_profile)

        # Menú lateral
        self.bt_menu.clicked.connect(self.mover_menu)

        # Instanciar el controlador de usuarios
        self.controlleruser = UsersController(self)
        self.controllerclient = ClientsController(self)
        self.controllerprovider = ProviderController(self)
        self.controllerenterprise = EnterpriseController(self)
        self.controllerproduct = ProductsController(self)
        self.controllersale = SalesController(self)

        # Configurar la tabla para mostrar usuarios
        self.tableUser.setColumnCount(5)  # Columnas: UID, Nombre, Email, Contraseña
        self.tableUser.setHorizontalHeaderLabels(['UID', 'Nombre', 'Email', 'Rol', 'Contraseña'])
		

    def menu_access(self):
        # Acceder a las páginas
        self.bt_inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_uno))
        self.btn_user.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.start_user()))
        self.btn_client.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.start_client()))
        self.btn_provider.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.start_provider()))
        self.btn_product.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.start_product()))
        self.btn_menu_venta.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.start_sale()))

    def icons(self):
        self.bt_minimizar.setIcon(QIcon('image/minus.svg'))
        self.bt_restaurar.setIcon(QIcon('image/chevron-up.svg'))
        self.bt_maximizar.setIcon(QIcon('image/chevron-down.svg'))
        self.bt_cerrar.setIcon(QIcon('image/x.svg'))
        self.bt_restaurar.hide()
        self.btn_enterprise.setIcon(QIcon('image/my-business.png'))
        self.bt_menu.setIcon(QIcon('image/menu.png'))
        self.bt_inicio.setIcon(QIcon('image/panel_control.png'))
        self.btn_user.setIcon(QIcon('image/user.png'))
        self.btn_users.setIcon(QIcon('image/user.png'))
        self.btn_client.setIcon(QIcon('image/client.png'))
        self.btn_clients.setIcon(QIcon('image/client.png'))
        self.btn_provider.setIcon(QIcon('image/provider.png'))
        self.btn_providers.setIcon(QIcon('image/provider.png'))
        self.btn_product.setIcon(QIcon('image/product.png'))
        self.btn_products.setIcon(QIcon('image/product.png'))
        self.btn_menu_venta.setIcon(QIcon('image/ventas.png'))
        self.btn_sell.setIcon(QIcon('image/ventas.png'))
        self.btn_menu_envios.setIcon(QIcon('image/send.png'))
        self.btn_send.setIcon(QIcon('image/send.png'))
        self.btn_menu_task.setIcon(QIcon('image/homework.png'))
        self.btn_menu_expenses.setIcon(QIcon('image/expenses.png'))
        self.btn_menu_income.setIcon(QIcon('image/income.png'))
        self.btn_perfil_user.setIcon(QIcon('image/user.png'))

    def show_profile(self, uid, name, email, password, role, image):
        self.frame_perfil.setVisible(False)

        self.uid_user_txt.setText(uid)
        self.rol_user_txt.setText(role)
        self.name_user_txt.setText(name)
        self.email_user_txt.setText(email)
        self.password_user_txt.setText(password)

        if image:
                response = requests.get(image)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    scaled_pixmap = pixmap.scaled(self.labelimageprofile.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.labelimageprofile.setPixmap(scaled_pixmap)
                else:
                    print(f"Error al obtener la imagen: {response.status_code}")
                    self.labelimageprofile.clear()
        else:
                print("No hay URL de imagen disponible")
                self.labelimageprofile.clear()

    def from_add_product(self):
        self.add_form = RegisterFormProduct()
        self.add_form.show()

    def start_user(self):
        self.show_users()
        return self.page
    
    def start_client(self):
        self.show_clients()
        return self.page_client

    def start_provider(self):
        self.show_providers()
        return self.page_provider
    
    def start_product(self):
        self.show_product()
        return self.page_product

    def start_sale(self):
        self.show_sales()
        return self.page_sale

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()

    def mover_menu(self):
        # Animación para mostrar/ocultar menú lateral
        width = self.frame_lateral.width()
        extender = 200 if width == 0 else 0
        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()

    def mover_menu_enterprise(self):
        # Animación para mostrar/ocultar menú lateral
        width = self.frame_lateral_enterprise.width()
        extender = 300 if width == 0 else 0
        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral_enterprise, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()

    def resizeEvent(self, event):
        # Reposicionar el SizeGrip al redimensionar la ventana
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        # Capturar posición de click para mover la ventana
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        # Mover la ventana si no está maximizada
        if not self.isMaximized() and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()

    def register_enterpise(self):
        name = self.nametxt.text()
        email = self.emailtxt.text()
        address = self.addresstxt.text()
        phone = self.phonetxt.text()
        image = self.imagetxt.text()

        if not name or not email or not address or not phone or not image:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        success, message = self.controllerenterprise.register_enterpise(name, email, address, phone, image)
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def add_image_enterprise(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if file_path:
            self.imagetxt.setText(file_path)

    def update_enterprise(self):
        # Obtener datos de usuarios desde el controlador
        enterprises = self.controllerenterprise.get_enterprise()

        if not enterprises:
            # Si no hay empresas disponibles, mostrar un mensaje por defecto
            self.labelnameenterpise.setText("No hay empresa disponibles")
            self.labelemailenterprise.setText("No hay empresa disponibles")
            self.labeladdressenterprise.setText("No hay empresa disponibles")
            self.labelphoneenterprise.setText("No hay empresa disponibles")
            return

        # Selecciona la primera empresa (siempre habrá al menos una)
        uid, enterprise = next(iter(enterprises.items()))
        enterprise_name = enterprise.get('name', 'Nombre no disponible')
        enterprise_email = enterprise.get('email', 'Email no diponible')
        enterprise_address = enterprise.get('address', 'Dirección no diponible')
        enterprise_phone = enterprise.get('phone', 'Teléfono no diponible')
        enterprise_image_path = enterprise.get('image', '../../image/add.png')  # Ruta de la imagen

    
        # Actualizar el label con el nombre de la empresa
        self.labelnameenterpise.setText(f"{enterprise_name}")
        self.labelemailenterprise.setText(f"{enterprise_email}")
        self.labeladdressenterprise.setText(f"{enterprise_address}")
        self.labelphoneenterprise.setText(f"{enterprise_phone}")

        if enterprise_image_path:
                response = requests.get(enterprise_image_path)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    scaled_pixmap = pixmap.scaled(self.labelimageenterprise.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.labelimageenterprise.setPixmap(scaled_pixmap)
                else:
                    print(f"Error al obtener la imagen: {response.status_code}")
                    self.labelimageenterprise.clear()
        else:
                print("No hay URL de imagen disponible")
                self.labelimageenterprise.clear()

    def delete_enterprise(self):
        # Obtener la empresa seleccionada
        enterprises = self.controllerenterprise.get_enterprise()
    
        
        uid, enterprise = next(iter(enterprises.items()))
        # Imprimir para depuración
        print("Datos de la empresa obtenidos:", enterprise)
        # Verificar si se ha seleccionado una empresa
        if enterprise and isinstance(enterprise, dict):
            enterprise_uid = enterprise.get('uid','')
        
            # Imprimir para depuración
            print("UID de la empresa:", enterprise_uid)
        
            if enterprise_uid:
                uid = enterprise_uid  # Asumiendo que enterprise_uid ya es una cadena de texto

                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación',
                                                   f"¿Estás seguro de eliminar la empresa con UID: {uid}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Eliminar empresa utilizando el controlador
                    if self.controllerenterprise.delete_enterprise(uid):
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Empresa eliminada correctamente.")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar la empresa.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "No se pudo obtener el UID de la empresa.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una empresa para eliminar.")

    #function user
    def show_users(self):
        # Obtener datos de usuarios desde el controlador
        users = self.controlleruser.get_users()

        # Limpiar la tabla
        self.tableUser.setRowCount(0)

        # Mostrar usuarios en la tabla
        for i, (uid, user) in enumerate(users.items()):
            self.tableUser.insertRow(i)
            self.tableUser.setItem(i, 0, QtWidgets.QTableWidgetItem(user.get('uid', '')))
            self.tableUser.setItem(i, 1, QtWidgets.QTableWidgetItem(user.get('name', '')))
            self.tableUser.setItem(i, 2, QtWidgets.QTableWidgetItem(user.get('email', '')))
            self.tableUser.setItem(i, 3, QtWidgets.QTableWidgetItem(user.get('role', '')))
            self.tableUser.setItem(i, 4, QtWidgets.QTableWidgetItem(user.get('password', '')))   # Ajustar según la estructura de datos

    def add_user(self):
        # Abrir el nuevo formulario de actualización
        self.add_form = RegisterForm()
        self.add_form.show()

    def update_users(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.tableUser.currentRow()

        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.tableUser.item(selected_row, 0)
            name_item = self.tableUser.item(selected_row, 1)
            email_item = self.tableUser.item(selected_row, 2)
            role_item = self.tableUser.item(selected_row, 3)
            password_item = self.tableUser.item(selected_row, 4)

            if uid_item and name_item and email_item and role_item and password_item:
                uid = uid_item.text()
                name = name_item.text()
                email = email_item.text()
                role = role_item.text()
                password = password_item.text()

                # Abrir el nuevo formulario de actualización
                self.update_form = UpdateForm(self.controlleruser,uid, name, email, role, password)
                self.update_form.show()
                self.show_users()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para actualizar.")

    def delete_users(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.tableUser.currentRow()
		# Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.tableUser.item(selected_row, 0)

            if uid_item:
                uid = uid_item.text()

                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', 
                                                   f"¿Estás seguro de eliminar al usuario con UID: {uid}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Eliminar usuario utilizando el controlador
                    if self.controlleruser.delete_user(uid):
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Usuario eliminado correctamente.")
                        self.show_users()  # Actualizar la tabla de usuarios después de eliminar
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar el usuario.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")
    
    def update_profile(self):
        uid = self.uid_user_txt.text()
        name = self.name_user_txt.text()
        email = self.email_user_txt.text()
        role = self.rol_user_txt.text()
        password = self.password_user_txt.text()
        image = self.image_user_txt.text()

        if not uid or not name or not email or not role or not password or not image:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        success, message = self.controlleruser.update_profile(uid,name, email, role, password, image)
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.warning(self, "Error", message)

    #end function user

    # function client

    def add_client(self):
        self.add_form = RegisterFormClient()
        self.add_form.show()

    def show_clients(self):
        # Obtener datos de usuarios desde el controlador
        clients = self.controllerclient.get_clients()

        # Limpiar la tabla
        self.table_client.setRowCount(0)

        # Mostrar usuarios en la tabla
        for i, (uid, client) in enumerate(clients.items()):
            self.table_client.insertRow(i)
            self.table_client.setItem(i, 0, QtWidgets.QTableWidgetItem(client.get('uid', '')))
            self.table_client.setItem(i, 1, QtWidgets.QTableWidgetItem(client.get('rut', '')))
            self.table_client.setItem(i, 2, QtWidgets.QTableWidgetItem(client.get('name', '')))
            self.table_client.setItem(i, 3, QtWidgets.QTableWidgetItem(client.get('lastname', '')))
            self.table_client.setItem(i, 4, QtWidgets.QTableWidgetItem(client.get('address', '')))
            self.table_client.setItem(i, 5, QtWidgets.QTableWidgetItem(client.get('phone', '')))  
            self.table_client.setItem(i, 6, QtWidgets.QTableWidgetItem(client.get('age', '')))
            self.table_client.setItem(i, 7, QtWidgets.QTableWidgetItem(client.get('email', '')))
            self.table_client.setItem(i, 8, QtWidgets.QTableWidgetItem(client.get('linksocial', '')))
            self.table_client.setItem(i, 9, QtWidgets.QTableWidgetItem(client.get('typeclient', '')))

    def update_client(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_client.currentRow()

        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_client.item(selected_row, 0)
            rut_item = self.table_client.item(selected_row, 1)
            name_item = self.table_client.item(selected_row, 2)
            lastname_item = self.table_client.item(selected_row, 3)
            address_item = self.table_client.item(selected_row, 4)
            phone_item = self.table_client.item(selected_row, 5)
            age_item = self.table_client.item(selected_row, 6)
            email_item = self.table_client.item(selected_row, 7)
            linksocial_item = self.table_client.item(selected_row, 8)
            typeclient_item = self.table_client.item(selected_row, 9)

            if uid_item and rut_item and name_item and lastname_item and address_item and phone_item and age_item and email_item and linksocial_item and typeclient_item:
                uid = uid_item.text()
                rut = rut_item.text()
                name = name_item.text()
                lastname = lastname_item.text()
                address = address_item.text()
                phone = phone_item.text()
                age = age_item.text()
                email = email_item.text()
                linksocial = linksocial_item.text()
                typeclient = typeclient_item.text()

                # Abrir el nuevo formulario de actualización
                self.update_form = ClientUpdateForm(self.controllerclient,uid, rut, name, lastname, address, phone, age, email, linksocial, typeclient)
                self.update_form.show()
                self.show_clients()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para actualizar.")

    def delete_client(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_client.currentRow()
		# Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_client.item(selected_row, 0)

            if uid_item:
                uid = uid_item.text()

                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', 
                                                   f"¿Estás seguro de eliminar al usuario con UID: {uid}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Eliminar usuario utilizando el controlador
                    if self.controllerclient.delete_client(uid):
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Cliente eliminado correctamente.")
                        self.show_clients()  # Actualizar la tabla de usuarios después de eliminar
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar el usuario.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")

    # end function client

    # function 

    def add_provider(self):
        self.add_form = RegisterFormProvider()
        self.add_form.show()

    def show_providers(self):
             # Obtener datos de usuarios desde el controlador
        providers = self.controllerprovider.get_providers()

        # Limpiar la tabla
        self.table_provider.setRowCount(0)

        # Mostrar usuarios en la tabla
        for i, (uid, client) in enumerate(providers.items()):
            self.table_provider.insertRow(i)
            self.table_provider.setItem(i, 0, QtWidgets.QTableWidgetItem(client.get('uid', '')))
            self.table_provider.setItem(i, 1, QtWidgets.QTableWidgetItem(client.get('name', '')))
            self.table_provider.setItem(i, 2, QtWidgets.QTableWidgetItem(client.get('bunisessocial', '')))
            self.table_provider.setItem(i, 3, QtWidgets.QTableWidgetItem(client.get('linksocial', '')))
            self.table_provider.setItem(i, 4, QtWidgets.QTableWidgetItem(client.get('address', '')))
            self.table_provider.setItem(i, 5, QtWidgets.QTableWidgetItem(client.get('email', '')))  
            self.table_provider.setItem(i, 6, QtWidgets.QTableWidgetItem(client.get('phone', '')))

    def update_provider(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_provider.currentRow()

        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_provider.item(selected_row, 0)
            name_item = self.table_provider.item(selected_row, 1)
            bunisessocial_item = self.table_provider.item(selected_row, 2)
            linksocial_item = self.table_provider.item(selected_row, 3)
            address_item = self.table_provider.item(selected_row, 4)
            email_item = self.table_provider.item(selected_row, 5)
            phone_item = self.table_provider.item(selected_row, 6)

            if uid_item and name_item and bunisessocial_item and linksocial_item and address_item and email_item and phone_item:
                uid = uid_item.text()
                name = name_item.text()
                bunisessocial = bunisessocial_item.text()
                linksocial = linksocial_item.text()
                address = address_item.text()
                email = email_item.text()
                phone = phone_item.text()

                # Abrir el nuevo formulario de actualización
                self.update_form = ProviderUpdateForm(self.controllerprovider,uid, name, bunisessocial, linksocial, address, email, phone)
                self.update_form.show()
                self.show_providers()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para actualizar.")

    def delete_provider(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_provider.currentRow()
		# Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_provider.item(selected_row, 0)

            if uid_item:
                uid = uid_item.text()

                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', 
                                                   f"¿Estás seguro de eliminar al usuario con UID: {uid}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Eliminar usuario utilizando el controlador
                    if self.controllerprovider.delete_provider(uid):
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Proveedor eliminado correctamente.")
                        self.show_clients()  # Actualizar la tabla de usuarios después de eliminar
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar el usuario.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")

    def show_product(self):
             # Obtener datos de usuarios desde el controlador
        products = self.controllerproduct.get_product()

        # Limpiar la tabla
        self.table_product.setRowCount(0)

        # Ajustar el tamaño de las filas y columnas
        self.table_product.verticalHeader().setDefaultSectionSize(200)
        self.table_product.horizontalHeader().setDefaultSectionSize(300)

        # Mostrar productos en la tabla
        for i, (uid, product) in enumerate(products.items()):
            self.table_product.insertRow(i)

            # Obtener la URL de la imagen
            image_url = product.get('image_url', '')

             # Crear un QTableWidgetItem para la imagen
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    # Ajustar el tamaño del pixmap
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    icon = QIcon(scaled_pixmap)
                    image_item = QtWidgets.QTableWidgetItem()
                    image_item.setIcon(icon)
                
                    # Ajustar el tamaño del ícono en la tabla
                    self.table_product.setIconSize(scaled_pixmap.size())
                
                    self.table_product.setItem(i, 0, image_item)  # Colocar la imagen en la primera columna
                else:
                    self.table_product.setItem(i, 0, QtWidgets.QTableWidgetItem('No Image'))
            else:
                self.table_product.setItem(i, 0, QtWidgets.QTableWidgetItem('No Image'))
            # Agregar el resto de los datos
            self.table_product.setItem(i, 1, QtWidgets.QTableWidgetItem(product.get('uid', '')))
            self.table_product.setItem(i, 2, QtWidgets.QTableWidgetItem(product.get('name', '')))
            self.table_product.setItem(i, 3, QtWidgets.QTableWidgetItem(str(product.get('stock', ''))))  # Convertir a cadena
            self.table_product.setItem(i, 4, QtWidgets.QTableWidgetItem(product.get('category', '')))
            self.table_product.setItem(i, 5, QtWidgets.QTableWidgetItem(str(product.get('purchaseprice', ''))))  # Convertir a cadena
            self.table_product.setItem(i, 6, QtWidgets.QTableWidgetItem(str(product.get('saleprice', ''))))  # Convertir a cadena
            self.table_product.setItem(i, 7, QtWidgets.QTableWidgetItem(product.get('providername', '')))

    def update_product(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_product.currentRow()

        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_product.item(selected_row, 0)
            name_item = self.table_product.item(selected_row, 1)
            stock_item = self.table_product.item(selected_row, 2)
            category_item = self.table_product.item(selected_row, 3)
            purchase_price__item = self.table_product.item(selected_row, 4)
            sale_price_item = self.table_product.item(selected_row, 5)
            name_provider_item = self.table_product.item(selected_row, 6)

            if uid_item and name_item and stock_item and category_item and purchase_price__item and sale_price_item and name_provider_item:
                uid = uid_item.text()
                name = name_item.text()
                stock = stock_item.text()
                category = category_item.text()
                purchase_price = purchase_price__item.text()
                sale_price = sale_price_item.text()
                name_provider = name_provider_item.text()

                # Abrir el nuevo formulario de actualización
                self.update_form = ProductUpdateForm(self.controllerproduct,uid, name, stock, category, purchase_price, sale_price, name_provider)
                self.update_form.show()
                return self.show_product()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para actualizar.")

    def delete_product(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_product.currentRow()
		# Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_product.item(selected_row, 0)

            if uid_item:
                uid = uid_item.text()

                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', 
                                                   f"¿Estás seguro de eliminar el producto con UID: {uid}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Eliminar usuario utilizando el controlador
                    if self.controllerproduct.delete_product(uid):
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Producto eliminado correctamente.")
                        return self.show_product()  # Actualizar la tabla de usuarios después de eliminar
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar el usuario.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")

    def add_sale(self):
        self.add_form = RegisterFormSale()
        self.add_form.show()

    def delete_sale(self):
         # Obtener las filas seleccionadas
        selected_rows = self.table_sale.selectionModel().selectedRows()

        if selected_rows:
             # Recopilar los UIDs de las filas seleccionadas
            uids = []
            for index in selected_rows:
                uid_item = self.table_sale.item(index.row(), 1)
                if uid_item:
                     uids.append(uid_item.text())

            if uids:
                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', 
                                                    f"¿Estás seguro de eliminar {len(uids)} productos seleccionados?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Intentar eliminar cada venta
                    success = True
                    for uid in uids:
                        if not self.controllersale.delete_sale(uids):
                            success = False
                            QtWidgets.QMessageBox.warning(self, "Error", f"Hubo un problema al eliminar el producto con UID: {uid}.")

                    if success:
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Productos eliminados correctamente.")
                        return self.show_product()  # Actualizar la tabla después de eliminar
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar algunos productos.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione al menos una fila para eliminar.")

    #function user
    def show_sales(self):
        # Obtener datos de usuarios desde el controlador
        sales = self.controllersale.get_sale()

        # Limpiar la tabla
        self.table_sale.setRowCount(0)

        # Mostrar usuarios en la tabla
        for i, (uid, sale) in enumerate(sales.items()):
            self.table_sale.insertRow(i)

            # Obtener la URL de la imagen
            image_url = sale.get('productimage', '')

             # Crear un QTableWidgetItem para la imagen
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    # Ajustar el tamaño del pixmap
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    icon = QIcon(scaled_pixmap)
                    image_item = QtWidgets.QTableWidgetItem()
                    image_item.setIcon(icon)
                
                    # Ajustar el tamaño del ícono en la tabla
                    self.table_sale.setIconSize(scaled_pixmap.size())
                
                    self.table_sale.setItem(i, 0, image_item)  # Colocar la imagen en la primera columna
                else:
                    self.table_sale.setItem(i, 0, QtWidgets.QTableWidgetItem('No Image'))
            else:
                self.table_sale.setItem(i, 0, QtWidgets.QTableWidgetItem('No Image'))

            self.table_sale.setItem(i, 1, QtWidgets.QTableWidgetItem(sale.get('uid', '')))
            self.table_sale.setItem(i, 2, QtWidgets.QTableWidgetItem(sale.get('productname', '')))
            self.table_sale.setItem(i, 3, QtWidgets.QTableWidgetItem(sale.get('client', '')))
            self.table_sale.setItem(i, 4, QtWidgets.QTableWidgetItem(str(sale.get('producttotal', ''))))   # Convertir a str
            self.table_sale.setItem(i, 5, QtWidgets.QTableWidgetItem(str(sale.get('productunitprice', ''))))   # Convertir a str
            self.table_sale.setItem(i, 6, QtWidgets.QTableWidgetItem(str(sale.get('productquantity', ''))))   # Convertir a str
            self.table_sale.setItem(i, 7, QtWidgets.QTableWidgetItem(sale.get('date', '')))
            self.table_sale.setItem(i, 8, QtWidgets.QTableWidgetItem(sale.get('user', '')))

    def add_image_user(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if file_path:
            self.image_user_txt.setText(file_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiAppAdmin()
    mi_app.show()
    sys.exit(app.exec_())
