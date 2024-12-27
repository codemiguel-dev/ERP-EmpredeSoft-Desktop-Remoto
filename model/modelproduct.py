import firebase_admin
from firebase_admin import credentials, db
from model.firebase_config import firebase_db, storage_bucket
import uuid
import bcrypt
import base64

class ProductModel:
    def __init__(self):
        pass

    def register_product(self, name, stock, category, purchaseprice, saleprice, providername, image_path):
        try:
            uid = str(uuid.uuid4())  # Generar un UID único

            # Generar un UID único para la imagen y crear un blob en Firebase Storage
            image_uid = str(uuid.uuid4())
            blob = storage_bucket.blob(f'images/{image_uid}')

            # Subir la imagen a Firebase Storage
            blob.upload_from_filename(image_path)

            # Construir la URL pública de la imagen manualmente
            bucket_name = storage_bucket.name
            image_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/images%2F{image_uid}?alt=media"

            # Convertir a numérico
            stock = int(stock)
            purchaseprice = float(purchaseprice)
            saleprice = float(saleprice)

            # Guardar los datos del producto en la base de datos
            firebase_db.child('product').child(uid).set({
            'uid': uid,
            'name': name,
            'stock': stock,
            'category': category,
            'purchaseprice': purchaseprice,
            'saleprice': saleprice,
            'providername': providername,
            'image_url': image_url  # Agregar la URL de la imagen
            })
            return True
        except Exception as e:
            print(f"Error registering product: {e}")
            return False

    def user_exists(self, username):
        try:
            users = firebase_db.child('users').get()
            if users is None:
                return False
            for uid, user in users.items():
                if user['name'] == username:
                    return True
            return False
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False

    def verify_user(self, username, password):
        try:
            users = firebase_db.child('users').get()
            if users is None:
                return None
            for uid, user in users.items():
                if user['name'] == username:
                    # Decodificar el hash de la contraseña usando base64 urlsafe
                    stored_hash = base64.urlsafe_b64decode(user['password'])
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        return user['role']
            return None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None

    def get_product(self):
        products = firebase_db.child('product').get()
        return products if products else {}

    def get_user_data(self, user_key):
        return firebase_db.child('users').child(user_key).get()

    def get_users_count(self):
        users = firebase_db.child('users').get()
        return len(users) if users else 0

    def update_product(self, uid, name, stock, category, purchase_price, sale_price, name_provider):
        try:
            firebase_db.child('product').child(uid).update({
                'name': name,
                'stock': stock,
                'category': category,
                'purchaseprice': purchase_price,
                'saleprice': sale_price,
                'providername': name_provider
            })
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_product(self, uid):
        try:
            firebase_db.child('product').child(uid).delete()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
