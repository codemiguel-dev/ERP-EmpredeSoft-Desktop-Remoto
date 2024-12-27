import sys
import os
import fitz  # PyMuPDF
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

class PDFViewer(QMainWindow):

    def __init__(self):
        super(PDFViewer, self).__init__()
        loadUi('design/designPrintsale.ui', self)
        self.setGeometry(100, 100, 800, 600)

        # Conectar botones a las funciones
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.print_button.clicked.connect(self.print_page)
        self.btn_open_file.clicked.connect(self.open_file_dialog)

        self.current_scale = 1.0  # Escala inicial para el zoom
        self.current_page = None  # Para almacenar la página actual

        # Configurar el QScrollArea
        self.scroll_area = self.findChild(QScrollArea, 'scrollArea')  # Asegúrate de que el nombre coincida con el del diseño
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.image_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.image_layout)

    def open_file_dialog(self):
        # Definir el directorio inicial
        initial_directory = os.path.join(os.path.dirname(__file__), 'pdf')

        # Abrir un diálogo para seleccionar un archivo PDF
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setDirectory(initial_directory)  # Establecer el directorio inicial

        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.load_pdf(file_paths[0])

    def load_pdf(self, pdf_path):
        # Abrir el archivo PDF
        self.pdf_document = fitz.open(pdf_path)

        # Mostrar las páginas como imágenes
        self.display_pages()

    def display_pages(self):
        # Limpiar las imágenes existentes
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Renderizar y mostrar las páginas
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(self.current_scale, self.current_scale))
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            self.image_layout.addWidget(label)

        # Almacenar la página actual
        self.current_page = self.pdf_document.load_page(0)  # Comienza con la primera página

    def zoom_in(self):
        self.current_scale += 0.1
        self.display_pages()

    def zoom_out(self):
        if self.current_scale > 0.1:
            self.current_scale -= 0.1
        self.display_pages()

    def print_page(self):
        if self.current_page is not None:
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                # Renderizar la página actual en el QPrinter
                pix = self.current_page.get_pixmap(matrix=fitz.Matrix(self.current_scale, self.current_scale))
                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                painter = QPainter(printer)
                rect = painter.viewport()
                size = img.scaled(rect.size(), Qt.KeepAspectRatio)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(img.rect())
                painter.drawImage(0, 0, img)
                painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
