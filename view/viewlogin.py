# view.py

from PyQt5.QtWidgets import QMainWindow, QLineEdit, QSizeGrip, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QCursor
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from controller.controllerlogin import LoginController
from model.modeluser import UserModel  # Importa el modelo
from view.viewregister import RegisterForm # type: ignore


class LoginView(QMainWindow):
    def __init__(self):
        super(LoginView, self).__init__()
        loadUi('design/designlogin.ui', self)  # Carga la interfaz desde el archivo designRegisteruser.ui
        # Configuración adicional de la interfaz y conectar eventos
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
        self.btn_register.clicked.connect(self.abrir_formulario_registro)
        self.pushButton.clicked.connect(self.login)

        self.bt_normal.hide()
        self.click_posicion = None

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        icon_user = QIcon("image/user.svg")
        icon_lock = QIcon("image/lock.svg")
        self.lineEdit1.addAction(icon_user, QLineEdit.LeadingPosition)
        self.lineEdit2.addAction(icon_lock, QLineEdit.LeadingPosition)

        self.gripSize = 10
        self.grip = QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_minimize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_normal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_maximize.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_close.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Crear instancia del controlador y pasar la vista
        self.controller = LoginController(self)

    def control_bt_normal(self):
        self.showNormal()
        self.bt_normal.hide()
        self.bt_maximize.show()

    def control_bt_maximize(self):
        self.showMaximized()
        self.bt_maximize.hide()
        self.bt_normal.show()

    def resizeEvent(self, event):
        # Ajustar tamaño del grip al cambiar tamaño de la ventana
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        # Capturar posición de clic para mover la ventana
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        # Mover la ventana al arrastrar el marco superior
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()

        # Maximizar/restaurar ventana al mover el ratón cerca de los bordes
        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()

    def abrir_formulario_registro(self):
        self.register_form = RegisterForm()  # Crea una instancia del formulario de registro
        self.register_form.show()  # Muestra el formulario de registro

    def login(self):
        self.controller.verify_credentials()

# Ejecución del programa principal
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    view = LoginView()
    view.show()
    sys.exit(app.exec_())
