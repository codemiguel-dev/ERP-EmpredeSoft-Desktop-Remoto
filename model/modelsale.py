import firebase_admin
from datetime import datetime
from firebase_admin import credentials, db
from model.firebase_config import firebase_db,  storage_bucket
import uuid
import bcrypt
import base64
from PyQt5.QtGui import QImage
import tempfile
from PyQt5.QtCore import QBuffer, QIODevice

class SaleModel:
    def __init__(self):
        pass


    def save_image_to_temp_file(self, image):
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file_path = temp_file.name  # Guardar la ruta del archivo temporal
        image.save(temp_file_path, "PNG")  # Guardar la imagen en la ruta del archivo temporal
        return temp_file_path  # Devolver la ruta del archivo temporal

    def register_sale(self, user, client, product_id, product_image, product_name, product_quantity, product_unit_price, product_total):
        try:
            uid = str(uuid.uuid4())  # Generar un UID único
            # Obtener la fecha y hora actuales
            sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Subir la imagen a Firebase Storage
            image_uid = str(uuid.uuid4())
            blob = storage_bucket.blob(f'images/{image_uid}')

            # Verificar el tipo de product_image y guardarla en un archivo temporal si es un QImage
            if isinstance(product_image, QImage):
                temp_file_path = self.save_image_to_temp_file(product_image)
                blob.upload_from_filename(temp_file_path)
            else:
                # Si product_image ya es una ruta de archivo, subir directamente
                blob.upload_from_filename(product_image)

            # Construir la URL pública de la imagen
            bucket_name = storage_bucket.name
            image_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/images%2F{image_uid}?alt=media"

            # Guardar la venta en Firebase
            firebase_db.child('sale').child(uid).set({
            'uid': uid,
            'user': user,
            'client': client,
            'productui': product_id,
            'productimage': image_url,
            'productname': product_name,
            'productquantity': product_quantity,
            'productunitprice': product_unit_price,
            'producttotal': product_total,
            'date': sale_date
            })
            self.update_stock(product_id, product_quantity)
            return True
        except Exception as e:
            print(f"Error registering sale: {e}")
            return False


    def update_stock(self, product_id, product_quantity):
        try:
            # Obtener el producto específico desde Firebase
            product = firebase_db.child('product').child(product_id).get()

            if product:
                current_stock = product.get('stock', 0)  # Usar 0 si el stock no está disponible

                # Asegurarse de que current_stock es un número entero
                if isinstance(current_stock, (int, float)):
                    current_stock = int(current_stock)
                else:
                    current_stock = 0

                # Calcular el nuevo stock
                new_stock = current_stock - product_quantity

                # Asegurarse de que el stock no sea negativo
                if new_stock < 0:
                    new_stock = 0

                # Actualizar el stock en Firebase
                firebase_db.child('product').child(product_id).update({'stock': new_stock})
                print(f"Stock actualizado para el producto {product_id}: {new_stock}")
                return True
            else:
                print(f"Producto {product_id} no encontrado.")
                return False
        except Exception as e:
            print(f"Error actualizando el stock: {e}")
            return False

    def get_sale(self):
        sales = firebase_db.child('sale').get()
        return sales if sales else {}

    def delete_sales(self, uids):
        success = True
        for uid in uids:
            try:
                firebase_db.child('sale').child(uid).delete()
            except Exception as e:
                print(f"Error deleting sale with UID {uid}: {e}")
                success = False
        return success