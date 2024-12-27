from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QLineEdit, QSizeGrip, QApplication, QPushButton, QLabel, QCheckBox, QWidget, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from google.cloud import storage
from google.oauth2 import service_account
import requests
from io import BytesIO
from controller.controllerproduct import ProductsController
from controller.controllerclient import ClientsController
from controller.controlleruser import UsersController
from controller.controllersale import SalesController
from view.admin.sale.viewexplorefile import PDFViewer

class RegisterFormSale(QMainWindow):
    def __init__(self):
        super(RegisterFormSale, self).__init__()
        loadUi('design/designRegistersale.ui', self)
        self.sale_total = 0.0 
        self.init_ui()

    def init_ui(self):
        self.bt_minimize.setIcon(QIcon('image/minus.svg')) 
        self.bt_maximize.setIcon(QIcon('image/chevron-down.svg'))
        self.bt_normal.setIcon(QIcon('image/chevron-up.svg')) 
        self.bt_close.setIcon(QIcon('image/x.svg'))

        self.bt_minimize.clicked.connect(self.showMinimized)
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(self.close)
        #self.btn_register_bd.clicked.connect(self.register_client)

        self.btn_update_stock.clicked.connect(self.update_stock_display)
        self.comboboxclient.currentIndexChanged.connect(self.show_client)
        self.btn_add_cart.clicked.connect(self.add_cart)
        self.btn_delete_product.clicked.connect(self.delete_product)

        self.btn_register_sale.clicked.connect(self.add_sale)

        self.btn_export_pdf.clicked.connect(self.export_pdf)

        self.btn_show_pdf.clicked.connect(self.explore_file)

        self.bt_normal.hide()
        self.click_posicion = None

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        icon_user = QIcon("image/user.svg")
        icon_lock = QIcon("image/lock.svg")
        #self.nametxt.addAction(icon_user, QLineEdit.LeadingPosition)
        #self.passwordtxt.addAction(icon_lock, QLineEdit.LeadingPosition)


        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_minimize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_normal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_maximize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_close.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.controllerproduct = ProductsController(self)
        self.controllerclient = ClientsController(self)
        self.controlleruser = UsersController(self)
        self.controllersale = SalesController(self)

        self.show_product()  # Llamar a show_product al inicializar la UI
        self.show_client()
        self.show_user()

    def control_bt_normal(self):
        self.showNormal()
        self.bt_normal.hide()
        self.bt_maximize.show()

    def control_bt_maximize(self):
        self.showMaximized()
        self.bt_maximize.hide()
        self.bt_normal.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()

        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()

    def register_client(self):
        name = self.nametxt.text()
        stock = self.stocktxt.text()
        category = self.categorytxt.text()
        purchaseprice = self.purchasepricetxt.text()
        saleprice = self.salepricetxt.text()
        providername = self.providernametxt.text()

        if not name or not stock or not category or not purchaseprice or not saleprice or not providername:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controllerproduct.register_product(name, stock, category, purchaseprice, saleprice, providername)
        QMessageBox.warning(self, "Información", "Datos ingresados")

    def show_product(self):
        # Desconectar la señal para evitar bucles infinitos
        self.comboboxproduct.blockSignals(True) 

        self.comboboxproduct.clear()
        # Obtener datos de usuarios desde el controlador
        products = self.controllerproduct.get_product()

        # Añadir productos al comboBox
        for uid, product in products.items():
            product_name = product.get('name', 'Nombre no disponible')
              # Obtener el stock del producto y actualizar el QLabel
            self.comboboxproduct.addItem(product_name, uid)


              # Añadir el nombre del producto y asociar el UID como dato

    def show_client(self):
        # Desconectar la señal para evitar bucles infinitos
        self.comboboxclient.blockSignals(True) 

        self.comboboxclient.clear()
        # Obtener datos de usuarios desde el controlador
        clients = self.controllerclient.get_clients()

        # Añadir productos al comboBox
        for uid, client in clients.items():
            client_name = client.get('name', 'Nombre no disponible')
            self.comboboxclient.addItem(client_name, uid)  # Añadir el nombre del producto y asociar el UID como dato

    def show_user(self):
        # Desconectar la señal para evitar bucles infinitos
        self.comboboxuser.blockSignals(True) 

        self.comboboxuser.clear()
        # Obtener datos de usuarios desde el controlador
        users = self.controlleruser.get_users()

        # Añadir productos al comboBox
        for uid, user in users.items():
            user_name = user.get('name', 'Nombre no disponible')
            self.comboboxuser.addItem(user_name, uid)  # Añadir el nombre del producto y asociar el UID como dato

    def get_signed_url(self,bucket_name, blob_name):
        credentials = service_account.Credentials.from_service_account_file('connect.json')
        client = storage.Client(credentials=credentials, project='desktop-program-emprendesoft')
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            expiration=datetime.timedelta(hours=1),  # URL válida por 1 hora
            method='GET'
        )
        return url

    def update_stock_display(self):
        current_index = self.comboboxproduct.currentIndex()
        if current_index >= 0:
            uid = self.comboboxproduct.itemData(current_index)
            products = self.controllerproduct.get_product()
            product = products.get(uid, {})

            product_stock = product.get('stock', 'Stock no disponible')
            product_name = product.get('name', 'Nombre no disponible')
            product_unit_price = product.get('saleprice', 'Precio no disponible')
            product_image_url = product.get('image_url', '')

            self.labelstock.setText(f"Cantidad Disponible: {product_stock}")
            self.labelname.setText(f"Nombre: {product_name}")
            self.labeluprice.setText(f"Precio Unitario: {product_unit_price}")
            self.unitpricetxt.setText(f"{product_unit_price}")
        
            if product_image_url:
                response = requests.get(product_image_url)
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    scaled_pixmap = pixmap.scaled(self.labelimage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.labelimage.setPixmap(scaled_pixmap)
                else:
                    print(f"Error al obtener la imagen: {response.status_code}")
                    self.labelimage.clear()
            else:
                print("No hay URL de imagen disponible")
                self.labelimage.clear()

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)
  
    def on_product_changed(self, index):
        # Obtener el UID del producto seleccionado
        product_uid = self.comboboxproduct.itemData(index)
        print(f"Producto seleccionado UID: {product_uid}")

    def add_cart(self):
        # Obtener los valores de los QLineEdit como cadenas
        product_unit_price_str = self.unitpricetxt.text()
        product_quantity_str = self.quantitytxt.text()

        # Ajustar el tamaño de las filas y columnas
        self.table_cart.verticalHeader().setDefaultSectionSize(200)
        self.table_cart.horizontalHeader().setDefaultSectionSize(300)

        try:
            # Convertir las cadenas a números
            product_unit_price = float(product_unit_price_str)
            product_quantity = int(product_quantity_str)

            # Obtener datos del producto desde el controlador
            products = self.controllerproduct.get_product()

            # Obtener la clave del producto seleccionado
            selected_product_id = self.comboboxproduct.currentData()  # O la clave que estés usando
            product = products.get(selected_product_id, {})

            # Obtener el stock del producto y convertirlo a entero
            product_stock_str = product.get('stock', '0')  # '0' si el stock no está disponible
        
            try:
                # Intentar convertir el stock a entero, manejando posibles errores
                product_stock = int(float(product_stock_str))  # Primero convertimos a float para manejar comas y puntos
            except ValueError:
                product_stock = 0  # Usar 0 si no se puede convertir el stock

            # Verificar si la cantidad solicitada excede el stock disponible
            if product_quantity > product_stock:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "La cantidad solicitada excede el stock disponible.")
                return  # Salir de la función si hay un problema

            # Calcular el total de cada producto
            total = product_unit_price * product_quantity

            # Sumar el total del producto al total acumulado
            self.sale_total += total

            # Mostrar el total acumulado en el QLabel
            self.labeltotal.setText(f"CLP {self.sale_total:.2f}")  # Mostrar con dos decimales
            self.totalpricetxt.setText(f"{self.sale_total}")

            # Añadir el producto al carro de compras
            row_position = self.table_cart.rowCount()
            self.table_cart.insertRow(row_position)

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
                    scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    label = QLabel()
                    label.setPixmap(scaled_pixmap)
                    label.setScaledContents(True)

                    # Colocar el QLabel con la imagen en la celda
                    self.table_cart.setCellWidget(row_position, 1, label)
                else:
                    self.table_cart.setItem(row_position, 1, QTableWidgetItem('No Image'))
            else:
                self.table_cart.setItem(row_position, 1, QTableWidgetItem('No Image'))

            # Agregar otros detalles del producto a la tabla
            self.table_cart.setItem(row_position, 0, QTableWidgetItem(str(selected_product_id)))
            self.table_cart.setItem(row_position, 2, QTableWidgetItem(product.get('name', '')))
            self.table_cart.setItem(row_position, 3, QTableWidgetItem(str(product_quantity)))
            self.table_cart.setItem(row_position, 4, QTableWidgetItem(str(product_unit_price)))
            self.table_cart.setItem(row_position, 5, QTableWidgetItem(str(total)))

        except ValueError:
            # Manejar el caso en el que la conversión falla
            self.labeltotal.setText("Error: Valores inválidos")

            
    def delete_product(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_cart.currentRow()
    
        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_cart.item(selected_row, 0).text()

            # Obtener el valor del total del producto que se va a eliminar
            total_item_str = self.table_cart.item(selected_row, 4).text()
            try:
                total_item = float(total_item_str)
            except ValueError:
                total_item = 0.0  # Usar 0.0 si no se puede convertir el total

            # Asegúrate de que self.sale_total sea un float
            try:
                self.sale_total = float(self.sale_total)
            except ValueError:
                self.sale_total = 0.0  # Usar 0.0 si self.sale_total no es convertible a float

            # Restar el total del producto del total acumulado
            self.sale_total -= total_item

            # Actualizar el QLabel con el total acumulado
            self.labeltotal.setText(f"CLP {self.sale_total:.2f}")
            self.totalpricetxt.setText(f"{self.sale_total:.2f}")

            # Eliminar la fila de la tabla en la interfaz gráfica
            self.table_cart.removeRow(selected_row)

            # Aquí deberías agregar la lógica para eliminar el producto de tu base de datos o estructura de datos.
            # Por ejemplo:
            # self.database.delete_product_by_uid(uid_item)

            # Mensaje de confirmación
            QtWidgets.QMessageBox.information(self, "Éxito", "El producto ha sido eliminado.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")

    def add_sale(self):
        user = self.comboboxuser.currentText()
        client = self.comboboxclient.currentText()

        if not user or not client:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        # Iterar sobre cada fila del carrito de compras
        for row in range(self.table_cart.rowCount()):
            # Obtener el ítem en la primera columna (ID del producto)
            product_id_item = self.table_cart.item(row, 0)
            product_id = product_id_item.text() if product_id_item else 'Desconocido'

            # Obtener el ítem en la segunda columna (Imagen del producto)
            product_image_item = self.table_cart.cellWidget(row, 1)
            if product_image_item and isinstance(product_image_item, QtWidgets.QLabel):
                # Obtener el QPixmap de la QLabel
                pixmap = product_image_item.pixmap()
                product_image = pixmap.toImage()  # Convertir QPixmap a QImage
                product_image = product_image if product_image else 'No Image'
            else:
                product_image = 'No Image'

            # Obtener los ítems en las columnas restantes
            product_name_item = self.table_cart.item(row, 2)
            product_quantity_item = self.table_cart.item(row, 3)
            product_unit_price_item = self.table_cart.item(row, 4)
            product_total_item = self.table_cart.item(row, 5)

            product_name = product_name_item.text() if product_name_item else 'Desconocido'
            product_quantity = int(product_quantity_item.text()) if product_quantity_item else 0
            product_unit_price = float(product_unit_price_item.text()) if product_unit_price_item else 0.0
            product_total = float(product_total_item.text()) if product_total_item else 0.0

            # Registrar la venta del producto en la base de datos
            self.controllersale.register_sale(user, client, product_id, product_image, product_name, product_quantity, product_unit_price, product_total)


    def export_pdf(self):
        # Obtener la fecha y hora actuales y formatearlas
        current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Ruta y nombre del archivo PDF
        pdf_file = f"view/admin/sale/pdf/venta_{current_date}.pdf"
        # Crear un lienzo
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        self.sale_total = self.totalpricetxt.text()

        # Título del documento
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 40, "Productos Comprados")
        c.drawString(450, height - 200, "Total: " + self.sale_total)


        # Coordenadas iniciales
        y = height - 80
        x = 50

        # Configuración de la fuente para los datos de la tabla
        c.setFont("Helvetica", 12)

        # Encabezados de la tabla
        headers = ["Nombre", "Cantidad", "Precio Unitario", "Total"]
        for i, header in enumerate(headers):
            c.drawString(x + i * 100, y, header)

        y -= 20

        # Iterar sobre cada fila del carrito de compras y agregar los datos al PDF
        for row in range(self.table_cart.rowCount()):
            product_name = self.table_cart.item(row, 2).text()
            product_quantity = self.table_cart.item(row, 3).text()
            product_unit_price = self.table_cart.item(row, 4).text()
            product_total = self.table_cart.item(row, 5).text()

            # Dibujar los datos de cada celda
            c.drawString(x, y, product_name)
            c.drawString(x + 100, y, product_quantity)
            c.drawString(x + 200, y, product_unit_price)
            c.drawString(x + 300, y, product_total)
            y -= 20

            # Comenzar una nueva página si la tabla se sale del margen inferior
            if y < 50:
                c.showPage()
                y = height - 50

        # Guardar el PDF
        c.save()

        # Mostrar un mensaje de éxito
        QtWidgets.QMessageBox.information(self, "Exportar a PDF", f"El carrito de compras ha sido exportado a {pdf_file}")

    def explore_file(self):
        self.add_form = PDFViewer()
        self.add_form.show()

   