# view/view.py
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QSizeGrip, QApplication, QPushButton, QLabel, QCheckBox, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QCursor
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from controller.controllerprovider import ProviderController

class RegisterFormProvider(QMainWindow):
    def __init__(self):
        super(RegisterFormProvider, self).__init__()
        loadUi('design/designRegisterprovider.ui', self)
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
        self.btn_register_bd.clicked.connect(self.register_provider)

        self.bt_normal.hide()
        self.click_posicion = None

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        icon_user = QIcon("image/user.svg")
        icon_lock = QIcon("image/lock.svg")
        icon_email = QIcon("image/email.svg")
        self.nametxt.addAction(icon_user, QLineEdit.LeadingPosition)
        #self.passwordtxt.addAction(icon_lock, QLineEdit.LeadingPosition)
        self.emailtxt.addAction(icon_email, QLineEdit.LeadingPosition)

        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_minimize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_normal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_maximize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_close.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.controller = ProviderController(self)

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

    def register_provider(self):
        name = self.nametxt.text()
        bunisessocial = self.bunisessocialtxt.text()
        linksocial = self.linksocialtxt.text()
        address = self.addresstxt.text()
        email = self.emailtxt.text()
        phone = self.phonetxt.text()

        if not name or not bunisessocial or not linksocial or not address or not email or not phone:
            QMessageBox.warning(self, "Advertencia", "Ambos campos deben ser llenados.")
            return

        self.controller.register_provider(name, bunisessocial, linksocial, address, email, phone)
        QMessageBox.warning(self, "Información", "Datos ingresados")


    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)