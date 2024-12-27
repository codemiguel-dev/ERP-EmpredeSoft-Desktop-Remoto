import firebase_admin
from PyQt5.QtWidgets import QMessageBox
from firebase_admin import credentials, db
from model.firebase_config import firebase_db, storage_bucket
import uuid

class EnterpriseModel:
    def __init__(self):
        pass

    def register_enterprise(self, name, email, address, phone, image):
        try:
            enterprises = firebase_db.child('enterprise').get()
            if enterprises:  # Verificar si ya existe alguna empresa registrada
                # Ya existe una empresa registrada
                return False, "Error: Ya existe una empresa registrada."

            # Si no existe ninguna empresa, proceder con el registro
            uid = str(uuid.uuid4())  # Generar un UID único

            # Generar un UID único para la imagen y crear un blob en Firebase Storage
            image_uid = str(uuid.uuid4())
            blob = storage_bucket.blob(f'images/{image_uid}')

            # Subir la imagen a Firebase Storage
            blob.upload_from_filename(image)

            # Construir la URL pública de la imagen manualmente
            bucket_name = storage_bucket.name
            image_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/images%2F{image_uid}?alt=media"

            firebase_db.child('enterprise').child(uid).set({
                'uid': uid,
                'name': name,
                'email': email,
                'address': address,
                'phone': phone,
                'image': image_url
            })
            return True, "Empresa registrada exitosamente."
   
        except Exception as e:
            print(f"Error registering enterprise: {e}")
            return False, f"Error registrando la empresa: {e}"

    def get_enterprise(self):
        enterprise = firebase_db.child('enterprise').get()
        return enterprise if enterprise else {}
    
    def delete_enterprise(self, uid):
        try:
            firebase_db.child('enterprise').child(uid).delete()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False