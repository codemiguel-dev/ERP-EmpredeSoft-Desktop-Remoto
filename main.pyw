import sys
from PyQt5.QtWidgets import QSplashScreen, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from view.viewlogin import LoginView
import requests

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.showMessage("Cargando...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)

def check_internet():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear y mostrar el splash screen
    pixmap = QPixmap("image/icon.png")  # Ruta a tu imagen de splash
    splash = SplashScreen(pixmap)
    splash.show()
    
    if not check_internet():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Este programa debe tener acceso a internet")
        msg_box.setWindowTitle("Advertencia")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        sys.exit(1)
    
    view = LoginView()
   
    # Mostrar la ventana principal después de un retraso
    QTimer.singleShot(3000, splash.close)  # El splash screen se mostrará durante 3 segundos
    QTimer.singleShot(3000, view.show)  # Mostrar la ventana principal después de 3 segundos
    
    sys.exit(app.exec_())
